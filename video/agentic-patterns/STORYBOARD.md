---
format: 1080x1920
duration: 73s
message: "Most AI agents are just a for loop with a prompt — here are the 8 patterns that actually make them work."
arc: hook → 4 single-agent patterns → 4 multi-agent patterns → CTA (comment guide)
audience: engineers building or evaluating AI agent systems
mode: autonomous
music: none
---

## Frame 1 — Hook

- scene: Cream ground with a faint circuit-trace motif; an eyebrow names the source, a two-line headline lands, then a smaller sub-line promises the count.
- voiceover: "Most AI agents are just a for loop with a prompt. Here are the eight patterns that actually make them work."
- duration: 5.6s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook

## Frame 2 — Tool Use

- scene: "PATTERN 1 OF 8" tick, "SINGLE-AGENT PATTERN" pill, "01 TOOL USE" label — then a live circuit diagram: MODEL node fires a "call" trace down to a TOOL node, which lights up, then a "result" trace draws back up and MODEL pulses.
- voiceover: "First. Tool use. The model doesn't call functions directly. It emits a structured call, your code runs it, and the result goes back in as a new message."
- duration: 8.76s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-pattern-1.html
- type: feature_showcase

## Frame 3 — ReAct

- scene: THOUGHT / ACTION / OBSERVE nodes on a closed, rounded triangular loop — the one deliberately cyclical diagram in the set — that draws once, then a small dot travels the loop to sell "repeat."
- voiceover: "Second. ReAct. Reason, then act, then observe, and repeat. You can't know what to search next until you see what the last search returned."
- duration: 8.58s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-pattern-2.html
- type: feature_showcase

## Frame 4 — Plan & Execute

- scene: Four STEP nodes appear together on a rail (the plan, drawn upfront), then light up solid one by one left to right (the execution, after the fact).
- voiceover: "Third. Plan and execute. One model plans every step upfront, then just runs the plan. More predictable, less adaptive than ReAct."
- duration: 8.12s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-pattern-3.html
- type: feature_showcase

## Frame 5 — Agentic RAG

- scene: The most elaborate diagram in the set (matching its real complexity): MODEL → RETRIEVE? (a decision node) branches to ANSWER directly ("no") or down to DOCS → ENOUGH? which either loops back to DOCS ("refine") or forward to ANSWER ("yes").
- voiceover: "Fourth. Agentic RAG. The model decides if it even needs to retrieve, what to search. And whether the results are good enough before it answers."
- duration: 8.54s
- transition_in: crossfade
- status: animated
- src: compositions/frames/05-pattern-4.html
- type: feature_showcase

## Frame 6 — Sequential

- scene: DRAFT → REVIEW → FORMAT in a straight line, lighting up strictly one after another — the baton-pass shape, contrasting with Parallel's simultaneous fan-out next.
- voiceover: "Fifth. Sequential. Agents run in a fixed pipeline. Draft, review, format. Each one's output feeding the next."
- duration: 6.52s
- transition_in: crossfade
- status: animated
- src: compositions/frames/06-pattern-5.html
- type: feature_showcase

## Frame 7 — Parallel

- scene: TASK fans out via a bus trace to AGENT A / B / C simultaneously, then a second bus converges them into MERGE — contrasts with Sequential's one-after-another and Router's single path next.
- voiceover: "Sixth. Parallel. Independent agents run at the same time on different pieces of the task, then their outputs get merged."
- duration: 7.8s
- transition_in: crossfade
- status: animated
- src: compositions/frames/07-pattern-6.html
- type: feature_showcase

## Frame 8 — Router

- scene: ROUTER dispatches down a bus that splits three ways to BILLING / TECHNICAL / ACCOUNT — but only ONE trace actually lights and draws; the other two destinations stay dim, unlike Parallel where all three fire.
- voiceover: "Seventh. Router. One agent classifies the task and sends it to whichever specialist actually handles it."
- duration: 5.68s
- transition_in: crossfade
- status: animated
- src: compositions/frames/08-pattern-7.html
- type: feature_showcase

## Frame 9 — Orchestrator-Worker

- scene: MANAGER at the hub with three WORKER nodes around it — each spoke draws out and back (bidirectional), unlike Router's one-way single dispatch.
- voiceover: "Eighth. Orchestrator worker. A manager agent breaks the task down, assigns it to workers, checks their results, and decides what happens next."
- duration: 8.78s
- transition_in: crossfade
- status: animated
- src: compositions/frames/09-pattern-8.html
- type: feature_showcase

## Frame 10 — CTA: Comment guide

- scene: A tick line promises "all 8, with code + failure cases"; "COMMENT GUIDE" lands under a cobalt accent-line and a pill reading "type it below" — holds fully still to the final frame.
- voiceover: "I wrote all eight up with code and the failure cases. Comment guide and I'll send it over."
- duration: 5.062s
- transition_in: crossfade
- status: animated
- src: compositions/frames/10-cta.html
- type: branding
