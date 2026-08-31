import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel

MAX_WORDS_PER_LINE_DEFAULT = 5
MAX_LINE_DURATION_DEFAULT = 2.5


def load_model(model_size="base", device="cpu", compute_type="int8"):
    print(f"Loading Whisper model ({model_size}, {device})...")
    return WhisperModel(model_size, device=device, compute_type=compute_type)


def generate_captions(model, audio_path, out_path, max_words_per_line=MAX_WORDS_PER_LINE_DEFAULT, max_line_duration=MAX_LINE_DURATION_DEFAULT):
    print(f"[{audio_path.stem}] transcribing with word-level timestamps...")
    segments, _ = model.transcribe(str(audio_path), word_timestamps=True)

    all_words = []
    for segment in segments:
        for word in segment.words:
            all_words.append({"word": word.word.strip(), "start": word.start, "end": word.end})

    caption_lines = []
    current_line = []
    line_start = None

    for w in all_words:
        if not current_line:
            line_start = w["start"]
        current_line.append(w)

        line_duration = w["end"] - line_start
        if len(current_line) >= max_words_per_line or line_duration >= max_line_duration:
            caption_lines.append({
                "text": " ".join(x["word"] for x in current_line),
                "start": line_start,
                "end": current_line[-1]["end"],
            })
            current_line = []

    if current_line:
        caption_lines.append({
            "text": " ".join(x["word"] for x in current_line),
            "start": line_start,
            "end": current_line[-1]["end"],
        })

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(caption_lines, f, indent=2)

    print(f"  saved {len(caption_lines)} caption lines to {out_path}")
    return caption_lines


def main():
    parser = argparse.ArgumentParser(description="Transcribe a wav into word/phrase-level caption lines.")
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--out", type=Path, help="Output .json path (default: <audio dir>/<audio stem>-captions.json)")
    parser.add_argument("--max-words-per-line", type=int, default=MAX_WORDS_PER_LINE_DEFAULT)
    parser.add_argument("--max-line-duration", type=float, default=MAX_LINE_DURATION_DEFAULT)
    parser.add_argument("--model-size", default="base")
    args = parser.parse_args()

    out = args.out or args.audio.parent / f"{args.audio.stem}-captions.json"

    model = load_model(args.model_size)
    generate_captions(model, args.audio, out, args.max_words_per_line, args.max_line_duration)


if __name__ == "__main__":
    main()
