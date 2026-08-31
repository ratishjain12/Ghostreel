import argparse
import re
import subprocess
from pathlib import Path

import torch
import torchaudio as ta
from chatterbox.tts_turbo import ChatterboxTurboTTS

SENTENCES_PER_CHUNK_DEFAULT = 2
SILENCE_GAP_SEC_DEFAULT = 0.15
# Chatterbox-Turbo's default pace reads as sluggish for reel narration; Turbo ignores
# cfg_weight/exaggeration (its own `generate()` warns and drops them), so pace isn't
# tunable at the model level — speed it up after the fact instead, pitch-preserved.
SPEED_DEFAULT = 1.12


def load_model():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    map_location = torch.device(device)

    torch_load_original = torch.load

    def patched_torch_load(*args, **kwargs):
        kwargs.setdefault("map_location", map_location)
        return torch_load_original(*args, **kwargs)

    torch.load = patched_torch_load

    print(f"Loading Chatterbox-Turbo on device: {device}")
    return ChatterboxTurboTTS.from_pretrained(device=device)


def wav_duration(path):
    info = ta.info(str(path))
    return info.num_frames / info.sample_rate


def chunk_text(text, sentences_per_chunk):
    sentences = re.split(r"(?<=[.!?])\s+", text.replace("\n\n", " ").replace("\n", " "))
    sentences = [s.strip() for s in sentences if s.strip()]
    return [
        " ".join(sentences[i:i + sentences_per_chunk])
        for i in range(0, len(sentences), sentences_per_chunk)
    ]


def _apply_speed(wav_path, speed):
    """Pitch-preserving tempo change via ffmpeg's atempo filter (0.5-2.0 in one pass)."""
    if speed == 1.0:
        return
    tmp_path = wav_path.with_suffix(".tmp.wav")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path), "-filter:a", f"atempo={speed}", str(tmp_path)],
        check=True,
    )
    tmp_path.replace(wav_path)


def generate_voice(model, text, voice_ref_path, out_path, sentences_per_chunk=SENTENCES_PER_CHUNK_DEFAULT, silence_gap_sec=SILENCE_GAP_SEC_DEFAULT, speed=SPEED_DEFAULT):
    chunks = chunk_text(text, sentences_per_chunk)
    print(f"[{out_path.stem}] {len(chunks)} chunk(s)")

    sample_rate = model.sr
    silence_gap = torch.zeros(1, int(sample_rate * silence_gap_sec))

    wav_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"  generating chunk {i + 1}/{len(chunks)}...")
        wav = model.generate(chunk, audio_prompt_path=str(voice_ref_path))
        wav_chunks.append(wav)
        if i < len(chunks) - 1:
            wav_chunks.append(silence_gap)

    final_wav = torch.cat(wav_chunks, dim=-1)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ta.save(str(out_path), final_wav, sample_rate)
    _apply_speed(out_path, speed)

    duration = wav_duration(out_path)
    print(f"  saved {out_path} ({duration:.2f}s)")
    return out_path, duration


def main():
    parser = argparse.ArgumentParser(description="Generate a Chatterbox voiceover from a text script.")
    parser.add_argument("--text", required=True, type=Path, help="Path to the narration script (.txt)")
    parser.add_argument("--voice-ref", default=Path("voice_ref.wav"), type=Path, help="Reference voice sample")
    parser.add_argument("--out", type=Path, help="Output .wav path (default: audio/<text stem>.wav)")
    parser.add_argument("--sentences-per-chunk", type=int, default=SENTENCES_PER_CHUNK_DEFAULT)
    parser.add_argument("--silence-gap", type=float, default=SILENCE_GAP_SEC_DEFAULT)
    parser.add_argument("--speed", type=float, default=SPEED_DEFAULT, help="Post-generation tempo multiplier, pitch-preserved (1.0 = off)")
    args = parser.parse_args()

    out = args.out or Path("audio") / f"{args.text.stem}.wav"
    text = args.text.read_text().strip()

    model = load_model()
    generate_voice(model, text, args.voice_ref, out, args.sentences_per_chunk, args.silence_gap, args.speed)


if __name__ == "__main__":
    main()
