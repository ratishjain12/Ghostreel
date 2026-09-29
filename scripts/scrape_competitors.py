import argparse
import json
import os
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import boto3
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
GROWTH_DIR = ROOT / "growth"
COMPETITORS_FILE = GROWTH_DIR / "competitors.json"
OUT_DIR = GROWTH_DIR / "competitors"

# business_discovery only exists on the Facebook Login flavor of the Graph API —
# graph.instagram.com (the Instagram Login token the rest of this repo uses) returns
# "nonexisting field (business_discovery)". Hence a second, separate token.
GRAPH_API_BASE = "https://graph.facebook.com/v21.0"
# media_url is a short-lived signed CDN link (hours), so transcribe_competitors.py has to
# run right after this. Meta omits it on reels with copyrighted audio.
MEDIA_FIELDS = "id,caption,like_count,comments_count,timestamp,media_type,media_product_type,permalink,media_url"
OUTLIER_RATIO = 3.0

load_dotenv(ROOT / ".env")
FB_TOKEN_PARAM = os.environ.get("IG_FB_ACCESS_TOKEN_PARAM", "/reel-pipeline/ig-fb-access-token")
FB_USER_ID_PARAM = os.environ.get("IG_FB_USER_ID_PARAM", "/reel-pipeline/ig-fb-user-id")


def _ssm_param(name):
    return boto3.client("ssm").get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]


def _graph_get(path, params):
    url = f"{GRAPH_API_BASE}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Graph API {exc.code}: {exc.read().decode()}") from exc


def fetch_account(ig_user_id, token, handle, limit, with_views):
    fields = MEDIA_FIELDS + (",view_count" if with_views else "")
    posts, after, profile = [], None, None
    while len(posts) < limit:
        page = f".after({after})" if after else ""
        bd = (
            f"business_discovery.username({handle})"
            f"{{followers_count,media_count,media.limit(25){page}{{{fields}}}}}"
        )
        data = _graph_get(ig_user_id, {"fields": bd, "access_token": token})["business_discovery"]
        profile = profile or {"followers_count": data.get("followers_count"), "media_count": data.get("media_count")}
        media = data.get("media", {})
        posts.extend(media.get("data", []))
        after = media.get("paging", {}).get("cursors", {}).get("after")
        if not after or not media.get("data"):
            break
    return profile, posts[:limit]


def score(posts):
    # Saves aren't exposed for accounts you don't own, so "outlier" here means
    # performance relative to that account's own median — normalises away follower
    # count so a 5K page and a 500K page are comparable. Reels and feed posts are
    # scored separately: only reels carry view_count, and feed likes run on a
    # different scale than reel likes, so one shared median would misrank both.
    medians = {}
    groups = {}
    for p in posts:
        groups.setdefault(p.get("media_product_type") or "FEED", []).append(p)
    for kind, group in groups.items():
        metric = "view_count" if sum(1 for p in group if p.get("view_count")) > len(group) / 2 else "like_count"
        values = [p[metric] for p in group if p.get(metric) is not None]
        median = statistics.median(values) if values else 0
        medians[kind] = {"metric": metric, "median": median, "posts": len(group)}
        for p in group:
            v = p.get(metric)
            p["score_metric"] = metric
            p["outlier_ratio"] = round(v / median, 2) if median and v is not None else None
    return medians


def main():
    parser = argparse.ArgumentParser(description="Pull public post metrics for competitor IG accounts via Business Discovery.")
    parser.add_argument("--handles", nargs="*", help=f"defaults to the list in {COMPETITORS_FILE.relative_to(ROOT)}")
    parser.add_argument("--limit", type=int, default=50, help="posts per account")
    args = parser.parse_args()

    handles = args.handles or json.loads(COMPETITORS_FILE.read_text())
    try:
        token = _ssm_param(FB_TOKEN_PARAM)
        ig_user_id = _ssm_param(FB_USER_ID_PARAM)
    except boto3.client("ssm").exceptions.ParameterNotFound:
        raise SystemExit(f"{FB_TOKEN_PARAM} / {FB_USER_ID_PARAM} not in SSM yet — see docs/meta-app-setup.md § 7b")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with_views = True
    outliers = []
    for handle in handles:
        print(f"{handle}: fetching…", flush=True)
        try:
            try:
                profile, posts = fetch_account(ig_user_id, token, handle, args.limit, with_views)
            except RuntimeError as exc:
                if not (with_views and "view_count" in str(exc)):
                    raise
                print("  view_count not available via business_discovery — falling back to likes", flush=True)
                with_views = False
                profile, posts = fetch_account(ig_user_id, token, handle, args.limit, with_views)
        except RuntimeError as exc:
            # Personal (non-Business/Creator) accounts aren't discoverable — skip, don't abort the batch.
            print(f"  skipped: {exc}", file=sys.stderr, flush=True)
            continue

        medians = score(posts)
        (OUT_DIR / f"{handle}.json").write_text(json.dumps({
            "handle": handle,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            **profile,
            "medians": medians,
            "posts": posts,
        }, indent=2))
        hits = [p for p in posts if (p.get("outlier_ratio") or 0) >= OUTLIER_RATIO]
        outliers.extend({"handle": handle, **p} for p in hits)
        summary = ", ".join(f"{k} median {m['metric']} {m['median']:g} (n={m['posts']})" for k, m in medians.items())
        print(f"  {len(posts)} posts — {summary} — {len(hits)} outliers (≥{OUTLIER_RATIO}x)", flush=True)

    outliers.sort(key=lambda p: p["outlier_ratio"], reverse=True)
    (GROWTH_DIR / "competitor-outliers.json").write_text(json.dumps(outliers, indent=2))
    print(f"wrote {len(outliers)} outliers to growth/competitor-outliers.json")


if __name__ == "__main__":
    main()
