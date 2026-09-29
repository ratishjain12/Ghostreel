import difflib, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WAV = ROOT.parents[1] / "audio/async-is-not-parallel.wav"
script = (ROOT / "user_script.txt").read_text().split()
whisper = json.loads((ROOT / "capture/extracted/whisper-words.json").read_text())
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())

a, b = [norm(w) for w in script], [norm(w["text"]) for w in whisper]
timed = [None] * len(script)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            timed[i1 + k] = (whisper[j1 + k]["start"], whisper[j1 + k]["end"])
    elif tag == "replace" or (tag == "insert" and False):
        s, e = whisper[j1]["start"], whisper[j2 - 1]["end"]
        n = i2 - i1
        for k in range(n):
            timed[i1 + k] = (s + (e - s) * k / n, s + (e - s) * (k + 1) / n)
for i, t in enumerate(timed):
    if t is None:
        prev = timed[i - 1][1] if i else 0.0
        timed[i] = (prev, prev + 0.12)
        print("untimed:", script[i])

# first word of each frame (script index) — frame boundaries at sentence breaks
starts = ["You", "The handler", "With async,", "That's concurrency:", "Now you add", "An async",
          "Running work", "So the", "Mix them", "Comment guide"]
idx, pos = [], 0
for s in starts:
    toks = s.split()
    while script[pos:pos + len(toks)] != toks:
        pos += 1
    idx.append(pos)
idx.append(len(script))

dur_total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(WAV)]))
cuts = [0.0]
for k in idx[1:-1]:
    cuts.append(round((timed[k - 1][1] + timed[k][0]) / 2, 3))
cuts.append(dur_total)

voice_dir = ROOT / "assets/voice"
voice_dir.mkdir(parents=True, exist_ok=True)
voices, gid = [], 0
for f in range(len(starts)):
    t0, t1 = cuts[f], cuts[f + 1]
    out = voice_dir / f"{f + 1:02d}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(WAV), "-ss", f"{t0}", "-to", f"{t1}", "-c:a", "pcm_s16le", str(out)], check=True)
    words = []
    for k in range(idx[f], idx[f + 1]):
        s, e = timed[k]
        words.append({"id": f"{f + 1:02d}-{gid:02d}", "text": script[k], "start": round(max(0, s - t0), 3), "end": round(min(t1, e) - t0, 3)})
        gid += 1
    voices.append({"frame": f + 1, "path": f"assets/voice/{f + 1:02d}.wav", "duration_s": round(t1 - t0, 3), "words": words})
    print(f + 1, round(t0, 2), round(t1, 2), round(t1 - t0, 3), " ".join(w["text"] for w in words))

(ROOT / "audio_meta.json").write_text(json.dumps({"bgm": None, "bgm_pending": False, "sfx": [], "voices": voices}, indent=2) + "\n")
