---
format: 1080x1920
duration: 79s
message: "An API gateway is the front door — traffic coming in from outside. A service mesh, built out of sidecars, is the hallways — traffic moving between your own services. You usually need all three, not just one."
arc: concept-explainer
audience: backend / platform engineers who reach for these three terms loosely; developers prepping system-design interviews
mode: autonomous
music: none
---

## Video direction

**Palette system** (from `frame.md`, never invented elsewhere): void-black canvas
(`canvas` / `canvas-raised` / `canvas-raised-2`) throughout — no other ground ever
appears. `frame.md`'s three signal colors are reused, but **remapped to this video's
three concepts** (this script is not the reverse-proxy/load-balancer/API-gateway video
the pack shipped with — "atoms are sacred, composition is free," per `frame.md`'s own
principle line): **violet `accent-3`** = an API gateway / a request being **gated**
through policy checks (unchanged from the pack — the gateway concept carries over
directly, gate-ticks = auth / rate limit / route); **amber `accent`** = a sidecar proxy
/ a request that just **forwards**, locally, next to one service instance; **teal
`accent-2`** = a service mesh / many sidecar edges being **coordinated** by a control
plane (retries, timeouts, encryption, observability — the "choose/route" edge behavior
reused for "the control plane routes/retries on your behalf"). `ink` / `ink-dim` /
`ink-faint` for text, `line` for hairlines. `danger` (rose) stays in reserve, unused —
nothing in this script is blocked/denied. The caption rail (`.hyperframes/caption-skin.html`)
borrows these same three colors for scarce keyword emphasis — one visual system, not two.

**Motion grammar + reveal model:** one continuous "camera travels further into the
same request path" feeling across the diagram frames (2 → 4), carried by (a) a shared
client / service / control-plane diagram vocabulary extended frame to frame, and (b)
`zoom-through` seams between them that read as pushing further into the same schematic.
The throughline is a literal zoom arc: Frame 2 holds the wide edge shot (client → gateway
→ services, north-south traffic), Frame 3 pushes tight into ONE service + its attached
sidecar (east-west, local), Frame 4 pulls back out to reveal the WHOLE mesh of many
sidecars talking to each other. Every reveal is timed to the voiceover — nothing drops in
whole at t=0; `power3` long-tail settles everywhere, no bounce/overshoot except the
deliberately-playful spring-pop on the hook's term flashes. Diagram edges are built with
`svg-path-draw` (they draw themselves as the VO names the behavior); gate-ticks flip
hollow → filled on their spoken word. Only the FINAL frame gets an exit tween (a settle);
every other frame's exit is its `transition_in`.

**Rhythm / held-frame allocation:** Frame 5 (front door / hallways synthesis) builds to a
**stillness-before-climax** hold — the two recap cards land, then everything holds dead
still while the "front door / hallways" line finishes — the video's one deliberate
breather-as-payoff. Frame 7 (CTA) ends on a calm settled hold. Every other frame keeps
developing to its own last beat — this is a denser, three-mechanism video with no other
slack beat to spare.

**Negative list:** no shadow, no gradient fill, no card glow on a diagram node (hairline
+ flat only — the one sanctioned glow is the ambient bloom behind Frame 5's held recap
and Frame 7's sign-off); no color on an edge/gate-tick other than the three fixed signal
colors, and their concept roles never swap mid-video; no rounded "pill" nodes; no lazy
breathing / idle wobble; no bad slow pan/push in a scene's back half; no front-loaded-then-
frozen diagram (every diagram frame keeps resolving into its back ~50%); nothing (including
the caption rail) below y≈1670 on the 1920-tall canvas, nothing load-bearing above y≈150.

---

## Frame 1 — API gateway, service mesh, sidecar proxy

- scene: three terms hard-cut flash across a void-black schematic sheet, each briefly ticked in its own signal color, before collapsing into a stacked list and the "all three, different jobs" stamp settles
- voiceover: "API gateway, service mesh, sidecar proxy. All three sit in the request path of a microservices system, and it's easy to think you only need one. You usually need all three, doing different jobs."
- duration: 11.31s
- transition_in: cut
- status: outline
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Concept announcement + counterintuitive claim
- beat: curiosity + recognition
- blueprint: kinetic-type-beats (Adapt)
- focal: the three term-words themselves
- roles: term words = foreground subject (hard-cut flashes, then stacked) · hairline schematic grid = background (dim, ambient) · "you only need one" ghost-term = supporting (the misconception, briefly shown then dismissed) · settling stamp line = supporting
- sfx: none

narrativeRole: Opens the cognitive gap immediately — names all three terms and states the contrarian claim (you need all three, not just one) as the punchiest possible first line, before any single concept is explained.
keyMessage: These three terms sit in the same request path but do different amounts of work — and you usually need all three, not just one.

Adapt: keep kinetic-type-beats' hard-cut word-swap signature; the "payoff" isn't a logo, it's the settled hook stamp naming the contrarian claim.
Scene 1 (0.0–2.54s): void canvas, faint hairline grid at ~12% alpha. On "API gateway," the words API GATEWAY hard-cut flash full-bleed in Fraunces `display`, ink, with a brief violet underline tick — Centered, ~70% of frame. On "service mesh," hard-cut swap to SERVICE MESH, brief teal tick. On "sidecar proxy," hard-cut swap to SIDECAR PROXY, brief amber tick.
Scene 2 (2.54–5.46s): as the VO says "all three sit in the request path of a microservices system," the three words collapse (scale-swap) into a smaller stacked list — violet / teal / amber ticks kept — sliding to the upper third; a kicker-weight Fraunces italic line "SAME REQUEST PATH" per-word staggered reveal fades in beneath — Rule-of-thirds, 2 depth layers.
Scene 3 (5.46–7.74s): on "and it's easy to think you only need one," a fourth, unticked, ink-faint "ghost" term-shape flickers once in the empty space beside the stack (no label, just a dim outline standing in for "pick one") then dissolves to nothing — visualizing and dismissing the misconception without literally naming a wrong answer.
Scene 4 (7.74–11.31s): on "you usually need all three, doing different jobs," all three stacked terms relight to full brightness simultaneously (a synced brightness pop, not sequential); beneath them a Fraunces `h2` stamp line builds word-by-word: "different jobs." — holding fully still for the cut into Frame 2, subtle jitter only.

---

## Frame 2 — The API gateway gates

- scene: client, gateway, and service node-boxes appear on the schematic stage; gate-ticks for AUTH / RATE LIMIT / ROUTE flip hollow-to-filled on the violet edge before it reaches the service
- voiceover: "An API gateway sits at the edge, the single door external clients come through. It's the one place handling auth, rate limiting, and routing requests to the right service, before anything is internal traffic yet."
- duration: 12.02s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/02-api-gateway.html
- type: product_intro
- persuasion: Concretization + progressive disclosure
- beat: clarity + orientation
- blueprint: spatial-pan-stations (Adapt)
- focal: the violet gate-edge, client → gateway → service, gated by ticks
- roles: GATEWAY node-box = foreground subject · CLIENT node-box = the external station · SERVICE node-box = the internal destination · gate-ticks (AUTH / RATE LIMIT / ROUTE) = the checklist riding the edge · "EXTERNAL" / "INTERNAL" station-labels = supporting
- sfx: none

narrativeRole: Establishes the API gateway as the edge / front-door concept — the single door external traffic passes through before anything is internal — and stages the diagram vocabulary (node-box, gate-tick) the rest of the video extends.
keyMessage: An API gateway is the single door at the edge where external clients enter — the one place auth, rate limiting, and routing happen before traffic becomes internal.

Adapt: this frame instantiates spatial-pan-stations directly — CLIENT / GATEWAY / SERVICE stations on one wide schematic stage, traversed by one virtual camera as the VO names each; keep the signature camera-travels-the-stations move.
Scene 1 (0.0–1.57s): void canvas + hairline grid. On "an API gateway sits at the edge," the GATEWAY node-box draws in (spring-pop, restrained) upper-center; a station-label "EDGE" ticks on in violet mono — Centered, ~40% of frame, camera holds close on it.
Scene 2 (1.57–4.32s): camera performs one continuous push-back (viewport-change) as "the single door external clients come through" plays — the CLIENT node-box draws in upper-left, labeled "EXTERNAL" in mono; the violet edge self-draws (svg-path-draw) from CLIENT to GATEWAY, one unbroken line.
Scene 3 (4.32–8.94s): as "it's the one place handling auth, rate limiting, and routing requests to the right service" plays, three gate-ticks appear in sequence directly on the edge past the gateway — "AUTH" (hollow → filled on "auth"), "RATE LIMIT" (hollow → filled on "rate limiting"), "ROUTE" (hollow → filled on "routing") — each flip lands exactly on its spoken word, the request visibly pausing at each; as ROUTE resolves, the edge continues to a SERVICE node-box drawing in below-right, labeled "the right service" in mono.
Scene 4 (8.94–12.02s): on "before anything is internal traffic yet," a station-label "INTERNAL" fades in dim (25%) just past the SERVICE box — clearly beyond the gate, still unlit/quiet — while the full CLIENT→GATEWAY→SERVICE violet line holds solid and still, held read, subtle jitter only.

---

## Frame 3 — The sidecar proxy forwards, per service

- scene: the camera pushes tight onto ONE service instance and its attached sidecar proxy, an amber edge forwarding everything in and out; the SERVICE+SIDECAR pair stays pinned while other service instances (each with their own identical pair) scroll past behind it
- voiceover: "A sidecar proxy is a small proxy deployed next to a single service instance, intercepting everything that service sends and receives. It's not about the edge, it's about every individual service having its own local traffic layer."
- duration: 12.79s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/03-sidecar-proxy.html
- type: feature_showcase
- persuasion: Contrast (not the edge — every individual service) + concretization
- beat: comprehension + momentum
- blueprint: fixed-anchor-cycle (Adapt)
- focal: the pinned SERVICE + SIDECAR pair and its amber forward-edge
- roles: SERVICE node-box + attached SIDECAR node-box = the pinned anchor pair · amber forward-edge (in + out, one line each, never branching) = foreground signal · the row of other identical SERVICE+SIDECAR pairs = the cycling context (dim, 25-40%) · "LOCAL TO THIS INSTANCE" station-label = supporting
- sfx: none

narrativeRole: Zooms the camera from the wide edge shot of Frame 2 into ONE service instance to show the sidecar's job is local, not architectural — a deliberate contrast with the gateway's single-door framing.
keyMessage: A sidecar proxy is a small proxy attached to one service instance, forwarding everything that instance sends and receives — every service gets its own, not a shared edge.

Adapt: keep fixed-anchor-cycle's signature (one pinned element, the surrounding state cycling) — the SERVICE+SIDECAR pair is the pin; the row of other identical pairs is what cycles past behind it, making "every individual service" a literal repeating pattern rather than a claim.
Scene 1 (0.0–1.0s): continues Frame 2's zoom-through arrival, now pushed tight — void canvas, hairline grid dimmed further (immersive close-up). On "a sidecar proxy is a small proxy," a small SIDECAR node-box draws in (spring-pop, restrained) snug beside a SERVICE node-box, both centered — ~45% of frame.
Scene 2 (1.0–3.48s): as "deployed next to a single service instance" plays, a station-label "ONE INSTANCE" ticks on beneath the pair in amber mono; the pair's border pulses amber once, establishing the pin.
Scene 3 (3.48–6.4s): on "intercepting everything that service sends and receives," an amber edge self-draws (svg-path-draw) as two short segments — one arrow curving IN to the SIDECAR from off-frame, one curving OUT — both routed through the SIDECAR box before reaching the SERVICE box, visibly intercepted; never a single pass-through line.
Scene 4 (6.4–8.0s): on "it's not about the edge," the violet gateway motif from Frame 2 flashes once, small and dim (25%, ink-faint outline only) at the frame's far edge, then fades — a quiet visual negation, not a full diagram.
Scene 5 (8.0–12.79s): as "it's about every individual service having its own local traffic layer" plays, 3-4 more SERVICE+SIDECAR pairs (identical amber-edged glyphs, dimmed to ~35%) scroll in from the right and drift past behind the pinned pair (cluster→outward expansion, fixed-anchor-cycle's signature), each briefly brightening to full amber as it passes center then dimming again — the pinned pair never moves, never dims — landing held on the pinned pair alone once the row settles, subtle jitter only.

---

## Frame 4 — The service mesh coordinates them all

- scene: the camera pulls back from Frame 3's single pair to reveal many sidecars networked together; a control-plane node above ticks off RETRIES / TIMEOUTS / ENCRYPTION / OBSERVABILITY as teal edges connect every sidecar-to-sidecar pair
- voiceover: "A service mesh is what you get when every service has its own sidecar, and a control plane manages all of them together, retries, timeouts, encryption, and observability, for every service-to-service call, consistently, without each team building it themselves."
- duration: 13.93s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/04-service-mesh.html
- type: feature_showcase
- persuasion: Causal chain (A → B → C) + progressive disclosure
- beat: comprehension + mastery
- blueprint: agent-progress-theater (Adapt)
- focal: the control-plane node and its four capability ticks resolving across the teal mesh
- roles: CONTROL PLANE node-box = foreground subject, elevated above the mesh · 4-5 SERVICE+SIDECAR pairs (carried over, now networked) = the coordinated mesh · 4 capability ticks (RETRIES / TIMEOUTS / ENCRYPTION / OBSERVABILITY) = the checklist that checks off · teal service-to-service edges = foreground signal
- sfx: none

narrativeRole: This is the video's richest mechanism — it makes "a control plane manages all of them together" concrete by literally staging each named capability as a tick checking off above a growing web of teal sidecar-to-sidecar edges, completing the zoom arc (wide edge → one instance → the whole coordinated mesh).
keyMessage: A service mesh is what you get when every service's sidecar is coordinated by one control plane — retries, timeouts, encryption, and observability applied consistently, without each team building it themselves.

Adapt: agent-progress-theater's "working-state theater, then the checklist checks off" signature, staged directly above the diagram instead of a separate panel — each named capability visibly applies itself across the mesh as it ticks.
Scene 1 (0.0–0.9s): camera pulls back (viewport-change, one continuous decelerating zoom-out) from Frame 3's single pinned pair — it becomes one of several SERVICE+SIDECAR pairs now visible in a loose cluster, all still amber-edged and static. On "a service mesh is what you get," a CONTROL PLANE node-box draws in (spring-pop, restrained) above the cluster, unlit — Centered stage, ~45% of frame.
Scene 2 (0.9–3.25s): on "when every service has its own sidecar," each visible pair's amber edge fades to ink-dim (25%) in sync, one by one, left to right (they're established, not the focus now) — de-emphasizing the amber layer to make room for teal.
Scene 3 (3.25–5.45s): as "and a control plane manages all of them together" plays, thin teal lines self-draw (svg-path-draw) from the CONTROL PLANE node down to every SIDECAR box at once (a fan of connections, not sequential) — the control plane visibly "reaching" all of them.
Scene 4 (5.45–8.8s): as "retries, timeouts, encryption, and observability" plays, four capability ticks appear in sequence on the CONTROL PLANE node itself — "RETRIES" (hollow → filled on "retries"), "TIMEOUTS" (on "timeouts"), "ENCRYPTION" (on "encryption"), "OBSERVABILITY" (on "observability") — each flip pulses a teal ripple outward along the fan-lines to every sidecar simultaneously, visibly applying that capability mesh-wide.
Scene 5 (8.8–13.93s): as "for every service-to-service call, consistently, without each team building it themselves" plays, direct sidecar-to-sidecar teal edges self-draw between adjacent pairs (not just up to the control plane) — the mesh reads as fully networked, every pair connected — landing held on the complete mesh, all four ticks filled, subtle jitter only.

---

## Frame 5 — Front door, hallways

- scene: two small recap diagram-cards — Frame 2's violet gate-edge, Frame 4's teal mesh-fan — self-assemble side by side, captioned "FRONT DOOR" and "HALLWAYS," then hold dead still
- voiceover: "So the gateway handles traffic coming into your system from outside. The mesh, built out of sidecars, handles traffic moving between your own services once it's already inside. One's the front door, the other is the hallways."
- duration: 12.29s
- transition_in: crossfade
- status: outline
- src: compositions/frames/05-thesis.html
- type: branding
- persuasion: Generalization (specific → principle) + visceral metaphor + callback
- beat: clarity + resolve
- blueprint: grid-card-assemble (Adapt)
- focal: the two recap cards landing then holding together
- roles: 2 recap diagram-cards (gateway = violet, mesh = teal) = foreground subject · "FRONT DOOR" / "HALLWAYS" captions = supporting · void canvas = background
- sfx: none

narrativeRole: This is the thesis payoff the video has been building toward — it names the axis (outside vs. already-inside) and lands the front-door/hallways metaphor as the single line the viewer keeps, recapping the gateway and mesh diagrams side by side.
keyMessage: The gateway is the front door — traffic coming in from outside. The mesh is the hallways — traffic moving between your own services once it's already inside.

Adapt: grid-card-assemble's self-assembling cascade, held to just TWO cards (not a grid) stacked vertically for portrait — the signature land-then-hold is kept; this is the video's stillness-before-climax beat.
Scene 1 (0.0–3.02s): void canvas. On "so the gateway handles traffic coming into your system from outside," recap-card 1 self-assembles (spring-pop, restrained) upper-half — a tiny violet gate-edge glyph (client → gate-ticks → service, echoing Frame 2) with an arrow pointing INTO the frame from off-canvas-top, captioned "FRONT DOOR" beneath in Fraunces `h3` — Centered, ~40% of frame.
Scene 2 (3.02–9.1s): on "the mesh, built out of sidecars, handles traffic moving between your own services once it's already inside," recap-card 2 lands beneath (same mechanic) — a tiny teal mesh-fan glyph (several sidecar dots interconnected, echoing Frame 4) with arrows pointing sideways BETWEEN nodes, captioned "HALLWAYS" beneath — card 1 dims slightly (40%) to cede focus as card 2 assembles, then both settle to equal brightness once card 2 completes.
Scene 3 (9.1–12.29s): on "one's the front door, the other is the hallways," both cards hold completely still together, side by side (stacked, portrait) — the video's stillness-before-climax payoff; a soft ambient glow blooms once behind the pair as the line lands, then holds — subtle jitter at most, no further motion.

---

## Frame 6 — When to reach for which

- scene: two guidance lines land top-to-bottom, each prefixed by its signal-color tick and a mono index number — API gateway's threshold first, service mesh's threshold second
- voiceover: "You need an API gateway as soon as external clients talk to more than one backend service. Add a service mesh once you have enough internal services that retries, mTLS, and observability between them can't be handled per-team anymore."
- duration: 13.25s
- transition_in: push-slide UP
- status: outline
- src: compositions/frames/06-guidance.html
- type: benefit_highlight
- persuasion: Signposting + comparison of two options
- beat: confidence + foresight
- blueprint: kinetic-type-beats (Adapt)
- focal: the currently-landing guidance line
- roles: 2 guidance statements = foreground subject, each ticked in its matching signal color (violet / teal) · mono index numbers = supporting chrome · void canvas = background
- sfx: none

narrativeRole: Converts the just-landed thesis into two concrete decision thresholds the viewer can apply directly — deliberately plain and list-shaped after the denser diagram and synthesis frames.
keyMessage: Reach for an API gateway as soon as external clients hit more than one backend service; add a service mesh once retries, mTLS, and observability between internal services can't be handled per-team anymore.

Adapt: kinetic-type-beats' per-statement landing, staged as a two-item vertical stack (portrait full-width strip) rather than a hero word — the push-slide-UP seam signals "new section" (practical thresholds) after the recap.
Scene 1 (0.0–4.06s): void canvas. On "you need an API gateway as soon as external clients talk to more than one backend service," line 1 lands (per-word staggered reveal) at the top, prefixed "01 ·" in violet mono, a violet tick beside "API gateway" — Full-width strip, top third.
Scene 2 (4.06–4.76s): a beat of held tension — line 1 sits alone, fully landed, before line 2 begins (no motion, letting the first threshold register).
Scene 3 (4.76–12.63s): on "add a service mesh once you have enough internal services that retries, mTLS, and observability between them can't be handled per-team anymore," line 2 lands beneath (same mechanic), prefixed "02 ·" in teal mono, a teal tick beside "service mesh" — line 1 dims slightly (40%) to cede focus; as "retries, mTLS, and observability" is spoken, those three words individually pulse teal in place (asr-keyword-glow) without leaving the line.
Scene 4 (12.63–13.25s): both lines hold together, stacked, line 2 at full brightness — settled for the cut, subtle jitter only.

---

## Frame 7 — Comment "guide"

- scene: a short sign-off line settles center-frame, the quoted word "guide" gets one violet emphasis pulse, small mono sub-line beneath
- voiceover: "Comment guide and I'll send over the full breakdown."
- duration: 2.43s
- transition_in: crossfade
- status: outline
- src: compositions/frames/07-cta.html
- type: cta
- persuasion: Direct address
- beat: satisfaction + inspiration
- blueprint: titlecard-reveal (Adapt)
- focal: the quoted word "guide"
- roles: sign-off line = foreground subject · "guide" word = the one emphasized element · mono sub-line = supporting
- sfx: none

narrativeRole: Closes on the exact, low-friction ask from the script — a single clean card, no new information, just the call to act.
keyMessage: Comment "guide" for the full breakdown.

Adapt: titlecard-reveal's one restrained move + still hold, closing the film calmly. Accent uses violet (this video's first-named signal — API gateway opens the hook, same principle `frame.md` applies to its own first-named term), not the amber the pack's original video used.
Scene 1 (0.0–0.61s): void canvas, centered. On "comment," the word COMMENT types on (per-word staggered reveal) in Fraunces `h2`, ink.
Scene 2 (0.61–2.43s): on "guide," the quoted word 'GUIDE' lands beside it with one violet spring-pop + a brief ambient glow bloom (the video's other sanctioned glow) behind it, in quotes; as "and I'll send over the full breakdown" plays, a small mono sub-line types on beneath: "the full breakdown →". The whole card then holds fully still — this frame's real exit (final frame): a slow, gentle settle, no further motion.
