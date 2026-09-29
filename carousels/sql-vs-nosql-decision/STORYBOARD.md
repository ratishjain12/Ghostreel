---
format: 1080x1080
duration: 42s
message: "SQL vs NoSQL, decided in 5 questions instead of a religious war."
arc: listicle
audience: backend/system-design engineers choosing a database for a new service
mode: autonomous
---

## Frame 1 — Cover

- scene: Cream cover, cobalt diagonal accent panel right third (steeper cut, further right), 3x3 cobalt dot grid. Eyebrow "SYSTEM DESIGN" over accent-line, bold-claim h1 "SQL vs NoSQL isn't a religious war." near-black, sub-line "It's 5 questions, answered in order." Bottom-right swipe cue: "SWIPE" label + arrow.
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/01-cover.html
- type: hook
- persuasion: Concept announcement + Direct address
- beat: curiosity
- blueprint: compose

narrativeRole: Opens the gap — reframes a tribal debate as a short, answerable checklist.
keyMessage: The SQL vs NoSQL choice reduces to five concrete questions.

## Frame 2 — Question 1: Data shape

- scene: Split + Highlight. Left: eyebrow "QUESTION 1 OF 5", h2 "Does your data have a fixed shape?" and one line of body copy. Right: cobalt-tinted highlight block contrasting "Fixed, well-known relationships -> SQL" against "Shape keeps changing -> NoSQL".
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/02-question-1.html
- type: feature_showcase
- persuasion: Frame-then-fill + Contrast
- beat: orientation

narrativeRole: First filter in the framework — schema rigidity decides the starting lean.
keyMessage: A stable, known schema favors SQL; a shape that keeps mutating favors NoSQL.

## Frame 3 — Question 2: Transactions

- scene: Mirrored Split + Highlight. Highlight card now on the LEFT (full cobalt border, rounded, no accent-bar), with a circular cobalt "VS" badge replacing the row divider. Eyebrow "QUESTION 2 OF 5", h2 "Do several rows need to change together, atomically?" stay top-of-frame; body copy moves to the RIGHT column. Card: "Need ACID across rows -> SQL" vs "Fine with eventual consistency -> NoSQL".
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/03-question-2.html
- type: feature_showcase
- persuasion: Worked example + Contrast
- beat: comprehension

narrativeRole: Second filter — consistency guarantees needed by the write path.
keyMessage: Multi-row atomicity requirements point to SQL; independent writes tolerate NoSQL.

## Frame 4 — Question 3: Query pattern

- scene: Full-width two-column card beneath the header/body (not a side stack). Eyebrow "QUESTION 3 OF 5", h2 "How will you actually query it?", body copy left as usual. Below: one wide card split by a vertical divider — SQL column (icon + tag + line) on the left half, NoSQL column on the right half: "Joins across entities -> SQL" vs "Lookups by one key/document -> NoSQL".
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/04-question-3.html
- type: feature_showcase
- persuasion: Comparison of two options
- beat: comprehension + momentum

narrativeRole: Third filter — the shape of the read path, not just the write path.
keyMessage: Relational joins favor SQL; single-key access patterns favor NoSQL.

## Frame 5 — Question 4: Scale trajectory

- scene: Mirrored Split + Highlight. Highlight card on the LEFT with a dashed cobalt border and a small solid-cobalt "THE TRADE-OFF" corner tag sitting on its top edge; body copy on the RIGHT. Card: "Vertical scaling is enough -> SQL" vs "Need to shard across many machines -> NoSQL".
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/05-question-4.html
- type: feature_showcase
- persuasion: Causal chain
- beat: foresight

narrativeRole: Fourth filter — where the system needs to be in a year, not just today.
keyMessage: Comfortable vertical growth favors SQL; anticipated horizontal sharding favors NoSQL.

## Frame 6 — Question 5: Team fluency

- scene: Climax treatment before the CTA. Left: eyebrow "QUESTION 5 OF 5", h2 "What can your team operate confidently at 3am?". Right: enlarged, bold solid-cobalt-bordered card with a soft cobalt "spotlight" disc behind the balance-scale icon, "Tie-breaker" tag, and centered line: "The tie-breaker: operational familiarity beats the theoretically-better option."
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/06-question-5.html
- type: feature_showcase
- persuasion: Anchoring on a familiar referent
- beat: confidence

narrativeRole: Closes the checklist with the practical tie-breaker when the first four are close.
keyMessage: When it's genuinely close, pick the database your team can debug under pressure.

## Frame 7 — Closing / CTA

- scene: High-impact treatment, full solid-cobalt background (the one slide that breaks from the cream canvas), concentric cream-tint rings behind center, recolored 5-check row callback. Accent-line, eyebrow "BEFORE YOU SCROLL ON", h1 "Save this. Follow for more.", sub-line "A repeatable framework beats a religious war every time." Two side-by-side button-shaped CTAs: a filled cream "Save this" button with a bookmark icon, and a cream-bordered "Follow @ratish.ai" button with a profile-plus icon. Caption beneath: "For more system design breakdowns."
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/07-closing.html
- type: cta
- persuasion: Distillation + direct dual ask (save + follow)
- beat: resolve

narrativeRole: Converts the checklist into two concrete actions — save the framework, follow for more.
keyMessage: Save this for your next stack decision, and follow @ratish.ai for more system design breakdowns.
