---
format: 1080x1920
duration: 73s
message: "Replication, partitioning, and sharding get suggested interchangeably as ways to 'scale the database' — they're not substitutes, each solves a different problem."
arc: listicle (rule-of-three: replication → partitioning → sharding) with synthesis contrast + practical guidance close
audience: backend / infra engineers who've reached for "scale the database" without knowing which lever actually fixes their problem
mode: autonomous
music: none
---

## Video direction

- **Palette** — from `frame.md` (Signal Path): void-black canvas (`canvas` #0A0D12), raised panels (`canvas-raised`/`canvas-raised-2`) for any card surface, `ink`/`ink-dim`/`ink-faint` for text. The pack's three signal colors are **re-mapped for this video's three concepts** (frame.md's own "composition is free" clause — the atoms are the palette + hairline + type system, not the specific proxy/LB/gateway edge semantics from the sibling video that pack was authored for): **amber (`accent`) = Replication** (broadcast/duplicate), **teal (`accent-2`) = Partitioning** (divide-in-place), **violet (`accent-3`) = Sharding** (distribute-across-servers). `danger` (rose) is reserved for a failure-mode beat only (a node dying / overflowing) — never a fourth concept color.
- **Typography** — Fraunces sentence-case display for every hook word, thesis line, and stamp; IBM Plex Sans for any reading sub-line; IBM Plex Mono uppercase for node-tags, index ticks, and diagram chrome — exactly frame.md's two-voice system.
- **The shared DATA stage** — Frames 2-4 reuse the SAME node-box diagram grammar so the video reads as one evolving schematic, not three disconnected slides: Frame 2 (replication) shows one `DATA` node duplicating into identical amber-bordered copies; Frame 3 (partitioning) shows a fresh `DATA` node fracturing into smaller teal-bordered chunks (never duplicating); Frame 4 (sharding) shows those same chunks migrating onto separate violet-bordered server boxes. Frame 5 recalls the stage in a two-band contrast; Frame 6 recaps all three as tiny triptych glyphs.
- **Motion grammar** — `power3` long-tail settles everywhere; no bounce/overshoot. Reveals are paced to the VO's spoken cues per frame — never front-loaded. Internal seams (a fill drain, a hard label swap) are velocity-matched cuts, not slideshow cuts.
- **Rhythm / held beats** — Frame 6 (2.63s) is the deliberate breather: the thesis lands, then holds fully still — no continuing motion. Frame 8 closes on a calm, settled hold. Frames 2-4 and 7 carry the sequential-build energy; each still ends its own window on a genuine hold before the transition.
- **Transitions** — `cut` (Frame 1 placeholder, and the two sharp landings: Frame 6's punchline, Frame 8's CTA), `crossfade` (topic pivots: hook→body at Frame 2, body→synthesis at Frame 5, synthesis→guidance at Frame 7), `push-slide LEFT` (the parallel rule-of-three items: Frame 3, Frame 4 — same seam repeated so the three concepts read as co-equal, swept items).
- **Negative list** — no second ink color beyond the three fixed signal roles (+ rare `danger`); no drop shadow, no gradient fill, no rounded corners beyond the pack's 4px/8px; no bouncy easing; no lazy breathing/circular pulse; no back-half pan or push; no floating bokeh / purple-blue AI-gradient cliché; no infinite/looping motion (finite tweens only).
- **Caption-band keep-out** — canvas is 1080×1920; bottom ~250px (y > 1670) stays clear for the caption pill, top ~150px stays clear of load-bearing content. Centered heroes anchor at y≈806, not the true midpoint.

## Frame 1 — The denial

- scene: Three terms hard-cut-flash center frame — REPLICATION (amber) → SHARDING (violet) → PARTITIONING (teal) — then get bracketed as equals and struck through on "They don't."
- voiceover: "Replication, sharding, partitioning. Say we need to scale the database and someone will suggest all three like they solve the same problem. They don't."
- duration: 8.533s
- transition_in: cut
- status: animated
- src: compositions/frames/01-the-denial.html
- type: hook
- persuasion: Counterintuitive claim + Rule of three
- beat: Skepticism + curiosity
- blueprint: kinetic-type-beats (Adapt)

narrativeRole: Opens the cognitive gap the growth analysis flags as this account's best-performing shape (a contrarian "these aren't the same" claim) — names all three terms as if interchangeable, then flatly denies it, framing the whole video as the correction.
keyMessage: Replication, partitioning, and sharding get suggested interchangeably — but they solve different problems.

Adapt: the blueprint's in-place word-swap becomes three sequential term flashes, each briefly tinted its own signal color (a preview of the thesis before it's explained) — no logo, no product.
focal: the three term-flashes, then "THEY DON'T."
roles: term flashes = foreground subject (sequential) · underline tick = supporting accent · hairline grid = background
sfx: soft-glitch, hard-click

Scene 1 (0.0–2.46s): void-black stage + faint hairline grid; as the VO names each term, "REPLICATION" (Fraunces h1, amber underline tick) hard-cuts to "SHARDING" (violet tick) hard-cuts to "PARTITIONING" (teal tick) — three centered term flashes, one per word, dead-center at y≈806.
Scene 2 (2.46–5.0s): terms clear to empty stage; as the VO says "Say we need to scale the database and someone will suggest," a smaller IBM Plex Sans line assembles beneath center via per-word staggered reveal: "scale the database?"
Scene 3 (5.0–6.9s): on "all three like they solve the same problem," the three term-words return as small mono chips (one each in amber/teal/violet) and align in a single row, bracketed together — frame-then-fill, presenting them as if equal.
Scene 4 (6.9–8.5s): on "They don't," a single decisive strike-through draws across the three chips in `danger` rose (fast self-draw) as "THEY DON'T." stamps below in Fraunces display weight on a hard cut; holds fully still into the cut to Frame 2.

## Frame 2 — Replication

- scene: A single "DATA" node duplicates into two identical amber-bordered copies; one fails and the reads still get served from the other two.
- voiceover: "Replication copies your entire dataset onto multiple servers. Every replica has the same data. It's for availability and read scale — if one node dies, another has everything, and you can spread reads across all of them."
- duration: 12.117s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-replication.html
- type: product_intro
- persuasion: Concretization (broadcast copy) + Frame-then-fill
- beat: Clarity + orientation
- blueprint: compose (opens the shared DATA-stage sequence carried through Frames 2-4)

narrativeRole: Establishes the shared DATA stage and shows replication's mechanism — one dataset becomes many identical copies — then grounds why that copying exists (availability + read scale).
keyMessage: Replication makes full copies of the same data so a node dying, or too many reads, doesn't take the system down.

focal: the central "DATA" node duplicating into 3 identical copies (amber edges)
roles: central DATA node = foreground subject (origin) · 2 duplicate node-boxes = foreground subject (result) · amber broadcast edges = supporting signature · "AVAILABILITY" mono label = supporting · hairline grid = background
sfx: soft-whoosh, tick

Scene 1 (0.0–1.24s): void-black stage; a single node-box labeled "DATA" (IBM Plex Mono node-tag) sits centered upper-middle (y≈806) as the VO opens on "Replication copies your entire dataset."
Scene 2 (1.24–2.88s): on "onto multiple servers," two amber edges self-draw branching from the DATA node to two new empty node-boxes flanking it below; as they complete on "servers," the two new boxes fill solid and hard-cut their label to "DATA" too — three identical filled nodes now sit in a row, all amber-bordered.
Scene 3 (2.88–5.2s): on "Every replica has the same data," the three node-boxes pulse once in unison — a single synchronized beat timed to the clause, not a loop — asserting their sameness.
Scene 4 (5.2–8.46s): on "It's for availability and read scale — if one node dies," the left node-box's fill drains to hollow (a brief `danger`-rose flicker, failure state) while a small mono label "AVAILABILITY" types on above the row.
Scene 5 (8.46–12.07s): on "another has everything, and you can spread reads across all of them," a thin amber line connects the two surviving nodes and small hollow-square read-dots fan out evenly from above onto the remaining nodes; holds still on the row — one hollow, two solid, all connected.

## Frame 3 — Partitioning

- scene: The same DATA node (now teal) fractures in place into smaller labeled chunk-tiles — it divides, it never copies.
- voiceover: "Partitioning does the opposite. Instead of copying everything everywhere, you split your data into smaller chunks — by date range, by customer ID, whatever — so no single piece gets too big to manage. It doesn't add copies, it divides the original."
- duration: 13.312s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/03-partitioning.html
- type: feature_showcase
- persuasion: Contrast (does the opposite) + Concretization
- beat: Comprehension + a small "aha"
- blueprint: compose (DATA stage continues)

narrativeRole: Shows partitioning as replication's structural opposite — the same stage now divides instead of duplicates.
keyMessage: Partitioning splits one dataset into smaller chunks so no single piece is unmanageably large — it divides, it never copies.

focal: the single DATA node fracturing into smaller labeled chunk-tiles (teal edges)
roles: DATA node = foreground subject (origin) · chunk tiles (date-range / customer-ID) = foreground subject (result) · teal divide-edges = supporting signature · "DIVIDES, NEVER COPIES" mono stamp = supporting · hairline grid = background
sfx: soft-glitch, click-off

Scene 1 (0.0–1.41s): stage cut carries forward — a fresh single "DATA" node-box, now teal-bordered, centered upper-middle; VO opens "Partitioning does the opposite."
Scene 2 (1.41–4.87s): on "Instead of copying everything everywhere, you split your data," the node-box cracks along two internal teal hairlines (self-draw) — no new boxes appear, it fractures in place.
Scene 3 (4.87–8.29s): on "into smaller chunks — by date range, by customer ID, whatever," the cracked node separates into 3 smaller adjacent tiles via per-word staggered reveal, one tile landing per named example (a bare tile / "DATE RANGE" mono tag / "CUSTOMER ID" mono tag), sliding apart just enough to show daylight between them, still touching — one dataset, divided.
Scene 4 (8.29–10.72s): on "so no single piece gets too big to manage," each tile's base fill-strip settles to a modest, equal height across all three (bars/fill wipe) — none overflowing.
Scene 5 (10.72–13.31s): on "It doesn't add copies, it divides the original," a mono stamp "DIVIDES, NEVER COPIES" types on below the tiles as a small readout ticks "1 dataset → 3 pieces"; holds still.

## Frame 4 — Sharding

- scene: The 3 partitioned tiles migrate onto 3 separate violet-bordered server boxes; write load (not just read load) now spreads across machines.
- voiceover: "Sharding is partitioning taken one level further. Each partition doesn't just live on a different table — it lives on a completely different database server. Now write load is split across machines too, not just read load."
- duration: 11.947s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/04-sharding.html
- type: feature_showcase
- persuasion: Build-up (partitioning taken further) + Causal chain
- beat: Comprehension + momentum
- blueprint: compose (DATA stage continues, final variation)

narrativeRole: Extends the partitioning tiles one more step — onto separate physical servers — introducing the write-load distinction from replication's read-only scaling.
keyMessage: Sharding takes those same partitioned chunks and puts each one on its own server, so writes — not just reads — spread across machines.

focal: the 3 partition tiles migrating onto 3 separate server node-boxes (violet edges)
roles: 3 partition tiles (callback to Frame 3) = foreground subject (origin) · 3 server node-boxes = foreground subject (destination) · violet distribute-edges = supporting signature · write/read tick marks = supporting · hairline grid = background
sfx: rising-whoosh, soft-impact

Scene 1 (0.0–0.99s): opens exactly where Frame 3 held — the 3 divided tiles sitting together; on "Sharding is partitioning," the tiles pulse once (callback beat).
Scene 2 (0.99–3.04s): on "taken one level further," a violet hairline self-draws downward from each tile toward three distinct empty server node-boxes appearing below, spaced apart.
Scene 3 (3.44–7.52s): on "Each partition doesn't just live on a different table — it lives on a completely different database server," each tile travels down its violet line and settles inside its own server box, one at a time via per-word staggered reveal, each server box hard-cutting a distinct mono tag ("SERVER A" / "SERVER B" / "SERVER C") as its tile lands.
Scene 4 (7.52–9.33s): on "Now write load is split across machines too," a small upward write-tick (↑) appears on each of the 3 servers together via a shared beat — visually distinct from Frame 2's downward hollow read-dots.
Scene 5 (9.33–12.03s): on "not just read load," a second, smaller read-dot fans across all 3 servers too (echoing Frame 2's motif, now on 3 separate machines); holds still on all three servers lit with both marks.

## Frame 5 — The divide

- scene: A top band ("a server dies / gets overloaded" → amber REPLICATION) contrasts against a bottom band ("the dataset itself is too big" → teal+violet PARTITIONING + SHARDING).
- voiceover: "So replication solves what if one server dies or gets too many reads. Partitioning and sharding solve what if the dataset itself is too big for one server to hold or write to."
- duration: 9.131s
- transition_in: crossfade
- status: animated
- src: compositions/frames/05-the-divide.html
- type: benefit_highlight
- persuasion: Comparison of two options + Distillation
- beat: Clarity + resolve
- blueprint: comparison-split (Adapt — portrait top/bottom stack instead of side-by-side)

narrativeRole: Compresses the whole video into the one distinction that matters — which problem each concept actually answers.
keyMessage: Replication answers "what if a server dies or gets overloaded"; partitioning and sharding answer "what if the data itself is too big for one server."

focal: the two stacked problem/solution bands
roles: top band (server-dies + REPLICATION tag) = foreground subject · bottom band (dataset-too-big + PARTITIONING+SHARDING tag) = foreground subject · divider hairline = supporting · grid = background
sfx: soft-alarm-tick, soft-mechanical-tick

Scene 1 (0.0–1.01s): crossfade from Frame 4's 3-server hold into a fresh, sparse stage (~55% empty); a top band frame-outlines itself (empty) at upper third as the VO opens "So."
Scene 2 (1.01–3.79s): on "replication solves what if one server dies or gets too many reads," the top band fills via per-word staggered reveal: a small server node-box flickers to hollow (`danger`-rose, failure state) beside a stack of read-dots piling up, an amber "REPLICATION" mono tag stamping in on a hard cut.
Scene 3 (3.79–4.54s): a hairline divider self-draws across the vertical middle.
Scene 4 (4.54–9.13s): on "Partitioning and sharding solve what if the dataset itself is too big for one server to hold or write to," the bottom band fills via per-word staggered reveal: a single oversized DATA node-box visibly strains against its own border (a subtle scale-press, no bounce), with a teal+violet dual mono tag "PARTITIONING + SHARDING" stamping in beside it; holds still on the stark top/bottom contrast, the node overflowing its frame on "hold or write to."

## Frame 6 — The punchline

- scene: Three tiny mini-diagram glyphs (amber / teal / violet) land in a vertical triptych, bind with a thin connecting line, then that line snaps into three distinct segments as the thesis stamps beneath.
- voiceover: "Different problems, often used together, never interchangeable."
- duration: 2.645s
- transition_in: cut
- status: animated
- src: compositions/frames/06-the-punchline.html
- type: branding
- persuasion: Distillation + Callback (to Frame 1's "They don't")
- beat: Resolution — "now I get it"
- blueprint: compose (instantiates frame.md's own Recap Triptych treatment)

narrativeRole: Lands the thesis the whole video has been building to — the direct payoff of Frame 1's "they don't."
keyMessage: Replication, partitioning, and sharding are different problems' answers — not substitutes for each other.

focal: the three mini-diagram cards, landing together and holding
roles: 3 mini-cards (duplicate / split / distribute glyphs) = foreground subject (co-equal) · "NEVER INTERCHANGEABLE." stamp = foreground subject (closing) · connecting hairline = supporting · grid = background
sfx: none — the deliberate quiet beat

Scene 1 (0.0–0.78s): hard cut from Frame 5's overflow hold; on "Different problems," three small mini-diagram cards spring-pop in one after another, stacked vertically — a duplicate-glyph (amber), a split-glyph (teal), a distribute-glyph (violet) — each already labeled in small Fraunces.
Scene 2 (0.78–1.56s): on "often used together," a thin connecting hairline self-draws between all three cards, binding them without merging them.
Scene 3 (1.56–2.63s): on "never interchangeable," the connecting line snaps into three distinct segments on a hard cut (not a fade) as "NEVER INTERCHANGEABLE." stamps beneath in Fraunces display weight — the video's held breather: settles fully still, subtle jitter only, no further motion.

## Frame 7 — The guidance list

- scene: Three rule-of-three statements land top-to-bottom, each with its own mono index tick and signal color — add replication first, partition when, shard when.
- voiceover: "Add replication first — almost every production database needs it for availability alone. Partition when a single table gets too large to query efficiently. Shard when write throughput on a single server becomes the actual bottleneck."
- duration: 12.544s
- transition_in: crossfade
- status: animated
- src: compositions/frames/07-the-guidance-list.html
- type: benefit_highlight
- persuasion: Signposting ("add… partition when… shard when…") + Rule of three
- beat: Confidence + mastery
- blueprint: grid-card-assemble (Adapt — 3 items land as a vertical list, not a grid, per frame.md's own Guidance List treatment)

narrativeRole: Converts the video's understanding into a decision rule — what to reach for, and in what order.
keyMessage: Add replication by default; partition when a table gets too big to query; shard when writes overload a single server.

focal: the 3 guidance statements landing top-to-bottom, each with its own signal-color index tick
roles: statement 1 "ADD REPLICATION FIRST" = foreground subject · statement 2 "PARTITION WHEN…" = foreground subject · statement 3 "SHARD WHEN…" = foreground subject · mono index ticks = supporting · grid = background
sfx: soft-tick

Scene 1 (0.0–1.01s): crossfade to a calm, ~60%-empty stage; as the VO says "Add replication first," a mono index "01" + amber tick lands upper-third with "ADD REPLICATION FIRST" in Fraunces (waterfall entry, single line).
Scene 2 (1.01–4.16s): on "almost every production database needs it for availability alone," a smaller IBM Plex Sans sub-line types on beneath statement 1.
Scene 3 (4.16–7.95s): on "Partition when a single table gets too large to query efficiently," statement 2 lands beneath (mono "02" + teal tick, waterfall entry) with its own sub-line typing on — statement 1 stays visible, dimmed to supporting.
Scene 4 (7.95–12.52s): on "Shard when write throughput on a single server becomes the actual bottleneck," statement 3 lands last (mono "03" + violet tick) with its sub-line — all three now stacked, statement 3 at full brightness; holds still on the complete rule-of-three list.

## Frame 8 — The ask

- scene: "COMMENT" types on, "GUIDE" hard-cuts in at full display weight in amber, a mono sub-line promises the full breakdown.
- voiceover: "Comment guide and I'll send over the full breakdown."
- duration: 3.269s
- transition_in: cut
- status: animated
- src: compositions/frames/08-the-ask.html
- type: cta
- persuasion: Direct address + Distillation
- beat: Satisfaction + invitation
- blueprint: titlecard-reveal (Adapt)

narrativeRole: Converts the viewer's new clarity into one concrete next action.
keyMessage: Comment "GUIDE" to get the full breakdown.

focal: the "GUIDE" keyword stamp
roles: "COMMENT" lead-in = supporting · "GUIDE" keyword = foreground subject (amber, the video's first-named signal color) · mono sub-line = supporting · grid = background
sfx: none

Scene 1 (0.0–0.9s): hard cut to a calm, mostly-empty stage; "COMMENT" types on center-upper (Fraunces kicker) as the VO opens.
Scene 2 (0.9–2.04s): on "guide and I'll send," the word "GUIDE" hard-cuts in below at full Fraunces display weight in amber, quote-marked.
Scene 3 (2.04–2.9s): on "over the full breakdown," a small mono sub-line "→ full breakdown in the comments" types on beneath, then holds fully still — the video's final frame, genuine exit via the harness's own end hold.
