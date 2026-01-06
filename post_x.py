#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

import requests
from requests_oauthlib import OAuth1

MEDIA_UPLOAD_URL = "https://upload.twitter.com/1.1/media/upload.json"
TWEET_CREATE_URL = "https://api.x.com/2/tweets"


def env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise SystemExit(f"Missing env var: {name}")
    return v


def upload_media_oauth1(image_path: Path, auth: OAuth1) -> str:
    with image_path.open("rb") as f:
        files = {"media": f}
        r = requests.post(MEDIA_UPLOAD_URL, files=files, auth=auth, timeout=60)
    r.raise_for_status()
    media_id = r.json().get("media_id_string")
    if not media_id:
        raise RuntimeError(f"media_id_string missing. response={r.text}")
    return media_id


def create_tweet_v2_oauth1(text: str, media_id: str, auth: OAuth1) -> str:
    payload = {"text": text, "media": {"media_ids": [media_id]}}
    r = requests.post(TWEET_CREATE_URL, json=payload, auth=auth, timeout=60)
    r.raise_for_status()
    data = r.json().get("data", {})
    tweet_id = data.get("id")
    if not tweet_id:
        raise RuntimeError(f"tweet id missing. response={r.text}")
    return tweet_id


def main():
    p = argparse.ArgumentParser(description="Upload image + post tweet (OAuth1 user context).")
    p.add_argument("--image", default="x_card.png", help="PNG path (default: x_card.png)")
    p.add_argument("--meta", default="x_out.json", help="Write output json (default: x_out.json)")
    p.add_argument("--text", default=None, help="Tweet text. If omitted, tries reading line1 from meta.")
    p.add_argument("--dry", action="store_true", help="Do everything except creating tweet (upload only).")
    args = p.parse_args()

    # OAuth 1.0a user context (this is the 'B yolu')
    api_key = env("X_API_KEY")
    api_secret = env("X_API_SECRET")
    access_token = env("X_ACCESS_TOKEN")
    access_secret = env("X_ACCESS_TOKEN_SECRET")

    auth = OAuth1(api_key, api_secret, access_token, access_secret)

    image_path = Path(args.image).resolve()
    if not image_path.exists():
        raise SystemExit(f"Image not found: {image_path}")

    # text
    text = args.text or "2026 is complete."
    # (istersen daha sonra run.py x_out.json yazıyorsa buradan okuyabiliriz)

    media_id = upload_media_oauth1(image_path, auth)
    print(f"OK: media_id={media_id}")

    out = {"media_id": media_id, "text": text}

    if args.dry:
        out["tweet_id"] = None
        print("DRY RUN: skipped tweet create.")
    else:
        tweet_id = create_tweet_v2_oauth1(text, media_id, auth)
        out["tweet_id"] = tweet_id
        print(f"OK: tweet_id={tweet_id}")

    Path(args.meta).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Saved meta: {Path(args.meta).resolve()}")


if __name__ == "__main__":
    main()