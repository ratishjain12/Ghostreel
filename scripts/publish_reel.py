import argparse
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_reel_batch import first_sentence
from upload_resources import get_client, set_trigger

GRAPH_API_BASE = "https://graph.instagram.com/v21.0"
MAX_DURATION_SEC = 90
POLL_INTERVAL_SEC = 10
POLL_TIMEOUT_SEC = 300

_ssm_cache = {}


def _ssm_param(name):
    if name not in _ssm_cache:
        ssm = boto3.client("ssm")
        resp = ssm.get_parameter(Name=name, WithDecryption=True)
        _ssm_cache[name] = resp["Parameter"]["Value"]
    return _ssm_cache[name]


def latest_render(project_dir):
    renders = sorted((project_dir / "renders").glob("*.mp4"), key=lambda p: p.stat().st_mtime)
    if not renders:
        raise SystemExit(f"no render found in {project_dir / 'renders'} — render the project first")
    return renders[-1]


def check_duration(video_path, max_duration=MAX_DURATION_SEC):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video_path)],
        capture_output=True, text=True, check=True,
    )
    duration = float(result.stdout.strip())
    if duration > max_duration:
        raise SystemExit(f"{video_path.name} is {duration:.1f}s — Instagram's API-published Reels cap is {max_duration}s")
    print(f"  duration OK: {duration:.1f}s")
    return duration


def upload_render(client, bucket, name, video_path):
    key = f"{name}/render.mp4"
    client.upload_file(str(video_path), bucket, key, ExtraArgs={"ContentType": "video/mp4"})
    print(f"  uploaded s3://{bucket}/{key}")
    url = client.generate_presigned_url("get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600)
    return url


def _graph_post(path, payload, access_token):
    url = f"{GRAPH_API_BASE}/{path}?access_token={access_token}"
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def _graph_get(path, params, access_token):
    params = {**params, "access_token": access_token}
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    with urllib.request.urlopen(f"{GRAPH_API_BASE}/{path}?{qs}") as resp:
        return json.loads(resp.read())


def create_container(ig_user_id, video_url, caption, access_token):
    resp = _graph_post(f"{ig_user_id}/media", {"media_type": "REELS", "video_url": video_url, "caption": caption}, access_token)
    creation_id = resp.get("id")
    if not creation_id:
        raise SystemExit(f"container creation failed: {resp}")
    print(f"  container created: {creation_id}")
    return creation_id


def wait_for_container(creation_id, access_token, timeout=POLL_TIMEOUT_SEC, interval=POLL_INTERVAL_SEC):
    elapsed = 0
    while elapsed <= timeout:
        status = _graph_get(creation_id, {"fields": "status_code,status"}, access_token)
        code = status.get("status_code")
        print(f"  container status: {code}")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise SystemExit(f"container processing failed: {status}")
        time.sleep(interval)
        elapsed += interval
    raise SystemExit(f"container did not finish processing within {timeout}s")


def publish_container(ig_user_id, creation_id, access_token):
    resp = _graph_post(f"{ig_user_id}/media_publish", {"creation_id": creation_id}, access_token)
    media_id = resp.get("id")
    if not media_id:
        raise SystemExit(f"publish failed: {resp}")
    print(f"  published: media id {media_id}")
    return media_id


def publish_reel(name, project_dir, bucket, caption=None, keyword=None, client=None):
    client = client or get_client()
    ig_user_id = _ssm_param("/reel-pipeline/ig-user-id")
    access_token = _ssm_param("/reel-pipeline/ig-access-token")

    video_path = latest_render(project_dir)
    check_duration(video_path)

    if caption is None:
        text_path = Path("scripts") / "reels" / f"{name}.txt"
        meta_path = Path("scripts") / "reels" / f"{name}.meta.json"
        text = text_path.read_text().strip() if text_path.exists() else ""
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        caption = meta.get("message") or (first_sentence(text) if text else name)

    video_url = upload_render(client, bucket, name, video_path)
    creation_id = create_container(ig_user_id, video_url, caption, access_token)
    wait_for_container(creation_id, access_token)
    media_id = publish_container(ig_user_id, creation_id, access_token)

    marker = {"media_id": media_id, "published_at": datetime.now(timezone.utc).isoformat()}
    published_path = project_dir / "resources" / "published.json"
    published_path.write_text(json.dumps(marker, indent=2))
    print(f"  wrote {published_path}")

    trigger_path = project_dir / "resources" / "trigger.json"
    if keyword is None and trigger_path.exists():
        keyword = json.loads(trigger_path.read_text()).get("keyword")

    pdf_key = f"{name}/guide.pdf"
    if keyword:
        set_trigger(name, project_dir, bucket, media_id, keyword, pdf_key, client=client)

    return marker


def main():
    parser = argparse.ArgumentParser(description="Publish a project's render to Instagram as a Reel, then register its trigger.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--video-out", default=Path("video"), type=Path)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--caption", help="Override caption (default: BRIEF message / script's first sentence)")
    parser.add_argument("--keyword", help="Trigger keyword to register against the new media id")
    args = parser.parse_args()

    project_dir = args.video_out / args.name
    publish_reel(args.name, project_dir, args.bucket, caption=args.caption, keyword=args.keyword)


if __name__ == "__main__":
    main()
