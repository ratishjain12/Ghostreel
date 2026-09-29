---
format: 1080x1920
duration: 89s
message: "An idempotency key stops the client from re-doing a write it already did. Deduplication stops the consumer from re-processing a message it already saw. A distributed lock stops multiple processes from touching the same critical section at once — a different axis (concurrency, not duplication) entirely."
arc: concept-explainer
audience: backend engineers who reach for these three terms loosely; developers prepping system-design interviews
mode: autonomous
music: none
---

## Video direction

**Palette system** (from `frame.md`, never invented elsewhere): void-black canvas
(`canvas` / `canvas-raised` / `canvas-raised-2`) throughout — no other ground ever
appears. `frame.md`'s three signal colors are reused, but **remapped to this video's
three concepts** (this script is not the reverse-proxy/load-balancer/API-gateway video
the pack shipped with — "atoms are sacred, composition is free," per `frame.md`'s own
principle line; the same remap was already done once for this account's
`api-gateway-vs-service-mesh-vs-sidecar-proxy` video, so this is the established fix for
the seeding pack always shipping the same dark schematic system regardless of topic):
**amber `accent`** = an idempotency key / a request that gets **checked against a key and
short-circuited** on retry; **teal `accent-2`** = deduplication / a message that gets
**checked against a seen-set and skipped** on retry; **violet `accent-3`** = a distributed
lock / multiple processes **converging on one gate where only one is let through**. None
of the three is "forwarding" in this script the way the pack's original edge-forward was —
all three are check-then-branch behaviors, so every diagram edge in this video carries at
least one gate-tick; what changes per concept is WHO is being checked (one client request,
a stream of messages, or competing processes) and WHAT happens on the two branches
(return cached result / skip and drop / wait-then-one-proceeds). `ink` / `ink-dim` /
`ink-faint` for text, `line` for hairlines. `danger` (rose) stays in reserve — nothing in
this script is a failure state, only a correctly-skipped duplicate or a correctly-waiting
process. The caption rail (`.hyperframes/caption-skin.html`) borrows these same three
colors for scarce keyword emphasis — one visual system, not two.

**Motion grammar + reveal model:** one continuous "same request/message/lock stage,
different mechanism" feeling across the diagram frames (2 → 4) — each reuses a small
CLIENT/PRODUCER/WORKER → gate → OUTCOME diagram vocabulary, just recomposed per concept,
linked by `zoom-through` seams that read as pushing into a new mechanism rather than
cutting to an unrelated slide. Frame 2 shows ONE client re-sending ONE request (a single
edge, sent twice, second pass diverts at the gate). Frame 3 shows a STREAM of message
dots arriving at a consumer (multiple edges, some diverted at the gate). Frame 4 shows
MULTIPLE worker nodes converging on ONE shared resource (edges converge inward instead of
diverging outward — the one topology this video needs that the pack's original
edge-choose didn't have, built from the same node-box/edge/gate-tick atoms). Every reveal
is timed to the voiceover; `power3` long-tail settles everywhere, no bounce/overshoot
except the deliberately-playful spring-pop on the hook's term flashes. Gate-ticks flip
hollow → filled on their spoken cue. Only the FINAL frame gets an exit tween (a settle);
every other frame's exit is its `transition_in`.

**Rhythm / held-frame allocation:** Frame 5 (the client-side/consumer-side/concurrency
thesis) builds to a **stillness-before-climax** hold — the three recap glyphs land, then
everything holds dead still while the closing clause finishes. Frame 7 (CTA) ends on a
calm settled hold. Every other frame keeps developing to its own last beat — three
distinct mechanisms in ~54s leaves no other slack beat to spare.

**Negative list:** no shadow, no gradient fill, no card glow on a diagram node (hairline +
flat only — the one sanctioned glow is the ambient bloom behind Frame 5's held recap and
Frame 7's sign-off); no color on an edge/gate-tick other than the three fixed signal
colors, and their concept roles never swap mid-video; no rounded "pill" nodes; no lazy
breathing / idle wobble; no bad slow pan/push in a scene's back half; no front-loaded-then-
frozen diagram (every diagram frame keeps resolving into its back ~50%); nothing
(including the caption rail) below y≈1670 on the 1920-tall canvas, nothing load-bearing
above y≈150 — this project's reel safe zone per `BRIEF.md`.

**Numerals & claims:** the script contains no invented figures — do not add latency
numbers, worker counts, or percentages beyond generic small counts a diagram needs (e.g.
"3 workers" as a generic illustrative count for Frame 4, never stated as a script fact).

---

## Frame 1 — Idempotency key, deduplication, distributed lock

- scene: three terms hard-cut flash across a void-black schematic sheet, each briefly ticked in its own signal color, before collapsing into a stacked list and the "three genuinely different problems" stamp settles
- voiceover: "Idempotency key, deduplication, distributed lock. Three ways to stop the same thing from happening twice, and they solve three genuinely different versions of that problem."
- duration: 9.72s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Concept announcement + counterintuitive claim (these are not interchangeable)
- beat: curiosity + recognition
- blueprint: kinetic-type-beats (Adapt)
- focal: the three term-words themselves
- roles: term words = foreground subject (hard-cut flashes, then stacked) · hairline schematic grid = background (dim, ambient) · "three different problems" stamp = supporting
- sfx: none

narrativeRole: Opens the cognitive gap immediately — names all three terms and states the contrarian claim (genuinely different problems, not one problem with three names) as the punchiest possible first line.
keyMessage: These three terms all "stop something from happening twice," but they solve three genuinely different versions of that problem.

Adapt: keep kinetic-type-beats' hard-cut word-swap signature; the payoff is the settled hook stamp naming the claim, not a logo.
Scene 1 (0.0–2.1s): void canvas, faint hairline grid at ~12% alpha. On "Idempotency key," the words IDEMPOTENCY KEY hard-cut flash full-bleed in Fraunces `display`, ink, with a brief amber underline tick — centered, ~65% of frame width. On "deduplication," hard-cut swap to DEDUPLICATION, brief teal tick. On "distributed lock," hard-cut swap to DISTRIBUTED LOCK, brief violet tick.
Scene 2 (2.1–4.6s): as the VO says "three ways to stop the same thing from happening twice," the three words collapse (scale-swap) into a smaller stacked list — amber / teal / violet ticks kept — sliding to the upper third; a kicker-weight Fraunces italic line "SAME THING, TWICE" per-word staggered reveal fades in beneath.
Scene 3 (4.6–7.0s): on "and they solve three genuinely different versions," each of the three stacked terms briefly pulses its own signal color outward as a thin ring (three separate pulses, staggered, not simultaneous) — visualizing "different versions" without yet explaining any of them.
Scene 4 (7.0–9.72s): on "of that problem," a Fraunces `h2` stamp line builds word-by-word beneath the stack: "three different problems." — holding fully still for the cut into Frame 2, subtle jitter only.

---

## Frame 2 — The idempotency key returns the original result

- scene: a CLIENT node sends the same request twice along an amber edge toward a SERVER; the first pass runs the WORK node and stores a result; the second pass hits a KEY-SEEN? gate-tick that's already filled and diverts straight to a RETURN ORIGINAL RESULT endpoint, never touching WORK again
- voiceover: "An idempotency key is something the client attaches to a request, a unique ID for that specific logical operation. If the same request gets sent twice, because of a retry, a flaky network, whatever, the server sees the same key and knows to return the original result instead of doing the work again."
- duration: 16.52s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/02-idempotency-key.html
- type: product_intro
- persuasion: Mechanism walkthrough — cause (retry) then effect (short-circuit)
- beat: clarity + relief (the system handles the retry gracefully)
- blueprint: spatial-pan-stations (Adapt)
- focal: the KEY-SEEN? gate-tick flipping from hollow to filled between pass 1 and pass 2
- roles: CLIENT node = supporting (fixed, left) · amber edge = the request path, traversed twice · KEY-SEEN? gate-tick = focal check · WORK node = supporting (reached once only) · RETURN ORIGINAL RESULT endpoint = supporting (reached on pass 2)
- sfx: click-soft, whoosh-short

narrativeRole: Establishes the first mechanism in concrete, visual terms — a client-attached key that lets the server recognize "I've already done this" and skip redoing the work.
keyMessage: The idempotency key is a client-side request ID; on retry, the server matches it and returns the original result instead of re-executing.

Adapt: spatial-pan-stations' station-to-station traversal becomes "the same edge, walked twice" — station order fixed (CLIENT → gate → WORK/RETURN), only which branch lights up changes between passes.
Scene 1 (0.0–3.3s): CLIENT node-box (station-label "CLIENT") sits left, mono micro tag beneath. As the VO says "attaches to a request, a unique ID," a small amber tag glyph ("KEY: 7f3a…") assembles above the client node, then rides an amber edge (`svg-path-draw`) rightward toward a KEY-SEEN? gate-tick sitting mid-edge (hollow, ink-dim).
Scene 2 (3.3–7.5s): on "the same request gets sent twice, because of a retry, a flaky network," the request dot completes pass 1 — the KEY-SEEN? gate is hollow (first time), so it passes straight through to a WORK node-box on the right, which briefly fills solid (amber) as "doing the work" — then a second identical request dot launches from CLIENT, retracing the same edge (visually distinguished only by "retry" ghost-trail behind it).
Scene 3 (7.5–12.5s): on "the server sees the same key and knows to," the second dot reaches the KEY-SEEN? gate-tick, which is now filled amber (checked) — the dot does NOT continue to WORK; it diverts downward along a short branch edge toward a new RETURN ORIGINAL RESULT node-box that assembles just as the dot arrives.
Scene 4 (12.5–16.52s): on "return the original result instead of doing the work again," the RETURN ORIGINAL RESULT node holds lit amber while the WORK node visibly stays dim/untouched on this second pass — the contrast (one lit, one dark) is the whole payoff — settling to a calm hold for the cut.

---

## Frame 3 — Deduplication skips the repeat message

- scene: a stream of message dots flows from a PRODUCER/queue toward a CONSUMER node; each dot carries a small ID tag; a SEEN-SET gate-tick on the edge lets first-seen IDs through to a PROCESSED node while a repeated ID is diverted to a SKIPPED bin
- voiceover: "Deduplication is the system's own job, not the client's. It's for event and message pipelines, where the same message can arrive more than once through no fault of the sender, and the consumer has to recognize it's already processed that exact message ID and skip it."
- duration: 14.75s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/03-deduplication.html
- type: feature_showcase
- persuasion: Contrast with Frame 2 — same-shaped problem, different owner (consumer, not client) and different unit (a message stream, not one request)
- beat: recognition (the pattern repeats, but the actor changed)
- blueprint: fixed-anchor-cycle (Adapt)
- focal: the SEEN-SET gate-tick catching a repeated message ID
- roles: message-dot stream = foreground subject (several dots, one repeated) · SEEN-SET gate-tick = focal check · PRODUCER/queue label = supporting (background, quiet) · CONSUMER node = supporting (fixed, right) · PROCESSED / SKIPPED endpoints = supporting
- sfx: click-soft, whoosh-short

narrativeRole: Draws the client-vs-system distinction the thesis (Frame 5) will name explicitly — dedup looks like idempotency's mirror image but the checking party and the unit being checked are both different.
keyMessage: Deduplication is the consumer's own responsibility in message/event pipelines — it recognizes an already-processed message ID and skips it, no client involvement.

Adapt: fixed-anchor-cycle's repeating-cycle signature becomes several message dots cycling along the SAME edge in sequence, one of which repeats an ID already seen — the "cycle" is the message stream itself, not a UI loop.
Scene 1 (0.0–3.0s): a quiet PRODUCER/queue station-label sits left (small, mono, low-emphasis — "not the client's job" is about who's on the RIGHT). A teal edge runs to a CONSUMER node-box on the right with a SEEN-SET gate-tick (hollow) mid-edge.
Scene 2 (3.0–7.0s): on "event and message pipelines, where the same message can arrive more than once," 3-4 small message dots (each with a tiny mono ID tag, e.g. "MSG-42," "MSG-43") launch in sequence along the teal edge — first two pass the hollow gate cleanly (gate stays hollow, nothing to catch yet) and land on a PROCESSED node-box that ticks up a small count (1, 2).
Scene 3 (7.0–11.0s): on "the consumer has to recognize it's already processed that exact message ID," a new dot arrives tagged "MSG-42" again (identical tag to one already seen) — the SEEN-SET gate-tick flips hollow → filled (teal) right as this dot reaches it, a brief comparison glyph (two matching ID tags overlapping) flashes at the gate.
Scene 4 (11.0–14.75s): on "and skip it," the repeated dot diverts downward off the main edge into a small SKIPPED bin/glyph (a dim outline, not a harsh "error" mark — this is correct, expected behavior) while PROCESSED's count stays unchanged — holding on the contrast between the ticking PROCESSED count and the quiet SKIPPED dot for the cut.

---

## Frame 4 — The distributed lock is about concurrency, not duplicates

- scene: three WORKER nodes on separate machines each send an edge converging on ONE shared CRITICAL SECTION node guarded by a single LOCK gate-tick; only one edge lights up and passes through while the other two visibly hold at the gate
- voiceover: "A distributed lock isn't really about duplicates at all, it's about concurrency. It makes sure that when multiple processes across multiple machines could all try to do the same critical section of work at the same time, only one of them actually gets to."
- duration: 13.48s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/04-distributed-lock.html
- type: feature_showcase
- persuasion: Reframe — explicitly denies the reader's likely assumption ("isn't really about duplicates") before giving the real mechanism
- beat: reorientation (this one is a different axis entirely)
- blueprint: agent-progress-theater (Adapt)
- focal: the single lit edge passing the LOCK gate while the other two hold dim/paused
- roles: three WORKER node-boxes = foreground subject (symmetric, converging) · violet edges = the three competing paths · LOCK gate-tick = focal check (single, shared) · CRITICAL SECTION node = supporting (center/right, the shared resource) · the two held-back workers = supporting (dim, waiting, not defeated)
- sfx: click-soft, impact-bass-1

narrativeRole: The pivot frame — explicitly reframes the axis from "duplicates" (Frames 2-3) to "concurrency," setting up Frame 5's thesis that a distributed lock is categorically different from the other two, not a third variant of the same idea.
keyMessage: A distributed lock isn't about recognizing a repeat — it's about letting only one of several simultaneous contenders proceed through a shared critical section.
sceneNote: this is the one topology in the video that converges INWARD (3 edges → 1 gate) rather than following a single edge outward — built from the same node-box/edge/gate-tick atoms as Frames 2-3, composed differently because this mechanism actually is different.

Adapt: agent-progress-theater's multiple-simultaneous-agents signature maps directly onto "multiple processes across multiple machines" — three parallel progress paths, only one resolves to completion in this beat.
Scene 1 (0.0–2.7s): on "isn't really about duplicates at all, it's about concurrency," three WORKER node-boxes (station-labels "WORKER A / B / C," mono) arrange in a symmetric arc, each with a violet edge stub extending toward a shared point at center-right where a CRITICAL SECTION node-box (larger, canvas-raised-2) sits, currently un-approached.
Scene 2 (2.7–6.5s): on "when multiple processes across multiple machines could all try to do the same critical section of work at the same time," all three violet edges draw simultaneously (`svg-path-draw`, synced start) converging toward a single LOCK gate-tick positioned just before CRITICAL SECTION — all three request-dots arrive at the gate at nearly the same moment, a visible "crowding" beat.
Scene 3 (6.5–10.5s): on "only one of them," the LOCK gate-tick resolves — flips filled violet — and Worker B's dot (arbitrary, established as visually mid/no different from the others beforehand, so the choice reads as contention resolution, not favoritism) passes through into CRITICAL SECTION, which lights up solid violet.
Scene 4 (10.5–13.48s): on "actually gets to," Worker A's and Worker C's dots visibly hold just before the gate — dim, static, a small mono "WAITING" micro-tag beside each — while CRITICAL SECTION stays lit for Worker B, holding still for the cut.

---

## Frame 5 — The real distinction

- scene: three small mini-glyphs (amber check-shortcut, teal check-skip, violet converge-gate) assemble side by side, each with a short Fraunces label naming what it stops and who owns the check; all three hold together as the thesis line lands
- voiceover: "So idempotency keys and deduplication both stop the same operation from running twice, one from the client side, one from the consumer side. A distributed lock stops different processes from colliding while doing that operation in the first place."
- duration: 14.22s
- transition_in: crossfade
- status: animated
- src: compositions/frames/05-thesis.html
- type: branding
- persuasion: Synthesis — names the shared trait (client-side vs consumer-side stop-a-repeat) before isolating the outlier (distributed lock prevents collision, not repetition)
- beat: payoff / clarity landing
- blueprint: grid-card-assemble (Adapt)
- focal: the three mini-glyphs landing then holding together
- roles: amber mini-glyph = "client side" · teal mini-glyph = "consumer side" · violet mini-glyph = "prevents the collision" (visually set apart from the first two, e.g. a small gap in the stack) · thesis line = foreground text, lands last
- sfx: click-soft

narrativeRole: The payoff — collects the three separately-explained mechanisms into one clean mental model: two are about not re-doing a finished operation (client vs consumer side), one is about not colliding while doing it in the first place.
keyMessage: Idempotency keys and deduplication both stop a completed operation from re-running (client-side vs consumer-side); a distributed lock stops the collision before the operation even starts.

Adapt: grid-card-assemble's simultaneous-card-landing becomes a staggered but grouped landing — cards 1-2 (amber, teal) assemble as a visually paired duo (both "stop a repeat"), a beat later card 3 (violet) assembles with a small physical gap from the duo (visually "different axis").
Scene 1 (0.0–4.5s): void canvas. On "idempotency keys and deduplication both stop the same operation from running twice," an amber mini-glyph (a tiny check-tick + diverted-arrow shape) and a teal mini-glyph (a tiny check-tick + skip-bin shape) assemble together, side by side, upper-center, each with a small Fraunces `h3` label beneath: "client side" (amber) and "consumer side" (teal).
Scene 2 (4.5–7.5s): on "one from the client side, one from the consumer side," each label's owning word ("client" / "consumer") gets a brief signal-color underline pulse matching its glyph — reinforcing the pairing without adding new shapes.
Scene 3 (7.5–11.5s): on "a distributed lock stops different processes from colliding," a violet mini-glyph (three tiny converging lines into one gate shape) assembles below the amber/teal pair with a deliberate visible gap, label "prevents the collision" building in beneath it.
Scene 4 (11.5–14.22s): on "while doing that operation in the first place," all three glyphs hold completely still (stillness-before-climax) while a final Fraunces `h2` line settles beneath all three: "same goal, three different guards." — full stop, no motion, for the hold into Frame 6.

---

## Frame 6 — When to reach for which

- scene: three short practical statements land top-to-bottom in sequence, each prefixed by a mono index tag and its matching signal-color tick
- voiceover: "Use an idempotency key for any client-initiated write that might get retried, payments especially. Use deduplication in any message or event pipeline where at-least-once delivery is possible. Reach for a distributed lock when multiple workers could pick up the same job simultaneously and you need exactly one of them to win."
- duration: 18.09s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/06-guidance.html
- type: benefit_highlight
- persuasion: Practical rule-of-three — converts the definitions into a decision guide
- beat: actionable takeaway
- blueprint: kinetic-type-beats (Adapt)
- focal: the statement currently landing
- roles: mono index tags (01/02/03) = chrome · amber/teal/violet ticks = matching each statement to its Frame 2-4 concept · three Fraunces statement lines = foreground subject, landing in sequence and staying visible
- sfx: click-soft

narrativeRole: Converts three definitions into a decision rule — the practical payoff a viewer screenshots or saves.
keyMessage: Idempotency key → client-initiated writes that might retry (payments). Deduplication → message/event pipelines with at-least-once delivery. Distributed lock → multiple workers racing for the same job, need exactly one winner.

Adapt: kinetic-type-beats' word-by-word landing becomes line-by-line landing, three lines total, each staying on screen (unlike Frame 1's hard-cut replace) so the list reads as a keepable rule-of-three.
Scene 1 (0.0–5.8s): on "use an idempotency key for any client-initiated write that might get retried, payments especially," line 1 lands top: mono "01" + amber tick, Fraunces `h3` "Idempotency key — client writes that might retry (payments)" builds word-by-word, settles.
Scene 2 (5.8–12.0s): on "use deduplication in any message or event pipeline where at-least-once delivery is possible," line 2 lands beneath: mono "02" + teal tick, "Deduplication — message/event pipelines, at-least-once delivery" builds word-by-word, settles; line 1 stays visible, slightly dimmed (ink-dim) to keep focus on line 2.
Scene 3 (12.0–18.09s): on "reach for a distributed lock when multiple workers could pick up the same job simultaneously and you need exactly one of them to win," line 3 lands beneath: mono "03" + violet tick, "Distributed lock — multiple workers, need exactly one winner" builds word-by-word; all three lines relight to equal brightness together as the line finishes, holding for the cut.

---

## Frame 7 — CTA

- scene: a single Fraunces sign-off line settles center frame with one emphasized quoted word, held calm
- voiceover: "Comment guide and I'll send over the full breakdown."
- duration: 2.53s
- transition_in: crossfade
- status: animated
- src: compositions/frames/07-cta.html
- type: cta
- persuasion: Direct, low-friction ask
- beat: warm closing address
- blueprint: titlecard-reveal (Adapt)
- focal: the quoted word "guide"
- roles: sign-off line = foreground subject · quoted "guide" = emphasized (amber, this video's first-named signal color, per frame.md's CTA convention) · mono sub-line = supporting, small
- sfx: none

narrativeRole: Closes on the account's standard engagement CTA, unchanged from the script.
keyMessage: Comment "guide" for the full breakdown.

Adapt: titlecard-reveal's single clean settle, no extra motion — this is the shortest frame in the video and should read as a calm exhale after Frame 6's density.
Scene 1 (0.0–1.3s): void canvas. Fraunces `h2` sign-off builds word-by-word: "Comment" "guide" "and I'll send over" — the word "guide" rendered in amber quote-marks as it lands, matching frame.md's CTA-uses-the-primary-signal-color convention.
Scene 2 (1.3–2.53s): "the full breakdown." completes the line beneath in `lead` weight; the whole line holds fully still (no exit tween — this is the video's final frame) for the render's last frame.
