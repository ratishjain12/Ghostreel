import json
import os
import re
import subprocess
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts" / "reels"
AUDIO_DIR = ROOT / "audio"
VIDEO_DIR = ROOT / "video"
CAROUSEL_SCRIPTS_DIR = ROOT / "scripts" / "carousels"
CAROUSEL_DIR = ROOT / "carousels"
STATIC_DIR = Path(__file__).resolve().parent / "static"
S3_BUCKET = os.environ.get("S3_BUCKET")
SCHEDULE_TABLE = os.environ.get("SCHEDULE_TABLE")
SCHEDULE_LAMBDA_ARN = os.environ.get("SCHEDULE_LAMBDA_ARN")
SCHEDULER_ROLE_ARN = os.environ.get("SCHEDULER_ROLE_ARN")
SCHEDULER_GROUP = os.environ.get("SCHEDULER_GROUP", "default")
MAX_SCHEDULED_VIDEO_DURATION_SEC = 90
TRIGGER_STATS_TABLE = os.environ.get("TRIGGER_STATS_TABLE")
IG_USER_ID_PARAM = os.environ.get("IG_USER_ID_PARAM", "/content-studio/ig-user-id")
IG_ACCESS_TOKEN_PARAM = os.environ.get("IG_ACCESS_TOKEN_PARAM", "/content-studio/ig-access-token")
IG_FB_ACCESS_TOKEN_PARAM = os.environ.get("IG_FB_ACCESS_TOKEN_PARAM", "/content-studio/ig-fb-access-token")
IG_FB_USER_ID_PARAM = os.environ.get("IG_FB_USER_ID_PARAM", "/content-studio/ig-fb-user-id")
FB_APP_SECRET_PARAM = os.environ.get("FB_APP_SECRET_PARAM", "/content-studio/fb-app-secret")
FB_APP_ID = os.environ.get("FB_APP_ID")
FB_LOGIN_CONFIG_ID = os.environ.get("FB_LOGIN_CONFIG_ID")

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")

app = FastAPI(title="Content Studio dashboard")

# ---- growth loop: content pillars + hook-style tags ----
#
# `pillar` is stored in meta.json under the existing `angle` key (already read by
# build_brief() in both gen_reel_batch.py and gen_carousel_batch.py, previously always
# left at its default "concept" — every one of the 12 existing meta.json files omits
# it). `hook_style` is a new meta.json key, same schemaless-JSON mechanism, no new
# plumbing. Both are optional — untagged posts just don't show up in pillar/hook
# breakdowns until edited.
PILLARS = {
    "ai-engineering": "AI Engineering",
    "system-design": "System Design",
    "dev-lessons": "Dev Lessons",
    "ai-news": "AI News",
    "engineering-opinions": "Engineering Opinions",
}
HOOK_STYLES = {
    "bold-claim": "Bold claim",
    "question": "Question",
    "number-promise": "Number + promise",
    "contrarian": "Contrarian",
    "before-after": "Before/after",
}
GROWTH_DIR = ROOT / "growth"


# ---- background jobs (subprocess + captured output) ----

class Job:
    def __init__(self, job_id, cmd, cwd, timeout=None, line_formatter=None):
        self.id = job_id
        self.cmd = cmd
        self.cwd = cwd
        self.timeout = timeout
        self.line_formatter = line_formatter or (lambda line: line)
        self.lines = []
        self.status = "running"
        self.returncode = None
        self.lock = threading.Lock()


JOBS = {}


def _run_job(job):
    try:
        proc = subprocess.Popen(
            job.cmd,
            cwd=job.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        def pump():
            for raw in proc.stdout:
                text = job.line_formatter(raw.rstrip("\n"))
                if text is None:
                    continue
                with job.lock:
                    job.lines.append(text)

        reader = threading.Thread(target=pump, daemon=True)
        reader.start()
        reader.join(timeout=job.timeout)

        if reader.is_alive():
            proc.kill()
            with job.lock:
                job.lines.append(f"[dashboard] killed after exceeding {job.timeout}s timeout")
            reader.join(timeout=5)

        proc.wait()
        with job.lock:
            job.returncode = proc.returncode
            job.status = "done" if proc.returncode == 0 else "error"
    except Exception as exc:
        with job.lock:
            job.lines.append(f"[dashboard] failed to start job: {exc}")
            job.status = "error"
            job.returncode = -1


def start_job(cmd, cwd, timeout=None, line_formatter=None):
    job_id = uuid.uuid4().hex[:12]
    job = Job(job_id, cmd, str(cwd), timeout=timeout, line_formatter=line_formatter)
    JOBS[job_id] = job
    threading.Thread(target=_run_job, args=(job,), daemon=True).start()
    return job_id


# ---- scripts ----

def _read_trigger(name):
    trigger_path = VIDEO_DIR / name / "resources" / "trigger.json"
    return json.loads(trigger_path.read_text()) if trigger_path.exists() else None


def script_status(name):
    txt = SCRIPTS_DIR / f"{name}.txt"
    meta_path = SCRIPTS_DIR / f"{name}.meta.json"
    project = VIDEO_DIR / name
    renders_dir = project / "renders"
    renders = sorted(renders_dir.glob("*.mp4")) if renders_dir.exists() else []
    return {
        "name": name,
        "text": txt.read_text() if txt.exists() else "",
        "meta": json.loads(meta_path.read_text()) if meta_path.exists() else {},
        "hasAudio": (AUDIO_DIR / f"{name}.wav").exists(),
        "hasCaptions": (AUDIO_DIR / f"{name}-captions.json").exists(),
        "hasProject": (project / "hyperframes.json").exists(),
        "hasBrief": (project / "BRIEF.md").exists(),
        "hasPdf": (project / "resources" / "guide.pdf").exists(),
        "pdfUrl": f"/media/{name}/resources/guide.pdf" if (project / "resources" / "guide.pdf").exists() else None,
        "hasUploaded": (project / "resources" / "uploaded.json").exists(),
        "hasPublished": (project / "resources" / "published.json").exists(),
        "trigger": _read_trigger(name),
        "renders": [r.name for r in renders],
    }


@app.get("/api/scripts")
def list_scripts():
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    names = sorted(p.stem for p in SCRIPTS_DIR.glob("*.txt"))
    return [script_status(n) for n in names]


class ScriptIn(BaseModel):
    name: str
    text: str
    message: str | None = None
    aspect: str | None = None
    pillar: str | None = None
    hook_style: str | None = None


@app.post("/api/scripts")
def create_script(body: ScriptIn):
    name = body.name.strip().lower()
    if not SLUG_RE.match(name):
        raise HTTPException(400, "name must be lowercase kebab-case, e.g. my-topic")
    text = body.text.strip()
    if not text:
        raise HTTPException(400, "script text is required")
    if body.pillar and body.pillar not in PILLARS:
        raise HTTPException(400, f"pillar must be one of {', '.join(PILLARS)}")
    if body.hook_style and body.hook_style not in HOOK_STYLES:
        raise HTTPException(400, f"hook_style must be one of {', '.join(HOOK_STYLES)}")

    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    (SCRIPTS_DIR / f"{name}.txt").write_text(text + "\n")

    meta = {}
    if body.message:
        meta["message"] = body.message
    if body.aspect:
        meta["aspect"] = body.aspect
    if body.pillar:
        meta["angle"] = body.pillar
    if body.hook_style:
        meta["hook_style"] = body.hook_style
    meta_path = SCRIPTS_DIR / f"{name}.meta.json"
    if meta:
        meta_path.write_text(json.dumps(meta, indent=2))
    elif meta_path.exists():
        meta_path.unlink()

    return script_status(name)


@app.delete("/api/scripts/{name}")
def delete_script(name: str):
    for suffix in (".txt", ".meta.json"):
        p = SCRIPTS_DIR / f"{name}{suffix}"
        if p.exists():
            p.unlink()
    return {"ok": True}


# ---- pipeline triggers ----

class GenerateIn(BaseModel):
    names: list[str] | None = None
    skip_project_init: bool = False


@app.post("/api/generate")
def generate(body: GenerateIn):
    if not list(SCRIPTS_DIR.glob("*.txt")):
        raise HTTPException(400, "no scripts in scripts/reels")
    cmd = [sys.executable, "-u", "scripts/gen_reel_batch.py", "--scripts-dir", str(SCRIPTS_DIR)]
    if body.names:
        cmd += ["--names", ",".join(body.names)]
    if body.skip_project_init:
        cmd.append("--skip-project-init")
    return {"job_id": start_job(cmd, cwd=ROOT)}


class RenderIn(BaseModel):
    name: str


@app.post("/api/render")
def render(body: RenderIn):
    project = VIDEO_DIR / body.name
    if not (project / "package.json").exists():
        raise HTTPException(404, f"no hyperframes project at video/{body.name}")
    return {"job_id": start_job(["npm", "run", "render"], cwd=project)}


AUTHOR_TIMEOUT_SEC = 3600  # storyboard + scene authoring + npm run render genuinely needs more than 30 min; 4 concurrent jobs hit this ceiling and got SIGKILL'd with no useful error

AUTHOR_PROMPT = """Work only inside the directory "video/{name}/" in this repository \
— do not modify any other project or file outside it.

That directory has a BRIEF.md already written (flow: automation, storyboard: no \
— autonomous mode, no clarifying questions). Read it, then run the faceless-explainer \
HyperFrames workflow end-to-end for this project: storyboard/script, audio_meta.json \
built from the existing locked voiceover + captions referenced in BRIEF.md, \
frame-by-frame composition authoring, and the final render.

If growth/analysis-latest.md exists at the repo root, read it — it's this account's most \
recent growth analysis (which pillars/hook styles are actually performing). Let its \
recommendations inform hook style, emphasis, and pacing choices for this project, but stay \
strictly faithful to this script's actual content — never invent facts or bend the material to \
fit a recommendation. If the file doesn't exist, proceed as usual.

No em dashes anywhere in any visible text (on-screen captions, headlines, labels) or in any \
caption/message copy you write into BRIEF.md or a sibling .meta.json — use a period, comma, or \
colon instead, and rewrite the sentence around it rather than just deleting the dash and leaving \
a run-on.

If video/{name}/frame.md already exists (BRIEF.md's Notes will say the design system \
is pre-seeded), do NOT run Step 2 design invention — go straight from Setup to the \
storyboard/script step, and reuse frame.md and assets/fonts/ exactly as they are. Every \
frame's @font-face block must match the ones already in assets/fonts/ verbatim — same \
family names, weights, and file paths. Do not let any individual frame fetch, invent, or \
substitute a different font; catching and re-fixing that per frame later is pure wasted \
time in an unattended run and must not happen here.

Two known failure patterns in this project's frame scripts — avoid both:
1. To get a frame's own root element from its inline `<script>`, use \
`document.querySelector('[data-composition-id="<this-frame-id>"]')`. Do NOT use \
`document.currentScript.closest(...)` — the compiler re-inserts each `<script>` to force \
execution, which detaches it from its original position in the tree, so `closest()` finds \
nothing and returns null. Also do NOT rely on `#root` as a selector — every frame's wrapper \
reuses that same id, so it is not unique once multiple frames share a document.
2. Before marking a frame done, check that every element visible at the same moment doesn't \
overlap another in screen space — a fixed-position label placed without accounting for a \
large, dynamically-centered neighbor (e.g. a big counter centered in a tall flex/grid box) is \
the recurring mistake. `npm run check`'s Layout section catches this \
(`content_overlap`/`canvas_overflow`); treat any error there (not just info-level findings) \
as blocking for that frame, not just for the final pre-render check.

This is unattended dashboard automation — there is no one to answer checkpoint \
questions. Do not stop to ask whether to render: once `npm run check` passes inside \
video/{name}/, proceed straight to `npm run render` so the run finishes with a real \
MP4 in video/{name}/renders/. State a one-line reason for each autonomous decision \
as you go, per the workflow's autonomous-mode rules, but do not wait for a reply."""


def _format_stream_json_line(raw):
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        return raw

    kind = obj.get("type")

    if kind == "assistant":
        content = (obj.get("message") or {}).get("content") or []
        parts = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text" and block.get("text", "").strip():
                parts.append(block["text"].strip())
            elif block.get("type") == "tool_use":
                parts.append(f"→ {block.get('name', 'tool')}")
        return "\n".join(parts) if parts else None

    if kind == "user":
        content = (obj.get("message") or {}).get("content") or []
        parts = []
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "tool_result":
                continue
            body = block.get("content")
            if isinstance(body, list):
                body = " ".join(b.get("text", "") for b in body if isinstance(b, dict))
            body = (body or "").strip()
            snippet = (body[:300] + "…") if len(body) > 300 else body
            if block.get("is_error"):
                parts.append(f"✗ tool error: {snippet}")
            elif snippet:
                parts.append(f"✓ {snippet.splitlines()[0][:120]}")
        return "\n".join(parts) if parts else None

    if kind == "result":
        return f"[result] {obj.get('result') or obj.get('subtype') or 'done'}"

    if kind == "system":
        subtype = obj.get("subtype", "")
        return f"[session] {subtype}" if subtype else None

    return raw


def _stream_json_line(raw):
    raw = raw.strip()
    if not raw:
        return None
    try:
        return _format_stream_json_line(raw)
    except Exception:
        return raw


class AuthorIn(BaseModel):
    name: str


@app.post("/api/author")
def author(body: AuthorIn):
    project = VIDEO_DIR / body.name
    if not (project / "BRIEF.md").exists():
        raise HTTPException(404, f"no BRIEF.md at video/{body.name} — generate it first")
    cmd = [
        "claude", "-p", AUTHOR_PROMPT.format(name=body.name),
        "--permission-mode", "bypassPermissions",
        "--output-format", "stream-json",
        "--verbose",
    ]
    job_id = start_job(cmd, cwd=ROOT, timeout=AUTHOR_TIMEOUT_SEC, line_formatter=_stream_json_line)
    return {"job_id": job_id}


PDF_TIMEOUT_SEC = 600

PDF_PROMPT = """Work only inside the directory "video/{name}/" in this repository \
— do not modify any other project or file outside it.

Read scripts/reels/{name}.txt (the narration script) and video/{name}/BRIEF.md and, if it \
exists, video/{name}/frame.md, for the topic, the hook/message, and the house design tokens.

Write a companion guide — expand the narration into a proper written guide: a short intro, \
headings/sections that break the material into digestible pieces, and maybe a closing line \
or key-takeaways recap. Stay strictly faithful to the script's actual content: restructure \
and clarify for readability, but do not invent facts, numbers, or claims that aren't in the \
source. This is not a video scene — no HyperFrames/GSAP conventions apply here, just a \
readable document.

Produce a real PDF at video/{name}/resources/guide.pdf. Choose whatever method you judge \
best (e.g. write HTML and convert it, or write and run a small Python script using a PDF \
library) — you have full Bash access. Before finishing, confirm the file exists and is \
non-trivial (opens correctly, has real content, not a near-empty shell).

No em dashes anywhere in the written guide — use a period, comma, or colon instead, and \
rewrite the sentence around it rather than just deleting the dash and leaving a run-on.

If the page background is anything other than plain white (a brand cream/dark canvas, an \
accent tint, etc.), `@page {{ margin: <anything nonzero> }}` is a hard defect, not a style \
choice — Chrome's print-to-PDF never paints `body`'s background into that carved-out margin \
region, so it stays pure white regardless of the margin value, and every page reads as a small \
inset panel floating in a white border. This is NOT fixable by tuning the margin number \
smaller; any nonzero `@page` margin reproduces it. The correct pattern: set `@page { size: ...; \
margin: 0; }` (full bleed, no browser-owned margin box at all) and do all spacing yourself with \
`padding` on `body` or on a wrapper element inside it, so the colored background paints the \
entire physical page and the "margin" is just inset content within that fully-painted area. \
If the page background is plain white, this doesn't matter and a normal `@page` margin is fine. \
Check the rendered PDF itself (not just the HTML/CSS source) before finishing: flip through it \
and confirm the background color, if any, reaches every edge of every page with no white border.

Paginate properly — a section must not fall apart across a page break. Never let a heading \
land alone at the bottom of a page with its own body text starting fresh on the next page \
(an orphaned heading); if a section doesn't fit in the remaining space, push the whole \
heading + at least its first line or two onto the next page instead. Keep a bullet list, a \
short paragraph, or a callout block from being split mid-item across a page boundary. If \
you're generating HTML, use page-break-inside: avoid / break-after: avoid on headings and \
list containers; if you're using a Python library directly, check the remaining vertical \
space before starting a new section and insert a page break yourself rather than letting \
the renderer split it. Check the actual rendered PDF (not just the source) for this before \
finishing — a heading orphaned at a page bottom is a defect, not a cosmetic detail.

This is unattended automation — there is no one to answer questions. Just produce the file \
and finish; do not wait for a reply."""


class PdfIn(BaseModel):
    name: str


@app.post("/api/generate-pdf")
def generate_pdf(body: PdfIn):
    project = VIDEO_DIR / body.name
    if not (project / "BRIEF.md").exists():
        raise HTTPException(404, f"no BRIEF.md at video/{body.name} — generate it first")
    cmd = [
        "claude", "-p", PDF_PROMPT.format(name=body.name),
        "--permission-mode", "bypassPermissions",
        "--output-format", "stream-json",
        "--verbose",
    ]
    job_id = start_job(cmd, cwd=ROOT, timeout=PDF_TIMEOUT_SEC, line_formatter=_stream_json_line)
    return {"job_id": job_id}


# ---- carousels ----
#
# A separate content type from reels: no voiceover/captions, no video render, no publish —
# this only drafts a set of square (1080x1080, safe for both Instagram and LinkedIn) static
# slide PNGs under carousels/<name>/slides/. Publishing a carousel (adding real IG-library
# music, posting/drafting) happens by hand in the Instagram app — there is no API for either
# of those, so this deliberately stops at "slides are ready to import."

CAROUSEL_MIN_SLIDES = 2
CAROUSEL_MAX_SLIDES = 10


def carousel_status(name):
    txt = CAROUSEL_SCRIPTS_DIR / f"{name}.txt"
    meta_path = CAROUSEL_SCRIPTS_DIR / f"{name}.meta.json"
    project = CAROUSEL_DIR / name
    slides_dir = project / "slides"
    slides = sorted(slides_dir.glob("*.png")) if slides_dir.exists() else []
    published_path = project / "resources" / "published.json"
    published = json.loads(published_path.read_text()) if published_path.exists() else None
    return {
        "name": name,
        "text": txt.read_text() if txt.exists() else "",
        "meta": json.loads(meta_path.read_text()) if meta_path.exists() else {},
        "hasProject": (project / "hyperframes.json").exists(),
        "slides": [f"/carousel-media/{name}/slides/{s.name}" for s in slides],
        "published": published,
    }


@app.get("/api/carousels")
def list_carousels():
    CAROUSEL_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    names = sorted(p.stem for p in CAROUSEL_SCRIPTS_DIR.glob("*.txt"))
    return [carousel_status(n) for n in names]


class CarouselIn(BaseModel):
    name: str
    text: str
    message: str | None = None
    slide_count: int = 6
    pillar: str | None = None
    hook_style: str | None = None


@app.post("/api/carousels")
def create_carousel(body: CarouselIn):
    name = body.name.strip().lower()
    if not SLUG_RE.match(name):
        raise HTTPException(400, "name must be lowercase kebab-case, e.g. my-topic")
    text = body.text.strip()
    if not text:
        raise HTTPException(400, "outline text is required")
    if not (CAROUSEL_MIN_SLIDES <= body.slide_count <= CAROUSEL_MAX_SLIDES):
        raise HTTPException(400, f"slide_count must be between {CAROUSEL_MIN_SLIDES} and {CAROUSEL_MAX_SLIDES}")
    if body.pillar and body.pillar not in PILLARS:
        raise HTTPException(400, f"pillar must be one of {', '.join(PILLARS)}")
    if body.hook_style and body.hook_style not in HOOK_STYLES:
        raise HTTPException(400, f"hook_style must be one of {', '.join(HOOK_STYLES)}")

    CAROUSEL_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    (CAROUSEL_SCRIPTS_DIR / f"{name}.txt").write_text(text + "\n")

    meta = {"slide_count": body.slide_count}
    if body.message:
        meta["message"] = body.message
    if body.pillar:
        meta["angle"] = body.pillar
    if body.hook_style:
        meta["hook_style"] = body.hook_style
    (CAROUSEL_SCRIPTS_DIR / f"{name}.meta.json").write_text(json.dumps(meta, indent=2))

    return carousel_status(name)


@app.delete("/api/carousels/{name}")
def delete_carousel(name: str):
    for suffix in (".txt", ".meta.json"):
        p = CAROUSEL_SCRIPTS_DIR / f"{name}{suffix}"
        if p.exists():
            p.unlink()
    return {"ok": True}


@app.post("/api/carousels/{name}/reveal")
def reveal_carousel(name: str):
    slides_dir = CAROUSEL_DIR / name / "slides"
    if not slides_dir.exists():
        raise HTTPException(404, f"no slides yet for {name}")
    subprocess.run(["open", str(slides_dir)])
    return {"ok": True}


class MarkCarouselPublishedIn(BaseModel):
    media_id: str


@app.post("/api/carousels/{name}/mark-published")
def mark_carousel_published(name: str, body: MarkCarouselPublishedIn):
    # Carousels are posted by hand in the Instagram app (see the module note above) — this
    # is the only place a carousel's media_id ever enters the pipeline, so it can join the
    # same insights/growth-analysis data reels already get from _gather_published_posts().
    project = CAROUSEL_DIR / name
    if not project.exists():
        raise HTTPException(404, f"no carousel project at carousels/{name}")
    media_id = body.media_id.strip()
    if not media_id:
        raise HTTPException(400, "media_id is required")

    resources_dir = project / "resources"
    resources_dir.mkdir(parents=True, exist_ok=True)
    (resources_dir / "published.json").write_text(json.dumps({
        "media_id": media_id,
        "published_at": datetime.now(timezone.utc).isoformat(),
    }, indent=2))
    return {"ok": True}


# Phones swap in typographic punctuation when a caption is pasted into the Instagram
# app, so the posted text rarely matches meta.json byte-for-byte.
_PUNCT_MAP = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "…": "..."})


def _normalize_caption(text):
    return " ".join((text or "").translate(_PUNCT_MAP).split()).strip().lower()


def _first_sentence(normalized):
    match = re.match(r"(.+?[.!?])(\s|$)", normalized)
    return match.group(1) if match else normalized


MIN_SENTENCE_MATCH_LEN = 25


@app.post("/api/carousels/sync-published")
def sync_carousels_published():
    # No manual media-id entry: since carousels are posted by hand in the app (no
    # publish webhook to hook into), this instead fetches the account's recent media
    # and auto-links each untracked local carousel to the post whose caption matches
    # what's stored in its meta.json message field — the same text the user would
    # have copy-pasted in when posting. This is a text-similarity heuristic, not a
    # platform-guaranteed match, so ambiguous/no-match carousels are reported back
    # rather than silently guessed at.
    if not (IG_USER_ID_PARAM and IG_ACCESS_TOKEN_PARAM):
        raise HTTPException(400, "insights aren't configured — set IG_USER_ID_PARAM/IG_ACCESS_TOKEN_PARAM in .env")
    try:
        ig_user_id = _ig_param(IG_USER_ID_PARAM)
        access_token = _ig_param(IG_ACCESS_TOKEN_PARAM)
    except Exception as exc:
        raise HTTPException(502, f"couldn't read IG credentials from SSM: {exc}")

    try:
        resp = _graph_get(f"{ig_user_id}/media", {"fields": "id,caption,timestamp,permalink,media_type", "limit": 50}, access_token)
    except Exception as exc:
        raise HTTPException(502, f"Graph API error: {exc}")
    candidates = [m for m in resp.get("data", []) if m.get("media_type") == "CAROUSEL_ALBUM"]

    claimed_ids = set()
    for project in CAROUSEL_DIR.iterdir() if CAROUSEL_DIR.exists() else []:
        published_path = project / "resources" / "published.json"
        if published_path.exists():
            claimed_ids.add(json.loads(published_path.read_text()).get("media_id"))

    matched, unmatched = [], []
    for name in sorted(p.stem for p in CAROUSEL_SCRIPTS_DIR.glob("*.txt")):
        project = CAROUSEL_DIR / name
        if not project.exists() or (project / "resources" / "published.json").exists():
            continue
        caption = _normalize_caption(_read_meta(CAROUSEL_SCRIPTS_DIR, name).get("message"))
        if not caption:
            unmatched.append(name)
            continue
        open_candidates = [m for m in candidates if m["id"] not in claimed_ids]
        found = next((m for m in open_candidates if caption[:80] in _normalize_caption(m.get("caption"))), None)
        if not found:
            # Captions often get a line tweaked right before posting, so fall back to the
            # opening sentence — but only when it's specific enough and picks out exactly
            # one post, never a best guess among several.
            opener = _first_sentence(caption)
            hits = [m for m in open_candidates if _normalize_caption(m.get("caption")).startswith(opener)]
            if len(opener) >= MIN_SENTENCE_MATCH_LEN and len(hits) == 1:
                found = hits[0]
        if not found:
            unmatched.append(name)
            continue
        resources_dir = project / "resources"
        resources_dir.mkdir(parents=True, exist_ok=True)
        (resources_dir / "published.json").write_text(json.dumps({
            "media_id": found["id"],
            "published_at": found.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        }, indent=2))
        claimed_ids.add(found["id"])
        matched.append(name)

    return {"matched": matched, "unmatched": unmatched, "candidates_checked": len(candidates)}


class GenerateCarouselIn(BaseModel):
    names: list[str] | None = None


@app.post("/api/generate-carousel")
def generate_carousel(body: GenerateCarouselIn):
    if not list(CAROUSEL_SCRIPTS_DIR.glob("*.txt")):
        raise HTTPException(400, "no outlines in scripts/carousels")
    cmd = [sys.executable, "-u", "scripts/gen_carousel_batch.py", "--scripts-dir", str(CAROUSEL_SCRIPTS_DIR)]
    if body.names:
        cmd += ["--names", ",".join(body.names)]
    return {"job_id": start_job(cmd, cwd=ROOT)}


CAROUSEL_AUTHOR_TIMEOUT_SEC = 1800

CAROUSEL_AUTHOR_PROMPT = """Work only inside the directory "carousels/{name}/" in this repository. \
Do not modify any other project or file outside it.

That directory has a BRIEF.md already written (flow: automation, storyboard: no, autonomous \
mode, no clarifying questions, content_type: carousel). Read it for its slide_count field and the \
message/angle/intent, then run the faceless-explainer HyperFrames workflow's Setup + \
storyboard/script + composition-authoring steps to build exactly that many static scenes, one per \
carousel slide, in the order they should appear. There is no voiceover and no captions for this \
project. Do not build an audio_meta.json or any VO-driven timing; each scene is a single still, \
not a frame of a continuous animation.

If growth/analysis-latest.md exists at the repo root, read it — it's this account's most \
recent growth analysis (which pillars/hook styles are actually performing). Let its \
recommendations inform hook style and emphasis for this carousel, but stay strictly faithful to \
this outline's actual content — never invent facts or bend the material to fit a \
recommendation. If the file doesn't exist, proceed as usual.

Quality bars, non-negotiable: (1) every scene needs a real supporting graphic, not just headline + \
subhead typography on a flat or gradient background — an icon, a small diagram (boxes/arrows for \
a flow, side-by-side columns for a comparison, a numbered/checklist layout for a listicle item), \
or a simple data element; typography-only slides are not acceptable. (2) no em dashes anywhere in \
any visible text (headlines, subheads, labels, captions) — use a period, comma, or colon instead, \
and rewrite the sentence around it rather than just deleting the dash and leaving a run-on. \
(3) slide 1 is the hook and carries most of the carousel's engagement — it must be a bold claim, \
a sharp question, or a number + promise, never a flat topic label, and it needs a visible swipe \
cue (an arrow icon or "Swipe" label), placed in the same spot every carousel uses for it (bottom- \
right is this account's convention). (4) the last slide is the CTA. Keep the base canvas \
background clearly visible, covering meaningfully more than half the frame — the accent-color \
card on top of it is a headline-sized banner (roughly the top third to top half of the frame, \
holding only the headline and optionally the subhead), not a near-full-bleed rectangle with a \
thin border around it; that fails the instruction just as much as a true full-bleed background \
does, both still read as a different post spliced onto the end. The two CTA buttons sit below the \
card, directly on the visible base canvas (solid accent-color pill buttons are fine, that's not \
the same as the whole slide going accent-color). Its ask is always save + follow — as two \
distinct, visually highlighted button-like shapes each with a small icon (bookmark for save, \
profile/plus for follow), never plain sentences: save this post, and follow @ratish.ai for more. \
Never use a "comment a keyword and I'll send/DM you something" CTA on a carousel — carousels \
never get published through this pipeline's Graph API automation, so nothing here can actually \
deliver on that promise. (5) every scene's content \
must fill and balance the full 1080x1080 frame vertically — center the content block, or \
distribute a headline block and a supporting-graphic block across the frame's height; never leave \
content clustered in the top half with dead empty space below. (6) one idea per slide, always, \
never two concepts or two comparisons crammed onto one scene. (7) max ~35 words of body text per \
scene (headline not counted) — cut or split across two scenes rather than shrinking type to fit \
more. (8) the exact same background color, fonts, margins, and accent color on every single scene \
including the CTA slide — a carousel must look like one post, not differently-designed slides \
stitched together. (9) if scenes carry a number/step indicator, use the exact same format and \
placement on every scene that has one.

If carousels/{name}/frame.md already exists (BRIEF.md's Notes will say the design system is \
pre-seeded), do NOT run Step 2 design invention — go straight to the storyboard/script step, and \
reuse frame.md and assets/fonts/ exactly as they are, same as every other project.

Two known failure patterns to avoid — same as the reel workflow: use \
`document.querySelector('[data-composition-id="<this-frame-id>"]')` to get a frame's own root \
element (never `document.currentScript.closest(...)` or `#root`), and check that no two elements \
visible at the same moment overlap in screen space (`npm run check`'s Layout section catches \
this — treat any error there as blocking).

Once every scene passes `npm run check`, capture one PNG still per scene with `npx hyperframes \
snapshot --at <one timestamp per scene, at each scene's midpoint>` and organize the output into \
carousels/{name}/slides/slide-01.png, slide-02.png, ... in scene order (rename/move the snapshot \
tool's output files into that convention if it doesn't already produce them that way). Confirm \
every slide PNG exists, is square (1080x1080), and looks correct before finishing.

This is unattended dashboard automation — there is no one to answer checkpoint questions. State a \
one-line reason for each autonomous decision as you go, but do not wait for a reply."""


class AuthorCarouselIn(BaseModel):
    name: str


@app.post("/api/author-carousel")
def author_carousel(body: AuthorCarouselIn):
    project = CAROUSEL_DIR / body.name
    if not (project / "BRIEF.md").exists():
        raise HTTPException(404, f"no BRIEF.md at carousels/{body.name} — generate it first")
    cmd = [
        "claude", "-p", CAROUSEL_AUTHOR_PROMPT.format(name=body.name),
        "--permission-mode", "bypassPermissions",
        "--output-format", "stream-json",
        "--verbose",
    ]
    job_id = start_job(cmd, cwd=ROOT, timeout=CAROUSEL_AUTHOR_TIMEOUT_SEC, line_formatter=_stream_json_line)
    return {"job_id": job_id}


class UploadIn(BaseModel):
    name: str


@app.post("/api/upload")
def upload(body: UploadIn):
    project = VIDEO_DIR / body.name
    if not (project / "resources" / "guide.pdf").exists():
        raise HTTPException(400, "generate the PDF guide first")
    if not S3_BUCKET:
        raise HTTPException(400, "S3_BUCKET is not set (add it to .env)")
    cmd = [sys.executable, "-u", "scripts/upload_resources.py", "--name", body.name, "--bucket", S3_BUCKET]
    return {"job_id": start_job(cmd, cwd=ROOT)}


class TriggerIn(BaseModel):
    name: str
    media_id: str
    keyword: str


@app.post("/api/set-trigger")
def set_trigger_endpoint(body: TriggerIn):
    project = VIDEO_DIR / body.name
    if not (project / "resources" / "guide.pdf").exists():
        raise HTTPException(400, "generate the PDF guide first")
    if not S3_BUCKET:
        raise HTTPException(400, "S3_BUCKET is not set (add it to .env)")
    cmd = [
        sys.executable, "-u", "scripts/upload_resources.py",
        "--name", body.name, "--bucket", S3_BUCKET,
        "--media-id", body.media_id, "--keyword", body.keyword,
    ]
    return {"job_id": start_job(cmd, cwd=ROOT)}


PUBLISH_TIMEOUT_SEC = 360


class PublishIn(BaseModel):
    name: str
    caption: str | None = None
    keyword: str | None = None


@app.post("/api/publish")
def publish(body: PublishIn):
    project = VIDEO_DIR / body.name
    if not (project / "resources" / "guide.pdf").exists():
        raise HTTPException(400, "generate the PDF guide first — publishing without a resource to deliver would create a dead trigger")
    renders_dir = project / "renders"
    if not renders_dir.exists() or not list(renders_dir.glob("*.mp4")):
        raise HTTPException(400, "render the project first")
    if not S3_BUCKET:
        raise HTTPException(400, "S3_BUCKET is not set (add it to .env)")
    cmd = [sys.executable, "-u", "scripts/publish_reel.py", "--name", body.name, "--bucket", S3_BUCKET]
    if body.caption:
        cmd += ["--caption", body.caption]
    if body.keyword:
        cmd += ["--keyword", body.keyword]
    return {"job_id": start_job(cmd, cwd=ROOT, timeout=PUBLISH_TIMEOUT_SEC)}


# ---- scheduled posts ----
#
# The actual firing happens in AWS, not here: creating a scheduled post uploads its
# render to S3 and registers a one-shot EventBridge Scheduler schedule that invokes
# SchedulePublishFunction (infra/lambda/schedule_publish.py) directly at that
# timestamp. That means a post fires on time even if this dashboard process (or the
# machine it's running on) isn't up at that moment — this file only handles CRUD
# against the tracking table plus keeping the schedule in sync, never the firing.


def _publishable(name):
    project = VIDEO_DIR / name
    renders_dir = project / "renders"
    return (project / "resources" / "guide.pdf").exists() and renders_dir.exists() and bool(list(renders_dir.glob("*.mp4")))


def _require_schedule_config():
    missing = [k for k, v in {
        "S3_BUCKET": S3_BUCKET,
        "SCHEDULE_TABLE": SCHEDULE_TABLE,
        "SCHEDULE_LAMBDA_ARN": SCHEDULE_LAMBDA_ARN,
        "SCHEDULER_ROLE_ARN": SCHEDULER_ROLE_ARN,
    }.items() if not v]
    if missing:
        raise HTTPException(400, f"scheduling isn't configured — set {', '.join(missing)} in .env (see infra/template.yaml outputs after `sam deploy`)")


def _schedule_table():
    return boto3.resource("dynamodb").Table(SCHEDULE_TABLE)


def _s3_client():
    region = boto3.Session().region_name or "us-east-1"
    return boto3.client("s3", region_name=region, endpoint_url=f"https://s3.{region}.amazonaws.com")


def _latest_render(project):
    renders = sorted((project / "renders").glob("*.mp4"), key=lambda p: p.stat().st_mtime)
    return renders[-1] if renders else None


def _video_duration_sec(video_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video_path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def _schedule_name(item_id):
    return f"reel-publish-{item_id}"


def _to_utc_at_expression(scheduled_at):
    # scheduled_at is a naive local datetime string (from <input type="datetime-local">).
    # Treat it as this machine's local time, convert to UTC — EventBridge Scheduler's
    # at() expression defaults to UTC when no ScheduleExpressionTimezone is given.
    local_naive = datetime.fromisoformat(scheduled_at)
    utc_dt = local_naive.astimezone().astimezone(timezone.utc)
    return f"at({utc_dt.strftime('%Y-%m-%dT%H:%M:%S')})"


def _upsert_eventbridge_schedule(item):
    client = boto3.client("scheduler")
    name = _schedule_name(item["id"])
    try:
        client.delete_schedule(Name=name, GroupName=SCHEDULER_GROUP)
    except client.exceptions.ResourceNotFoundException:
        pass
    try:
        client.create_schedule(
            Name=name,
            GroupName=SCHEDULER_GROUP,
            ScheduleExpression=_to_utc_at_expression(item["scheduled_at"]),
            FlexibleTimeWindow={"Mode": "OFF"},
            ActionAfterCompletion="DELETE",
            Target={
                "Arn": SCHEDULE_LAMBDA_ARN,
                "RoleArn": SCHEDULER_ROLE_ARN,
                "Input": json.dumps({
                    "id": item["id"],
                    "name": item["name"],
                    "s3_key": item["s3_key"],
                    "caption": item.get("caption"),
                    "keyword": item.get("keyword"),
                    "pdf_key": item.get("pdf_key"),
                }),
            },
        )
    except Exception as exc:
        raise HTTPException(502, f"failed to schedule via EventBridge Scheduler: {exc}")


def _delete_eventbridge_schedule(item_id):
    client = boto3.client("scheduler")
    try:
        client.delete_schedule(Name=_schedule_name(item_id), GroupName=SCHEDULER_GROUP)
    except client.exceptions.ResourceNotFoundException:
        pass


class ScheduleIn(BaseModel):
    name: str
    scheduled_at: str  # ISO local datetime, e.g. from <input type="datetime-local">
    caption: str | None = None
    keyword: str | None = None  # None/blank means this post gets no comment trigger, period


@app.get("/api/schedule")
def list_schedule():
    _require_schedule_config()
    items = _schedule_table().scan().get("Items", [])
    return sorted(items, key=lambda i: i.get("scheduled_at", ""))


@app.post("/api/schedule")
def create_schedule(body: ScheduleIn):
    _require_schedule_config()
    if not _publishable(body.name):
        raise HTTPException(400, "generate the PDF guide and render the project first")
    project = VIDEO_DIR / body.name
    if not (project / "resources" / "uploaded.json").exists():
        raise HTTPException(400, "upload the PDF guide to S3 first (Pipeline tab → Upload)")
    try:
        scheduled_dt = datetime.fromisoformat(body.scheduled_at)
    except ValueError:
        raise HTTPException(400, "scheduled_at must be an ISO datetime")
    if scheduled_dt <= datetime.now():
        raise HTTPException(400, "scheduled_at must be in the future")

    video_path = _latest_render(project)
    duration = _video_duration_sec(video_path)
    if duration > MAX_SCHEDULED_VIDEO_DURATION_SEC:
        raise HTTPException(400, f"{video_path.name} is {duration:.1f}s — Instagram's API-published Reels cap is {MAX_SCHEDULED_VIDEO_DURATION_SEC}s")

    item_id = uuid.uuid4().hex[:10]
    s3_key = f"{body.name}/scheduled/{item_id}.mp4"
    _s3_client().upload_file(str(video_path), S3_BUCKET, s3_key, ExtraArgs={"ContentType": "video/mp4"})

    item = {
        "id": item_id,
        "name": body.name,
        "caption": body.caption or None,
        "keyword": (body.keyword or "").strip() or None,
        "pdf_key": f"{body.name}/guide.pdf",
        "s3_key": s3_key,
        "scheduled_at": body.scheduled_at,
        "status": "pending",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    _upsert_eventbridge_schedule(item)
    _schedule_table().put_item(Item={k: v for k, v in item.items() if v is not None})
    return item


class ScheduleUpdateIn(BaseModel):
    scheduled_at: str | None = None
    caption: str | None = None
    keyword: str | None = None  # explicit "" clears any trigger — never silently carried over


@app.patch("/api/schedule/{item_id}")
def update_schedule(item_id: str, body: ScheduleUpdateIn):
    _require_schedule_config()
    if body.scheduled_at is not None:
        try:
            parsed = datetime.fromisoformat(body.scheduled_at)
        except ValueError:
            raise HTTPException(400, "scheduled_at must be an ISO datetime")
        if parsed <= datetime.now():
            raise HTTPException(400, "scheduled_at must be in the future")

    table = _schedule_table()
    item = table.get_item(Key={"id": item_id}).get("Item")
    if not item:
        raise HTTPException(404, "unknown schedule item")
    if item["status"] not in ("pending", "error"):
        raise HTTPException(400, f"cannot edit a schedule item that is already {item['status']}")

    if body.scheduled_at is not None:
        item["scheduled_at"] = body.scheduled_at
    if body.caption is not None:
        item["caption"] = body.caption.strip() or None
    if body.keyword is not None:
        item["keyword"] = body.keyword.strip() or None
    item["status"] = "pending"
    item.pop("error", None)

    _upsert_eventbridge_schedule(item)
    table.put_item(Item={k: v for k, v in item.items() if v is not None})
    return item


@app.delete("/api/schedule/{item_id}")
def delete_schedule(item_id: str):
    _require_schedule_config()
    _delete_eventbridge_schedule(item_id)
    _schedule_table().delete_item(Key={"id": item_id})
    return {"ok": True}


@app.get("/api/jobs/{job_id}")
def job_status(job_id: str, since: int = 0):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(404, "unknown job")
    with job.lock:
        lines = job.lines[since:]
        return {
            "status": job.status,
            "lines": lines,
            "next": since + len(lines),
            "returncode": job.returncode,
        }


# ---- performance / insights ----
#
# Read-only: pulls real Instagram numbers per published post (Graph API) plus
# trigger-conversion counts the webhook Lambda writes to TRIGGER_STATS_TABLE
# (see infra/lambda/handler.py's _increment_stat). Two sources feed the post
# list because there are two ways a post ends up published in this repo: the
# Schedule tab (ScheduledPostsTable rows with status="done") and the older
# manual Approve & Publish flow (video/<name>/resources/published.json).

GRAPH_API_BASE = "https://graph.instagram.com/v21.0"
# profile_visits was tried here as the follow-intent proxy (see growth/ section below)
# but the live Graph API rejects it for this account's Reels — "does not support the
# profile_visits metric for this media product type" — and an insights call 400s
# entirely if any requested metric is invalid, so it can't be requested at all here.
# saved/shares are the real proxies actually available: saves are Instagram's own
# stated strongest ranking signal, and both are genuine per-post data, not guesses.
INSIGHTS_METRICS_REEL = "reach,likes,comments,saved,shares,views,total_interactions"
INSIGHTS_METRICS_CAROUSEL = "reach,likes,comments,saved,shares,total_interactions"

_ig_param_cache = {}


def _ig_param(param_name):
    if param_name not in _ig_param_cache:
        ssm = boto3.client("ssm")
        resp = ssm.get_parameter(Name=param_name, WithDecryption=True)
        _ig_param_cache[param_name] = resp["Parameter"]["Value"]
    return _ig_param_cache[param_name]


def _graph_get(path, params, access_token):
    qs = "&".join(f"{k}={v}" for k, v in {**params, "access_token": access_token}.items())
    req = urllib.request.Request(f"{GRAPH_API_BASE}/{path}?{qs}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()
        raise RuntimeError(f"Graph API {exc.code}: {detail}") from exc


def _trigger_stats_table():
    return boto3.resource("dynamodb").Table(TRIGGER_STATS_TABLE)


def _trigger_stats(media_id):
    if not TRIGGER_STATS_TABLE:
        return {"matched": 0, "delivered": 0}
    item = _trigger_stats_table().get_item(Key={"pk": f"stats#{media_id}", "sk": "counts"}).get("Item") or {}
    return {"matched": int(item.get("matched", 0)), "delivered": int(item.get("delivered", 0))}


def _read_meta(meta_dir, name):
    meta_path = meta_dir / f"{name}.meta.json"
    return json.loads(meta_path.read_text()) if meta_path.exists() else {}


def _gather_published_posts():
    posts = {}

    if SCHEDULE_TABLE:
        try:
            for item in _schedule_table().scan().get("Items", []):
                if item.get("status") == "done" and item.get("media_id"):
                    meta = _read_meta(SCRIPTS_DIR, item["name"])
                    posts[item["media_id"]] = {
                        "name": item["name"],
                        "media_id": item["media_id"],
                        "published_at": item.get("published_at"),
                        "caption": item.get("caption"),
                        "content_type": "reel",
                        "pillar": meta.get("angle"),
                        "hook_style": meta.get("hook_style"),
                    }
        except Exception as exc:
            print(f"insights: failed to scan schedule table: {exc}", file=sys.stderr)

    for project in VIDEO_DIR.iterdir() if VIDEO_DIR.exists() else []:
        published_path = project / "resources" / "published.json"
        if not published_path.exists():
            continue
        published = json.loads(published_path.read_text())
        media_id = published.get("media_id")
        if not media_id or media_id in posts:
            continue
        meta = _read_meta(SCRIPTS_DIR, project.name)
        posts[media_id] = {
            "name": project.name,
            "media_id": media_id,
            "published_at": published.get("published_at"),
            "caption": meta.get("message"),
            "content_type": "reel",
            "pillar": meta.get("angle"),
            "hook_style": meta.get("hook_style"),
        }

    for project in CAROUSEL_DIR.iterdir() if CAROUSEL_DIR.exists() else []:
        published_path = project / "resources" / "published.json"
        if not published_path.exists():
            continue
        published = json.loads(published_path.read_text())
        media_id = published.get("media_id")
        if not media_id or media_id in posts:
            continue
        meta = _read_meta(CAROUSEL_SCRIPTS_DIR, project.name)
        posts[media_id] = {
            "name": project.name,
            "media_id": media_id,
            "published_at": published.get("published_at"),
            "caption": meta.get("message"),
            "content_type": "carousel",
            "pillar": meta.get("angle"),
            "hook_style": meta.get("hook_style"),
        }

    return list(posts.values())


def _compute_insights(access_token):
    posts = _gather_published_posts()
    results = []
    for post in posts:
        media_id = post["media_id"]
        metrics_str = INSIGHTS_METRICS_CAROUSEL if post.get("content_type") == "carousel" else INSIGHTS_METRICS_REEL
        entry = {**post, "permalink": None, "timestamp": None, "metrics": None, "trigger": None, "error": None}
        try:
            fields = _graph_get(media_id, {"fields": "permalink,timestamp"}, access_token)
            entry["permalink"] = fields.get("permalink")
            entry["timestamp"] = fields.get("timestamp")
        except Exception as exc:
            entry["error"] = str(exc)[:300]
        try:
            insights = _graph_get(f"{media_id}/insights", {"metric": metrics_str}, access_token)
            metrics = {row["name"]: (row.get("values") or [{}])[0].get("value", 0) for row in insights.get("data", [])}
            entry["metrics"] = metrics
        except Exception as exc:
            entry["error"] = (entry["error"] + "; " if entry["error"] else "") + str(exc)[:300]
        try:
            entry["trigger"] = _trigger_stats(media_id)
        except Exception as exc:
            print(f"insights: trigger stats failed for {media_id}: {exc}", file=sys.stderr)
            entry["trigger"] = {"matched": 0, "delivered": 0}
        results.append(entry)

    results.sort(key=lambda e: e.get("published_at") or "", reverse=True)
    return results


@app.get("/api/insights")
def list_insights():
    if not (IG_USER_ID_PARAM and IG_ACCESS_TOKEN_PARAM):
        raise HTTPException(400, "insights aren't configured — set IG_USER_ID_PARAM/IG_ACCESS_TOKEN_PARAM in .env")

    try:
        access_token = _ig_param(IG_ACCESS_TOKEN_PARAM)
    except Exception as exc:
        raise HTTPException(502, f"couldn't read IG access token from SSM: {exc}")

    return _compute_insights(access_token)


# ---- growth loop: follower snapshots + on-demand learning analysis ----
#
# There is no Graph API metric anywhere for "new followers attributable to this
# post" — confirmed against Meta's current docs. The `follows` field that does exist
# is the account's cumulative follower count repeated on every post, and only applies
# to FEED/STORY, not Reels. profile_visits looked like the closest real proxy for
# follow-intent, but the live API rejects it for this account's Reels entirely (see
# INSIGHTS_METRICS_REEL above) — so the real signals here are saved/reach ("save
# rate" — Instagram's own stated strongest ranking signal, and genuine per-post data)
# plus the account's followers_count sampled over time, correlated after the fact
# with what got posted.
# Both are stored as flat local JSON — same convention as BRIEF.md/meta.json/
# published.json elsewhere in this repo — so this needs no new DynamoDB table and no
# infra.yaml change.

@app.post("/api/growth/snapshot")
def growth_snapshot():
    if not (IG_USER_ID_PARAM and IG_ACCESS_TOKEN_PARAM):
        raise HTTPException(400, "insights aren't configured — set IG_USER_ID_PARAM/IG_ACCESS_TOKEN_PARAM in .env")
    try:
        ig_user_id = _ig_param(IG_USER_ID_PARAM)
        access_token = _ig_param(IG_ACCESS_TOKEN_PARAM)
    except Exception as exc:
        raise HTTPException(502, f"couldn't read IG credentials from SSM: {exc}")

    try:
        fields = _graph_get(ig_user_id, {"fields": "followers_count"}, access_token)
    except Exception as exc:
        raise HTTPException(502, f"Graph API error: {exc}")
    followers_count = fields.get("followers_count")
    if followers_count is None:
        raise HTTPException(502, f"Graph API didn't return followers_count: {fields}")

    GROWTH_DIR.mkdir(parents=True, exist_ok=True)
    history_path = GROWTH_DIR / "follower-history.json"
    history = json.loads(history_path.read_text()) if history_path.exists() else []
    today = datetime.now().date().isoformat()
    history = [h for h in history if h["date"] != today]
    history.append({"date": today, "followers_count": followers_count})
    history.sort(key=lambda h: h["date"])
    history_path.write_text(json.dumps(history, indent=2))
    return {"date": today, "followers_count": followers_count}


# ---- token health + Facebook reconnect ----
#
# The Instagram Login token is refreshed weekly by TokenRefreshFunction (infra/), so
# its expiry is ~60 days after the SSM parameter was last written — graph.instagram.com
# has no debug_token to ask directly. The competitor-research Page token never expires
# itself but carries Meta's 90-day data-access limit, which only a fresh login resets —
# hence /api/fb/connect: one click through Meta's own login dialog instead of redoing
# the Graph API Explorer steps by hand.

FB_GRAPH = "https://graph.facebook.com/v21.0"
FB_REDIRECT_URI = "http://localhost:8787/api/fb/callback"
IG_TOKEN_LIFETIME_DAYS = 60
_oauth_states = {}


def _ssm():
    return boto3.client("ssm")


def _fb_get(path, params):
    url = f"{FB_GRAPH}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Graph API {exc.code}: {exc.read().decode()}") from exc


def _days_until(ts):
    return round((ts - datetime.now(timezone.utc).timestamp()) / 86400, 1)


@app.get("/api/tokens/status")
def token_status():
    out = {}
    try:
        param = _ssm().get_parameter(Name=IG_ACCESS_TOKEN_PARAM)["Parameter"]
        expires = param["LastModifiedDate"] + timedelta(days=IG_TOKEN_LIFETIME_DAYS)
        out["instagram"] = {"ok": True, "days_left": _days_until(expires.timestamp()), "last_refreshed": param["LastModifiedDate"].isoformat()}
    except Exception as exc:
        out["instagram"] = {"ok": False, "error": str(exc)[:300]}
    try:
        ssm = _ssm()
        get = lambda n: ssm.get_parameter(Name=n, WithDecryption=True)["Parameter"]["Value"]
        data = _fb_get("debug_token", {
            "input_token": get(IG_FB_ACCESS_TOKEN_PARAM),
            "access_token": f"{FB_APP_ID}|{get(FB_APP_SECRET_PARAM)}",
        })["data"]
        deadlines = [t for t in (data.get("expires_at"), data.get("data_access_expires_at")) if t]
        out["competitor"] = {
            "ok": bool(data.get("is_valid")),
            "days_left": _days_until(min(deadlines)) if deadlines else None,
            "error": (data.get("error") or {}).get("message"),
        }
    except Exception as exc:
        out["competitor"] = {"ok": False, "error": str(exc)[:300]}
    out["reconnect_configured"] = bool(FB_APP_ID and FB_LOGIN_CONFIG_ID)
    return out


@app.get("/api/fb/connect")
def fb_connect(return_to: str = "http://localhost:8787/"):
    if not (FB_APP_ID and FB_LOGIN_CONFIG_ID):
        raise HTTPException(400, "set FB_APP_ID and FB_LOGIN_CONFIG_ID in .env")
    state = uuid.uuid4().hex
    _oauth_states[state] = return_to
    qs = urllib.parse.urlencode({
        "client_id": FB_APP_ID,
        "redirect_uri": FB_REDIRECT_URI,
        "config_id": FB_LOGIN_CONFIG_ID,
        "response_type": "code",
        "state": state,
    })
    return RedirectResponse(f"https://www.facebook.com/v21.0/dialog/oauth?{qs}")


@app.get("/api/fb/callback")
def fb_callback(state: str, code: str = None, error_description: str = None):
    return_to = _oauth_states.pop(state, None)
    if return_to is None:
        raise HTTPException(400, "unknown or reused OAuth state — start again from the dashboard")
    if not code:
        raise HTTPException(400, f"Facebook login was cancelled or failed: {error_description}")

    ssm = _ssm()
    secret = ssm.get_parameter(Name=FB_APP_SECRET_PARAM, WithDecryption=True)["Parameter"]["Value"]
    ig_id = ssm.get_parameter(Name=IG_FB_USER_ID_PARAM, WithDecryption=True)["Parameter"]["Value"]
    short = _fb_get("oauth/access_token", {
        "client_id": FB_APP_ID, "client_secret": secret, "redirect_uri": FB_REDIRECT_URI, "code": code,
    })["access_token"]
    long_user = _fb_get("oauth/access_token", {
        "grant_type": "fb_exchange_token", "client_id": FB_APP_ID, "client_secret": secret, "fb_exchange_token": short,
    })["access_token"]
    # A Page token derived from a long-lived user token has no expiry of its own.
    pages = _fb_get("me/accounts", {"fields": "name,access_token,instagram_business_account", "access_token": long_user})["data"]
    page = next((p for p in pages if (p.get("instagram_business_account") or {}).get("id") == ig_id), None)
    if not page:
        raise HTTPException(400, f"no Page linked to IG account {ig_id} was granted — tick the Page and IG account in the login popup")
    ssm.put_parameter(Name=IG_FB_ACCESS_TOKEN_PARAM, Value=page["access_token"], Type="SecureString", Overwrite=True)
    return RedirectResponse(return_to)


GROWTH_ANALYSIS_TIMEOUT_SEC = 900

GROWTH_ANALYSIS_PROMPT = """Read the file growth/analysis-input.json in this repository. It \
contains a JSON object: {{"window_days": N, "posts": [...], "follower_history": [...]}}. Each \
entry in "posts" is one published Reel or carousel from the last N days, with its Graph API \
metrics (reach, likes, comments, saved, shares, views for Reels, total_interactions), its \
content pillar ("pillar", one of {pillars}), and its hook style ("hook_style", one of \
{hook_styles}) — either field may be null if that post was never tagged. "follower_history" is \
a list of {{date, followers_count}} samples across the same window.

There is no metric anywhere for "new followers from this specific post" (Instagram's API \
doesn't expose that, and profile_visits — which looked like the closest proxy — turned out to \
be rejected outright for this account's Reels), so do not invent one or imply the data supports \
precise per-post attribution. The two real signals available are: saved divided by reach ("save \
rate" — Instagram's own stated strongest ranking signal, and genuine per-post data), and the \
account's followers_count trend over the window, which you can only correlate with what was \
posted, not attribute precisely.

Write a concise markdown report to growth/analysis-{today}.md answering, specifically and \
concretely (never generic advice like "post more engaging content"):
1. Which pillar had the best average reach and save-rate this window, and which had the worst \
— name them explicitly with the actual numbers, not just "the AI ones."
2. Which hook style performed best on the same measures, same rule: name it, cite the numbers.
3. What the follower count actually did across the window (net change, not just start/end), and \
whether the timing of any spike lines up with a specific post or pillar in the data — flag this \
as a correlation, not a proven cause.
4. Two or three specific, concrete recommendations for what to make next: which pillar(s) to \
lean into, which hook style to reuse, and anything to stop doing, all grounded in this window's \
actual numbers, not generic best practices.

If there are fewer than 3 posts in the window, say so plainly and note that the sample is too \
small for the pillar/hook breakdown to mean much yet, then still report on follower trend and \
raw metrics.

After writing growth/analysis-{today}.md, copy it verbatim to growth/analysis-latest.md \
(overwrite if it exists) so future content-authoring runs always read the latest one. This is \
unattended automation, there is no one to answer questions — just write the file and finish."""


class GrowthAnalyzeIn(BaseModel):
    days: int = 7


@app.post("/api/growth/analyze")
def growth_analyze(body: GrowthAnalyzeIn):
    if not (IG_USER_ID_PARAM and IG_ACCESS_TOKEN_PARAM):
        raise HTTPException(400, "insights aren't configured — set IG_USER_ID_PARAM/IG_ACCESS_TOKEN_PARAM in .env")
    try:
        access_token = _ig_param(IG_ACCESS_TOKEN_PARAM)
    except Exception as exc:
        raise HTTPException(502, f"couldn't read IG access token from SSM: {exc}")

    all_posts = _compute_insights(access_token)
    cutoff = datetime.now(timezone.utc) - timedelta(days=body.days)
    window = []
    for post in all_posts:
        ts = post.get("published_at")
        if not ts:
            continue
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        if dt >= cutoff:
            window.append(post)

    GROWTH_DIR.mkdir(parents=True, exist_ok=True)
    history_path = GROWTH_DIR / "follower-history.json"
    history = json.loads(history_path.read_text()) if history_path.exists() else []
    cutoff_date = cutoff.date().isoformat()
    recent_history = [h for h in history if h["date"] >= cutoff_date]

    (GROWTH_DIR / "analysis-input.json").write_text(json.dumps({
        "window_days": body.days,
        "posts": window,
        "follower_history": recent_history,
    }, indent=2))

    today = datetime.now().date().isoformat()
    prompt = GROWTH_ANALYSIS_PROMPT.format(
        pillars=", ".join(PILLARS),
        hook_styles=", ".join(HOOK_STYLES),
        today=today,
    )
    cmd = [
        "claude", "-p", prompt,
        "--permission-mode", "bypassPermissions",
        "--output-format", "stream-json",
        "--verbose",
    ]
    job_id = start_job(cmd, cwd=ROOT, timeout=GROWTH_ANALYSIS_TIMEOUT_SEC, line_formatter=_stream_json_line)
    return {"job_id": job_id, "posts_in_window": len(window)}


# ---- videos ----

@app.get("/api/videos")
def list_videos():
    if not VIDEO_DIR.exists():
        return []
    out = []
    for project in sorted(VIDEO_DIR.iterdir()):
        if not project.is_dir():
            continue
        renders_dir = project / "renders"
        if not renders_dir.exists():
            continue
        renders = sorted(renders_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
        if renders:
            out.append({
                "name": project.name,
                "renders": [{"file": r.name, "url": f"/media/{project.name}/renders/{r.name}"} for r in renders],
            })
    return out


VIDEO_DIR.mkdir(parents=True, exist_ok=True)
CAROUSEL_DIR.mkdir(parents=True, exist_ok=True)
GROWTH_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(VIDEO_DIR)), name="media")
app.mount("/carousel-media", StaticFiles(directory=str(CAROUSEL_DIR)), name="carousel-media")
app.mount("/growth-data", StaticFiles(directory=str(GROWTH_DIR)), name="growth-data")
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    # 0.0.0.0 (not just localhost) so the dashboard is reachable from a phone on the
    # same trusted home Wi-Fi — needed to copy captions/view slides without a
    # separate transfer step. This does mean anything else on that network can reach
    # it too (it has real publish/AWS-touching endpoints) — don't run this on public
    # or shared/untrusted Wi-Fi.
    uvicorn.run(app, host="0.0.0.0", port=8787)
