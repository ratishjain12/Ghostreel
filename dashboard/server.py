import json
import os
import re
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts" / "reels"
AUDIO_DIR = ROOT / "audio"
VIDEO_DIR = ROOT / "video"
STATIC_DIR = Path(__file__).resolve().parent / "static"
S3_BUCKET = os.environ.get("S3_BUCKET")

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")

app = FastAPI(title="Reel pipeline dashboard")


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


@app.post("/api/scripts")
def create_script(body: ScriptIn):
    name = body.name.strip().lower()
    if not SLUG_RE.match(name):
        raise HTTPException(400, "name must be lowercase kebab-case, e.g. my-topic")
    text = body.text.strip()
    if not text:
        raise HTTPException(400, "script text is required")

    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    (SCRIPTS_DIR / f"{name}.txt").write_text(text + "\n")

    meta = {}
    if body.message:
        meta["message"] = body.message
    if body.aspect:
        meta["aspect"] = body.aspect
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


AUTHOR_TIMEOUT_SEC = 1800

AUTHOR_PROMPT = """Work only inside the directory "video/{name}/" in this repository \
— do not modify any other project or file outside it.

That directory has a BRIEF.md already written (flow: automation, storyboard: no \
— autonomous mode, no clarifying questions). Read it, then run the faceless-explainer \
HyperFrames workflow end-to-end for this project: storyboard/script, audio_meta.json \
built from the existing locked voiceover + captions referenced in BRIEF.md, \
frame-by-frame composition authoring, and the final render.

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
app.mount("/media", StaticFiles(directory=str(VIDEO_DIR)), name="media")
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8787)
