import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

import boto3

GRAPH_API_BASE = "https://graph.instagram.com/v21.0"
POLL_INTERVAL_SEC = 10
POLL_TIMEOUT_SEC = 300
TRIGGERS_KEY = "triggers.json"

_REGION = os.environ.get("AWS_REGION", "us-east-1")
s3 = boto3.client("s3", region_name=_REGION, endpoint_url=f"https://s3.{_REGION}.amazonaws.com")
ssm = boto3.client("ssm")
dynamodb = boto3.resource("dynamodb")

BUCKET = os.environ["BUCKET_NAME"]
SCHEDULE_TABLE = os.environ["SCHEDULE_TABLE"]

_param_cache = {}


def _param(name_env):
    if name_env not in _param_cache:
        name = os.environ[name_env]
        resp = ssm.get_parameter(Name=name, WithDecryption=True)
        _param_cache[name_env] = resp["Parameter"]["Value"]
    return _param_cache[name_env]


def _table():
    return dynamodb.Table(SCHEDULE_TABLE)


def _graph_error(exc, url):
    # Without this, a rejected request just shows up as "HTTP Error 400: Bad
    # Request" in the schedule item's error field — Instagram's actual reason
    # (invalid token, unsupported format, rate limit, ...) is in the response
    # body, which urllib doesn't surface unless you read it off the exception.
    try:
        body = exc.read().decode()
    except Exception:
        body = "<no response body>"
    return RuntimeError(f"Graph API error {exc.code} for {url}: {body}")


def _graph_post(path, payload, access_token):
    url = f"{GRAPH_API_BASE}/{path}?access_token={access_token}"
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise _graph_error(exc, f"POST {path}") from exc


def _graph_get(path, params, access_token):
    params = {**params, "access_token": access_token}
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    try:
        with urllib.request.urlopen(f"{GRAPH_API_BASE}/{path}?{qs}") as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise _graph_error(exc, f"GET {path}") from exc


def _create_container(ig_user_id, video_url, caption, access_token):
    resp = _graph_post(f"{ig_user_id}/media", {"media_type": "REELS", "video_url": video_url, "caption": caption}, access_token)
    creation_id = resp.get("id")
    if not creation_id:
        raise RuntimeError(f"container creation failed: {resp}")
    return creation_id


def _wait_for_container(creation_id, access_token):
    elapsed = 0
    while elapsed <= POLL_TIMEOUT_SEC:
        status = _graph_get(creation_id, {"fields": "status_code,status"}, access_token)
        code = status.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container processing failed: {status}")
        time.sleep(POLL_INTERVAL_SEC)
        elapsed += POLL_INTERVAL_SEC
    raise RuntimeError(f"container did not finish processing within {POLL_TIMEOUT_SEC}s")


def _publish_container(ig_user_id, creation_id, access_token):
    resp = _graph_post(f"{ig_user_id}/media_publish", {"creation_id": creation_id}, access_token)
    media_id = resp.get("id")
    if not media_id:
        raise RuntimeError(f"publish failed: {resp}")
    return media_id


def _register_trigger(name, media_id, keyword, pdf_key):
    try:
        triggers = json.loads(s3.get_object(Bucket=BUCKET, Key=TRIGGERS_KEY)["Body"].read())
    except s3.exceptions.NoSuchKey:
        triggers = {}
    triggers[media_id] = {"keyword": keyword, "name": name, "pdf_key": pdf_key}
    s3.put_object(Bucket=BUCKET, Key=TRIGGERS_KEY, Body=json.dumps(triggers, indent=2).encode(), ContentType="application/json")


def handler(event, context):
    item_id = event["id"]
    name = event["name"]
    s3_key = event["s3_key"]
    caption = event.get("caption") or name
    pdf_key = event.get("pdf_key")
    # Blank/absent keyword must mean "no trigger, ever" — this is the only place a
    # trigger gets registered, and it only runs when the caller explicitly asked.
    keyword = (event.get("keyword") or "").strip() or None

    table = _table()

    try:
        ig_user_id = _param("IG_USER_ID_PARAM")
        access_token = _param("ACCESS_TOKEN_PARAM")

        video_url = s3.generate_presigned_url("get_object", Params={"Bucket": BUCKET, "Key": s3_key}, ExpiresIn=3600)
        creation_id = _create_container(ig_user_id, video_url, caption, access_token)
        _wait_for_container(creation_id, access_token)
        media_id = _publish_container(ig_user_id, creation_id, access_token)

        if keyword and pdf_key:
            _register_trigger(name, media_id, keyword, pdf_key)

        table.update_item(
            Key={"id": item_id},
            UpdateExpression="SET #s = :status, media_id = :media_id, published_at = :published_at REMOVE #e",
            ExpressionAttributeNames={"#s": "status", "#e": "error"},
            ExpressionAttributeValues={
                ":status": "done",
                ":media_id": media_id,
                ":published_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as exc:
        table.update_item(
            Key={"id": item_id},
            UpdateExpression="SET #s = :status, #e = :error",
            ExpressionAttributeNames={"#s": "status", "#e": "error"},
            ExpressionAttributeValues={":status": "error", ":error": str(exc)[:500]},
        )
        raise
