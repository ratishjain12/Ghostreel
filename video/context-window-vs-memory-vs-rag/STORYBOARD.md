---
format: 1080x1920
duration: 79s
message: "The context window is just the space. Memory decides what from your own conversation earns a spot in it. RAG decides what from outside the conversation earns a spot in it — same space, two different gatekeepers."
arc: concept-explainer
audience: AI engineers and builders who use "context window," "memory," and "RAG" loosely and end up building systems that forget things or drown in noise
mode: autonomous
music: none
---

## Video direction

**Palette system** (from `frame.md`, reused verbatim — atoms are sacred, this composition is new): void-black canvas (`canvas` / `canvas-raised` / `canvas-raised-2`) throughout — no other ground ever appears. `frame.md` was built for a different video ("reverse proxy vs load balancer vs API gateway") but its three-signal-color argument — one fixed color per concept, worn on an edge behavior — maps directly onto this script's own three-way comparison, so the diagram grammar is reused, the diagram's CONTENT is invented fresh for this topic. Three fixed signal colors carry the whole argument and never swap roles: **amber `accent`** = the context window itself / a request for space that just gets granted, no decision involved; **teal `accent-2`** = memory / a choice among several past turns, one (or some) selected to carry forward; **violet `accent-3`** = RAG / a retrieval gated by a query-match check before anything is allowed in. `ink` / `ink-dim` / `ink-faint` for text, `line` for hairlines. `danger` (rose) stays in reserve, unused — nothing in this script is denied or blocked.

**Diagram stage (invented for this video, not the source project's client/proxy/server stage):** a single **CONTEXT WINDOW** node-box is the fixed destination every frame builds toward — the one thing all three concepts put text into. Frame 2 introduces it nearly empty, holding only the live prompt (amber, direct, no gate). Frame 3 reuses the SAME box and adds a second inbound edge from a **PAST TURNS** store, arriving through a **MEMORY** chooser (teal, forks across several past turns, one/some lit). Frame 4 reuses the same box again and adds a third inbound edge from an **EXTERNAL DOCS** store, arriving through a **QUERY** gate (violet, gate-ticks: match → rank → inject). By the end of Frame 4 the CONTEXT WINDOW box visibly holds three distinct layers (prompt / carried-forward history / retrieved doc) — the diagram itself becomes the thesis. This is the same "reuse and extend one stage across the diagram-build frames" law `frame.md` names for its own source project, applied to new content.

**Motion grammar + reveal model:** one continuous "the same window keeps filling" feeling across Frames 2→4, carried by (a) the SAME context-window box reused and extended frame to frame, and (b) `zoom-through` seams between them that read as pushing further into the same schematic. Every reveal is timed to the voiceover — nothing drops in whole at t=0; `power3` long-tail settles everywhere, no bounce/overshoot except a restrained spring-pop on the hook's term flashes and each new node-box's entrance. Diagram edges are built with `svg-path-draw` (they draw as the VO names the behavior); the gate-ticks in Frame 4 resolve one at a time, on their spoken word, never all at once.

**Rhythm:** Frame 5 (the thesis recap) builds to a **stillness-before-climax** hold — the three recap cards land, then everything holds dead still while the "same space, two gatekeepers" line finishes. Frame 7 (CTA) ends on a calm settled hold, this project's real exit. Every other frame keeps developing into its own back half — no diagram frame is allowed to sit static after ~25% of its duration.

**Negative list:** no shadow, no gradient fill, no card glow on a diagram node (hairline + flat only — the one sanctioned glow is the ambient bloom behind Frame 5's held recap and Frame 7's sign-off); no color on an edge/gate-tick other than the three fixed signal colors; no rounded "pill" nodes; no lazy breathing / idle wobble; no front-loaded-then-frozen diagram; nothing (including the caption rail) below y≈1670 on the 1920-tall canvas, nothing load-bearing above y≈150.

**Numerals (hard rule, per `frame.md`):** the only numeral in this script is "five messages ago" (Frame 3, memory). Render exactly that — do not invent token counts, percentages, latency numbers, or document counts anywhere else in the video.

**Approved real entities:** none — every node is a generic labeled box (PROMPT / CONTEXT WINDOW / MEMORY / PAST TURNS / EXTERNAL DOCS / QUERY). No real product names, vendors, or logos.

---

## Frame 1 — The three terms, and what happens if you mix them up

- scene: three terms hard-cut flash across a void-black schematic sheet, each briefly ticked in its own signal color, before the stakes line settles
- voiceover: "Context window, memory, RAG. All three end up putting text in front of the model. But confuse them, and you'll build a system that either forgets everything or drowns in irrelevant context."
- duration: 10.628s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Concept announcement + stakes
- beat: curiosity + tension
- blueprint: kinetic-type-beats (Adapt)
- focal: the three term-words themselves
- roles: term words = foreground subject (hard-cut flashes) · hairline schematic grid = background (dim, ambient) · stakes line = supporting
- sfx: none

narrativeRole: Opens the cognitive gap immediately — names all three terms in one breath, then states the real cost of confusing them, before any single one is explained.
keyMessage: Context window, memory, and RAG all put text in front of the model — but they are not the same thing, and confusing them breaks your system in one of two opposite ways.

Scene 1 (0.0–2.38s): void canvas, faint hairline grid at ~12% alpha. On "Context window, memory, RAG," the three terms hard-cut flash full-bleed in Fraunces `display`, ink, one after another — CONTEXT WINDOW (brief amber underline tick), MEMORY (brief teal tick), RAG (brief violet tick) — centered, ~70% of frame, instant cuts, no fade.
Scene 2 (2.38–4.4s): as "all three end up putting text in front of the model" plays, the three words collapse (scale-swap) into a smaller stacked list, each still carrying its own signal-color tick, sliding to the upper third; a kicker-weight Fraunces italic line "ALL THREE FEED THE SAME MODEL" per-word staggered reveal fades in beneath.
Scene 3 (4.82–10.628s): on "but confuse them, and you'll build a system that either forgets everything or drowns in irrelevant context," a Fraunces `h2` line builds word-by-word beneath the stacked list, splitting into two clauses that land on opposite sides — "forgets everything" (dimming toward `ink-faint`, as if erased) and "drowns in irrelevant context" (crowding/overlapping duplicate ghost-text, as if flooded) — the three stacked terms sit quiet, still ticked, holding for the cut into Frame 2.

---

## Frame 2 — The context window is just the space

- scene: a single CONTEXT WINDOW node-box appears with a token-budget fill bar; the live prompt text flows straight into it on one unbranching amber edge; anything outside the box's boundary fades to ink-faint and is labeled unreachable
- voiceover: "The context window is just the raw space, the token budget for a single call. Whatever's inside it, the model can see, whatever's outside it, the model has never heard of, full stop."
- duration: 10.056s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/02-context-window.html
- type: product_intro
- persuasion: Concretization + progressive disclosure
- beat: clarity + orientation
- blueprint: spatial-pan-stations (Adapt)
- focal: the amber edge from PROMPT into the CONTEXT WINDOW box, and the box's fill bar
- roles: CONTEXT WINDOW node-box = foreground subject · PROMPT node-box = supporting station · faded unreachable content outside the boundary = supporting (dimmed) · hairline grid = background
- sfx: none

narrativeRole: Establishes the context window as the base case and the diagram's anchor stage every later frame extends — a bounded space with a hard edge, nothing more.
keyMessage: The context window is only the raw space available in one call — what's inside it, the model can see; what's outside it, the model has never heard of.

Scene 1 (0.0–4.26s): void canvas + hairline grid. On "the context window is just the raw space, the token budget for a single call," a CONTEXT WINDOW node-box draws in (spring-pop, restrained) center-stage with a mono micro fill-bar beneath it reading "TOKEN BUDGET"; the bar itself is empty/outlined, not yet filled — centered, ~45% of frame.
Scene 2 (4.26–6.6s): on "whatever's inside it, the model can see," a PROMPT node-box draws in to the left; one single amber edge self-draws (svg-path-draw) straight from PROMPT into CONTEXT WINDOW, no branch, no gate; as it lands, the fill bar ticks up partway and the box's interior text becomes legible (ink, full brightness).
Scene 3 (6.6–8.36s): on "whatever's outside it, the model has never heard of," faint ghost text fragments appear scattered outside the box's boundary, immediately fading to `ink-faint` (near-invisible) with a small mono tag "UNREACHABLE" ticking on beside them once, then holding dim.
Scene 4 (8.36–10.056s): on "full stop," the whole composition holds completely still — box, edge, and fill bar frozen mid-fill — a hard, deliberate stop (no further motion, subtle jitter only) that visually enacts the line.

---

## Frame 3 — Memory decides what gets carried forward

- scene: the same CONTEXT WINDOW box from Frame 2 stays on stage; a PAST TURNS store of several message fragments appears beside it, and a MEMORY node (pinned) forks a teal edge across them, lighting the ones it selects, which then draw into the CONTEXT WINDOW alongside the amber prompt edge
- voiceover: "Memory is what decides what from past turns, or past sessions, gets carried forward and re-inserted into that window. Without memory, every new call starts from zero, the model has no idea what you said five messages ago unless something explicitly put it back in."
- duration: 14.788s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/03-memory.html
- type: feature_showcase
- persuasion: Causal chain (A → B → C) + concretization
- beat: comprehension + momentum
- blueprint: fixed-anchor-cycle (Adapt)
- focal: the teal choosing-edge lighting one past turn among several, then feeding into the CONTEXT WINDOW box
- roles: MEMORY node-box = the pinned anchor · PAST-TURN fragments (several small boxes) = cycling candidates · teal edge = foreground signal · CONTEXT WINDOW box (carried over from Frame 2) = the shared destination
- sfx: none

narrativeRole: Extends the SAME stage from Frame 2 by adding the one thing memory does — choosing among past turns — making "decides what gets carried forward" visually literal, then shows the cost of having none.
keyMessage: Memory is the chooser that decides which past turns get pulled back into the context window; without it, every call starts from zero.

Scene 1 (0.0–3.42s): continues Frame 2's held composition (zoom-through arrival, CONTEXT WINDOW box now slightly smaller, upper area of frame). On "memory is what decides," a MEMORY node-box draws in (spring-pop) to the right, pinned in place — a station-label "MEMORY" ticks on in teal mono.
Scene 2 (3.42–7.82s): as "what from past turns, or past sessions, gets carried forward and re-inserted into that window" plays, 4-5 small PAST-TURN fragment boxes draw in beneath MEMORY in a loose row (cluster→outward expansion); a teal edge forks from MEMORY toward all of them, dim at 25%; one at a time, a fragment lights full teal (fixed-anchor-cycle's signature: MEMORY stays pinned, the lit fragment cycles) then that fragment's edge continues on into the CONTEXT WINDOW box, landing beside the still-present amber prompt edge — the box's fill bar ticks up further and a second content layer becomes visible inside it.
Scene 3 (7.82–11.58s): on "without memory, every new call starts from zero, the model has no idea what you said," the teal edge and all past-turn fragments abruptly grey out to `ink-faint` and the CONTEXT WINDOW box's second layer empties back out (reverse-wipe) — a stark before/after within the same shot, dramatizing absence.
Scene 4 (11.58–14.788s): on "five messages ago, unless something explicitly put it back in," a mono index counter ticks up "1… 2… 3… 4… 5" beside the greyed past-turn row (the video's one numeral, rendered exactly as scripted), landing on a small "5" badge that stays visible and dim — held read, subtle jitter only, no further push.

---

## Frame 4 — RAG gates in what the model was never told

- scene: the same stage gains an EXTERNAL DOCS store, clearly separate from the past-turn fragments; a QUERY gate interrupts a violet edge with resolving gate-ticks (match / rank / inject) before it reaches the CONTEXT WINDOW box, which gains a third visible content layer
- voiceover: "RAG isn't about the past conversation at all, it's about knowledge the model was never told in the first place. It retrieves relevant documents from an external source based on the current query, and injects them into the same context window, right alongside the conversation history."
- duration: 14.196s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/04-rag.html
- type: feature_showcase
- persuasion: Progressive disclosure + causal chain (A → B → C)
- beat: comprehension + mastery
- blueprint: agent-progress-theater (Adapt)
- focal: the gate-ticks resolving in sequence on the violet edge, then landing in the CONTEXT WINDOW box beside the memory layer
- roles: EXTERNAL DOCS node-box = foreground subject (visually distinct from Frame 3's past-turn fragments — a separate store, not conversation) · QUERY gate-ticks (MATCH / RANK / INJECT) = the checklist that checks off · violet edge = foreground signal · CONTEXT WINDOW box (carried over) = shared destination, now three-layered
- sfx: none

narrativeRole: This is the video's richest single mechanism — it makes "knowledge the model was never told" concrete by staging retrieval as friction ON the path (a real gate, not a free pass) before the doc is allowed to sit beside the conversation history.
keyMessage: RAG pulls in documents the model was never given, gated by a query match, and lands them in the same context window right alongside whatever memory already carried forward.

Scene 1 (0.0–3.4s): stage carries over from Frame 3 (zoom-through arrival). On "RAG isn't about the past conversation at all, it's about knowledge the model was never told in the first place," an EXTERNAL DOCS node-box draws in on the far side of the stage from the (now dimmed, 25%) past-turn fragments — deliberately distant and visually distinct, labeled in mono, clarifying it is not part of the conversation.
Scene 2 (3.4–7.0s): on "it retrieves relevant documents from an external source based on the current query," a QUERY node ticks on between EXTERNAL DOCS and the CONTEXT WINDOW box; the first gate-tick "MATCH" appears hollow on the edge, then flips filled violet — the request visibly pauses at the tick.
Scene 3 (7.0–11.2s): as "and injects them into the same context window" plays, two more gate-ticks resolve in sequence — "RANK" then "INJECT," each hollow-then-filled exactly on its beat — once INJECT resolves, the violet edge completes into the CONTEXT WINDOW box, adding a third distinct content layer (visually separate from the amber prompt layer and teal memory layer already inside it).
Scene 4 (11.2–14.196s): on "right alongside the conversation history," the camera holds on the now three-layered CONTEXT WINDOW box — prompt (amber) / memory (teal) / retrieved doc (violet) stacked and clearly labeled — while the past-turn fragments brighten back to full visibility beside the new doc layer, landing held, subtle jitter only.

---

## Frame 5 — Same space, two different gatekeepers

- scene: three small recap diagram-cards — Frame 2's amber straight edge, Frame 3's teal fork, Frame 4's violet gate — self-assemble in a vertical stack beside a single small "CONTEXT WINDOW" glyph they all point into, then hold
- voiceover: "So the context window is the space. Memory decides what from the conversation's own history earns a spot in that space. RAG decides what from outside the conversation entirely earns a spot in that same space."
- duration: 12.54s
- transition_in: crossfade
- status: animated
- src: compositions/frames/05-thesis.html
- type: branding
- persuasion: Generalization (specific → principle) + callback
- beat: clarity + resolve
- blueprint: grid-card-assemble (Adapt)
- focal: the three recap cards landing then holding together, all pointed at one shared space glyph
- roles: 3 recap diagram-cards = foreground subject, each in its own fixed signal color · shared CONTEXT WINDOW glyph = the callback anchor · thesis line = supporting · void canvas = background
- sfx: none

narrativeRole: This is the thesis payoff the whole video has been building toward — it names the single space all three concepts share and recaps exactly how each one earns a spot in it, clicking the three diagrams into one frame.
keyMessage: All three concepts point at the exact same space — the context window; what differs is who decides what earns a spot in it: nobody (it's just there), memory (from your own history), or RAG (from outside it).

Scene 1 (0.0–1.58s): void canvas. On "so the context window is the space," a small amber-outlined glyph labeled "CONTEXT WINDOW" draws in and settles upper-center — held small, the callback to Frames 2-4's shared box.
Scene 2 (1.58–5.74s): as "memory decides what from the conversation's own history earns a spot in that space" plays, recap-card 1 (a tiny teal fork glyph, one branch lit) self-assembles (spring-pop, restrained) beneath the CONTEXT WINDOW glyph with a short Fraunces caption "FROM YOUR OWN HISTORY," a thin teal line connecting card to glyph.
Scene 3 (5.74–10.06s): on "RAG decides what from outside the conversation entirely earns a spot in that same space," recap-card 2 (a tiny violet gate-tick glyph) lands beneath card 1 with caption "FROM OUTSIDE IT," a thin violet line connecting it to the same CONTEXT WINDOW glyph.
Scene 4 (10.06–12.54s): once both cards have landed, everything holds completely still — the stillness-before-climax payoff — two lines (teal, violet) both converging on the one amber glyph, silently making the "same space, different gatekeeper" point visual, no further motion beyond a subtle jitter.

---

## Frame 6 — When to reach for which

- scene: three short guidance lines land top-to-bottom, portrait-stacked, each prefixed by its signal-color tick and a mono index number
- voiceover: "You always have a context window, that's just the constraint. Add memory the moment your app needs to remember something across turns or sessions. Add RAG the moment the model needs facts it was never given, from your docs, your database, wherever."
- duration: 13.452s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/06-guidance.html
- type: benefit_highlight
- persuasion: Rule of three + signposting
- beat: confidence + foresight
- blueprint: kinetic-type-beats (Adapt)
- focal: the currently-landing guidance line
- roles: 3 guidance statements = foreground subject, each ticked in its matching signal color · mono index numbers = supporting chrome · void canvas = background
- sfx: none

narrativeRole: Converts the just-landed thesis into a practical decision rule the viewer can act on immediately — the "so what do I actually do" payoff, deliberately plain and list-shaped after the denser diagram and recap frames.
keyMessage: You always have a context window; add memory when your app needs to remember across turns or sessions; add RAG when the model needs facts it was never given.

Scene 1 (0.0–4.26s): void canvas. On "you always have a context window, that's just the constraint," line 1 lands (per-word staggered reveal) at the top, prefixed "01 ·" in amber mono, an amber tick beside "context window" — full-width strip, top third.
Scene 2 (4.26–8.94s): on "add memory the moment your app needs to remember something across turns or sessions," line 2 lands beneath (same mechanic), prefixed "02 ·" in teal mono, a teal tick beside "memory" — the two lines now stack, line 1 dimming slightly (40%) to cede focus.
Scene 3 (8.94–13.452s): on "add RAG the moment the model needs facts it was never given, from your docs, your database, wherever," line 3 lands beneath (same mechanic), prefixed "03 ·" in violet mono, a violet tick beside "RAG" — all three now visible, stacked, line 3 at full brightness, holding still for the cut.

---

## Frame 7 — Comment "guide"

- scene: a short sign-off line settles center-frame, the quoted word "guide" gets one amber emphasis pulse, small mono sub-line beneath
- voiceover: "Comment guide and I'll send over the full breakdown."
- duration: 3.044s
- transition_in: crossfade
- status: animated
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

Scene 1 (0.0–1.36s): void canvas, centered. On "comment," the word COMMENT types on (per-word staggered reveal) in Fraunces `h2`, ink.
Scene 2 (1.36–3.044s): on "guide," the quoted word 'GUIDE' lands beside it with one amber spring-pop + a brief ambient glow bloom (this video's one other sanctioned glow) behind it, in quotes; as "and I'll send over the full breakdown" plays, a small mono sub-line types on beneath: "full breakdown →". The whole card then holds fully still through the trailing silence — this frame's real exit (final frame): a slow, gentle settle, no further motion.
