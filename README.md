# Reel Pipeline — Setup Guide

Turns a short script into a voiced, captioned, rendered vertical video (1080×1920, ready for
Reels/Shorts/TikTok) via a local dashboard. You write or paste a script, the tool generates a
voiceover + word-level captions, and renders the final MP4 — no video editing required.

This guide covers **script → voice → captions → render**, the part this team needs day to day.
A couple of buttons in the dashboard (PDF, Approve & Publish) belong to a separate workflow —
ignore those.

---

## 1. Install prerequisites (once per machine)

You need four things installed. If you already have some of these, skip ahead.

- **Python 3.12+** — check with `python3 --version`.
- **[uv](https://docs.astral.sh/uv/)** (Python package manager):
  - Mac/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Node.js 20 LTS** — install from [nodejs.org](https://nodejs.org). This gives you `npm`.
- **ffmpeg**:
  - Mac: `brew install ffmpeg`
  - Windows: `choco install ffmpeg` (or download from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to PATH)
  - Linux: `sudo apt install ffmpeg`

> This has been run and verified on macOS. If something fails specifically on Windows or Linux
> during setup, that's likely a first-time-on-this-OS wrinkle, not something you're doing
> wrong — flag it rather than fighting it.

## 2. First-time setup

1. Unzip the project folder and open a terminal inside it.
2. Install the frontend dependencies:
   ```bash
   cd dashboard/web && npm install && cd ../..
   ```
3. Add a reference voice sample: drop a `voice_ref.wav` (a clean ~10-30s clip of the voice you
   want narration cloned from, no background noise/music) at the project root. This is a personal
   recording, not something that ships with the repo — you supply your own; it's gitignored so it
   never gets committed. Pass a different file per run with `--voice-ref` if you want more than one.
4. That's it for setup — Python dependencies install automatically the first time you run the
   dashboard (next step). That first run downloads the voice + captioning models, which can take
   a while (a few GB) — normal, only happens once.

## 3. Run the dashboard

**Mac/Linux**, from the project root:
```bash
make dev
```
This starts the backend and the frontend together. Open **http://localhost:5173**. Stop both
with `Ctrl+C`.

**Windows** (or if `make` isn't available), run these in two separate terminals from the project
root:
```bash
# terminal 1
uv run dashboard/server.py

# terminal 2
cd dashboard/web
npm run dev
```
Open **http://localhost:5173**.

The first `uv run` will take a few minutes — it's installing Python packages and downloading the
voice/captioning models. Later runs start in seconds.

## 4. Day-to-day workflow

1. **Add a script** — click **Add script** at the bottom of the Scripts panel, give it a
   lowercase-hyphenated name (e.g. `q4-launch-teaser`), paste the narration text, save.
2. **Generate** — select the script (checkbox) and click **Generate selected** (or **Generate
   all** for multiple). This creates the voiceover audio and word-level captions. Watch progress
   in the job log.
3. **Render** — once generation finishes, click **Render** on that script's row. This produces
   the final MP4.
4. **Preview** — rendered videos show up in the **Videos** panel, playable right in the browser.
   Files also land on disk at `video/<script-name>/renders/*.mp4`.

Everything else in each row (PDF, Approve & Publish) is a different, unrelated workflow — skip
those buttons.

## 5. Getting a new visual template

Render uses whatever scene visuals already exist in that project — a script alone doesn't invent
new visuals. New projects created via `scripts/gen_reel_batch.py` are auto-seeded with the shared
brand kit at `assets/` (`frame.md` design spec + `assets/fonts/`), so they start from an
established look instead of a blank slate. `video/explainer-01/` is a working example with
authored scenes already built on top of that same kit. If you need a genuinely different visual
template built from scratch, that's a step outside this guide — ask Ratish.

## Troubleshooting

- **`npm install` or `uv run` fails outright** — send the exact error, don't try to work around
  it blind.
- **Generate/Render job log shows an error** — the job log in the dashboard shows the real
  output; copy the last ~20 lines when asking for help.
- **A render looks visually broken or empty** — most likely the project has no authored scenes
  yet (see § 5) rather than a bug in Generate/Render themselves.
