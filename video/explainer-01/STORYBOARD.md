---
format: 1080x1920
duration: 41s
message: "A cache expiring under load doesn't fail quietly — it floods your database, unless you coalesce the requests."
arc: concept-explainer — Hook → Problem → Escalation → Fix → Landing
audience: backend / software engineers who work with caching layers
mode: autonomous
music: none
---

## Video direction

- **Palette** (from `frame.md`, Blue Professional): warm cream `bg` ground on every frame; a single saturated cobalt `primary` carries every accent — the exploding counter, the cache-key glow, the flood of request dots, the load-meter fill, the gate icon, the term-card accent line. Near-black `text` for headlines, muted `text-muted` for labels, tinted `card-bg`/`border` for any card surface. `negative` red is used only as the alarm-peg color on the database load bar in Frame 3 — never a second brand accent, never a fill elsewhere.
- **Motion grammar + reveal model**: `power3` long-tail settles everywhere; no bounce/overshoot/elastic. Every frame's entrance carries only what the VO is saying at t=0 — each further piece (a stat, a layer, a card) reveals on its spoken cue, weighted into the back ~50%. During a hold, the only sanctioned aliveness is subtle jitter or a live SVG internal (e.g. a spinner) — never breathing, never a back-half pan/push.
- **Continuity**: Frames 2 and 3 share one stage — the cache-tile → flood-of-requests → database composition — connected by `crossfade` so the flood leaving Frame 2 is the flood arriving in Frame 3 (a handoff, not a reset). The cache-key tile and request-dot motif carry visually from Frame 1 through Frame 4.
- **Rhythm / held beats**: Frame 3 ends on a genuine held beat (load meter pegged red, "10,000 queries" stamped, real stillness) — the alarm peak right before the turn. Frame 5 is the deliberate breather/landing beat (title-card chain), holding to the final frame.
- **Negative list**: no bouncy/elastic entrances; no lazy breathing or back-half camera drift; no generic AI bokeh / purple-blue gradients; no real browser/OS chrome or literal cursors — every request/server/database/gate is an invented icon + label, never a screenshot.

## Frame 1 — Hook: the expiry that isn't quiet

- scene: A single glowing cache-key tile counts down and flips to EXPIRED; a stat explodes to "10,000 requests" slamming into a server icon; lands on the term "The Thundering Herd Problem."
- voiceover: "Ever wonder what happens when your cache entry expires at the exact same moment 10,000 requests hit your server? That's the thundering herd problem."
- duration: 8.76s
- transition_in: cut
- status: outline
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Shocking statistic + Rhetorical question (stakes)
- beat: curiosity + tension
- blueprint: dataviz-countup (Adapt — Hook cold-open counter-burst)
- focal: the "10,000" counter
- roles: counter = foreground subject (cobalt, center) · cache-key tile = supporting (upper, ticks to EXPIRED) · request-dot icons = supporting (small cobalt marks flinging to a server glyph) · closing term card = the late focal

Adapt: keep the cold-open counter-burst signature move (icons puncture in, the number explodes in size); extend the ending into a coined-term card instead of a plain lean-in.

Scene 1 (0.0–1.6s): cream ground; a single cache-key tile (rounded, cobalt border) sits upper-center with a thin cobalt countdown ring — nothing else on screen, camera static.
Scene 2 (1.6–4.64s): on "expires," the ring completes and the tile flips from filled cobalt to a hollow "EXPIRED" outline (`scale-swap-transition`); as the VO reaches "10,000," a bold cobalt counter beneath it starts a value-scaled count-up, growing in size as it climbs (`counting-dynamic-scale`).
Scene 3 (4.64–6.06s): small cobalt request-dot icons puncture in clustered around the counter and fling outward toward a faint server glyph low-center as the counter lands on "10,000" at full size — a long-tail settle (`spring-pop-entrance`), no bounce.
Scene 4 (6.62–8.76s): counter and dots settle and dim ~40%; a coined-term card assembles word-by-word beneath (`dynamic-content-sequencing`): "The Thundering Herd Problem" — lands and holds fully still.

narrativeRole: Opens the cognitive gap — a familiar cache expiry becomes catastrophic at scale, then names the phenomenon.
keyMessage: A single cache expiry, at the wrong moment, can trigger thousands of simultaneous requests — this is the thundering herd problem.

## Frame 2 — Problem: one key, missing for everyone at once

- scene: The cache-key tile flips from filled to empty; a cluster of request icons that were all reading it discover it's gone at the same instant and stream toward a database icon.
- voiceover: "One cache key expires. Every request that needed that data suddenly finds it missing, all at once. So all 10,000 requests go straight to the database to recompute the—"
- duration: 10.76s
- transition_in: crossfade
- status: outline
- src: compositions/frames/02-cache-expires.html
- type: pain_point
- persuasion: Demonstration (show the mechanism running) + Causal chain (A → B → C)
- beat: recognition + mounting tension
- blueprint: compose
- focal: the cache-key tile transitioning into a flood of request-dot icons
- roles: cache-key tile = foreground subject (Scene 1) fading to context · request-dot icons = foreground subject (Scene 2+, cobalt, many, each labeled "req") · database glyph = supporting (revealed lower-frame, awaiting)

Scene 1 (0.0–1.84s): cream ground, asymmetric layout; the empty/hollow cache-key tile from Frame 1 sits upper-left (continuity) — static, nothing else yet.
Scene 2 (1.84–5.3s): small cobalt request-dot chips reveal one by one around the tile as the VO names them — per-item layer-reveal (`dynamic-content-sequencing`); each dot briefly touches the tile and recoils, finding it empty.
Scene 3 (5.3–9.26s): the recoiling dots swap direction in lockstep — a cluster→outward expansion (`center-outward-expansion`) sends the whole cluster streaming downward toward a database glyph now revealed lower-frame; a small steady counter beside the stream climbs toward "10,000" (`counting-dynamic-scale`, fixed size, no growth).
Scene 4 (9.26–10.76s): the stream arrives at the database glyph's edge, dots stacking and queuing against it — held on the moment of arrival; the impact carries into Frame 3 via the crossfade.

narrativeRole: Shows the mechanism of failure — simultaneity, not the expiry itself, is the root cause.
keyMessage: When one cache key expires, every request that depended on it finds it missing at the exact same instant.

## Frame 3 — Escalation: light load to slammed

- scene: Same stage continues — a database load meter that sat calm and thin suddenly spikes to a maxed red bar as "10,000 queries" stamps in.
- voiceover: "—same value. Your database, which was handling light load a second ago, just got hit with 10,000 queries at the same time. The—"
- duration: 8.24s
- transition_in: crossfade
- status: outline
- src: compositions/frames/03-database-overload.html
- type: social_proof
- persuasion: Before/after contrast + Statistical proof
- beat: alarm
- blueprint: dataviz-countup (Adapt — Problem push-through, camera dropped: same stage continues from Frame 2)
- focal: the database load bar
- roles: database metric-card = foreground subject · load bar = the payload (calm → pegged red) · "10,000 queries" stat = supporting, lands beside the bar

Adapt: keep the count-up/fill signature; drop the traversal camera (the stage is already established, continuing from Frame 2's arrival) and land the fill's color-step escalation as the beat.

Scene 1 (0.0–2.06s): same stage continues (crossfade in) — the queued dot-stack from Frame 2 sits against a tinted metric-card labeled "DATABASE"; a slim cobalt load-bar beneath it sits thin and calm.
Scene 2 (2.06–5.02s): the load-bar holds its calm state briefly (`stat-bars-and-fills`), then on "just got hit" the queued dot-stack slams into the card in one beat — a long-tail impact settle (`spring-pop-entrance`), not bouncy.
Scene 3 (5.02–6.54s): the load-bar fill rockets from calm to maxed, stepping color cobalt→negative-red at the peg (`stat-bars-and-fills`), as a bold "10,000 queries" stat stamps in beside it (`counting-dynamic-scale`).
Scene 4 (6.54–8.24s): hold — the pegged red bar and the stat sit genuinely still (allocated stillness; at most a subtle jitter on the bar's edge, `sine-wave-loop` low-amplitude) — the alarm peak right before the turn.

narrativeRole: Quantifies the consequence — a calm system instantly overwhelmed by identical, redundant work.
keyMessage: A database handling light load gets hit with 10,000 identical queries in the same instant.

## Frame 4 — The fix: one winner, everyone else waits

- scene: The same flood arrives, but now hits a gate icon; one request is highlighted through to recompute while the rest queue, then all read the refilled cache key together.
- voiceover: "—fix is simple: only one request is allowed to recompute the value. Every other request waits for that result, then reads it from cache."
- duration: 8.48s
- transition_in: crossfade
- status: outline
- src: compositions/frames/04-the-fix.html
- type: feature_showcase
- persuasion: Before/after contrast + Frame-then-fill (state the rule, then show it running)
- beat: clarity + relief
- blueprint: agent-progress-theater (Adapt)
- focal: the single highlighted request passing the gate
- roles: gate icon = foreground subject (a cobalt pill with a lock glyph) · the singled-out request dot = foreground subject while it "works" · the queued dot-field = supporting, waiting · the cache-key tile = supporting, flips filled again on resolve

Adapt: recast the "machine visibly works, then a receipt cascades" signature as one request winning the gate while the rest queue, then all flip to a cache-hit state together — same shape, backend content.

Scene 1 (0.0–1.74s): the request-dot field from Frame 3 now queues at a new cobalt gate icon; as the VO says "only one," a single dot highlights and passes through — `scale-swap-transition` singles it out from the pack.
Scene 2 (1.74–3.12s): the highlighted dot travels alone toward the database card; a small "recomputing…" status label types on beside it (`discrete-text-sequence`) — a finite, diegetic working-state, not decorative.
Scene 3 (3.12–6.92s): the rest of the dot-field sits queued at the gate (status label reads "waiting…"); then on "reads," the recompute resolves — the cache-key tile flips back to filled cobalt, and the receipt cascades: each queued dot flips in sequence from outline to a solid cobalt check (`scale-swap-transition` + checkmark draw), staggered left→right.
Scene 4 (6.92–8.48s): all dots checked, the cache-key tile glowing filled cobalt — hold the resolved state (`ambient-glow-bloom` behind the tile, static, finite) as the beat lands on relief.

narrativeRole: Introduces the fix mechanism — coalesce concurrent recomputation into one winner; everyone else waits and reads the cached result.
keyMessage: Only one request is allowed to recompute the value; every other request waits, then reads the result from cache.

## Frame 5 — Landing: it has a name

- scene: Two clean term cards land in sequence — "Request Coalescing" then "Distributed Lock" — under one line about the recompute step, closing on a calm held frame.
- voiceover: "This is usually called request coalescing, or a distributed lock around the recompute step."
- duration: 4.68s
- transition_in: crossfade
- status: outline
- src: compositions/frames/05-landing.html
- type: branding
- persuasion: Coined term / distillation
- beat: satisfaction — "now I get it"
- blueprint: titlecard-reveal (Reproduce — card chain)
- focal: the term cards
- roles: term card = foreground subject (centered, near-black on cream) · cobalt accent-line = supporting

Scene 1 (0.0–2.12s): cream ground, centered, calm; a term card fades up with a subtle scale-up settle (`scale-swap-transition`) reading "Request Coalescing" under a small cobalt accent-line.
Scene 2 (2.12–3.52s): an instant hard cut (no crossfade — the card-chain seam) to a second identical-format term card: "Distributed Lock."
Scene 3 (3.52–4.68s): a small caption line settles beneath the held card — "around the recompute step" — the whole frame holds fully still to the final frame, the video's landing beat.

narrativeRole: Lands the takeaway with its name so the viewer can recall and look for it later.
keyMessage: This fix has a name — request coalescing, or a distributed lock around the recompute step.
