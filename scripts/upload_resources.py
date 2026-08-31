import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import boto3

TRIGGERS_KEY = "triggers.json"


def get_client():
    # See the matching comment in infra/lambda/handler.py — boto3's default S3
    # client presigns against the global s3.amazonaws.com host even with a
    # region set, which S3 rejects outside us-east-1. Force the regional
    # endpoint explicitly.
    region = boto3.Session().region_name or "us-east-1"
    return boto3.client("s3", region_name=region, endpoint_url=f"https://s3.{region}.amazonaws.com")


def _load_triggers(client, bucket):
    try:
        obj = client.get_object(Bucket=bucket, Key=TRIGGERS_KEY)
        return json.loads(obj["Body"].read())
    except client.exceptions.NoSuchKey:
        return {}


def _save_triggers(client, bucket, triggers):
    client.put_object(
        Bucket=bucket,
        Key=TRIGGERS_KEY,
        Body=json.dumps(triggers, indent=2).encode(),
        ContentType="application/json",
    )


def upload_resources(name, project_dir, bucket, client=None, media_id=None, keyword=None):
    client = client or get_client()

    guide_path = project_dir / "resources" / "guide.pdf"
    if not guide_path.exists():
        raise SystemExit(f"no {guide_path} — generate the PDF guide first")

    pdf_key = f"{name}/guide.pdf"
    client.upload_file(str(guide_path), bucket, pdf_key, ExtraArgs={"ContentType": "application/pdf"})
    print(f"  uploaded s3://{bucket}/{pdf_key}")

    marker = {
        "bucket": bucket,
        "pdf_key": pdf_key,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
    marker_path = project_dir / "resources" / "uploaded.json"
    marker_path.write_text(json.dumps(marker, indent=2))
    print(f"  wrote {marker_path}")

    trigger_path = project_dir / "resources" / "trigger.json"
    if media_id is None and trigger_path.exists():
        existing = json.loads(trigger_path.read_text())
        media_id = existing.get("media_id")
        keyword = keyword or existing.get("keyword")

    if media_id and keyword:
        set_trigger(name, project_dir, bucket, media_id, keyword, pdf_key, client=client)

    return marker


def set_trigger(name, project_dir, bucket, media_id, keyword, pdf_key, client=None):
    client = client or get_client()

    trigger_path = project_dir / "resources" / "trigger.json"
    trigger = {"media_id": media_id, "keyword": keyword}
    trigger_path.write_text(json.dumps(trigger, indent=2))
    print(f"  wrote {trigger_path}")

    triggers = _load_triggers(client, bucket)
    triggers[media_id] = {"keyword": keyword, "name": name, "pdf_key": pdf_key}
    _save_triggers(client, bucket, triggers)
    print(f"  updated s3://{bucket}/{TRIGGERS_KEY} ({len(triggers)} trigger(s))")

    return triggers


def main():
    parser = argparse.ArgumentParser(description="Upload a project's PDF guide to S3 and register its comment trigger.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--video-out", default=Path("video"), type=Path)
    parser.add_argument("--bucket", required=True, help="S3 bucket name (or set via --bucket)")
    parser.add_argument("--media-id", help="Instagram media ID to trigger on")
    parser.add_argument("--keyword", help="Comment trigger keyword")
    args = parser.parse_args()

    project_dir = args.video_out / args.name
    upload_resources(args.name, project_dir, args.bucket, media_id=args.media_id, keyword=args.keyword)


if __name__ == "__main__":
    main()
