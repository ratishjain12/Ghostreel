---
format: 1080x1080
duration: n/a (static carousel — 6 stills, no timeline)
message: "Your agent isn't dumb — its context is. 4 ways context quietly kills agent performance, and the curation habit that fixes it."
arc: listicle
audience: AI/ML engineers building agents
mode: autonomous
music: none
---

## Frame 1 — Cover / Hook

- scene: Cover treatment. Cobalt accent-line + eyebrow "CONTEXT ENGINEERING" above a 2-line near-black h1 hook; diagonal cobalt-tint panel + dot grid on the right third per frame.md's Cover recipe.
- voiceover:
- duration: 4s
- transition_in: cut
- status: built
- src: compositions/frames/01-cover.html
- type: hook
- persuasion: Counterintuitive claim
- beat: curiosity + recognition

narrativeRole: Opens the cognitive gap — reframes "my agent is bad at this" as a context problem, not a model problem.
keyMessage: The performance problem you're debugging is almost always a context problem.

## Frame 2 — Context Poisoning

- scene: Split+Highlight treatment. Eyebrow "01 · CONTEXT POISONING" + h2 + Inter body column beside a cobalt-tint highlight block carrying the one-line fix-callout.
- voiceover:
- duration: 4s
- transition_in: cut
- status: built
- src: compositions/frames/02-poisoning.html
- type: feature_showcase
- persuasion: Causal chain
- beat: recognition

narrativeRole: Names failure mode #1 — a hallucination or wrong tool call enters the transcript and gets treated as ground truth, compounding every turn after.
keyMessage: One bad output, left in context, becomes the foundation for every output after it.

## Frame 3 — Context Distraction

- scene: Split+Highlight treatment. Eyebrow "02 · CONTEXT DISTRACTION" + h2 + body column beside highlight block.
- voiceover:
- duration: 4s
- transition_in: cut
- status: built
- src: compositions/frames/03-distraction.html
- type: feature_showcase
- persuasion: Common-belief vs reality
- beat: recognition + unease

narrativeRole: Names failure mode #2 — as history accumulates, the agent starts echoing its own past actions instead of reasoning about the current instruction.
keyMessage: Past a point, more context doesn't help the agent focus — it pulls focus away from the task in front of it.

## Frame 4 — Context Confusion

- scene: Split+Highlight treatment. Eyebrow "03 · CONTEXT CONFUSION" + h2 + body column beside highlight block.
- voiceover:
- duration: 4s
- transition_in: cut
- status: built
- src: compositions/frames/04-confusion.html
- type: feature_showcase
- persuasion: Demonstration
- beat: recognition

narrativeRole: Names failure mode #3 — irrelevant tools, stale docs, and unrelated examples sitting in the window skew tool choice and output even when unneeded.
keyMessage: A tool or doc doesn't have to be used to do damage — sitting in context unused is enough to skew the next decision.

## Frame 5 — Context Clash

- scene: Split+Highlight treatment. Eyebrow "04 · CONTEXT CLASH" + h2 + body column beside highlight block.
- voiceover:
- duration: 4s
- transition_in: cut
- status: built
- src: compositions/frames/05-clash.html
- type: feature_showcase
- persuasion: Counterexample
- beat: recognition + concern

narrativeRole: Names failure mode #4 — new information contradicts something stated earlier in the transcript, and the agent silently blends both instead of resolving the conflict.
keyMessage: Contradictions in context don't get resolved on their own — they get quietly averaged into a worse answer.

## Frame 6 — Closing / CTA

- scene: Closing/CTA treatment. Accent-line + centered h1 "the fix" + body + one solid cobalt cta-button reading the comment ask, with concentric closing-rings behind.
- voiceover:
- duration: 4s
- transition_in: cut
- status: built
- src: compositions/frames/06-closing.html
- type: cta
- persuasion: Distillation
- beat: resolve + inspiration

narrativeRole: Lands the payoff — the single habit (curation) that prevents all four failure modes — and converts attention into the comment CTA.
keyMessage: Curate context every turn — prune, summarize, remove — and comment "GUIDE" for the full breakdown.
