---
format: 1080x1920
duration: 77s
message: "Retry, circuit breaker, and fallback fire at completely different moments in a failure — not the same thing wearing three names."
arc: Hook → Retry → Circuit Breaker → Fallback → Recap → Guidance → CTA
audience: backend / distributed-systems engineers who already use all three and blur them together
mode: autonomous
music: none
---

## Video direction

**Structure:** concept-explainer (name the three terms up front, reveal each mechanism layer by layer, land the sequence, then practical guidance, then CTA). Locked VO (`VO_MODE: verbatim`) — every `voiceover` line below is the exact locked script text, segmented at sentence/paragraph boundaries only; nothing is paraphrased. Growth-analysis note (autonomous decision, not altering content): this account's best-performing post to date is the same "N related concepts, same position, different job" comparison format with a contrarian hook — this script already IS that format natively (three patterns people treat as one thing, actually firing at different moments), so the hook leans into that existing contrarian framing without inventing anything beyond the script.

**Palette (from `frame.md`, Blue Professional):** warm cream `{colors.bg}` ground on every frame, no exceptions. `{colors.primary}` cobalt is the ONLY accent — eyebrows, step-circles, index tags, accent-lines, card borders/fills, the CTA button. Headlines stay near-black `{colors.text}`; body copy is `{colors.text-muted}` Inter. No second accent color anywhere.

**Motion grammar:** long-tail `power3` eases throughout (smooth, never bouncy). VO-paced reveal model — at each Scene's start only what the voiceover is saying enters; nothing is dumped at t=0. Holds read as stillness (at most a subtle jitter) — never a lazy drift/breathe.

**Rhythm / held-frame allocation:** Frames 2–4 (Retry / Circuit Breaker / Fallback) are the build frames — each mechanism assembles across its full duration, paced to its own VO. Frame 1 (Hook) and Frame 5 (Recap) are the two deliberate held/breather beats — Hook lands its rule-of-three stack and holds before the body begins; Recap resolves its 3-up synthesis and holds before the practical turn. Frame 6 (Guidance) steps through 3 rows in sequence. Frame 7 (CTA) is a short, calm closing hold.

**Negative list:** no drop shadows anywhere (tinted cards only); no gradient fills; no square content corners (progress-bar excepted); no second accent color; no cobalt headlines; no purple-blue "AI" bokeh/glow clichés; no front-loaded-then-frozen frames; no continuous camera drift/breathing during a hold.

**Safe zone (this project's own reel spec, supersedes the generic caption-band default):** nothing load-bearing below y≈1670 or above y≈150 on the 1920-tall canvas; caption rail sits y≈1480–1630.

---

## Frame 1 — Hook

- scene: Three terms land one by one into a vertical stack, then a pivot line undercuts the idea that they're the same thing
- voiceover: "Retry, circuit breaker, fallback. Three resilience patterns that show up together in almost every distributed system, and get used like they're one thing. They fire at completely different moments."
- duration: 10.325s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Concept announcement + Rule of three
- beat: intrigue + recognition
- blueprint: kinetic-type-beats (Adapt)
- focal: the vertical term stack — Retry / Circuit breaker / Fallback
- roles: term stack = foreground subject · "THREE RESILIENCE PATTERNS" eyebrow = supporting chrome · cobalt accent-line ticks = supporting

narrativeRole: Names all three terms together and immediately flags that treating them as interchangeable is the misconception this video corrects.
keyMessage: Retry, circuit breaker, and fallback are usually lumped together — but they are not the same move.

Adapt: keep kinetic-type-beats' in-place stacked-landing signature move; instead of hard-cut token swaps, each term lands once and stays, building a stack rather than replacing.

Scene 1 (0.0–1.5s): cream ground, a faint cobalt dot-grid sits in the top band (~12% opacity, atmosphere). "Retry," lands centered (Space Grotesk h1, near-black), a cobalt accent-line ticks in above it. Centered, ~40% of frame.
Scene 2 (1.5–6.4s): as the VO names the shared pattern ("three resilience patterns that show up together... distributed system,"), "Retry," dims to a small cobalt tag-pill at top and "Circuit breaker," lands beneath the eyebrow "THREE RESILIENCE PATTERNS" — a second stacked line, layer-reveal. Triptych, vertical stack building, ~50% of frame.
Scene 3 (6.4–8.24s): on "and get used like they're one thing," the third term "Fallback." lands, completing the 3-line stack (all near-black, small cobalt tag-pill eyebrows above each); the stack pulses one shared cobalt underline once across all three — layer-reveal + pulse. Triptych stack held, ~55% of frame.
Scene 4 (8.24–10.30s): on "They fire at completely different moments," the shared underline splits into three separate cobalt ticks, one under each term; a small Space Grotesk sub-line lands beneath the stack: "Different moments." Hold on this read — still, subtle jitter at most. Centered stack held to end.

---

## Frame 2 — Retry

- scene: A slide-header names the pattern, then a request timeline draws itself: fail, wait, retry
- voiceover: "A retry just tries again. A request fails, you wait a bit, maybe with backoff, and send it again, betting the failure was transient, a blip, not a real outage."
- duration: 9.899s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-retry.html
- type: feature_showcase
- persuasion: Progressive disclosure + Concretization
- beat: comprehension
- blueprint: compose
- focal: a horizontal request timeline strip
- roles: step-circle "1" (cobalt filled) = foreground subject · slide-header (eyebrow RETRY + tag-pill "1 / 3") = supporting chrome · timeline strip = supporting mechanism · split-highlight card = supporting evidence

narrativeRole: Defines retry as the simplest, cheapest response — just try again, betting on a transient blip.
keyMessage: A retry is a bet that the failure was momentary, not a real outage.

Scene 1 (0.0–1.05s): cream ground. Slide-header lands: cobalt step-circle "1" filled top-left + eyebrow "RETRY" + h2 "Just tries again." near-black. Asymmetric 60/40, upper zone.
Scene 2 (1.05–3.16s): on "A request fails, you wait," a thin cobalt-8%-track timeline strip begins drawing left to right beneath the header; a cobalt node marked "request" appears, then a second node "fails" lands on the strip. Full-width strip, ~40% of frame.
Scene 3 (3.16–5.80s): on "a bit, maybe with backoff, and send it again," the strip pauses at a visibly gapped segment labeled "wait + backoff," then a fresh cobalt tick "retry sent" lands further along the strip. Layer-reveal, same strip.
Scene 4 (5.80–9.86s): on "betting the failure was transient, a blip, not a real outage," a split-highlight card slides in from the right with a 4px cobalt left-rule carrying "betting the failure was transient — a blip, not a real outage" in Inter body; the timeline strip dims to ~30% behind it. Split, card ~55% of frame, held to end.

---

## Frame 3 — Circuit Breaker

- scene: The header names the pattern, then a three-state sequence builds: watching, trips, cooldown
- voiceover: "A circuit breaker is what stops you from retrying forever into a dependency that's actually down. It watches the failure rate, and once it crosses a threshold, it trips, blocking new requests to that service entirely for a cooldown period. It protects the failing service from being hammered, and protects you from wasting time on calls that will fail anyway."
- duration: 18.091s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-circuit-breaker.html
- type: feature_showcase
- persuasion: Causal chain + Progressive disclosure
- beat: comprehension → mastery
- blueprint: compose
- focal: a 3-slot state sequence — Watching / Trips / Cooldown
- roles: step-circle "2" (cobalt filled) = foreground subject · slide-header (eyebrow CIRCUIT BREAKER + tag-pill "2 / 3") = supporting chrome · 3-slot state row (opacity-fade sequence) = supporting mechanism · split-highlight card = supporting evidence

narrativeRole: The video's dense exception — walks the full trip/cooldown mechanism as one continuous evolving build, since this is the longest and most causal of the three patterns.
keyMessage: A circuit breaker stops you from retrying into something that's actually down by tripping open for a cooldown period.

Scene 1 (0.0–4.59s): cream ground. Slide-header lands: cobalt step-circle "2" filled + eyebrow "CIRCUIT BREAKER" + h2 "Stops you retrying into something that's actually down." Asymmetric 60/40, upper zone.
Scene 2 (4.59–8.22s): on "It watches the failure rate, and once it crosses a threshold, it trips," a 3-slot step-circle row begins below the header: slot 1 "WATCHING" lands filled cobalt (opacity 1.0), and a thin cobalt bar-track fills left-to-right beside it as the failure rate rises. Full-width strip, ~40% of frame.
Scene 3 (8.22–11.77s): on "blocking new requests to that service entirely for a cooldown period," slot 2 "TRIPPED" lands (opacity 0.85, cobalt fill) and the bar-track locks/dims to ~8% to show blocked traffic; slot 3 "COOLDOWN" ticks in faded (opacity 0.7), completing the 3-state row. Layer-reveal, same strip.
Scene 4 (11.77–18.08s): on "It protects the failing service from being hammered, and protects you from wasting time on calls that will fail anyway," the state row dims to ~30% as background; a split-highlight card slides in with a 4px cobalt left-rule carrying "protects the failing service — and protects you from wasting time on calls that will fail anyway" in Inter body. Split, card ~55% of frame, held to end.

---

## Frame 4 — Fallback

- scene: The header names the pattern, then three option chips land — cached data, default value, degraded response
- voiceover: "A fallback is what you do instead, once retry has given up or the breaker is open. Return cached data, a default value, a degraded response, anything that keeps the system usable instead of returning an error."
- duration: 12.203s
- transition_in: cut
- status: animated
- src: compositions/frames/04-fallback.html
- type: feature_showcase
- persuasion: Concretization + Numbered enumeration
- beat: comprehension
- blueprint: compose
- focal: 3 tinted option chips — cached data / default value / degraded response
- transition_note: transition_in changed from crossfade to cut post-build — frames 3 and 4 share the identical top-left step-circle position (consistent-stage continuity), so a crossfade double-exposed "2" over "3" for 0.5s (caught by `npm run check`'s Layout content_overlap finding at t=38.55s)
- roles: step-circle "3" (cobalt filled) = foreground subject · slide-header (eyebrow FALLBACK + tag-pill "3 / 3") = supporting chrome · 3 option chips = supporting enumeration

narrativeRole: Defines fallback as the last resort — what actually keeps the system usable once the first two patterns have run out.
keyMessage: A fallback swaps in something usable (cache, default, degraded response) instead of surfacing an error.

Scene 1 (0.0–4.23s): cream ground. Slide-header lands: cobalt step-circle "3" filled + eyebrow "FALLBACK" + h2 "What you do instead." Asymmetric 60/40, upper zone.
Scene 2 (4.23–6.62s): on "Return cached data, a default value," the first tinted chip "cached data" lands left, then the second chip "default value" lands beside it — tinted cards, cobalt 4% fill / 20% border, no shadow. Triptych row forming, left-to-right stagger.
Scene 3 (6.62–8.56s): on "a degraded response," the third chip "degraded response" lands, completing the 3-chip row. Triptych row complete.
Scene 4 (8.56–12.24s): on "anything that keeps the system usable instead of returning an error," the 3 chips settle to ~85% opacity as a closing line lands beneath them in Inter body: "anything that keeps the system usable instead of returning an error." Centered, held to end.

---

## Frame 5 — Recap

- scene: Three cards land in sequence — retry handles the blip, circuit breaker the outage, fallback what the user sees
- voiceover: "So the real sequence is, retry handles the blip, the circuit breaker handles the outage, and the fallback handles what the user actually sees while all of that is happening."
- duration: 10.155s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/05-recap.html
- type: branding
- persuasion: Distillation + Rule of three
- beat: clarity + "now I get it"
- blueprint: titlecard-reveal (Adapt)
- focal: 3 tinted cards, one per pattern, landing to a held 3-up row
- roles: 3 cards = foreground subject, equal weight · "THE REAL SEQUENCE" eyebrow = supporting chrome

narrativeRole: Distills the whole video into the one line the viewer should leave with — the sequence, not just the definitions.
keyMessage: Retry handles the blip, the circuit breaker handles the outage, and the fallback handles what the user actually experiences.

Scene 1 (0.0–1.12s): cream ground. Eyebrow "THE REAL SEQUENCE" lands top-center with a cobalt accent-line. Centered, low density.
Scene 2 (1.12–2.74s): on "retry handles the blip," card 1 lands — cobalt tag "RETRY" + "handles the blip," tinted card, no shadow. Dashboard 3-up forming, card 1 of 3.
Scene 3 (2.74–5.40s): on "the circuit breaker handles the outage," card 2 lands beside/below card 1 — "CIRCUIT BREAKER" + "handles the outage." Dashboard row, card 2 of 3.
Scene 4 (5.40–10.03s): on "and the fallback handles what the user actually sees while all of that is happening," card 3 lands — "FALLBACK" + "handles what the user actually sees" — completing the 3-up row; all three hold together, still. Dashboard complete, held to end.

---

## Frame 6 — Guidance

- scene: Three "add this" statements land top to bottom, each with a small cobalt index tag
- voiceover: "Add retries for calls that can genuinely fail transiently, like a flaky network blip. Add a circuit breaker around any dependency that can go down for real, so you're not making things worse. Add a fallback wherever a failure would otherwise be user-facing."
- duration: 13.568s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/06-guidance.html
- type: benefit_highlight
- persuasion: Numbered enumeration + Rule of three
- beat: confidence
- blueprint: compose
- focal: 3 stacked statement rows, each with a cobalt index tag
- roles: index tags "01 / 02 / 03" = supporting chrome · statement lines = foreground subject, landing in sequence

narrativeRole: Turns the three definitions into three concrete actions the viewer can apply.
keyMessage: Add a retry for transient blips, a circuit breaker for real outages, a fallback wherever failure would otherwise reach the user.

Scene 1 (0.0–4.15s): cream ground. Row 1 lands top: cobalt index tag "01" + statement "Add retries for calls that can genuinely fail transiently." Stacked list, top third.
Scene 2 (4.15–9.45s): row 1 dims to ~55%; row 2 lands: index tag "02" + "Add a circuit breaker around any dependency that can go down for real." Stacked list, middle third.
Scene 3 (9.45–13.44s): row 2 dims to ~55%; row 3 lands: index tag "03" + "Add a fallback wherever a failure would otherwise be user-facing." All 3 rows hold, row 3 at full emphasis. Stacked list complete, held to end.

---

## Frame 7 — CTA

- scene: The CTA button lands center on a calm closing ground, a short sub-line follows
- voiceover: "Comment guide and I'll send over the full breakdown."
- duration: 2.475s
- transition_in: cut
- status: animated
- src: compositions/frames/07-cta.html
- type: cta
- persuasion: Direct address
- beat: resolve
- blueprint: titlecard-reveal (Reproduce)
- focal: cta-button pill "Comment GUIDE"
- roles: cta-button = foreground subject · concentric closing-rings = supporting atmosphere

narrativeRole: The closing ask — turns the explanation into an action the viewer can take right now.
keyMessage: Comment "GUIDE" to get the full breakdown.

Scene 1 (0.0–1.23s): cream ground + faint concentric cobalt closing-rings behind. Cta-button pill spring-pops in center: "Comment GUIDE," cobalt fill, cream text. Centered.
Scene 2 (1.23–2.40s): on "over the full breakdown," a small Inter sub-line lands beneath the button: "and I'll send the full breakdown." Hold, still — rings barely alive, subtle jitter at most.
