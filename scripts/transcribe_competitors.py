import argparse
import json
import subprocess
import urllib.request
from pathlib import Path

from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent
GROWTH_DIR = ROOT / "growth"
MEDIA_DIR = GROWTH_DIR / "competitors" / "media"
TRANSCRIPTS_DIR = GROWTH_DIR / "competitors" / "transcripts"
HOOK_SECONDS = 3.0


def _shortcode(permalink):
    return permalink.rstrip("/").rsplit("/", 1)[-1]


def _download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
        f.write(resp.read())


def _to_wav(video, wav):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-ac", "1", "-ar", "16000", str(wav)], check=True)


def transcribe(model, wav):
    segments, info = model.transcribe(str(wav), word_timestamps=True, vad_filter=True)
    words = [{"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)} for s in segments for w in s.words]
    text = " ".join(w["word"] for w in words)
    speech = (words[-1]["end"] - words[0]["start"]) if words else 0
    return {
        "language": info.language,
        "duration": round(info.duration, 1),
        "word_count": len(words),
        "words_per_minute": round(len(words) / speech * 60) if speech else 0,
        "hook": " ".join(w["word"] for w in words if w["start"] < HOOK_SECONDS),
        "text": text,
        "words": words,
    }


def main():
    parser = argparse.ArgumentParser(description="Download and transcribe competitor outlier reels (run right after scrape_competitors.py).")
    parser.add_argument("--model", default="base")
    parser.add_argument("--min-ratio", type=float, default=1.5,
                        help="lower than the 3x outlier bar: most 3x reels use licensed music, which Meta strips media_url from")
    parser.add_argument("--force", action="store_true", help="re-transcribe reels that already have a transcript")
    args = parser.parse_args()

    reels = []
    for f in sorted((GROWTH_DIR / "competitors").glob("*.json")):
        account = json.loads(f.read_text())
        reels += [{"handle": account["handle"], **p} for p in account["posts"]
                  if p.get("media_type") == "VIDEO" and (p.get("outlier_ratio") or 0) >= args.min_ratio]
    reels.sort(key=lambda p: p["outlier_ratio"], reverse=True)
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    model = None
    for p in reels:
        code = _shortcode(p["permalink"])
        out = TRANSCRIPTS_DIR / f"{code}.json"
        if out.exists() and not args.force:
            continue
        if not p.get("media_url"):
            print(f"{p['handle']}/{code}: no media_url (copyrighted audio?), skipped", flush=True)
            continue
        video, wav = MEDIA_DIR / f"{code}.mp4", MEDIA_DIR / f"{code}.wav"
        try:
            if not video.exists():
                _download(p["media_url"], video)
            _to_wav(video, wav)
        except Exception as exc:
            print(f"{p['handle']}/{code}: download failed ({exc}), rerun scrape_competitors.py for fresh URLs", flush=True)
            continue
        model = model or WhisperModel(args.model, device="cpu", compute_type="int8")
        result = transcribe(model, wav)
        # Music-only reels make whisper hallucinate a few words in a random language.
        result["has_voiceover"] = result["word_count"] >= 30 and result["language"] == "en"
        out.write_text(json.dumps({
            "handle": p["handle"],
            "permalink": p["permalink"],
            "outlier_ratio": p["outlier_ratio"],
            "view_count": p.get("view_count"),
            "caption": p.get("caption"),
            **result,
        }, indent=2))
        if not result["has_voiceover"]:
            print(f"{p['handle']}/{code}: no voiceover (music/text-only reel)", flush=True)
            continue
        print(f"{p['handle']}/{code}: {p['outlier_ratio']}x, {result['duration']}s, {result['words_per_minute']} wpm — hook: {result['hook']!r}", flush=True)

    print(f"transcripts in {TRANSCRIPTS_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
