import base64
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.request

import boto3
from boto3.dynamodb.conditions import Key

# This app uses the Instagram Login flow (instagram_business_basic +
# instagram_business_manage_comments/messages permissions) — confirmed during setup.
GRAPH_API_BASE = "https://graph.instagram.com/v21.0"

# boto3's default S3 client generates presigned URLs against the global
# s3.amazonaws.com host even when the client/session region is set — the
# signature is region-scoped but the host isn't, so S3 rejects it outside
# us-east-1 (AuthorizationQueryParametersError). Force the regional endpoint
# explicitly so presigned URLs actually work in this stack's region.
_REGION = os.environ.get("AWS_REGION", "us-east-1")
s3 = boto3.client("s3", region_name=_REGION, endpoint_url=f"https://s3.{_REGION}.amazonaws.com")
ssm = boto3.client("ssm")
dynamodb = boto3.resource("dynamodb")

BUCKET = os.environ["BUCKET_NAME"]
SENT_TABLE = os.environ["SENT_TABLE"]

_param_cache = {}


def _param(name_env):
    if name_env not in _param_cache:
        name = os.environ[name_env]
        resp = ssm.get_parameter(Name=name, WithDecryption=True)
        _param_cache[name_env] = resp["Parameter"]["Value"]
    return _param_cache[name_env]


def _table():
    return dynamodb.Table(SENT_TABLE)


def _already_sent(marker_id):
    return "Item" in _table().get_item(Key={"pk": f"marker#{marker_id}", "sk": "x"})


def _mark_sent(marker_id):
    _table().put_item(Item={"pk": f"marker#{marker_id}", "sk": "x"})


# Permanent, no TTL — unlike the pending# prompt below, "have I ever delivered
# this exact post's guide to this exact person" should never expire. Without
# this, a completely natural reply-comment like "thanks for the guide!" carries
# a brand-new comment_id and contains the keyword, so _handle_comment treats it
# as a fresh trigger match and resends the whole thing.
def _already_delivered(sender_id, media_id):
    return "Item" in _table().get_item(Key={"pk": f"delivered#{sender_id}", "sk": media_id})


def _mark_delivered(sender_id, media_id):
    _table().put_item(Item={"pk": f"delivered#{sender_id}", "sk": media_id})


PENDING_TTL_SEC = 3 * 24 * 60 * 60  # 3 days


def _set_pending(sender_id, media_id, entry):
    # Keyed by (sender, media) — one pending record per post someone has triggered,
    # not a single slot per sender, so commenting on two tracked posts before
    # replying to either doesn't silently drop the first one.
    #
    # TTL matters here: _handle_message treats ANY message or button tap from a
    # sender as "recheck and deliver" as long as they have an outstanding pending
    # record — that's what lets a plain text reply (not just the button) confirm
    # follow status. Without an expiry, someone who triggers a post, gets the
    # follow-gate prompt, and never taps it leaves that record sitting forever —
    # then an unrelated DM weeks later (about anything) silently resurfaces and
    # delivers that long-forgotten guide. The `ttl` attribute (DynamoDB-native
    # expiry, enabled on this table) makes an abandoned prompt just quietly expire
    # instead of lying in wait for the next unrelated message.
    _table().put_item(Item={
        "pk": f"pending#{sender_id}",
        "sk": media_id,
        "pdf_key": entry["pdf_key"],
        "keyword": entry.get("keyword", ""),
        "ttl": int(time.time()) + PENDING_TTL_SEC,
    })


def _get_pending_all(sender_id):
    resp = _table().query(KeyConditionExpression=Key("pk").eq(f"pending#{sender_id}"))
    return resp.get("Items", [])


def _clear_pending(sender_id, media_id):
    _table().delete_item(Key={"pk": f"pending#{sender_id}", "sk": media_id})


# Durable per-post counters for the dashboard's Performance tab — separate from
# the pending#/marker# rows above, which are transient by design (pending rows
# are deleted once delivered, so they can't answer "how many people ever got
# this"). Wrapped so a stats-write failure can never block the actual
# comment-reply / DM-delivery flow, which is the one thing that must not break.
def _increment_stat(media_id, field):
    try:
        _table().update_item(
            Key={"pk": f"stats#{media_id}", "sk": "counts"},
            UpdateExpression=f"ADD {field} :one",
            ExpressionAttributeValues={":one": 1},
        )
    except Exception as exc:
        print(f"stats: failed to increment {field} for {media_id}: {exc}")


def _load_triggers():
    obj = s3.get_object(Bucket=BUCKET, Key="triggers.json")
    return json.loads(obj["Body"].read())


def _graph_post(path, payload):
    access_token = _param("ACCESS_TOKEN_PARAM")
    url = f"{GRAPH_API_BASE}/{path}?access_token={access_token}"
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def _graph_get(path, params):
    access_token = _param("ACCESS_TOKEN_PARAM")
    params = {**params, "access_token": access_token}
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    with urllib.request.urlopen(f"{GRAPH_API_BASE}/{path}?{qs}") as resp:
        return json.loads(resp.read())


_profile_url_cache = {}


def _profile_url():
    if "url" not in _profile_url_cache:
        ig_user_id = _param("IG_USER_ID_PARAM")
        profile = _graph_get(ig_user_id, {"fields": "username"})
        _profile_url_cache["url"] = f"https://www.instagram.com/{profile['username']}/"
    return _profile_url_cache["url"]


FOLLOW_CHECK_PAYLOAD = "CHECK_FOLLOW"


def _send_buttons(recipient, text, buttons):
    ig_user_id = _param("IG_USER_ID_PARAM")
    _graph_post(f"{ig_user_id}/messages", {
        "recipient": recipient,
        "message": {"attachment": {"type": "template", "payload": {"template_type": "button", "text": text, "buttons": buttons}}},
    })


def _follow_gate_buttons():
    return [
        {"type": "web_url", "url": _profile_url(), "title": "Visit Profile"},
        {"type": "postback", "payload": FOLLOW_CHECK_PAYLOAD, "title": "I'm following"},
    ]


def _verify_signature(body_bytes, signature_header):
    if not signature_header:
        print("signature check: no X-Hub-Signature-256 header present")
        return False
    app_secret = _param("APP_SECRET_PARAM")
    expected = "sha256=" + hmac.new(app_secret.encode(), body_bytes, hashlib.sha256).hexdigest()
    ok = hmac.compare_digest(expected, signature_header)
    if not ok:
        print(f"signature check FAILED — received={signature_header} expected={expected} body_len={len(body_bytes)}")
    return ok


DELIVERY_MESSAGE = "Here's the full guide you asked for — thanks for following!"


def _deliver_pending(sender_id, recipient):
    # Shared by both callers: _handle_comment (recipient={"comment_id": ...}, the private-reply
    # shape needed to open the messaging window from a public comment) and _handle_message
    # (recipient={"id": sender_id}, valid once that window is already open). A generic reply
    # ("done", "yes") can't tell us which specific post they're replying about, so this delivers
    # everything the sender has triggered and not yet received.
    #
    # Native file attachment, not a link in text: a presigned-URL link would expose the raw S3
    # URL (bucket name, signed query params) directly in the DM, which reads as suspicious and
    # has an uncertain effective lifetime (signed with the Lambda role's own short-lived
    # credentials). An attachment sidesteps both — Meta fetches the file from the presigned URL
    # almost immediately at send time, so only needs to survive a few seconds, and the recipient
    # gets a trusted, natively-rendered file instead of a link to tap. Costs one extra message
    # bubble (text can't share a message with an attachment), which is the right trade.
    items = _get_pending_all(sender_id)
    if not items:
        return

    ig_user_id = _param("IG_USER_ID_PARAM")

    _graph_post(f"{ig_user_id}/messages", {
        "recipient": recipient,
        "message": {"text": DELIVERY_MESSAGE},
    })

    for item in items:
        # Isolated per item: one item's send/clear failing (a transient Graph API
        # error, a bad pdf_key) must not abort the loop and leave every item after
        # it un-cleared — those would otherwise sit pending indefinitely, waiting
        # to resurface on the person's next unrelated message. Skip and move on;
        # the failed one stays pending and gets a fresh attempt next interaction,
        # bounded by PENDING_TTL_SEC either way.
        try:
            pdf_url = s3.generate_presigned_url("get_object", Params={"Bucket": BUCKET, "Key": item["pdf_key"]}, ExpiresIn=3600)
            try:
                _graph_post(f"{ig_user_id}/messages", {
                    "recipient": recipient,
                    "message": {"attachment": {"type": "file", "payload": {"url": pdf_url, "is_reusable": False}}},
                })
            except urllib.error.HTTPError as exc:
                if exc.code != 500:
                    raise
                # Observed in production twice: this call can return HTTP 500 even though
                # the file attachment is actually delivered — confirmed both times by the
                # account's own is_echo webhook event for the file message arriving right
                # after the "failed" call. Treating every 500 here as a hard failure left
                # the pending record stuck (never cleared, delivered stat never
                # incremented) even though the recipient already had the file — this
                # exact log line is what to grep for if that assumption is ever wrong for
                # a specific case.
                print(f"deliver: file-send got HTTP 500 for sender={sender_id} media={item['sk']} "
                      f"— treating as delivered (known Graph API flakiness, not retrying)")
            _clear_pending(sender_id, item["sk"])
            _mark_delivered(sender_id, item["sk"])
            _increment_stat(item["sk"], "delivered")
        except Exception as exc:
            print(f"deliver: failed for sender={sender_id} media={item['sk']}: {exc}")


COMMENT_ACK_TEXT = "Sent you a DM — check your inbox! 📩"


def _reply_to_comment(comment_id, text):
    # Public reply on the comment itself (POST /{comment-id}/replies), separate from the private
    # DM — nudges the commenter to actually check their inbox (comment-reply notifications get
    # noticed more reliably than a DM alone) and doubles as visible proof under the post that the
    # automation replies to people, not just silently.
    _graph_post(f"{comment_id}/replies", {"message": text})


def _handle_comment(value):
    comment_id = value.get("id")
    media_id = (value.get("media") or {}).get("id")
    sender_id = (value.get("from") or {}).get("id")
    text = (value.get("text") or "").strip().lower()
    print(f"comment: id={comment_id} media_id={media_id!r} sender_id={sender_id} text={text!r}")
    if not comment_id or not media_id or not sender_id:
        print("comment: missing id/media_id/sender_id, ignoring")
        return
    if _already_sent(comment_id):
        print(f"comment: {comment_id} already processed, ignoring")
        return

    triggers = _load_triggers()
    print(f"triggers.json keys: {list(triggers.keys())}")
    entry = triggers.get(media_id)
    if not entry:
        print(f"comment: media_id {media_id!r} not in triggers.json, ignoring")
        return
    if entry["keyword"].strip().lower() not in text:
        print(f"comment: keyword {entry['keyword']!r} not found in comment text, ignoring")
        return
    if _already_delivered(sender_id, media_id):
        # A natural reply like "thanks for the guide!" contains the keyword and has
        # a brand-new comment_id, so without this check it reads as a fresh trigger
        # and resends the whole thing to someone who already has it.
        print(f"comment: {sender_id} already received this post's guide, not re-sending")
        _mark_sent(comment_id)
        return

    _mark_sent(comment_id)
    _set_pending(sender_id, media_id, entry)
    _increment_stat(media_id, "matched")

    # Check follow status up front — a commenter who already follows doesn't need the
    # follow-gate CTA at all; sending it anyway meant they'd get the CTA *and then* the PDF
    # once they tapped/replied, instead of just the PDF right away.
    #
    # The profile lookup needs user consent, which only exists once the person has a DM thread
    # with the account — a first-time commenter gets IGApiException code 230 (surfaced as HTTP
    # 500). Fall through to the follow-gate private reply, which needs no consent; tapping its
    # button opens the thread so _handle_message's follow check then works.
    try:
        profile = _graph_get(sender_id, {"fields": "is_user_follow_business"})
    except urllib.error.HTTPError as exc:
        print(f"comment: profile lookup failed for {sender_id} ({exc.code}: {exc.read().decode()[:300]}) — treating as not following")
        profile = {}
    if profile.get("is_user_follow_business"):
        print("comment: match! already following — delivering PDF directly")
        _deliver_pending(sender_id, {"comment_id": comment_id})
    else:
        print("comment: match! not following yet — sending private reply with follow-gate buttons")
        _send_buttons(
            {"comment_id": comment_id},
            "Thanks for the comment! Tap below once you're following and I'll send the guide right over.",
            _follow_gate_buttons(),
        )

    # Either branch above just sent something to their DMs — a public nudge under the comment
    # itself gets noticed even by people who don't have DM notifications on.
    _reply_to_comment(comment_id, COMMENT_ACK_TEXT)


def _handle_message(messaging_event):
    # A postback (button tap) carries its own mid, same idempotency shape as a typed message.
    message_id = (messaging_event.get("message") or {}).get("mid") or (messaging_event.get("postback") or {}).get("mid")
    sender_id = (messaging_event.get("sender") or {}).get("id")
    if not sender_id:
        return
    if message_id:
        if _already_sent(message_id):
            return
        _mark_sent(message_id)

    pending_items = _get_pending_all(sender_id)
    if not pending_items:
        return  # not a reply this flow is tracking — ignore (e.g. an unrelated DM)

    profile = _graph_get(sender_id, {"fields": "is_user_follow_business"})

    if not profile.get("is_user_follow_business"):
        _send_buttons(
            {"id": sender_id},
            "Looks like you're not following yet — follow, then tap the button again and I'll send it right over.",
            _follow_gate_buttons(),
        )
        return

    _deliver_pending(sender_id, {"id": sender_id})


PRIVACY_POLICY_HTML = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Privacy Policy — @ratish.ai automation</title>
<meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="font-family: system-ui, sans-serif; max-width: 640px; margin: 40px auto; padding: 0 16px; line-height: 1.5;">
<h1>Privacy Policy</h1>
<p>This page covers the automation connected to the Instagram account <strong>@ratish.ai</strong>,
which replies to comments containing a trigger keyword with a private message, and delivers a
resource (a PDF guide) once the sender confirms they follow the account.</p>

<h2>What data is collected</h2>
<ul>
<li>Your Instagram-scoped user ID and the ID of your comment/message (assigned by Instagram, not
a phone number, email, or real name).</li>
<li>The text of a comment you leave on a tracked post, only to check whether it contains the
trigger keyword.</li>
<li>Whether you follow the account (a yes/no check via Instagram's own API), to decide whether to
send the resource or a follow prompt.</li>
</ul>
<p>No email address, phone number, or payment information is ever collected by this automation.</p>

<h2>How it's used</h2>
<p>Solely to run the reply flow: match your comment to a trigger, send you a private reply, check
your follow status when you respond, and deliver the matching resource. Nothing is used for
advertising, profiling, or shared with any third party.</p>

<h2>Storage and retention</h2>
<ul>
<li>A record that you're waiting on a resource is stored temporarily (AWS DynamoDB) and deleted
as soon as the resource is delivered.</li>
<li>A small idempotency marker (comment/message ID only) is kept so a retried webhook delivery
doesn't send a duplicate reply.</li>
<li>The resource files themselves (PDFs) are stored privately (AWS S3) and only ever served via
short-lived, single-use links sent directly to you.</li>
</ul>

<h2>Deletion requests</h2>
<p>To request deletion of any data associated with your account, contact
<a href="mailto:ratishjain6@gmail.com">ratishjain6@gmail.com</a>.</p>
</body></html>"""


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod")

    path = event.get("rawPath") or event.get("requestContext", {}).get("http", {}).get("path", "")

    print(f"{method} {path}")

    if method == "GET" and path == "/privacy":
        return {"statusCode": 200, "headers": {"Content-Type": "text/html"}, "body": PRIVACY_POLICY_HTML}

    if method == "GET" and path == "/oauth-redirect":
        # Not an OAuth flow we actually use (the access token is generated directly in
        # the Meta dashboard for this self-use Tester account) — this route exists only
        # because Meta's Instagram Business Login setup requires a reachable redirect
        # URL to consider the use case fully configured.
        return {"statusCode": 200, "body": "OK"}

    if method == "GET":
        qs = event.get("queryStringParameters") or {}
        if qs.get("hub.mode") == "subscribe" and qs.get("hub.verify_token") == _param("VERIFY_TOKEN_PARAM"):
            return {"statusCode": 200, "body": qs.get("hub.challenge", "")}
        return {"statusCode": 403, "body": "verification failed"}

    body_raw = event.get("body") or ""
    body_bytes = base64.b64decode(body_raw) if event.get("isBase64Encoded") else body_raw.encode()

    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    if not _verify_signature(body_bytes, headers.get("x-hub-signature-256")):
        return {"statusCode": 403, "body": "bad signature"}

    payload = json.loads(body_bytes)
    print(f"payload: {json.dumps(payload)[:2000]}")
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            print(f"change field={change.get('field')!r}")
            if change.get("field") == "comments":
                try:
                    _handle_comment(change.get("value") or {})
                except Exception as exc:
                    print(f"comment handling failed: {exc}")
        for msg_event in entry.get("messaging", []):
            try:
                _handle_message(msg_event)
            except Exception as exc:
                print(f"message handling failed: {exc}")

    return {"statusCode": 200, "body": "ok"}
