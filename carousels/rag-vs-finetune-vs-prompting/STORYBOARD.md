---
format: 1080x1080
duration: 12s
message: "RAG vs fine-tuning vs prompting — most people reach for the wrong one first. One question tells you which you actually need."
arc: Hook → The question → Option 1 (Prompting) → Option 2 (RAG) → Option 3 (Fine-tuning) → CTA
audience: AI engineers / builders shipping LLM features on IG + LinkedIn
mode: autonomous
---

## Frame 1 — Cover

- status: built
- src: compositions/frames/01-cover.html
- duration: 2s
- transition_in: cut
- scene: Cream cover, cobalt eyebrow "AI ENGINEERING", h1 "RAG vs Fine-tuning vs Prompting", subhead names the mistake. Treatment: Cover (diagonal panel + dot grid, left-anchored).

Hook. Names all three techniques up front so the swipe payoff is legible from slide 1, then states the premise: most people reach for the wrong one first.

## Frame 2 — The question

- status: built
- src: compositions/frames/02-question.html
- duration: 2s
- transition_in: cut
- scene: Centered blockquote over a faint cobalt quote-mark and concentric rings: "What's actually missing — knowledge, behavior, or instructions?" Cite line below in cobalt uppercase. Treatment: Pull Quote.

The single decision question. Everything after this slide is one branch of the answer.

## Frame 3 — Option 1: Prompting

- status: built
- src: compositions/frames/03-prompting.html
- duration: 2s
- transition_in: cut
- scene: Split + Highlight. Left column — eyebrow "OPTION 1", h2 "Prompting", Inter body defining it. Right — cobalt-tinted highlight block (4px left rule) stating the use-when line. Treatment: Split + Highlight.

Prompting closes an instructions gap: the model already has the knowledge and the right behavior, it just needs clearer direction — format, tone, examples, constraints.

## Frame 4 — Option 2: RAG

- status: built
- src: compositions/frames/04-rag.html
- duration: 2s
- transition_in: cut
- scene: Same Split + Highlight shell as Frame 3, eyebrow "OPTION 2", h2 "RAG". Use-when highlight names the knowledge gap. Treatment: Split + Highlight.

RAG closes a knowledge gap: facts, docs, or data the model was never trained on (or that changed since) — pulled in at query time from a source you control.

## Frame 5 — Option 3: Fine-tuning

- status: built
- src: compositions/frames/05-fine-tuning.html
- duration: 2s
- transition_in: cut
- scene: Same Split + Highlight shell, eyebrow "OPTION 3", h2 "Fine-tuning". Use-when highlight names the behavior gap. Treatment: Split + Highlight.

Fine-tuning closes a behavior gap: the model has the facts but responds the wrong way — retrain it to change tone, structure, or task-specific reasoning.

## Frame 6 — Closing / CTA

- status: built
- src: compositions/frames/06-closing.html
- duration: 2s
- transition_in: cut
- scene: Centered closing over concentric rings. h1 "Pick by the gap, not the hype." Body names the three gaps in one line. Solid cobalt CTA pill: "Comment GUIDE". Treatment: Closing / CTA.

Recap + the brief's exact ask: comment "GUIDE" for the full breakdown.
