---
format: 1080x1920
duration: 41s
message: "A cache expiring under load doesn't just miss once — it lets every waiting request stampede the database at the same instant."
arc: concept-explainer with process — hook → name the concept → problem mechanism (expiry → stampede → overload) → the fix (coalescing/lock) → land the term
audience: backend / infra engineers who've shipped a cache but never hit this failure mode
mode: autonomous
music: none
---

## Video direction

- **Palette** — from `frame.md` (cobalt-grid): cream paper ground, cobalt ink is the ONLY ink — headlines, diagrams, rules, grid, chrome. Never a second hue. Hierarchy comes from size (Newsreader ramp) and Hanken→Newsreader switches, never color.
- **Motion grammar** — `power3` long-tail settles everywhere; no bounce/overshoot. Reveals are paced to the VO's spoken cues per frame (never front-loaded); each frame's Scene 1 shows only what the line says at t=0. Internal seams (a HIT→MISS flip, a hard word-swap) are velocity-matched cuts per `cut-catalog.md`, not slideshow cuts.
- **Continuous stages** — three shared diagrams carry the body so the film reads as one system, not eight slides: the **cache-node stage** (Frames 3–5: the HIT/MISS node + request-dot ring + database icon), the **gate stage** (Frames 6–7: the turnstile + queue, resolving back onto a callback to the Frame 3 cache node), and standalone type-led beats bookending it (Frames 1–2 open, Frame 8 closes).
- **Rhythm / held beats** — Frame 2 (2.1s) and Frame 8 (5.3s) are the deliberate breathers: settle fast, then hold still — no continuing motion. Frames 3–7 carry the sequential-build energy. Every frame's final ~1–1.5s is a genuine hold (subtle jitter at most), never a mid-video exit.
- **Negative list** — no second ink color; no drop shadow or rounded corner (cobalt-grid is 0-radius, flat); no bouncy easing; no lazy breathing/circular pulse; no back-half pan or push; no floating bokeh / purple-blue AI-gradient cliché; no infinite/looping motion (finite tweens only).
- **Caption-band keep-out** — canvas is 1080×1920; bottom ~17% (≈327px) stays clear for the caption pill. Centered heroes anchor at y≈806, not the true midpoint.

## Frame 1 — The question

- scene: Cold open on a single glowing cache node; as the line lands, "10,000" explodes into a hero numeral pushed toward camera, tiny request dots flinging outward to their marks.
- voiceover: "Ever wonder what happens when your cache entry expires at the exact same moment 10,000 requests hit your server?"
- duration: 6.656s
- transition_in: cut
- status: animated
- src: compositions/frames/01-the-question.html
- type: hook
- persuasion: Rhetorical question + Anchoring on a familiar referent (a cache entry expiring)
- beat: Curiosity + tension
- blueprint: dataviz-countup

narrativeRole: Opens the cognitive gap — a scenario every backend engineer half-recognizes but hasn't fully thought through.
keyMessage: A cache expiring at the wrong instant is a bigger problem than it sounds.

Adapt: portrait single-stage push-through (no scroll); keep the count-up-burst signature.
focal: the "10,000" hero numeral
roles: cache-entry node = supporting (Scene 1–2 only) · "10,000" numeral = foreground subject · request-dot ring = supporting · grid/hairlines = background
sfx: tick, soft-whoosh

Scene 1 (0.0–2.5s): centered, a single cobalt-outlined square node labeled "CACHE ENTRY" (Hanken micro-label) sits mid-frame (y≈806) on the paper+grid ground; as the VO opens, a thin cobalt ring around the node drains via a self-draw wipe (`svg-path-draw`), synced to "cache entry expires."
Scene 2 (2.5–4.3s): on "the exact same moment," the ring hits zero and the node's fill hard-cuts to empty (`discrete-text-sequence`-style instant swap, no tween); it holds small as supporting context.
Scene 3 (4.3–6.656s): on "10,000 requests hit your server," the numeral "10,000" bursts in dead-center via a **value-scaled counter** (`counting-dynamic-scale`), Newsreader display-hero weight, growing to ~55% of frame width; a ring of small hollow request-dot glyphs flings outward from center to its marks (`center-outward-expansion`), landing and holding (subtle jitter only, `sine-wave-loop`) as the line ends.

## Frame 2 — Naming it

- scene: The hero numeral clears; one Newsreader headline lockup types/settles center frame: "The Thundering Herd Problem."
- voiceover: "That's the thundering herd problem."
- duration: 2.133s
- transition_in: cut
- status: animated
- src: compositions/frames/02-naming-it.html
- type: product_intro
- persuasion: Coined term / mnemonic
- beat: Recognition + orientation
- blueprint: kinetic-type-beats

narrativeRole: Gives the scenario a name — the "protagonist" of the explanation, so every following frame can refer back to it.
keyMessage: This failure mode has a name: the thundering herd problem.

Reproduce — held/breather beat, no adaptation needed.
focal: "Thundering Herd Problem." headline lockup
roles: kicker label = supporting · headline = foreground subject · grid = background
sfx: none

Scene 1 (0.0–0.9s): numeral clears on the hard `cut`; a Hanken uppercase kicker "THAT'S CALLED THE" fades up small, upper-third, as the VO says "That's the."
Scene 2 (0.9–2.133s): on "thundering herd," the headline "Thundering Herd" assembles via **per-word staggered reveal** (`dynamic-content-sequencing`), Newsreader display-chapter weight, centered at y≈806; "Problem." lands a beat after as a smaller trailing line via **hard-cut word-swap** (`discrete-text-sequence`), then holds fully still — the deliberate breather, no further motion.

## Frame 3 — The trigger

- scene: Establishes the recurring system-diagram stage: a central cache-key node flips from a solid "HIT" tile to an empty "MISS" tile; the ring of request dots around it flicker from filled to hollow, one by one.
- voiceover: "One cache key expires — every request that needed that data suddenly finds it missing, all at once."
- duration: 6.571s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-the-trigger.html
- type: pain_point
- persuasion: Causal chain (A → B)
- beat: Concern + tension building

narrativeRole: Shows the mechanism's first domino — one expiry event turns into many simultaneous misses.
keyMessage: A single expiring key means every dependent request loses its cache hit at the same instant.

blueprint: compose (cache-node stage, shared with Frames 4–5)
focal: the central cache node (HIT → MISS)
roles: cache node = foreground subject · request-dot ring = supporting · "CACHE KEY" label = supporting · grid = background
sfx: soft-glitch, click-off

Scene 1 (0.0–1.44s): establishes the stage — a single cobalt-outlined square node, centered upper-middle (y≈806), solid-filled, labeled "HIT" (mono-tag); a ring of 12 small hollow-square request glyphs enters once via **cluster→outward expansion** (`center-outward-expansion`) and settles at rest around it, calm, as the VO opens on "One cache key." A Hanken uppercase label "CACHE KEY" sits beneath.
Scene 2 (1.44–3.36s): as the VO says "expires… every request that needed that data," the node's fill drains in a **bars/fill wipe** (`stat-bars-and-fills`) and its label hard-cuts "HIT" → "MISS" (`discrete-text-sequence`); the ring dots nearest the node flip hollow one at a time, sequenced to "every… request… that… needed… that… data" (per-word staggered reveal).
Scene 3 (3.78–6.571s): on "suddenly find it missing, all at once," the remaining ring dots flip hollow together in one **kinetic beat-slam** (`kinetic-beat-slam`) rather than sequentially — landing "all at once" as a single visual beat — then holds still, ring fully hollow, node reading "MISS."

## Frame 4 — The stampede

- scene: Same diagram stage continues: the ring of request dots (now all hollow) breaks formation and streams as one dense flock toward a database icon at the frame's base; "10,000" ticks up beside the flock as it travels.
- voiceover: "So all 10,000 requests go straight to the database to recompute the same value —"
- duration: 5.12s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/04-the-stampede.html
- type: pain_point
- persuasion: Demonstration (show the mechanism running)
- beat: Escalating urgency

narrativeRole: Makes the "herd" concrete and visible — thousands of identical requests converging on one resource at once.
keyMessage: Every one of those requests recomputes the exact same value, redundantly, at the same time.

blueprint: compose (cache-node stage continues)
focal: the converging request flock
roles: database icon = foreground subject (destination) · request flock = foreground subject (in motion) · "10,000" tick counter = supporting · grid = background
sfx: rising-whoosh, impact-soft

Scene 1 (0.0–1.3s): opens exactly where Frame 3 held — the hollow ring around the emptied "MISS" node; as the VO says "So all 10,000," the ring dots begin breaking formation.
Scene 2 (1.3–2.8s): a cobalt-outlined square database icon (mono-tag "DATABASE") enters at the lower third via a **spring-pop entrance** (`spring-pop-entrance`, smooth long-tail, no bounce) as the VO says "requests go straight to"; the ring streams toward it as one dense flock (reverse `center-outward-expansion` — a convergence), with **motion-blur streak** (`motion-blur-streak`) on the lead dots for velocity.
Scene 3 (2.8–5.12s): on "the database to recompute the same value," the flock arrives and clusters tightly atop the icon; a small "10,000" mono-tag **value-scaled counter** (`counting-dynamic-scale`, modest size — supporting, not hero) ticks up beside the cluster, then holds, jittering subtly in place (`sine-wave-loop`, low amplitude).

## Frame 5 — The overload

- scene: Mirrored book-open contrast: left panel "A SECOND AGO" shows the database icon calm with a thin, low pixel-stack load bar; right panel "RIGHT NOW" shows the same icon straining under a maxed-out pixel-stack bar and the "10,000" numeral stamped beside it.
- voiceover: "Your database, which was handling light load a second ago, just got hit with 10,000 queries at the same time."
- duration: 6.997s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/05-the-overload.html
- type: social_proof
- persuasion: Before/after contrast
- beat: Alarm — the consequence lands

narrativeRole: Grounds the abstract "stampede" in a concrete before/after so the reader feels the scale of the spike.
keyMessage: The same database went from idle to slammed in an instant, with zero ramp-up.

blueprint: comparison-split (Adapt — portrait stacks top/bottom instead of side-by-side)
focal: the bottom "RIGHT NOW" pixel-stack-bar (maxed load)
roles: top band "A SECOND AGO" = supporting/context · bottom band "RIGHT NOW" = foreground subject · divider hairline = supporting · grid = background
sfx: soft alarm-tick on the bottom fill

Scene 1 (0.0–2.92s): stage cut carries the database icon forward, now small and calm in a top band labeled "A SECOND AGO" (Hanken uppercase kicker) above a mostly-empty pixel-stack-bar row (1–2 cells lit); the band builds via **per-word staggered reveal** timed to "your database… was handling light load a second ago" — bottom half of frame stays empty.
Scene 2 (3.44–5.0s): as the VO hits "just got hit with 10,000," a hairline divider **self-draws** (`svg-path-draw`) across the vertical middle, and a bottom band "RIGHT NOW" enters with a mirrored book-open tilt (`split-tilt-cards`, the comparison-split signature move) — its pixel-stack-bar row primed empty.
Scene 3 (5.0–6.997s): on "queries at the same time," the bottom pixel-stack-bar row fills almost to the top in a fast sweep (`stat-bars-and-fills`) and a "10,000" mono-tag stamps in beside it on a hard cut (no roll); holds still on the stark top/bottom contrast.

## Frame 6 — The fix

- scene: New stage: a single gate/turnstile diagram. One request dot approaches the gate and passes through, lighting it green; behind it, other dots queue and freeze in place mid-approach.
- voiceover: "The fix is simple — only one request is allowed to recompute the value,"
- duration: 4.352s
- transition_in: crossfade
- status: animated
- src: compositions/frames/06-the-fix.html
- type: feature_showcase
- persuasion: Signposting ("the fix is simple") + Frame-then-fill
- beat: Relief + clarity — the pivot

narrativeRole: Introduces the solution mechanism's first rule, mirroring the "one key, many requests" shape of the problem it resolves.
keyMessage: Only one request is ever allowed through to do the expensive recompute.

blueprint: compose (gate stage, shared with Frame 7)
focal: the single dot passing the gate
roles: gate glyph = foreground subject · passing dot = foreground subject · queued dots = supporting · grid = background
sfx: click-through, soft-lock

Scene 1 (0.0–0.82s): crossfade to a fresh, sparse stage (~55% empty) — a single cobalt gate glyph (two parallel hairlines with a gap) centered upper-middle; a Hanken kicker "THE FIX IS SIMPLE" types on with a caret (`discrete-text-sequence` + `context-sensitive-cursor`) as the VO says it.
Scene 2 (1.36–2.62s): as the VO says "only one request is allowed," one small square request-dot approaches the gate from below (`motion-blur-streak`, moderate speed) and passes through — the gate flashes cobalt-solid on contact via a **button press** (`press-release-spring`, no bounce).
Scene 3 (2.62–4.352s): on "to recompute the value," the passed dot continues upward and holds just above the gate with a bounded glow (`ambient-glow-bloom`); several other dots enter from below and freeze mid-approach beneath the now-closed gate, each landing dead-still on its own beat (per-word staggered reveal, no bounce). Holds.

## Frame 7 — The payoff

- scene: Same gate stage: the lead dot reaches the cache node and refills it (MISS tile flips back to HIT); the queued dots release in sequence, each one grazing the now-full cache node instead of the gate.
- voiceover: "Every other request waits for that result, then reads it from cache."
- duration: 3.584s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/07-the-payoff.html
- type: feature_showcase
- persuasion: Progressive disclosure ("waits… then reads")
- beat: Comprehension + confidence

narrativeRole: Closes the solution's loop — shows where the waiting requests' value actually comes from.
keyMessage: The queued requests never touch the database — they all read the one fresh value from cache.

blueprint: compose (gate stage continues; callback to the Frame 3 cache node)
focal: the refilled cache node (callback to Frame 3)
roles: cache node = foreground subject · queued/releasing dots = foreground subject (in motion) · gate glyph = supporting (recedes) · grid = background
sfx: soft-chime, whoosh-light

Scene 1 (0.0–1.28s): opens exactly where Frame 6 held — queued dots frozen beneath the gate, the passed dot glowing above; as the VO says "every other request waits," the queued dots pulse once in unison (a single beat, not a loop), timed to "waits."
Scene 2 (1.28–2.6s): as the VO says "for that result," the glowing dot travels up to a small cache-node glyph (reusing Frame 3's node shape, now solid — a deliberate visual callback) and merges into it via **scale-swap** (`scale-swap-transition`), the label hard-cutting "MISS" → "HIT."
Scene 3 (2.6–3.584s): on "then reads it from cache," the queued dots release one at a time — staggered, not simultaneous — and travel directly to the refilled node, bypassing the gate; each settles into a small cluster beside it; holds still on the resolved cluster.

## Frame 8 — The term

- scene: Calm landing card: two stacked labels settle center frame — "REQUEST COALESCING" over a thin cobalt rule, "DISTRIBUTED LOCK" beneath it — on an open, mostly-empty grid.
- voiceover: "This is usually called request coalescing, or a distributed lock around the recompute step."
- duration: 5.205s
- transition_in: crossfade
- status: animated
- src: compositions/frames/08-the-term.html
- type: branding
- persuasion: Distillation (compress the mechanism to its two names)
- beat: Resolution — "now I get it"
- blueprint: titlecard-reveal

narrativeRole: Lands the generalizable principle under its real engineering names, so the viewer can look it up.
keyMessage: The pattern that fixes this has a name — request coalescing, or a distributed lock around the recompute.

focal: the "REQUEST COALESCING" / "DISTRIBUTED LOCK" stacked lockup
roles: "REQUEST COALESCING" label = foreground subject · "DISTRIBUTED LOCK" label = foreground subject · connecting rule = supporting · grid = background
sfx: none

Scene 1 (0.0–1.88s): crossfade to a calm, ~55%-empty stage; as the VO says "This is usually called request," "REQUEST COALESCING" assembles via **per-word staggered reveal**, Newsreader row-headline weight, upper-center, with a thin cobalt rule self-drawing beneath it (`svg-path-draw`) as "coalescing" completes.
Scene 2 (1.88–3.68s): as the VO says "or a distributed lock," "DISTRIBUTED LOCK" slides up into place beneath the rule (`titlecard-reveal`'s slide-up-crossfade signature move).
Scene 3 (3.68–5.205s): on "around the recompute step," both labels hold fully settled; page-chrome ticks in quietly at the corner (framework furniture). Final hold of the video — subtle jitter only (`sine-wave-loop`, low amplitude), no further motion.
