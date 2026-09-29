import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

import boto3

ssm = boto3.client("ssm")

# A competitor-research Page token has expires_at=0, but it still carries Meta's
# 90-day data-access expiry, and only the user logging in again resets that. There's
# no API to extend it, so the most this can do is fail loudly well before it lapses.
DATA_ACCESS_WARN_DAYS = 14


def _get_param(name):
    return ssm.get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]


def _get_json(url):
    try:
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"{exc.code} from {url.split('?')[0]}: {exc.read().decode()}") from exc


def refresh_instagram_token():
    # Instagram Login long-lived tokens last 60 days and can be refreshed once
    # they're at least 24h old; each refresh returns a fresh 60-day token. Running
    # weekly keeps it far from expiry, so a missed run or two is harmless.
    name = os.environ["ACCESS_TOKEN_PARAM"]
    qs = urllib.parse.urlencode({"grant_type": "ig_refresh_token", "access_token": _get_param(name)})
    resp = _get_json(f"https://graph.instagram.com/refresh_access_token?{qs}")
    ssm.put_parameter(Name=name, Value=resp["access_token"], Type="SecureString", Overwrite=True)
    days = resp.get("expires_in", 0) // 86400
    print(f"instagram token refreshed, valid for {days} more days")
    return days


def check_competitor_token():
    app_token = f"{os.environ['FB_APP_ID']}|{_get_param(os.environ['FB_APP_SECRET_PARAM'])}"
    qs = urllib.parse.urlencode({"input_token": _get_param(os.environ["FB_TOKEN_PARAM"]), "access_token": app_token})
    data = _get_json(f"https://graph.facebook.com/v21.0/debug_token?{qs}")["data"]
    if not data.get("is_valid"):
        raise RuntimeError(f"competitor-research token is invalid: {data.get('error')}")
    now = time.time()
    deadlines = [t for t in (data.get("expires_at"), data.get("data_access_expires_at")) if t]
    days_left = (min(deadlines) - now) / 86400 if deadlines else None
    if days_left is not None and days_left < DATA_ACCESS_WARN_DAYS:
        raise RuntimeError(
            f"competitor-research token loses data access in {days_left:.0f} days: regenerate it "
            "(docs/meta-app-setup.md § 7b) or switch to a system-user token"
        )
    print(f"competitor token OK, {'no expiry' if days_left is None else f'{days_left:.0f} days of data access left'}")
    return days_left


def handler(event, context):
    errors = []
    result = {}
    for key, fn in (("instagram_days", refresh_instagram_token), ("competitor_days", check_competitor_token)):
        try:
            result[key] = fn()
        except Exception as exc:
            print(f"ERROR {fn.__name__}: {exc}")
            errors.append(f"{fn.__name__}: {exc}")
    if errors:
        # Raise so a failed refresh shows up as a Lambda error in CloudWatch.
        raise RuntimeError("; ".join(errors))
    return result
