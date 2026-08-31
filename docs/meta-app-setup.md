# Meta app + webhook setup

One-time manual setup in Meta's own dashboard and AWS, for the comment → DM → follow-check →
PDF-guide growth loop. This automates only your own Instagram account, so **no App Review is
required** — App Review only kicks in when other people's accounts connect to your app.

## 1. Overview

```
comment (trigger keyword) → Meta webhook → API Gateway → Lambda
  → private reply, asking them to follow + reply
  → (on their reply) real follow-check via the User Profile API
  → following: PDF guide delivered as a message attachment
  → not following: prompted to follow and reply again
```

Everything runs on AWS free tier (API Gateway HTTP API, Lambda, S3, a tiny DynamoDB table) plus
Meta's free Graph API — no subscriptions.

## 2. Prerequisites

- Instagram account converted to **Business or Creator** (Professional) — personal accounts
  aren't supported by the API.
- That account linked to a Facebook Page.
- The infra deployed (`sam build && sam deploy --guided` from `infra/`) — you need the resulting
  API Gateway URL and the S3 bucket name before starting the Meta side below.

## 3. Creating the Meta Developer App

1. Go to [developers.facebook.com/apps](https://developers.facebook.com/apps) → Create App →
   choose the type that includes the **Instagram** product (Business type covers this).
2. Add the **Instagram** product to the app from the app dashboard.

## 4. Instagram Tester role — this is what avoids App Review

1. In the app dashboard, under Instagram → API setup (or Roles → Instagram Testers, depending on
   the current dashboard layout), add your own Instagram account as a **Tester**.
2. Accept the invite from your Instagram app's own Settings → Apps and Websites (or the
   notification Meta sends).
3. Leave the app in **Development Mode** — since only your own tester-role account will ever
   connect, it never needs to go Live or through Review.

## 5. Generating a long-lived access token

1. Use the Graph API Explorer (or the token generation flow in the app's Instagram setup page) to
   generate a token for your account with `instagram_business_basic` +
   `instagram_business_manage_comments` (Instagram Login) — or `instagram_basic` +
   `instagram_manage_comments` + `pages_read_engagement` if you're on the Facebook Login flow
   (see the note in `infra/lambda/handler.py` about `GRAPH_API_BASE` — confirm which flow you're
   on and that the constant matches).
2. Exchange it for a **long-lived** token (60-day, Meta documents the exchange endpoint).
3. Store it in SSM Parameter Store as a `SecureString` at the parameter name your stack uses
   (default `/reel-pipeline/ig-access-token`):
   ```bash
   aws ssm put-parameter --name /reel-pipeline/ig-access-token --type SecureString --value "<token>"
   ```
4. Also store your **IG business account's user id** the same way
   (`/reel-pipeline/ig-user-id`), the **app secret** from the app's Basic Settings
   (`/reel-pipeline/ig-app-secret`), and a **verify token** you make up yourself — any random
   string, it's just a shared secret for the webhook handshake (`/reel-pipeline/ig-verify-token`).

## 6. Subscribing to webhooks

1. In the app dashboard, under Webhooks (or Instagram → Webhooks), point the callback URL at the
   `WebhookUrl` output from your SAM deploy (`.../webhook`), and enter the same verify token you
   stored in step 5.
2. Meta calls the URL with a `GET` to confirm; the Lambda's verification handler responds — this
   should go green immediately if the token matches.
3. Subscribe to the **`comments`** and **`messages`** fields on the Instagram object.

## 7. Publishing a reel

**Preferred: the dashboard's "Approve & Publish" button** — one click reviews the caption, posts
the reel live via Meta's Content Publishing API, and registers its trigger against the real media
ID automatically, no manual ID-copying. It needs one extra permission first:

1. In the app dashboard: Permissions and features → add **`instagram_content_publish`** (alongside
   the three already granted).
2. **Regenerate the access token** for the tester account — a token's granted scopes are fixed at
   generation time, so the existing one won't include the new permission until refreshed.
3. Update the SSM parameter with the new token (same parameter the Lambda already reads):
   ```bash
   aws ssm put-parameter --name /reel-pipeline/ig-access-token --type SecureString --value "<new token>" --overwrite
   ```
4. In the dashboard, once a project shows **PDF** and **REN** lit, click **Approve & Publish** —
   confirm the caption in the dialog, enter (or accept the pre-filled) trigger keyword, and it
   handles the rest: uploads the render to S3, creates the Reels container, waits for Meta to
   finish processing it (30s–a few minutes), publishes it live, and writes the trigger.

Note: API-published Reels are capped at **90 seconds**, MP4/MOV with H.264 — the publish script
checks this via `ffprobe` and fails clearly before calling Meta's API if a render is too long.

**Fallback — publishing manually through the Instagram app instead:** still fully supported.

1. Get the reel's **IG media ID** (Graph API Explorer: `GET /{ig-user-id}/media`, or from the
   post's permalink via the API).
2. In the dashboard, once that project shows **Uploaded**, enter the media ID and your chosen
   trigger keyword in its trigger form and hit **Save trigger** — this updates `triggers.json` in
   S3, which the Lambda reads on every webhook event. No redeploy needed.

## 8. Testing checklist

**Before testing: add the second account as a Tester too.** While the app is in Development
Mode, Meta only surfaces data (API reads *and* webhook events) for accounts that have an
assigned role on the app. A comment from an account with no role is invisible end-to-end — it
won't appear via `GET /{media-id}/comments` (you'll see `comments_count` go up but `data: []`,
with populated pagination cursors — that combination is the tell) and no `comments` webhook
fires for it. Add the second account under Instagram → API setup → Testers, accept the invite
from that account's own Settings → Apps and Websites, then proceed below.

1. From a **second** Instagram account (added as a Tester, see above), comment the trigger keyword on the tracked post.
2. Confirm the private reply arrives in that account's DMs.
3. Reply to it (anything).
4. Confirm the follow-check branches correctly — test once **not** following (should prompt to
   follow) and once **following** (should deliver the PDF).
5. Confirm the PDF attachment actually opens.

## 9. Rate limits & policy notes

- Standard Graph API rate limits apply at this account's scale — not a practical concern for a
  personal creator account's comment volume.
- Meta's platform policy requires trigger keywords to be genuinely relevant to the content, not
  spam bait ("comment ANYTHING for a prize").
- The Private Reply window is 7 days from the comment's creation time — comfortably covered by a
  webhook, which fires in real time.
