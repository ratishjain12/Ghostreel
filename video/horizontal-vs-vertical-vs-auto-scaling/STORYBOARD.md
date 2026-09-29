---
format: 1080x1920
duration: 76s
message: "Comment 'GUIDE' and I'll send you the full breakdown. Vertical scaling, horizontal scaling, auto-scaling — 'we need to scale' is actually three separate decisions, and only one of them is about automation."
arc: concept-explainer (comparison spine)
audience: engineers and infra-adjacent builders who conflate scaling decisions with the automation decision
mode: autonomous
music: none
---

## Video direction

**Palette system (from `frame.md`, reused verbatim — this is the "Signal Path" design system, originally written for a reverse-proxy/load-balancer/gateway comparison, then already reused once for an agent/workflow/pipeline comparison; its atoms are reused again here, its three signal-color meanings remapped 1:1 onto this video's three concepts).** Void-black canvas (`colors.canvas` `#0A0D12`) + hairline circuit grid, every frame, no exceptions. Three signal colors, semantically fixed and never mixed inside one non-split frame:
- `colors.accent` (amber `#FF9F45`) = **vertical scaling** — one machine, one edge, simply forwarding to a single node that grows bigger. Nothing forks.
- `colors.accent-2` (teal `#4DE8C2`) = **horizontal scaling** — the edge forks into several identical, simultaneously-lit destination nodes (copies running side by side).
- `colors.accent-3` (violet `#B98CFF`) = **auto-scaling** — a gate/control loop sitting on top of the diagram, watching and resolving add/remove decisions before capacity changes.

This remap is faithful to `frame.md`'s own logic (forward/choose/gate), not arbitrary: vertical scaling is one path forwarding at higher capacity, horizontal scaling is one path choosing to fork into parallel copies, auto-scaling is a live decision gating whether/when capacity changes.

**Type** — Fraunces sentence-case display for every hook/thesis/CTA line; IBM Plex Sans for body copy; IBM Plex Mono uppercase for diagram chrome, node tags, and the caption rail (per `frame.md`).

**Build** — every diagram assembles on VO cue (the build IS the teaching), never dropped in whole. Safe zone respected: nothing load-bearing below y≈1670 (caption band) or above y≈150 (per BRIEF.md reel-safe-zone note).

**Fabrication** — no invented numbers or facts; the script's own claims are the only content (no numerals appear in this script).

**Transitions** — `cut` (frame 1, no predecessor) then `crossfade` throughout, consistent with `frame.md`'s "one continuous schematic" feel and the diagram-build pattern reused frame to frame.

**Motion grammar + reveal model** — long-tail `power3` settles everywhere (no bouncy/overshoot); every frame paces its reveals to the spoken line (nothing before its VO cue, development weighted into the back ~50%); a settled frame holds still, with subtle jitter as the only sanctioned aliveness — no lazy breathing, no back-half pan/push.

**Rhythm / held-frame allocation** — Frames 2-4 build progressively (each diagram develops across its full duration, never front-loaded); Frame 5 is the video's held breather (the triptych lands then holds, letting the reframe land before Frame 6's faster rule-of-three cadence); Frame 7 ends on a hard, deliberate still hold (no jitter — the last frame of the film).

**Negative list** — no shadow/gradient fill/glow on any diagram node (frame.md's flat-hairline rule); no color outside the three signal colors + rare danger rose; no slideshow (front-load-then-freeze — every frame's content arrives on VO cue); no screensaver (independently-floating elements); no repeat/yoyo/infinite loops; no bouncy easing.

## Frame 1 — Hook

- scene: Void canvas, hairline grid. Three terms — VERTICAL, HORIZONTAL, AUTO — flash one at a time, each briefly underlined in its own signal color (amber/teal/violet), then a kicker + headline settles the thesis-tease: scaling is three separate decisions.
- voiceover: "Vertical scaling, horizontal scaling, auto-scaling. People say we need to scale like it's one decision. It's actually three separate ones, and only one of them is really about automation."
- duration: 10.837s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Counterintuitive claim + concept announcement
- beat: curiosity + recognition
- blueprint: kinetic-type-beats (Adapt)
- focal: the three flashing terms, then the settling headline
- roles: VERTICAL/HORIZONTAL/AUTO term flashes = foreground subject · signal-color underline ticks = supporting · kicker line = supporting · headline = foreground subject
- sfx: none

Adapt: keep the hard-cut word-swap signature move; instead of one fixed line, each flashed term borrows its own signal color as an underline tick (a preview of the thesis), and the beat resolves into a settled headline instead of a spring-pop payoff.

Scene 1 (0.0–3.2s): void canvas + hairline grid; "VERTICAL" flashes centered in Fraunces display as the VO names it, an amber underline tick draws beneath it — hard-cut word-swap to "HORIZONTAL" (teal tick) at 1.12s — hard-cut to "AUTO" (violet tick) at 2.33s. Centered, type-only.
Scene 2 (3.2–5.84s): the three terms clear; a small mono kicker line types on with caret — "like it's one decision" — as the VO speaks it, centered beneath the (now empty) term slot.
Scene 3 (5.84–10.8s): kicker clears; a Fraunces h1 headline assembles via per-word staggered reveal timed to "actually three separate ones"; "automation" lands last in violet with a keyword glow as the VO says "about automation." Holds still on the settled headline — subtle jitter only.

narrativeRole: Opens the cognitive gap — names all three terms up front, then immediately undercuts the assumption that "scale" is one decision.
keyMessage: Vertical, horizontal, and auto-scaling are three separate decisions, and only one is about automation.

## Frame 2 — Vertical scaling

- scene: A single client node-box connected by ONE amber edge-forward to a single server node-box; the server node itself grows larger in place (no fork, no new nodes) as the VO names "more CPU, more RAM." A thin hairline ceiling cap materializes just above the node as the VO says "hardware ceiling," and a small crack/warning tick appears on the node as it says "can go down." "VERTICAL" mono label, "ONE MACHINE, BIGGER" caption line.
- voiceover: "Vertical scaling means making one machine bigger, more CPU, more RAM, on the same box. It's the simplest option, nothing about your architecture has to change, but you eventually hit a hardware ceiling, and there's still just one machine that can go down."
- duration: 14.165s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-vertical.html
- type: product_intro
- persuasion: Frame-then-fill (state the shape, then populate it)
- beat: clarity + orientation
- blueprint: compose
- focal: the single server node-box growing bigger
- roles: client node-box = supporting (small, upper) · amber edge-forward = supporting connector · server node-box = foreground subject (grows in place) · ceiling cap + crack tick = supporting
- sfx: none

Compose: no 22-blueprint shape fits a schematic node-and-edge diagram; built from `frame.md`'s Diagram-Build treatment + the motion vocabulary.

Scene 1 (0.0–1.97s): void canvas + hairline grid; a small CLIENT node-box (mono tag) fades in upper area, a single amber edge-forward draws rightward (SVG self-draw) as the VO says "Vertical scaling." Asymmetric 70/30, 2 depth layers.
Scene 2 (1.97–4.54s): a SERVER node-box appears at the edge's end and grows larger in place (value-scaled counter feel, no numeral) as the VO says "making one machine bigger, more CPU, more RAM" — "VERTICAL" mono label and "CPU"/"RAM" micro tags land one at a time via per-word staggered reveal.
Scene 3 (4.54–9.98s): node holds at its larger size as the VO says "the simplest option, nothing about your architecture has to change" — a "SAME BOX" mono caption settles beneath (per-word staggered reveal); mostly still.
Scene 4 (9.98–11.68s): a thin hairline ceiling cap draws in (SVG self-draw) just above the node as the VO says "hardware ceiling" — the node visibly presses against it.
Scene 5 (11.68–14.13s): a small crack/warning tick flashes on the node (keyword glow) as the VO says "can go down"; holds on the capped, cracked node to the frame's end — subtle jitter only.

narrativeRole: Names the simplest point on the spectrum — the baseline "same machine, just bigger" case, plus its ceiling.
keyMessage: Vertical scaling is one machine getting bigger — simple, but capped and still a single point of failure.

## Frame 3 — Horizontal scaling

- scene: The same client node-box, now its edge forks via teal edge-choose into 2-3 identical server node-boxes appearing side by side, one after another, all lit simultaneously (not one-at-a-time — this is redundancy, not routing). One node briefly dims/flickers out as the VO says "if one instance dies," while the others stay lit, then it relights. "HORIZONTAL" mono label, "MANY MACHINES, SAME JOB" caption line.
- voiceover: "Horizontal scaling means adding more machines instead, running the same service side by side. No hard ceiling the way vertical has, and you get redundancy for free, if one instance dies, the others are still there. The tradeoff is your app has to be built to run as multiple, coordinated copies."
- duration: 15.104s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-horizontal.html
- type: feature_showcase
- persuasion: Contrast against Frame 2's ceiling + build-up
- beat: comprehension + momentum
- blueprint: compose
- focal: the forking teal edge and its stack of identical server nodes
- roles: client node-box = supporting · teal edge-choose = foreground subject (forks) · server node-boxes ×3 = foreground subject (the copies) · flickering node = supporting emphasis
- sfx: none

Compose: continues Frame 2's diagram grammar (`frame.md`'s Diagram-Build treatment); no 22-blueprint shape fits a forking node diagram.

Scene 1 (0.0–1.08s): void canvas + hairline grid; Frame 2's node dissolves (crossfade continuity) to a neutral single client node-box as the VO begins "Horizontal scaling."
Scene 2 (1.08–4.32s): as the VO says "adding more machines instead, running the same service side by side," the edge forks (edge-choose, teal) and 2-3 node-boxes draw in left to right via cluster→outward expansion, each staying fully lit (never one-at-a-time-dim, unlike a load-balancer beat) — "HORIZONTAL" mono label appears.
Scene 3 (4.32–8.52s): a "MANY MACHINES, SAME JOB" caption settles beneath the stack (per-word staggered reveal) as the VO says "no hard ceiling... redundancy for free" — stack holds, no new nodes.
Scene 4 (8.52–10.55s): the middle node dims out briefly (keyword glow, inverse) as the VO says "if one instance dies," then relights within the same window as the VO says "the others are still there," demonstrating redundancy live.
Scene 5 (10.55–15.0s): stack holds steady through "the tradeoff... multiple, coordinated copies" — a "COORDINATED COPIES" mono sub-line types on with caret beneath the stack; settles held — subtle jitter only.

narrativeRole: Contrasts directly against vertical's ceiling and single point of failure — more machines instead of a bigger one.
keyMessage: Horizontal scaling adds redundant copies with no hard ceiling, at the cost of needing coordinated, multi-instance-aware code.

## Frame 4 — Auto-scaling

- scene: The same horizontal node stack from Frame 3 (now dimmed to a quiet base layer), with a violet gate/control loop glyph positioned above it — a small pulsing eye/loop-arrow "watching" the stack. As the VO says "adds or removes capacity," a gate-tick fires and a node-box appears or fades from the stack below, controlled by the loop, not by a person. "AUTO" mono label, "WATCHES + DECIDES" caption line.
- voiceover: "Auto-scaling isn't a third way to add capacity, it's the automation layer on top of the other two. It watches real demand and adds or removes capacity for you, instead of a human deciding when to scale up or down."
- duration: 11.861s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-auto.html
- type: feature_showcase
- persuasion: Reframe (not a third option, a layer on the first two) + causal demonstration
- beat: "aha" + focus
- blueprint: compose
- focal: the violet gate/control loop watching the node stack
- roles: horizontal node stack (dimmed, carried over from Frame 3) = background · violet control-loop glyph = foreground subject · sightline + gate-tick = supporting
- sfx: none

Compose: no 22-blueprint shape fits a control-loop-gating-a-diagram beat; built from `frame.md`'s edge-gate component + the motion vocabulary.

Scene 1 (0.0–2.78s): Frame 3's node stack carries over (crossfade continuity), dimmed to ~40% as a quiet base layer, as the VO says "Auto-scaling isn't a third way to add capacity" — a violet loop-arrow glyph draws in above the stack (SVG self-draw) as the VO reaches "the automation layer on top of the other two"; "AUTO" mono label appears.
Scene 2 (2.78–6.94s): the loop glyph pulses (live SVG internals) as the VO says "it watches real demand" — a thin dashed sightline draws from the loop down to the stack (SVG self-draw).
Scene 3 (6.94–9.32s): a gate-tick on the sightline flips hollow→filled (violet) as the VO says "adds or removes capacity" — in the same beat, a node-box in the dimmed stack below fades in or out, visibly driven by the loop.
Scene 4 (9.32–11.88s): a "WATCHES + DECIDES" mono caption settles beneath as the VO finishes "instead of a human deciding when to scale up or down"; holds still — subtle jitter only on the loop glyph's internals.

narrativeRole: Completes the three-way comparison by reframing auto-scaling as orthogonal to the other two — a decision layer, not a capacity mechanism.
keyMessage: Auto-scaling doesn't add capacity itself — it automates the decision to use vertical or horizontal capacity.

## Frame 5 — The real split

- scene: Frames 2-4's diagrams shrink into a Recap Triptych — three mini node-glyphs stacked (portrait), each in its own signal color with a one-line label ("gets bigger" amber / "gets copies" teal / "decides when" violet) — then a simple two-way split label draws underneath: "CAPACITY" bracketing the amber+teal glyphs, "DECISION" bracketing the violet glyph.
- voiceover: "So vertical and horizontal answer how do we get more capacity. Auto-scaling answers who decides when we need it, and how fast do we react."
- duration: 8.533s
- transition_in: crossfade
- status: animated
- src: compositions/frames/05-split.html
- type: benefit_highlight
- persuasion: Distillation (compress to one line) + reframing
- beat: clarity + conviction
- blueprint: compose
- focal: the three mini node-glyphs and the CAPACITY / DECISION split label
- roles: amber mini-glyph = foreground subject · teal mini-glyph = foreground subject · violet mini-glyph = foreground subject · CAPACITY/DECISION bracket labels = supporting
- sfx: none

Compose: instantiates `frame.md`'s Recap Triptych treatment (not in the 22-blueprint menu, which skews product-UI); nearest analog is a calm distillation beat like `titlecard-reveal`, adapted to three colored glyphs instead of one card.

Scene 1 (0.0–1.77s): void canvas; Frames 2-3's diagrams shrink and land as mini node-glyphs stacked vertically (cluster→outward expansion, inward), amber then teal, as the VO says "So vertical and horizontal answer."
Scene 2 (1.77–4.07s): a "CAPACITY" mono bracket label draws beneath the amber+teal pair (SVG self-draw) as the VO completes "how do we get more capacity?"
Scene 3 (4.07–7.27s): the violet glyph lands third as the VO says "Auto-scaling answers who decides when we need it" — a "DECISION" mono bracket label draws beneath it.
Scene 4 (7.27–8.48s): "how fast do we react?" lands as a small emphasized Fraunces line beside the violet glyph, "fast" landing with a keyword glow; holds on all three glyphs and both bracket labels — subtle jitter only.

narrativeRole: Reframes the whole comparison around the real axis (capacity mechanism vs. decision-making) instead of treating all three as one spectrum.
keyMessage: Vertical and horizontal answer "how do we get more capacity"; auto-scaling answers "who decides, and how fast."

## Frame 6 — Guidance

- scene: Three short statements land top-to-bottom in sequence (portrait stack), each prefixed by a mono index tag and its matching signal-color tick (amber/teal/violet), echoing the triptych's colors from Frame 5.
- voiceover: "Scale vertically first, it's the cheapest fix while you're small. Move to horizontal once you need redundancy or you're hitting the ceiling of a single machine. Add auto-scaling once your traffic is unpredictable enough that manual scaling can't keep up."
- duration: 13.056s
- transition_in: crossfade
- status: animated
- src: compositions/frames/06-guidance.html
- type: social_proof
- persuasion: Rule of three + signposting
- beat: mastery + conviction
- blueprint: grid-card-assemble (Adapt)
- focal: the three rule-of-three statements landing top-to-bottom
- roles: statement 1 (amber tick) = foreground subject · statement 2 (teal tick) = foreground subject · statement 3 (violet tick) = foreground subject
- sfx: none

Adapt: keep the staggered-cascade signature move; instead of cards/tiles, each item is a mono index tag + signal-color tick + a short Fraunces statement, echoing Frame 5's triptych colors.

Scene 1 (0.0–3.25s): void canvas + hairline grid; mono index tag "01" + amber tick land upper area, then "Scale vertically first, it's the cheapest fix while you're small." lands via per-word staggered reveal as the VO speaks it.
Scene 2 (3.25–8.19s): first statement dims slightly; mono index tag "02" + teal tick land beneath it, "Move to horizontal once you need redundancy or you're hitting the ceiling of a single machine." lands via per-word staggered reveal.
Scene 3 (8.19–13.0s): second statement dims; mono index tag "03" + violet tick land beneath, "Add auto-scaling once your traffic is unpredictable enough that manual scaling can't keep up." lands via per-word staggered reveal, "keep up" landing as the final keyword-glow emphasis; holds on all three stacked statements — subtle jitter only.

narrativeRole: Converts the taxonomy into a decision rule the viewer can actually apply, in the same order the video introduced the three concepts.
keyMessage: Scale vertically first, go horizontal for redundancy or ceiling, add auto-scaling only once traffic is unpredictable.

## Frame 7 — CTA

- scene: A short Fraunces sign-off line settles, "GUIDE" emphasized in amber (the video's primary/first-named signal — vertical scaling, per `frame.md`'s CTA convention), a small mono sub-line beneath — holds fully still to the final frame.
- voiceover: "Comment guide, and I'll send over the full breakdown."
- duration: 2.429s
- transition_in: crossfade
- status: animated
- src: compositions/frames/07-cta.html
- type: cta
- persuasion: Direct address
- beat: resolve + inevitability
- blueprint: titlecard-reveal (Adapt)
- focal: the sign-off line with "GUIDE" emphasized
- roles: sign-off line = foreground subject · mono sub-line = supporting
- sfx: none

Adapt: keep the one-restrained-move-then-still-hold signature (per `frame.md`'s Brand/CTA treatment); no card chain given the 2.4s duration.

Scene 1 (0.0–1.08s): void canvas; a short Fraunces sign-off line slides up as the VO begins, "Comment" — centered, single clean move.
Scene 2 (1.08–2.28s): "guide" lands in amber with a keyword glow as the VO says it, the rest of the line completes via per-word staggered reveal; a small mono sub-line settles beneath; holds fully still to the final frame — no jitter, this is the video's last frame.

narrativeRole: Closes with the concrete, low-friction ask.
keyMessage: Comment "GUIDE" to get the full breakdown.
