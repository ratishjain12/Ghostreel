# SCRIPT — async-is-not-parallel

**Voice:** locked recording (`audio/async-is-not-parallel.wav`, split per frame into `assets/voice/NN.wav`). No TTS.
**Voice settings:** n/a (verbatim / locked VO)
**Voice direction:** Fast, direct, conversational engineer-to-engineer.

---

## Line 1 — Hook (Frame 1)

**Time:** 0.00 – 8.12s

    You rewrite an API handler with async and it goes from four hundred milliseconds to forty. Then you add one line and it's back to four hundred. Here's why.

## Line 2 — Written normally (Frame 2)

**Time:** 8.12 – 13.71s

    The handler makes three network calls. Written normally, it waits for each one before starting the next.

## Line 3 — The waiting overlaps (Frame 3)

**Time:** 13.71 – 19.27s

    With async, it starts all three and waits while they're in flight. The waiting overlaps.

## Line 4 — Concurrency (Frame 4)

**Time:** 19.27 – 23.20s

    That's concurrency: one worker juggling many tasks that are mostly waiting.

## Line 5 — Pure computation (Frame 5)

**Time:** 23.20 – 28.17s

    Now you add a function that resizes an image. That's not waiting, that's pure computation.

## Line 6 — Stuck behind it (Frame 6)

**Time:** 28.17 – 36.90s

    An async event loop runs on a single thread, so while it's resizing, nothing else can move. Every other request on that server is stuck behind it.

## Line 7 — Parallelism (Frame 7)

**Time:** 36.90 – 46.22s

    Running work at the same instant needs parallelism: multiple CPU cores working at once. That means a worker pool, separate processes, or a background queue.

## Line 8 — The rule (Frame 8)

**Time:** 46.22 – 53.15s

    So the rule is simple. Async helps when your code is waiting on something. Parallelism helps when your code is computing something.

## Line 9 — Slower, not faster (Frame 9)

**Time:** 53.15 – 55.96s

    Mix them up, and async makes things slower, not faster.

## Line 10 — CTA (Frame 10)

**Time:** 55.96 – 59.14s

    Comment guide and I'll send you the full breakdown.
