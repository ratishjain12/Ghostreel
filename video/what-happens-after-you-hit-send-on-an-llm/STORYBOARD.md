---
format: 1080x1920
duration: 59s
message: "Between hitting send and the first word, a prompt passes through six systems. When an LLM feels slow, one of them is the reason."
arc: Hook → Gateway → Cache → Router → Batching → Prefill → Decode → Diagnose → CTA
audience: engineers who call LLM APIs daily but treat the request as one black-box hop
mode: autonomous
music: none
---

## Video direction

**Structure:** how-to / process explainer. A single request travels down one path of six numbered stations, one station per frame, then a diagnostic recap and a CTA. Locked VO (`VO_MODE: verbatim`): every `voiceover` line below is the exact script text, split at paragraph boundaries only.

**Growth-analysis note (autonomous decision):** `growth/analysis-latest.md` says three straight contrarian hooks underperformed and recommends testing a `number-promise` hook next. This script's hook already is a number promise ("six systems"), so Frame 1 lands the figure **6** as its payoff and every station carries a mono `0N / 06` index so the promise visibly pays off in order. Nothing in the content was changed to fit the recommendation.

**Palette (from `frame.md`, Code editorial):** warm cream `{colors.cream}` paper is the ground on every frame, with `{colors.tile}` for secondary surfaces. `{colors.ink}` for headlines and body. The warm-navy code surface (`{colors.navy}` / `navy-soft` / `navy-elev`) holds the technical mechanism in each frame (checklists, token strips, queues). `{colors.coral}` is the single voltage per frame: the traveling request, the active station dot, the one thing that matters. Never two coral elements competing, never a fourth hue. Syntax teal/amber only inside navy code surfaces, sparingly.

**Type:** EB Garamond 400 sentence case for display (station names), Inter 400 body, JetBrains Mono uppercase kickers with the coral ✱ prefix, and mono for labels and code. Only weights 400 and 700 ship; use those. The canonical `@font-face` block at the end of `frame.md` is copied verbatim into every frame; no other font is ever loaded.

**Shared chrome (identical in every frame 02 to 07, so the path reads as one continuous journey):** a "request path" spine at the top of the frame, a row of six small circles joined by a hairline, centered horizontally, at y ≈ 210–250 (clear of the top 150px). Past stations are filled ink at low opacity, the current station is filled coral, future stations are hollow hairline circles. Beneath it, the kicker `✱ STEP 0N / 06` at y ≈ 300. The station display name sits below the kicker. The spine is present from t=0 in each station frame (it is chrome, not a reveal); only the current dot's coral fill pops on at the frame's start.

**Motion grammar:** Code editorial's register: short cross-dissolves, `power3.out` long-tail eases, no overshoot, no bounce, no elastic. Coral is the only thing that "draws on". Code and tokens type or step on line by line. VO-paced reveal model: at each Scene's start only what the voiceover is naming enters; nothing is dumped at t=0. Holds read as stillness. The between-station transition is `push-slide UP`: the request is moving *down* the path, so content moves up.

**Rhythm / held-frame allocation:** Frames 02 to 07 are build frames, each mechanism assembling to its own VO. Frame 01 (Hook) is fast and lands on the held **6**. Frame 08 (Diagnose) is the held synthesis: the six stations stacked, one question. Frame 09 (CTA) is a short calm hold.

**Negative list:** no heavy drop shadows (hairline plus at most one soft warm shadow), no gradients, no glow, no purple-blue "AI" bokeh, no pure white or cool gray, no invented numbers (no latency figures, no GPU counts, no percentages; the only numerals are the script's own: 2 seconds, six, step indices), no em dashes in any visible text, no front-loaded-then-frozen frames, no idle drift or breathing during holds.

**Safe zone (this project's reel spec, supersedes the generic caption default):** scene content lives between y ≈ 150 and y ≈ 1400 on the 1920-tall canvas. The caption pill sits in a band at y ≈ 1440–1660. Nothing load-bearing below y ≈ 1400, nothing at all below y ≈ 1670.

---

## Frame 1 — Hook

- scene: A prompt types into a composer and gets sent; a two-second fuse draws; the figure 6 lands with six empty station dots
- voiceover: "You type a prompt and hit send. In the two seconds before the first word appears, your message goes through six systems."
- duration: 6.36s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Number promise + Concretization
- beat: recognition, then intrigue
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the figure "6" number-lockup with the unit "SYSTEMS"
- roles: navy composer panel = foreground subject (Scenes 1-2) · two-second fuse line = supporting · "6 SYSTEMS" lockup = foreground subject (Scene 3) · six hollow station dots = supporting · faint hairline grid on cream = background

narrativeRole: Opens on the everyday action every viewer has done, then reveals that a whole pipeline hides inside it.
keyMessage: Hitting send starts a request that passes through six separate systems before any word comes back.

Adapt: keep the prompt-types-then-submit signature move, but instead of the machine answering, the submit launches the two-second fuse and the payoff is the count of systems.

Scene 1 (0.0–1.8s): visible at the first frame: cream ground with a faint hairline grid; a navy composer panel sits in the upper-middle (~70% width). Mono text "your prompt" is already typing into it with a caret; a coral "Send" pill sits at the panel's right edge. On "hit send" (~1.45s) the Send pill does one press-release. Centered, panel ~35% of frame height.
Scene 2 (1.8–4.3s): the composer lifts and shrinks to the top third. Beneath it a hairline fuse draws left to right, labeled in mono at its ends "SEND" and "FIRST WORD", with the EB Garamond line "Two seconds" appearing above the fuse on "two seconds" (~2.1s). The coral request dot rides the fuse. Full-width strip, ~30% of frame.
Scene 3 (4.3–6.36s): on "six systems" (~5.5s) the fuse compresses into a row of six hollow station dots and the number-hero "6" lands centered above them with the mono unit "SYSTEMS" beside it (count-up is not needed; it is one figure). Hold still on the lockup. Centered hero at y ≈ 800, ~45% of frame.

---

## Frame 2 — Gateway

- scene: Station 01 of 06: the request hits the API gateway, which checks key, rate limit, and token allowance one by one
- voiceover: "First, an API gateway. It checks your key, your rate limit, and how many tokens you're allowed to spend."
- duration: 5.7s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/02-gateway.html
- type: feature_showcase
- persuasion: Progressive disclosure
- beat: comprehension
- blueprint: agent-progress-theater (Adapt)
- focal: a navy "gateway" checklist panel with three check rows
- roles: request path spine (dot 1 coral) = supporting chrome · "API gateway" display = headline · navy checklist panel = foreground subject · coral request chip = supporting

narrativeRole: First station: the gate that decides whether the request is allowed in at all.
keyMessage: The gateway checks your key, your rate limit, and your token allowance before anything else runs.

Adapt: keep the checklist-that-checks-off signature; no loaders or status theater, each row just resolves on its spoken cue.

Scene 1 (0.0–1.7s): spine present, dot 1 fills coral; kicker "✱ STEP 01 / 06"; on "API gateway" (~0.66s) the display "API gateway" rises in beneath. A coral request chip labeled "request" sits waiting just above a navy panel's top edge. Headline block upper third.
Scene 2 (1.7–3.6s): navy checklist panel (~80% width, centered, ~40% of frame) is present with three mono rows in dim cream. On "your key" (~2.4s) row 1 "API key" gets a teal check; on "rate limit" (~3.2s) row 2 "Rate limit" checks. Layer-reveal, row by row.
Scene 3 (3.6–5.7s): on "how many tokens you're allowed to spend" (~4.2s) row 3 "Token allowance" checks, then the coral request chip passes down through the panel's bottom edge (it was let through). Hold the three checked rows still.

---

## Frame 3 — Cache

- scene: Station 02 of 06: the start of the prompt is matched against already-processed work; the matching prefix is reused, not recomputed
- voiceover: "Second, a cache lookup. If the start of your prompt matches something the provider has already processed, like a long system prompt, that work gets reused instead of recomputed."
- duration: 9.8s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/03-cache.html
- type: feature_showcase
- persuasion: Concretization + visual metaphor
- beat: comprehension, small "aha"
- blueprint: compose
- focal: two stacked token strips, "already processed" above "your prompt", with the matching prefix bracketed
- roles: spine (dot 2 coral) = supporting chrome · "Cache lookup" display = headline · navy token strips = foreground subject · prefix bracket + "reused" tag = the coral voltage · struck-through "recomputed" = supporting

narrativeRole: Second station: work the provider already did can be skipped entirely.
keyMessage: When the start of your prompt matches something already processed, like a long system prompt, that work is reused.

Scene 1 (0.0–1.4s): spine present, dot 2 fills coral; kicker "✱ STEP 02 / 06"; display "Cache lookup" rises in on "cache lookup" (~0.6s). Headline block upper third.
Scene 2 (1.4–3.4s): on "the start of your prompt" a navy strip labeled in mono "YOUR PROMPT" steps on as a row of token blocks (left to right, one short cascade), the first long run of blocks slightly different in tint from the tail. Full-width strip, centered, lower-middle.
Scene 3 (3.4–5.3s): on "already processed" (~4.3s) a second strip labeled "ALREADY PROCESSED" appears above it, a copy of only the long first run. Hairline connectors draw between matching blocks, left to right.
Scene 4 (5.3–7.1s): on "like a long system prompt" (~5.7s) a bracket spans the matched run of both strips with the mono label "system prompt".
Scene 5 (7.1–9.8s): on "reused" (~7.9s) the matched run of "YOUR PROMPT" turns coral-edged with the tag "reused"; on "recomputed" (~8.9s) a small mono "recomputed" appears beside it and gets struck through by a hairline. Hold still.

---

## Frame 4 — Router

- scene: Station 03 of 06: a router sends the request down one branch to the GPU cluster that fits the requested model and its current load
- voiceover: "Third, a router picks which model and which GPU cluster handles you, based on load and on the model you asked for."
- duration: 6.885s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/04-router.html
- type: feature_showcase
- persuasion: Visual metaphor (branching path)
- beat: comprehension
- blueprint: compose
- focal: a branching route diagram: one router node fanning to three GPU cluster cards
- roles: spine (dot 3 coral) = supporting chrome · "Router" display = headline · router node + three branches = foreground subject · three cluster cards each with a load bar = supporting · the chosen coral path = voltage

narrativeRole: Third station: the request is assigned to specific hardware.
keyMessage: A router picks the model and GPU cluster, based on load and on which model you asked for.

Scene 1 (0.0–1.4s): spine present, dot 3 fills coral; kicker "✱ STEP 03 / 06"; display "Router" rises on "router" (~0.46s). A small ink router node appears centered below the headline.
Scene 2 (1.4–3.8s): on "which model" (~1.4s) three hairline branches draw down from the router node (svg path draw) to three tile cluster cards stacked side by side, each labeled in mono "GPU CLUSTER" with A, B, C. On "GPU cluster" (~2.4s) the cards settle. Stacked below headline, ~45% of frame.
Scene 3 (3.8–5.5s): on "based on load" (~3.9s) each card's horizontal load bar fills to a different level (no numbers, relative only: high, low, medium).
Scene 4 (5.5–6.885s): on "the model you asked for" (~5.6s) a mono tag "your model" appears on the router node, and the branch to the low-load card draws in coral; the coral request dot travels down it and seats in that card. Hold.

---

## Frame 5 — Batching

- scene: Station 04 of 06: the request waits a few milliseconds in a queue, then boards one shared GPU pass with dozens of others
- voiceover: "Fourth, a batching queue. Your request waits a few milliseconds so it can share a GPU pass with dozens of others. That's how inference stays affordable."
- duration: 8.615s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/05-batching.html
- type: feature_showcase
- persuasion: Concretization + scale
- beat: comprehension, then a small payoff
- blueprint: grid-card-assemble (Adapt)
- focal: a grid of request dots (one coral among dozens of ink) collecting into one "GPU pass" frame
- roles: spine (dot 4 coral) = supporting chrome · "Batching queue" display = headline · the coral "your request" dot = voltage · dozens of ink dots = foreground subject (as a group) · navy "ONE GPU PASS" container = supporting · payoff line = supporting

narrativeRole: Fourth station: your request deliberately waits so it can share hardware.
keyMessage: A few milliseconds of waiting lets one GPU pass serve dozens of requests, which keeps inference affordable.

Adapt: keep the staggered-cascade grid assemble signature; the grid is request dots filling a batch, then the whole batch moves as one.

Scene 1 (0.0–1.5s): spine present, dot 4 fills coral; kicker "✱ STEP 04 / 06"; display "Batching queue" rises on "batching queue" (~0.5s).
Scene 2 (1.5–3.7s): on "your request" (~1.6s) a single coral dot appears with the mono label "you" in the middle zone; on "waits a few milliseconds" (~2.1s) a mono timer label "waiting: a few ms" appears beside it and a thin hairline arc ticks around the dot once. Centered, ~20% of frame.
Scene 3 (3.7–6.5s): on "share a GPU pass" (~3.8s) a navy container labeled "ONE GPU PASS" draws around the coral dot; on "dozens of others" (~5.3s) ink/cream dots cascade in around it to fill a grid inside the container (a few dozen, staggered, arrival reads as one beat). Container ~50% of frame.
Scene 4 (6.5–8.615s): the full container slides down as one unit a short distance (the pass runs); on "affordable" (~8.0s) an EB Garamond italic line lands below it: "That's how inference stays affordable." Hold.

---

## Frame 6 — Prefill

- scene: Station 05 of 06: the whole prompt lights up in one parallel sweep; then a visible pause before the first token
- voiceover: "Fifth, prefill. The model reads your entire prompt in one parallel pass. This is the pause before the first token."
- duration: 6.6s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/06-prefill.html
- type: feature_showcase
- persuasion: Contrast setup (parallel here, sequential next)
- beat: comprehension
- blueprint: compose
- focal: a navy block of prompt tokens (a multi-row grid) that lights all at once in one sweep
- roles: spine (dot 5 coral) = supporting chrome · "Prefill" display = headline · token grid = foreground subject · single coral sweep line = voltage · pause timeline with "FIRST TOKEN" marker = supporting

narrativeRole: Fifth station: the model ingests the whole prompt at once, and this is where the wait before output lives.
keyMessage: Prefill reads your entire prompt in one parallel pass, and it is the pause before the first token.

Scene 1 (0.0–1.4s): spine present, dot 5 fills coral; kicker "✱ STEP 05 / 06"; display "Prefill" rises on "prefill" (~0.6s).
Scene 2 (1.4–3.3s): on "reads your entire prompt" (~1.9s) a navy panel appears holding a grid of dim token blocks (several rows, ~50% of frame), labeled mono "YOUR PROMPT".
Scene 3 (3.3–4.7s): on "one parallel pass" (~3.4s) a single coral vertical sweep line crosses the grid once, left to right, and every row lights to cream at the same moment the line passes (all rows together, not row by row). Mono label "ALL AT ONCE" appears.
Scene 4 (4.7–6.6s): on "the pause before the first token" (~5.1s) a hairline timeline draws below the panel with the grid's lit state at its left end and a hollow marker "FIRST TOKEN" at its right; the gap between them is labeled "pause". Hold.

---

## Frame 7 — Decode

- scene: Station 06 of 06: tokens appear one at a time and each is streamed back the moment it exists
- voiceover: "And sixth, decode. The model generates one token at a time, and each one is streamed back to you the moment it exists."
- duration: 7.3s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/07-decode.html
- type: feature_showcase
- persuasion: Contrast payoff (one at a time vs the prior all-at-once)
- beat: comprehension, satisfaction
- blueprint: prompt-type-submit-generate (Adapt)
- focal: a navy response panel where word-tokens stream in one chip at a time
- roles: spine (dot 6 coral, all six now visited) = supporting chrome · "Decode" display = headline · streaming token chips = foreground subject · the newest chip's coral edge = voltage · "STREAMED TO YOU" arrow rail = supporting

narrativeRole: Sixth station: output is produced sequentially, which is why you watch text appear word by word.
keyMessage: Decode generates one token at a time and streams each one back the moment it exists.

Adapt: keep only the streaming-answer signature move from the blueprint; the answer is the narration's own sentence rendered as token chips.

Scene 1 (0.0–1.6s): spine present, dot 6 fills coral; kicker "✱ STEP 06 / 06"; display "Decode" rises on "decode" (~0.77s).
Scene 2 (1.6–4.1s): on "generates one token at a time" (~2.2s) a navy response panel appears (~80% width) and mono token chips stream into it one by one, each chip appearing on its own beat: "The" "model" "generates" "one" "token" "at" "a" "time". The newest chip has a coral edge that passes to the next chip as it arrives. Mono counter "tokens: N" ticks with each chip.
Scene 3 (4.1–7.3s): on "streamed back to you" (~4.8s) a hairline arrow rail labeled "STREAMED TO YOU" draws beneath the panel; each further chip that arrives sends a small coral tick along the rail. On "the moment it exists" the streaming continues at the same cadence to the end of the frame. The last chips settle and hold.

---

## Frame 8 — Diagnose

- scene: The six stations stacked as one path; a single question asks which one is slow
- voiceover: "So when an LLM feels slow, ask which of those six steps is slow."
- duration: 4.9s
- transition_in: crossfade
- status: animated
- src: compositions/frames/08-diagnose.html
- type: benefit_highlight
- persuasion: Recap + actionable question
- beat: synthesis
- blueprint: grid-card-assemble (Adapt)
- focal: a vertical list of the six stations, 01 to 06, as one connected path
- roles: six station rows (mono index + EB Garamond name) = foreground subject · coral scan marker = voltage · question line = headline

narrativeRole: Turns the six-station model into a diagnostic habit.
keyMessage: When an LLM feels slow, the useful question is which of the six steps is slow.

Adapt: keep the vertical-list staggered cascade; the list is the whole request path, and a single scan marker walks it.

Scene 1 (0.0–1.9s): on "when an LLM feels slow" the display line "When an LLM feels slow," lands in the upper third (EB Garamond). Beneath, the six rows cascade in top to bottom as one quick beat: "01 API gateway", "02 Cache lookup", "03 Router", "04 Batching queue", "05 Prefill", "06 Decode", joined by a vertical hairline on the left (the spine turned vertical). Vertical list, ~50% of frame.
Scene 2 (1.9–3.5s): on "ask which of those six steps" (~2.4s) a coral scan marker steps down the six rows once, one row per beat, each row brightening as it is passed.
Scene 3 (3.5–4.9s): on "is slow" (~4.2s) the marker comes to rest beside the list as a coral "?" and the line "Which step is slow?" lands under the list. No row is singled out (the script does not name one). Hold still.

---

## Frame 9 — CTA

- scene: Comment GUIDE for the full request path
- voiceover: "Comment guide and I'll send you the full request path."
- duration: 2.849s
- transition_in: crossfade
- status: animated
- src: compositions/frames/09-cta.html
- type: cta
- persuasion: Direct ask
- beat: resolution
- blueprint: titlecard-reveal (Reproduce)
- focal: a coral callout block reading "Comment GUIDE"
- roles: coral callout = voltage + foreground subject · "for the full request path" line = supporting · faint six-dot spine = background echo

narrativeRole: Converts attention into a comment.
keyMessage: Comment GUIDE to get the full request path.

Scene 1 (0.0–1.0s): the six-dot spine sits faint at the top as an echo; on "Comment guide" (~0.1s) a coral callout block slides up with a crossfade, cream text: kicker "✱ COMMENT" and EB Garamond "GUIDE". Centered at y ≈ 800, ~35% of frame.
Scene 2 (1.0–2.849s): on "full request path" (~1.6s) the line "and I'll send you the full request path" lands beneath in Inter. Hold still to the end.
