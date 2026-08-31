---
name: reel-batch
description: "Turn a folder of narration scripts into a batch of locked-VO HyperFrames reel projects — voice (Chatterbox) + word-level captions (faster-whisper) + a pre-filled BRIEF.md per video, generated in one pass with models loaded once. Use when the user wants to generate many (10-20+) reels from scripts instead of one hardcoded voice.py run at a time. Does not author scene visuals or render — hands off to /faceless-explainer per project for that."
---

# Reel batch pipeline

Turns N narration scripts into N HyperFrames projects that are ready for scene authoring —
no hardcoded paths, no re-loading the TTS/Whisper models per video.

## Dashboard

`dashboard/` has a local web UI over this same pipeline — add/select scripts, trigger
generate/render, preview rendered MP4s, and preview a generated PDF guide inline (a
"Preview PDF" disclosure per row once `hasPdf` is true — `script_status()`'s `pdfUrl` field
points at the file, already served statically via the existing `/media` mount, no new route
needed), all with a live job log. It calls the exact same `scripts/gen_reel_batch.py` / `npm
run render` underneath (see `dashboard/server.py`); the CLI steps below still work standalone.

```bash
cd dashboard/web && npm install && npm run build   # once, and after any src/ change
uv run dashboard/server.py                         # serves the UI + API on :8787
```

**`make dev` does not hot-reload the Python backend.** It hot-reloads the Vite frontend
(`npm run dev` watches `dashboard/web/src`) but runs `uv run dashboard/server.py` as a plain
background process with no `--reload` — any change to `server.py` (a new `script_status()`
field, a new route) needs the backend process killed and restarted before it takes effect.
A symptom that traces back to this: a frontend feature that reads a new field renders as if
the feature doesn't exist at all (the field is just `undefined`), not as an error — check
`ps aux | grep server.py` for how long it's been running before assuming a bug in the new code.

**Job-log subprocesses need `python -u` or their `print()`s won't stream live.** `start_job()`
pipes a child process's stdout and reads it line-by-line (`for raw in proc.stdout`), but Python
fully buffers stdout by default when it isn't a terminal (a pipe counts) — a script that
`print()`s periodically over a long-running loop (`publish_reel.py`'s container-status poll,
every ~10s for up to 5 minutes) has all of that output held in the child's internal buffer and
released in one burst at exit, not as it happens. The dashboard's frontend polls `/api/jobs/{id}`
every 700ms and appends new lines correctly (`useJobRunner.js`) — the missing-live-updates bug
was entirely server-side buffering, not a frontend polling gap. Fix: every `[sys.executable,
"scripts/...py", ...]` command in `server.py` needs `-u` right after `sys.executable` (forces
unbuffered stdout/stderr for that one process) — added to all four Python subprocess call sites
(`generate`, `upload`, `set-trigger`, `publish`) rather than only the one where the gap was most
visible, since they all had the same latent issue.

## Pipeline

```
scripts/reels/<name>.txt  (+ optional <name>.meta.json)
        │
        ▼  scripts/gen_reel_batch.py  (loads Chatterbox + Whisper ONCE for the whole batch)
        │
        ├── audio/<name>.wav                    (gen_voice.py — Chatterbox TTS)
        ├── audio/<name>-captions.json           (gen_captions.py — faster-whisper word timing)
        └── video/<name>/                        (npx hyperframes init, then theme seed, then BRIEF.md)
                 frame.md + assets/fonts/  — copied from --theme-source (default: assets/, the
                             repo's shared brand kit)
                 BRIEF.md  — workflow: faceless-explainer, VO_MODE: verbatim/locked,
                             pointing at the audio + captions above, Notes say the design
                             system is pre-seeded so Step 2 (design invention) is skipped
```

Scene visuals (`compositions/frames/*.html`) are per-topic creative work, not something to
template/batch mechanically — that step is `/faceless-explainer` (or the dashboard's Author
action), run once per project. The design system (palette/typography/fonts) is different: by
default every new project is seeded from the repo-root `assets/` folder (`assets/frame.md` +
`assets/fonts/`) — the shared brand kit, independent of any specific example project (`--theme-
source`, pass an existing `video/<name>` project name to reuse its look instead, or `""` to
disable). Letting each frame sub-agent pick its own font independently and reconciling them in a
later pass wastes real time in an unattended run; pre-seeding the files removes the need for that
pass. `video/explainer-01/` is one already-built project on top of that same kit, not the source
of it — deleting or heavily editing that example no longer changes what new projects default to.

## Running the batch step

1. Drop one `.txt` per video into `scripts/reels/` (plain narration text, sentence-punctuated —
   it's chunked on `.`/`!`/`?` for TTS generation).
2. Optionally add `scripts/reels/<name>.meta.json` to override any BRIEF field:
   ```json
   { "message": "...", "intent": "...", "destination": "reels", "aspect": "1080x1920", "language": "en", "angle": "concept" }
   ```
   Unset fields default to: destination `reels`, aspect `1080x1920` (9:16), language `en`,
   angle `concept`, message/intent derived from the script's first sentence.
3. Run:
   ```bash
   uv run scripts/gen_reel_batch.py --scripts-dir scripts/reels
   ```
   This is the single command that replaces hand-editing `voice.py` / `transcribe_captions.py`
   per video. Re-running is safe — any `video/<name>/` that already has `hyperframes.json` is
   left untouched (init and BRIEF.md are only written once).
4. Use `--skip-project-init` to only regenerate `audio/*.wav` + `audio/*-captions.json`
   (e.g. re-doing narration for an existing project) without touching `video/`.
5. Audio/caption generation only runs for stages that don't already exist — safe to re-run
   on a mixed batch. `--theme-source ""` opts a batch out of design-system seeding, for a
   look that should be uniquely invented instead of reused; `--theme-source <project-name>`
   reuses an already-built project's look instead of the default shared brand kit.

Single-video ad hoc use (no batching) still works directly:
```bash
uv run scripts/gen_voice.py --text scripts/reels/my-topic.txt --out audio/my-topic.wav
uv run scripts/gen_captions.py --audio audio/my-topic.wav
```

## After the batch step: authoring + render

Each `video/<name>/` has `BRIEF.md` already confirmed (`storyboard: no`, `flow: automation`
→ autonomous mode — no checkpoint questions). Per the brief contract, a workflow that finds
`BRIEF.md` reads it and asks nothing further. For each project, either:

- Run `/faceless-explainer` with that project directory as the target, one at a time, reviewing
  the render before moving to the next — safest for a first batch or unfamiliar scripts.
- Or fan multiple projects out with the `Agent` tool (`subagent_type: "claude"` or a fresh
  general-purpose agent per project, run in parallel) once you trust the pattern — each project's
  authoring + render is independent. For a large batch (10-20), prefer a `Workflow` run if the
  user has explicitly asked for multi-agent orchestration; otherwise run projects a few at a time.

## Reel safe zone (carried into every project's BRIEF.md Notes)

Keep the last ~250px of the 1920px-tall canvas and the first ~150px free of anything critical
(captions, key text) — that's where Reels/TikTok/Shorts draw their own username, caption bar,
and action-button chrome. `video/explainer-01/compositions/captions.html` has the reference
implementation: the caption band is `top`+`height`-bound and stops well short of the canvas
edge (`--cap-band-top: 1600px; --cap-band-height: 160px` on a 1920px canvas), not flush against
it. Reuse that shape for new caption engines instead of a band that touches `height: 100%`.

## Notes

- `gen_voice.py` and `gen_captions.py` each expose an importable `generate_*` function, not just
  a CLI — `gen_reel_batch.py` uses these directly so Chatterbox/Whisper load once per batch run,
  not once per video. Reuse the same functions rather than shelling out per file.
- Voice reference defaults to `voice_ref.wav` at the repo root; pass `--voice-ref` to use a
  different one for a specific batch.

## PDF guide + Instagram growth loop

Beyond the video, each project can get a companion PDF and be wired into a comment→DM growth
automation on Instagram — see `docs/meta-app-setup.md` for the full setup (Meta app, AWS deploy,
webhook wiring). The pipeline side:

- **PDF** — dashboard's `PDF` button (`POST /api/generate-pdf`) spawns a headless Claude agent
  (same `bypassPermissions` mechanism as Author) that reads the script + `BRIEF.md`/`frame.md`
  and writes `video/<name>/resources/guide.pdf` — a real written guide, not a mechanical reflow.
  Once that succeeds, the dashboard automatically chains an upload (`POST /api/upload`, needs
  `S3_BUCKET` in `.env`) that runs `scripts/upload_resources.py`, pushing the PDF to S3 and
  marking `video/<name>/resources/uploaded.json` locally — one click covers both steps; there's
  no separate manual upload button. `PDF_PROMPT` requires clean pagination — no heading orphaned
  alone at the bottom of a page with its body starting fresh on the next, no bullet/paragraph
  split mid-item across a page break. The agent must check the rendered PDF itself for this, not
  just its HTML/source, before finishing.
  - **Re-running this is non-deterministic — verify content, not just that a file exists.**
    Clicking `PDF` again spawns a fresh headless-agent pass from scratch; a later run on
    `video/agentic-patterns` silently dropped the per-pattern code example + failure case that
    `BRIEF.md`'s own Notes explicitly required (the instruction was still right there in the
    file — the agent just didn't fully honor it that time). `hasPdf` only proves *a* PDF exists,
    not that it still matches spec. After any regeneration, open the actual PDF and check it
    against the brief's requirements before trusting it, the same way you'd check `npm run
    check` after a frame edit rather than assuming success.
  - **A print document's page background should be white, not a brand color.** `@page { margin:
    ... }` carves out a margin region that stays the browser's default (white/transparent) —
    it is never filled by the page's own `body { background }`. Set a colored `body` background
    on a multi-page print stylesheet and every single page reads as an odd inset panel floating
    inside a white border, which shows up as "bad padding/spacing" even though the actual margin
    values are perfectly reasonable. Brand color belongs in accents (rules, headings, code-block
    borders) in a print document, not the page fill — that's a video-canvas convention, not a
    document one.
  - **Editing `video/<name>/resources/guide.pdf` locally does nothing for real deliveries until
    it's re-uploaded.** The Lambda delivers whatever object currently sits at `s3://<bucket>/
    <name>/guide.pdf` — it has no awareness of the local file at all. Fixing the local PDF (a
    padding bug, a content regression, anything) and stopping there leaves live comment triggers
    still handing out the *old* S3 copy, silently, with no error anywhere — this happened for
    real on `agentic-patterns` after the padding/content fix, and wasn't caught until a live test
    showed the stale version arriving. Any local `guide.pdf` edit made after the project was
    already uploaded (`resources/uploaded.json` exists) must be followed by `uv run
    scripts/upload_resources.py --name <name> --bucket <bucket>` before it's actually fixed for
    anyone. If `resources/trigger.json` already exists (the project is a *live* trigger, not just
    uploaded), that re-upload also silently re-registers the same trigger in S3's
    `triggers.json` — harmless (same media ID, same keyword), but worth knowing it happens.
- **Publish** — dashboard's **Approve & Publish** button (`POST /api/publish`, gated on `hasPdf &&
  renders.length > 0`) runs `scripts/publish_reel.py`: uploads the render to S3, posts it live via
  Meta's Content Publishing API (`media_type=REELS`, poll `status_code` until `FINISHED`, then
  `media_publish`), writes `resources/published.json`, and — if a keyword was given or one already
  exists in `resources/trigger.json` — registers the trigger against the real media ID
  automatically via `upload_resources.set_trigger()` (imported, not duplicated). Needs the
  `instagram_content_publish` permission granted + the SSM access token regenerated first (see
  `docs/meta-app-setup.md` § 7). Caps renders at 90s (checked via `ffprobe` before calling Meta at
  all). The confirm()/prompt() dialogs in `ScriptRow.jsx` are the entire approval gate — this posts
  live, public content immediately, there's no draft state.
- **Trigger mapping (manual fallback)** — if you publish through the Instagram app yourself
  instead, once a project shows **Uploaded** the row's IG-media-id + keyword form
  (`POST /api/set-trigger`) does the same `triggers.json` update by hand.
- **Infra** — `infra/template.yaml` (AWS SAM) deploys the API Gateway + Lambda + a small DynamoDB
  table (composite `pk`/`sk` key: `marker#…` for webhook-retry idempotency, `pending#<sender>` /
  `<media_id>` for per-post pending deliveries, so triggering two tracked posts before replying to
  either delivers both instead of losing one) that receives Meta's `comments`/`messages` webhooks,
  sends a private-reply follow-gate, checks the real `is_user_follow_business` field once the
  commenter responds, and delivers the PDF as a message attachment. Both the Lambda and
  `upload_resources.get_client()` pin the S3 client to an explicit regional endpoint — boto3's
  default client presigns against the global `s3.amazonaws.com` host even with a region set, which
  S3 rejects outside `us-east-1` (a real bug caught while building the publish flow). Also serves
  `GET /privacy` (a plain HTML page baked into `handler.py`) so there's a reachable Privacy Policy
  URL for Meta's App Review, without standing up separate static hosting.
- **Follow-gate CTA buttons** — both the initial private reply and the "not following yet"
  follow-up use Instagram's Button Template (`attachment.type=template`,
  `payload.template_type=button`, max 3 buttons) instead of plain text: a `web_url` button
  ("Visit Profile", linking to the account's own profile) and a `postback` button ("I'm following",
  payload `CHECK_FOLLOW`) that fires a `messaging_postbacks` webhook event. `_handle_message`
  extracts the idempotency `mid` from either `message` or `postback` so a button tap routes through
  the exact same follow-check-then-deliver path as a typed reply — no separate postback handler.
  `_handle_comment` also checks `is_user_follow_business` up front, before sending anything: an
  already-following commenter gets the PDF delivered directly as the private reply (no CTA at
  all), instead of the CTA followed by the PDF once they tap/reply — the follow-gate is only for
  people who genuinely aren't following yet. Both paths share `_deliver_pending(sender_id,
  recipient)`; `recipient` is `{"comment_id": ...}` when called fresh off a comment (the shape
  required to open the messaging window) and `{"id": sender_id}` once that window is already
  open (from `_handle_message`).
- **Public comment acknowledgment, separate from the private DM.** After either branch of
  `_handle_comment` sends something to DMs, it also calls `_reply_to_comment(comment_id,
  COMMENT_ACK_TEXT)` — a normal public reply (`POST /{comment-id}/replies`) visible under the
  post itself, nudging the commenter to check their inbox. Two reasons this exists as a *second*
  send rather than folding into the private reply: comment-reply notifications get noticed by
  people who don't have DM notifications on, and a visible public reply is social proof under the
  post that the automation actually responds, not just a silent DM nobody but the recipient ever
  sees. Covered by the same `_already_sent(comment_id)` idempotency guard as everything else in
  `_handle_comment` — Meta's webhook retries can't cause a duplicate public reply.
- **Delivery is a text greeting then a native file attachment — deliberately two messages, not
  a link-in-text.** The Send API's `message` object carries `text` *or* `attachment`, never
  both, so a captioned PDF is unavoidably ≥2 sends if it's an attachment. A link-in-one-message
  alternative was tried and reverted: a presigned S3 URL pasted into a text message exposes the
  bucket name and a long signed query string directly in the DM (reads as a phishing link, not a
  trustworthy one), and its effective click window is uncertain (signed with the Lambda
  execution role's own short-lived temporary credentials, which don't reliably last anywhere
  near the requested `ExpiresIn`, even up to SigV4's 7-day max). The attachment sidesteps both
  problems — Meta fetches the file from the presigned URL almost immediately at send time (needs
  only seconds of validity, so `ExpiresIn=3600` is comfortably generous, not tight), and the
  recipient gets a natively-rendered, trusted file instead of a link to tap. Two message bubbles
  is the correct trade here, not a compromise to engineer around. If a one-message link ever
  becomes worth revisiting, do it properly (a clean redirect / custom domain in front of S3), not
  by just widening `ExpiresIn` — that number was never the actual ceiling.
- **Development Mode data visibility** — while the Meta app is in Development Mode, both API reads
  and webhook events are filtered to accounts with an assigned role (Admin/Developer/Tester) on the
  app. A comment from an account with no role is invisible end-to-end: `comments_count` on the
  media goes up but `GET /{media-id}/comments` returns `data: []` with populated pagination cursors
  — that combination (not a plain empty result) is the tell that it's a visibility filter, not a
  missing comment. Add any test account as a Tester (Instagram → API setup → Testers) before using
  it to test the flow. Going to Production requires App Review per permission used, which itself
  requires a reachable Privacy Policy URL — see `GET /privacy` above.

## Frame-script pitfalls seen in practice

Two mistakes have shown up in authored frames; the Author prompt (in `dashboard/server.py`)
already tells the agent to avoid both, kept here as a durable record of why:

- **Root lookup:** a frame's inline `<script>` gets re-inserted by the compiler to force
  execution, detaching it from its original spot in the tree — so
  `document.currentScript.closest('#root')` returns null and the next line throws
  `Cannot read properties of null`. Use `document.querySelector('[data-composition-id="<id>"]')`
  instead (what every working frame in `video/explainer-01` and the fixed frames in
  `video/thundering-herd` do). `#root` also isn't a safe selector on its own — every frame
  reuses that id, so it collides once more than one frame is loaded into the same document.
- **Spatial overlap between independently-placed elements:** a fixed-position label and a
  large, dynamically-centered element (e.g. a counter centered in a tall flex/grid box) can
  land on top of each other even though each was placed correctly on its own — the label's
  `top` didn't account for how far down the counter's actual glyph box reaches. `npm run
  check`'s Layout section catches this (`content_overlap`); treat it as blocking per frame,
  not just at the final pre-render check.
- **SVG paths without an explicit `fill`:** an open polyline (`<path d="M x,y L x,y ...">`)
  used as a decorative line/trace renders as a solid filled shape if the CSS class applied to
  it doesn't set `fill: none` itself — relying on a *different* shared class (e.g. a base
  `.dtrace` rule) to supply `fill: none` breaks the moment that one path is authored with only
  the modifier class (`.dtrace-idle`) and not the base class. Give every trace/line class its
  own explicit `fill: none`, don't assume it's inherited from a sibling class.
- **Decoration in the first ~3 seconds:** the hook/opening beat is the highest-stakes real
  estate in a reel — a viewer decides whether to keep watching there. Don't spend any of it on
  ambient/atmospheric decoration (background motifs, corner marks, etc.), even subtle ones —
  restraint there is not a missed opportunity, it's the right call. Save visual signature
  moments for the body of the video, once the hook has already earned the watch.
- **Vertical whitespace must be deliberately balanced, not just safe-zone-legal.** Clearing the
  top ~150px / bottom ~250px exclusion bands is necessary but not sufficient — a frame can still
  read as badly composed if it leaves e.g. 700px of dead space above the first line of content
  while everything else crowds into the remaining ~1200px. After placing content, check the
  actual empty-space ratio top vs. bottom (not just "is anything inside the exclusion bands"),
  and rebalance if one side is more than ~2x the other.
- **Don't pair a tiny label with a huge one right next to each other.** A small numeral/tag
  (e.g. "01") set immediately beside a large headline (e.g. a 74px word) at a very different
  size reads as broken/awkward, especially once cropped or viewed close-up — it's not a normal
  eyebrow-above-headline hierarchy, it's two incompatible scales colliding on one baseline. If
  the number is already communicated elsewhere (an eyebrow line, a "1 of 8" tick), don't repeat
  it a second time at a clashing size right next to the headline — say it once.
- **A global coordinate shift (e.g. "move this block up 400px") must be verified to have
  actually reached every coordinate, not assumed from the diff.** Y-values embedded in raw SVG
  `d="M x,y L x,y"` path strings, inline `style="top:Npx"` attributes, and values passed as a
  *variable* rather than a literal (e.g. `node(f"id-{i}", x, 1150, ...)` where `x` is a loop
  variable) are each easy for a find/replace or regex pass to miss silently — the node moves but
  the wire connecting to it doesn't, or vice versa. After any bulk reposition, render and
  visually spot-check the actual frames (not just re-read the source diff) before considering it
  done; a mismatch between a node and the trace that's supposed to meet it is not caught by
  `npm run check`'s layout/overlap rules, since both pieces are individually valid, just
  disconnected from each other.
- **Evenly-spaced ≠ centered.** A row of N nodes with identical spacing between each pair can
  still sit off-center on the canvas if the spacing was chosen without also solving for the
  midpoint — e.g. `xs = [230, 476, 722, 968]` has perfectly equal 246px gaps but centers on 599,
  not the canvas's true center 540 (every value is +59 off). Every other row-style diagram in
  this project got this right by building outward symmetrically from 540 (e.g. `[540-1.5*gap,
  540-0.5*gap, 540+0.5*gap, 540+1.5*gap]`); always derive multi-node row positions from the
  canvas center this way, not from an arbitrary starting x plus a fixed increment — the latter
  makes it easy to get internal spacing right while missing overall centering, and eyeballing
  the code won't catch it (check by computing (min_edge + max_edge) / 2 against canvas_width / 2).
- **A connecting line/trace should stay part of the same visual system as the nodes it
  connects.** If nodes animate through states (idle → lit → solid) to show progress, a
  connector that never changes from a static idle style over the same span reads as
  disconnected from that progress, even when its position is correct — decide deliberately
  whether each connector should track the animation (most cases) or is intentionally a static
  background rail (rare, and should look intentional, not like an oversight).
