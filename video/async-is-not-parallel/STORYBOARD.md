---
format: 1080x1920
duration: 59s
message: "Async overlaps waiting; it does not compute faster. CPU-heavy work needs parallelism (multiple cores), and mixing the two up makes async slower, not faster."
arc: concept-explainer with process (hook before/after → mechanism: sequential vs overlapped waits → name concurrency → the CPU trap → the fix: parallelism → the rule → landing → CTA)
audience: backend engineers who reach for async as a general "make it fast" switch
mode: autonomous
music: none
hook_style: before-after
---

## Video direction

- **Palette** (from `frame.md`, broadside): two registers only. **Dark** register (ink-black ground, cream text, fire-orange the lone accent) carries the documentary frames. **Orange** register (fire-orange ground, ink text, never cream on orange) is reserved for the three declarations: Frame 4 (naming concurrency), the bottom half of Frame 8 (parallelism), and Frame 10 (CTA). Semantic color binding across the film: **cream-hint outlined bars = WAITING** (network calls, idle time); **solid fire-orange block = COMPUTING** (the image resize, CPU work). The viewer learns "orange = CPU" in Frame 5 and it pays off in Frames 6 to 8. No second hue ever.
- **Type**: Barlow lowercase 900 negative-tracked for every hero word/numeral (one display moment per frame); IBM Plex Mono uppercase 0.14em for every label, lane name, and tag. Fonts are the locked `@font-face` block in `frame.md` (Fonts (locked)), verbatim, nothing else.
- **The shared stage** (Frames 2, 3, 5, 6, 7): a **time-lane diagram**. Horizontal lanes stacked vertically, a 1px `border-dark` hairline baseline under each lane, a mono lane label left-aligned above each lane, and a mono `TIME →` axis tag at the top-right of the stage. Bars grow left-to-right along their lane (scaleX from the left edge). Same lane geometry, spacing, and stage position in every stage frame so the film reads as one instrument re-measured, not five diagrams.
- **Motion grammar**: `power3` long-tail settles everywhere; no bounce, no overshoot. Numeral swaps are hard cuts (`discrete-text-sequence`), never rolls. Bars self-draw left to right on their spoken cue. Every reveal is timed to its word in the VO; nothing front-loads. Only Frame 10 has an exit.
- **Rhythm / held beats**: Frame 4 (concurrency named, 3.9s) and Frame 9 (slower, not faster, 2.8s) are the breathers: land fast, then hold dead still. Frame 8 (the rule) settles and holds its last ~0.6s so the takeaway is screenshot-able (growth analysis: saves are the account's strongest signal). Frames 1 to 3 and 5 to 7 carry the build energy.
- **Pacing** (short ~60s reel, per brief and growth notes): hook numeral visible by t=0.3s; one idea per frame; frames switch on sentence boundaries.
- **Negative list**: no second accent color; no cream text on orange; no drop shadow, no radius, no gradient ground; no bouncy easing; no lazy breathing, no back-half pan or push; no floating bokeh or purple-blue AI gradient; no infinite/looping motion; no em dashes in any visible text; no invented figures. The only numbers on screen are the script's own: 400ms, 40ms, and the counts three / one / single. Bars carry no ms values.
- **Safe zones**: canvas 1080×1920. Scene content lives between y≈150 and y≈1590 (caption band + platform chrome below, username chrome above). Centered heroes anchor around y≈806.

## Frame 1 — The before and after

- scene: A giant "400ms" numeral hard-cuts to an orange "40ms" as async lands, then a mono "+1 LINE" tag drops in and the numeral snaps back to "400ms".
- voiceover: "You rewrite an API handler with async and it goes from four hundred milliseconds to forty. Then you add one line and it's back to four hundred. Here's why."
- duration: 8.12s
- transition_in: cut
- status: outline
- src: compositions/frames/01-the-before-and-after.html
- type: hook
- persuasion: Before/after + Counterexample (the win, then the one line that undoes it)
- beat: Surprise + puzzlement
- blueprint: kinetic-type-beats (Adapt)

narrativeRole: Opens the gap with a concrete before/after the viewer has either lived or wants: async gives a 10x win, then one line silently takes it back.
keyMessage: Async made it fast, and one line made it slow again; something about async is being misunderstood.

Adapt: keep the in-place token swap signature (the numeral slot swaps by hard cut); the swapped token is a latency numeral instead of a word.
focal: the latency numeral ("400ms" / "40ms" / "400ms")
roles: latency numeral = foreground subject · mono kicker "API HANDLER" + state tag = supporting · 1px hairline rule under the numeral = supporting · ink-black ground = background
sfx: tick, impact-soft

Scene 1 (0.0–1.6s): dark register. A mono kicker "API HANDLER" sits upper-left (~y 360) with the 36×2 orange rule stub; the cream numeral "400ms" is already landing by t=0.3s via a fast `waterfall-entry` rise, Barlow 900 lowercase, near full-bleed (~85% width), centered around y≈806. A 1px hairline runs full width under it. A small mono state tag "SYNC" sits under the hairline, left.
Scene 2 (1.6–3.9s): on "async" (1.58s) the state tag hard-cuts "SYNC" → "ASYNC" (`discrete-text-sequence`). On "forty" (3.88s) the numeral hard-cuts to "40ms" in fire-orange (`discrete-text-sequence`, same slot, same baseline); a single short orange underline stub pulses once under it (finite, no loop).
Scene 3 (3.9–6.9s): on "one line" (5.12s) a mono tag "+1 LINE" drops in to the right of the state tag: a short downward slide plus fade on a smooth power3 long-tail settle (no overshoot). On "four hundred" (6.42s) the numeral hard-cuts back to cream "400ms" on the same hard cut (no glitch effect), and the orange underline stub disappears with it.
Scene 4 (6.9–8.12s): on "Here's why" (7.16s) a mono kicker "WHY?" fades up bottom-left of the stage (above y≈1500); everything holds still.

## Frame 2 — Written normally

- scene: The time-lane stage appears: three lanes, and three waiting bars draw one after another in a staircase, each starting only where the previous ended.
- voiceover: "The handler makes three network calls. Written normally, it waits for each one before starting the next."
- duration: 5.59s
- transition_in: crossfade
- status: outline
- src: compositions/frames/02-written-normally.html
- type: feature_showcase
- persuasion: Demonstration (show the mechanism running) + Signposting (one, then the next)
- beat: Orientation + comprehension
- blueprint: compose (time-lane stage, shared with Frames 3, 5, 6, 7)

narrativeRole: Establishes the stage and the baseline: sequential waits stack end to end, so total time is the sum of the waits.
keyMessage: Sequential code waits for each call before starting the next one.

focal: the three waiting bars in a staircase
roles: three lanes with mono labels "CALL 1" / "CALL 2" / "CALL 3" = supporting · waiting bars (cream-hint 1px outline, faint mono "WAITING" inside) = foreground subject · mono kicker "SEQUENTIAL" = supporting · "TIME →" axis tag = supporting · ground = background
sfx: soft-whoosh

Scene 1 (0.0–1.9s): dark register. Mono kicker "SEQUENTIAL" upper-left (~y 330) with the orange rule stub; "TIME →" mono tag at the stage's top-right. On "three network calls" (0.7–1.3s) the three lanes enter top to bottom via `waterfall-entry` (label + hairline baseline per lane), stacked in the middle band of the frame (~y 560 to ~1250), full width inside pad-x. Lanes are empty.
Scene 2 (1.9–3.2s): on "Written normally" (1.98s) bar 1 self-draws left to right along lane 1 (`stat-bars-and-fills`, scaleX from left), occupying the first third of the lane width.
Scene 3 (3.2–4.4s): on "waits for each one" (3.26s) bar 2 draws along lane 2, starting exactly where bar 1 ended (second third).
Scene 4 (4.4–5.59s): on "starting the next" (4.42s) bar 3 draws along lane 3 in the last third; a thin 1px bracket then draws under all three lanes spanning the full width with a mono tag "ONE AFTER ANOTHER" (`svg-path-draw`) by ~5.1s, then holds still.

## Frame 3 — The waiting overlaps

- scene: Same stage: the three bars slide left to all start at zero and stack on top of each other in time; an orange band marks the shared window where the waiting overlaps.
- voiceover: "With async, it starts all three and waits while they're in flight. The waiting overlaps."
- duration: 5.56s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/03-the-waiting-overlaps.html
- type: feature_showcase
- persuasion: Before/after (same stage, rearranged) + Demonstration
- beat: "Aha"
- blueprint: compose (time-lane stage continues)

narrativeRole: Shows what async actually does: it does not make any call faster, it lets the waits overlap so their durations no longer add up.
keyMessage: Async starts all three and lets the waiting overlap.

focal: the three bars snapping to a common start
roles: waiting bars = foreground subject · overlap band (translucent fire-orange vertical band across all three lanes) = supporting · mono kicker "ASYNC" = supporting · lanes + "TIME →" = supporting · ground = background
sfx: whoosh-soft, click

Scene 1 (0.0–1.3s): opens on the Frame 2 end state rebuilt identically (same lanes, same staircase bars, same geometry), kicker now reads "ASYNC". On "async" (0.53s) the kicker hard-cuts in (`discrete-text-sequence`).
Scene 2 (1.3–3.0s): on "starts all three" (1.47–2.23s) bars 2 and 3 slide left to start at x=0 alongside bar 1 via a `nudge-curve` group slide (slow-fast-slow), so all three bars now occupy the same first third of their lanes. The empty right two-thirds of each lane is suddenly visible.
Scene 3 (3.0–4.5s): on "in flight" (3.57s) each bar's faint "WAITING" label brightens left-to-right (per-word staggered reveal across the three bars, `dynamic-content-sequencing`).
Scene 4 (4.5–5.56s): on "The waiting overlaps" (4.61s) a translucent fire-orange vertical band wipes down across all three lanes over the shared window (`stat-bars-and-fills` fill wipe, top to bottom), and a mono tag "OVERLAP" appears at its foot; the right two-thirds of the lanes stays empty (the saved time, no number). Hold.

## Frame 4 — Concurrency

- scene: Orange declaration frame: the word "concurrency" lands as the one display moment, with a mono definition tag building beneath it.
- voiceover: "That's concurrency: one worker juggling many tasks that are mostly waiting."
- duration: 3.93s
- transition_in: crossfade
- status: outline
- src: compositions/frames/04-concurrency.html
- type: product_intro
- persuasion: Coined term + Distillation
- beat: Clarity
- blueprint: kinetic-type-beats (Reproduce)

narrativeRole: Names the idea the viewer just watched, so the rest of the film can contrast it.
keyMessage: Concurrency is one worker juggling tasks that are mostly waiting.

focal: the word "concurrency"
roles: "concurrency" display word (ink on orange) = foreground subject · three-part mono tag stack "1 WORKER" / "MANY TASKS" / "MOSTLY WAITING" = supporting · fire-orange ground = background
sfx: impact-soft

Scene 1 (0.0–1.2s): orange register, chrome suppressed. On "concurrency" (0.51s) the word "concurrency" enters via `waterfall-entry` (letters whip up in a fast cascade), Barlow 900 lowercase ink, left-anchored, ~88% of the content width, around y≈700. A 36×2 ink rule stub sits above it with the mono kicker "THAT'S" in 55% ink.
Scene 2 (1.2–3.4s): under the word, three mono tags stack one per line, each landing on its spoken cue via per-word staggered reveal (`dynamic-content-sequencing`): "1 WORKER" on "one worker" (1.23s), "MANY TASKS" on "many tasks" (1.99s), "MOSTLY WAITING" on "mostly waiting" (3.01s). Tags are ink at 75%, the last one full ink.
Scene 3 (3.4–3.93s): held breather. Everything still.

## Frame 5 — Pure computation

- scene: Back on the lane stage: a fourth lane "RESIZE IMAGE" appears and fills with a solid fire-orange block; its label hard-cuts from "WAITING?" to "COMPUTING".
- voiceover: "Now you add a function that resizes an image. That's not waiting, that's pure computation."
- duration: 4.97s
- transition_in: cut
- status: outline
- src: compositions/frames/05-pure-computation.html
- type: pain_point
- persuasion: Contrast (waiting vs computing) + Counterexample
- beat: Unease
- blueprint: compose (time-lane stage continues)

narrativeRole: Introduces the one line from the hook and shows it is a different kind of work: the CPU is busy, not idle.
keyMessage: Resizing an image is computation, not waiting.

focal: the solid fire-orange compute block
roles: three overlapped waiting bars (dimmed to ~40%) = supporting · new lane "RESIZE IMAGE" + solid orange block = foreground subject · mono state tag on the block = supporting · lanes + "TIME →" = supporting · ground = background
sfx: impact-soft, glitch-short

Scene 1 (0.0–1.6s): the Frame 3 end state rebuilt identically (three overlapped outline bars, overlap band removed), dimmed to ~40% via `depth-of-field-blur` (slight blur + dim) on "Now you add" (0.2s). Kicker "+1 LINE" upper-left.
Scene 2 (1.6–2.9s): on "resizes an image" (1.6s) a fourth lane with mono label "RESIZE IMAGE" appears below the three via `waterfall-entry`, and a SOLID fire-orange block self-draws along it (`stat-bars-and-fills`, scaleX from left), wider than the waiting bars (~half the lane).
Scene 3 (2.9–4.2s): on "not waiting" (3.26s) a mono tag on the block reads "WAITING?" in ink, then on "pure computation" (4.14s) it hard-cuts to "COMPUTING" (`discrete-text-sequence`). A mono "CPU" tag appears at the lane's left.
Scene 4 (4.2–4.97s): hold; the orange block is the one lit thing on screen.

## Frame 6 — Stuck behind it

- scene: A single thread rail labeled "EVENT LOOP · 1 THREAD"; the orange resize block occupies it while request tiles arrive from the left and pile up in a growing queue behind it, frozen.
- voiceover: "An async event loop runs on a single thread, so while it's resizing, nothing else can move. Every other request on that server is stuck behind it."
- duration: 8.73s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/06-stuck-behind-it.html
- type: pain_point
- persuasion: Causal chain (single thread → block → everyone waits) + Concretization
- beat: Tension + recognition
- blueprint: compose (time-lane stage, collapsed to one lane)

narrativeRole: Explains why one CPU-heavy line undoes the whole win: async shares one thread, so blocking it freezes every request on the server.
keyMessage: On a single-threaded event loop, one computation blocks every other request.

focal: the queue of stuck request tiles piling up behind the orange block
roles: single thread rail (thicker hairline lane) = supporting · orange "RESIZE" block on the rail = foreground subject · request tiles (small cream-hint outlined squares, mono "REQ") = foreground subject · mono kicker "EVENT LOOP" + tag "1 THREAD" = supporting · ground = background
sfx: soft-whoosh, click-off

Scene 1 (0.0–2.6s): dark register. On "event loop" (0.81s) mono kicker "EVENT LOOP" upper-left with orange rule stub; on "single thread" (1.87s) a single horizontal thread rail draws across the full stage width at ~y 820 (`svg-path-draw`) and a mono tag "1 THREAD" lands at its left end. Three small request tiles glide along the rail left to right (finite tweens) showing normal flow.
Scene 2 (2.6–4.9s): on "while it's resizing" (3.17s) the solid orange "RESIZE" block drops onto the rail center (`spring-pop-entrance`, smooth long-tail). On "nothing else can move" (4.15s) the moving tiles stop dead in place (hard stop, no ease) and dim slightly.
Scene 3 (4.9–8.0s): on "Every other request" (5.75s) new request tiles arrive from the left edge and stack up behind the block in a growing queue (a staggered `waterfall-entry` cascade, rows building upward above and below the rail within the stage band y≈500 to ≈1250), cued across "on that server" to "stuck" (5.75s to 7.81s): ~12 tiles in total, each arrival index-staggered.
Scene 4 (8.0–8.73s): on "stuck behind it" (7.81s) a mono tag "STUCK" appears over the queue in fire-orange; everything holds still.

## Frame 7 — Parallelism

- scene: Four core lanes "CORE 1" to "CORE 4" each fill with an orange compute block at the same instant; then three mono bullets name the ways to get there.
- voiceover: "Running work at the same instant needs parallelism: multiple CPU cores working at once. That means a worker pool, separate processes, or a background queue."
- duration: 9.32s
- transition_in: crossfade
- status: outline
- src: compositions/frames/07-parallelism.html
- type: feature_showcase
- persuasion: Contrast (one lane vs many) + Rule of three
- beat: Resolve + comprehension
- blueprint: grid-card-assemble (Adapt)

narrativeRole: Gives the correct tool for CPU work: more cores computing simultaneously, and names the three practical forms.
keyMessage: CPU work needs parallelism: multiple cores, via a worker pool, separate processes, or a background queue.

Adapt: keep the staggered self-assembling list signature for the three options; the upper half is the lane stage with four core lanes.
focal: four orange compute blocks filling simultaneously
roles: "parallelism" h1 word (cream, Barlow 900 lowercase) = supporting headline · four core lanes + orange blocks = foreground subject · three `/` bullets = supporting · ground = background
sfx: rising-whoosh, tick

Scene 1 (0.0–2.9s): dark register. On "parallelism" (2.06s) the word "parallelism" lands upper-left (~y 300) via `waterfall-entry`, Barlow 900 lowercase cream, ~80% width. Before that (0.16–2.0s, "Running work at the same instant") the four lanes "CORE 1" to "CORE 4" enter top to bottom via `waterfall-entry` in the stage band (~y 480 to ~960), empty.
Scene 2 (2.9–5.4s): on "multiple CPU cores" (3.02–3.74s) all four solid orange blocks self-draw along their lanes at the same moment (`stat-bars-and-fills`, identical start and duration, all four bars as ONE beat), finishing on "at once" (4.62s). A mono tag "AT ONCE" lands at the stage's right edge.
Scene 3 (5.4–9.32s): below the stage (~y 1080 to ~1480) three bullets with the orange mono `/` marker assemble one per spoken cue (`grid-card-assemble` cascade, each bullet Barlow lead weight, lowercase): "worker pool" on "worker pool" (6.16s), "separate processes" on "separate processes" (7.0s), "background queue" on "background queue" (8.48s). Hold after the third.

## Frame 8 — The rule

- scene: A stacked compare panel: top dark panel "waiting → async", bottom fire-orange panel "computing → parallelism", each revealed on its line.
- voiceover: "So the rule is simple. Async helps when your code is waiting on something. Parallelism helps when your code is computing something."
- duration: 6.93s
- transition_in: cut
- status: outline
- src: compositions/frames/08-the-rule.html
- type: branding
- persuasion: Distillation + Comparison of two options
- beat: Clarity + satisfaction
- blueprint: comparison-split (Adapt)

narrativeRole: Compresses the whole video into one savable rule that maps a kind of work to a tool.
keyMessage: Waiting → async. Computing → parallelism.

Adapt: portrait, so the two paired items stack (dark over orange, per frame.md compare-panel) instead of entering from side wings; keep the paired-equal-weight reveal and the punctuating badge per panel.
focal: the two-panel rule
roles: top dark panel (mono label "WAITING" + h1 "async" cream) = foreground subject · bottom orange panel (mono label "COMPUTING" + h1 "parallelism" ink) = foreground subject · mono kicker "THE RULE" = supporting · 1px divider = supporting · ground = background
sfx: click, impact-soft

Scene 1 (0.0–1.0s): dark register, chrome suppressed. On "the rule" (0.5s) mono kicker "THE RULE" with the orange rule stub lands upper-left (~y 250).
Scene 2 (1.0–4.0s): the top panel (y≈340 to ≈900) reveals: on "Async" (1.04s) the word "async" slides up into place (`waterfall-entry`), Barlow 900 lowercase cream; on "waiting on something" (2.6s) its mono badge "WHEN WAITING" pops in beside it (`spring-pop-entrance`, smooth settle).
Scene 3 (4.0–6.3s): a 1px divider draws across (`svg-path-draw`), then the bottom panel (y≈920 to ≈1480) fills fire-orange via a top-to-bottom wipe on "Parallelism" (4.08s) (`stat-bars-and-fills` fill); "parallelism" lands in ink Barlow 900 lowercase; on "computing something" (5.9s) its mono badge "WHEN COMPUTING" pops in (ink on orange).
Scene 4 (6.3–6.93s): held read, both panels still.

## Frame 9 — Slower, not faster

- scene: Statement frame: "slower," in fire-orange stacked over "not faster." in cream, landing word by word.
- voiceover: "Mix them up, and async makes things slower, not faster."
- duration: 2.81s
- transition_in: cut
- status: outline
- src: compositions/frames/09-slower-not-faster.html
- type: benefit_highlight
- persuasion: Callback (to the hook's 400ms) + Distillation
- beat: Inevitability
- blueprint: kinetic-type-beats (Reproduce)

narrativeRole: Lands the cost of the mistake as a single blunt line, closing the loop opened by the hook.
keyMessage: Using async for CPU work makes things slower, not faster.

focal: the word "slower,"
roles: "slower," (fire-orange display) = foreground subject · "not faster." (cream h1) = supporting · mono kicker "MIX THEM UP" = supporting · ground = background
sfx: impact-soft

Scene 1 (0.0–1.7s): dark register, chrome suppressed. On "Mix them up" (0.19s) a mono kicker "MIX THEM UP" lands upper-left (~y 520) with the orange rule stub.
Scene 2 (1.7–2.3s): on "slower" (1.75s) "slower," slams in via `kinetic-beat-slam` (scale-slam, smooth settle, no overshoot), Barlow 900 lowercase fire-orange, ~85% width, around y≈760.
Scene 3 (2.3–2.81s): on "not faster" (2.23s) "not faster." lands under it in cream via a hard cut (`discrete-text-sequence`) and holds dead still.

## Frame 10 — Comment guide

- scene: Orange CTA frame: mono kicker "COMMENT", the word "guide" as the one display moment, and a short lead line beneath.
- voiceover: "Comment guide and I'll send you the full breakdown."
- duration: 3.179s
- transition_in: crossfade
- status: outline
- src: compositions/frames/10-comment-guide.html
- type: cta
- persuasion: Direct address + a single low-friction ask
- beat: Resolve
- blueprint: titlecard-reveal (Adapt)

narrativeRole: Turns the explanation into one action: comment the keyword to get the full breakdown.
keyMessage: Comment "guide" to get the full breakdown.

Adapt: one restrained reveal then a still hold; the kicker leads, the keyword is the card.
focal: the word "guide"
roles: "guide" display word (ink on orange) = foreground subject · mono kicker "COMMENT" = supporting · lead line "the full breakdown" = supporting · fire-orange ground = background
sfx: click

Scene 1 (0.0–0.8s): orange register. On "Comment" (0.0s) mono kicker "COMMENT" + ink rule stub lands upper-left (~y 560) in 55% ink.
Scene 2 (0.8–2.4s): on "guide" (0.76s) the word "guide" rises in via a slide-up settle (`waterfall-entry`), Barlow 900 lowercase ink, near full-bleed (~80% width), around y≈806. On "full breakdown" (2.22s) a Barlow lead line "the full breakdown" lands beneath in 75% ink.
Scene 3 (2.4–3.179s): hold; in the final ~0.3s the whole card settles with a gentle fade to ~85% (final-frame exit only).
