---
format: 1080x1080
message: "Cache-aside vs write-through vs write-behind — the one that's quietly risking data loss surprises most people."
arc: concept-explainer
audience: backend / system-design engineers on Instagram & LinkedIn
mode: autonomous
music: none
---

## Frame 1 — Cover

- scene: Cover treatment. Cobalt diagonal panel + dot grid, right third. Left-aligned hook headline over an accent-line + eyebrow.
- voiceover:
- duration: 3s
- transition_in: cut
- status: built
- src: compositions/frames/01-cover.html
- type: hook
- persuasion: Stakes / consequence
- beat: curiosity + concern

narrativeRole: Opens the carousel on the stakes — three strategies look interchangeable but one of them quietly loses data.
keyMessage: There are three common caching strategies, and one of them can silently lose writes.

## Frame 2 — Cache-Aside

- scene: Split + Highlight treatment. Left column explains the read-through-on-miss mechanic; right highlight block calls out the cold-key cost.
- voiceover:
- duration: 3s
- transition_in: cut
- status: built
- src: compositions/frames/02-cache-aside.html
- type: feature_showcase
- persuasion: Signposting (first the miss, then the backfill)
- beat: orientation + comprehension

narrativeRole: Establishes the baseline pattern everyone already half-knows, so the two writes-focused strategies that follow read as variations on it.
keyMessage: Cache-aside: the app checks the cache first, and only goes to the database — and repopulates the cache — on a miss.

## Frame 3 — Write-Through

- scene: Split + Highlight treatment, same stage as Frame 2 (consistent left-column + right-highlight composition) so the sequence reads as one comparison.
- voiceover:
- duration: 3s
- transition_in: cut
- status: built
- src: compositions/frames/03-write-through.html
- type: feature_showcase
- persuasion: Comparison of two options
- beat: confidence

narrativeRole: Shows the "safe" write strategy — cache and database updated together — as the contrast case for Frame 4's risk.
keyMessage: Write-through writes to the cache and the database in the same request, so the two are never out of sync.

## Frame 4 — Write-Behind

- scene: Split + Highlight treatment, same stage again. The highlight block's callout carries the warning tone (inline negative-colored risk text, per frame.md's directional-chip rule) instead of the neutral tone used in Frames 2–3.
- voiceover:
- duration: 3s
- transition_in: cut
- status: built
- src: compositions/frames/04-write-behind.html
- type: pain_point
- persuasion: Counterexample (here is when it breaks)
- beat: surprise + unease

narrativeRole: Delivers the thesis's payoff — the strategy that looks fastest is the one that can silently drop writes.
keyMessage: Write-behind acknowledges the write before the database has it; if the cache dies before it flushes, that data never existed.

## Frame 5 — The Trade-off

- scene: Bar Ranking treatment. Three labeled cobalt-fill bars — Cache-Aside, Write-Through, Write-Behind — sized to a qualitative Low/Low/High durability-risk read (illustrative ranking, not a fabricated statistic), with inline positive/negative text labels.
- voiceover:
- duration: 3s
- transition_in: cut
- status: built
- src: compositions/frames/05-risk-comparison.html
- type: social_proof
- persuasion: Rule of three
- beat: "aha" + clarity

narrativeRole: Distills the three mechanisms into one glanceable comparison so the risk lands as a structural pattern, not just Frame 4's one example.
keyMessage: Cache-aside and write-through carry low durability risk by construction; write-behind trades that durability for write speed.

## Frame 6 — Closing / CTA

- scene: Closing/CTA treatment. Centered concentric cobalt rings behind a near-black h1 sign-off and the one solid cobalt CTA pill.
- voiceover:
- duration: 3s
- transition_in: cut
- status: built
- src: compositions/frames/06-cta.html
- type: cta
- persuasion: Distillation
- beat: resolve

narrativeRole: Converts the "aha" from Frame 5 into an action — commenting for the full breakdown.
keyMessage: Pick the caching strategy that matches the durability you can actually afford to lose — comment "GUIDE" for the full breakdown.
