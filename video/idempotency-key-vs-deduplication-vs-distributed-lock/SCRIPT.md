# SCRIPT — idempotency-key-vs-deduplication-vs-distributed-lock

**Voice:** locked recording (`audio/idempotency-key-vs-deduplication-vs-distributed-lock.wav`) — VO_MODE verbatim/locked, per BRIEF.md. Not synthesized by this project; segmented here at paragraph boundaries only, words unchanged. Word-level timing re-derived via `hyperframes transcribe` on the locked wav, aligned back onto the exact script words (the raw ASR pass mis-heard several terms — "idempotency" split/garbled, "deduplication" heard as "dead duplication," "flaky" as "leaky" — timing kept, text corrected to the source script).
**Voice settings:** n/a (pre-recorded)
**Voice direction:** measured, confident, explanatory — a system-design debrief, matching the account's best-performing pillar (system-design) and hook style (contrarian/comparison: "these solve three genuinely different problems").

---

## Line 1 — The three terms, together (Frame 1)

**Time:** 0.0 – 9.72s
**Delivery:** the hook; states the contrarian claim immediately — these are not interchangeable.

    Idempotency key, deduplication, distributed lock. Three ways to stop the same thing from happening twice, and they solve three genuinely different versions of that problem.

## Line 2 — The idempotency key returns the original result (Frame 2)

**Time:** 9.72 – 16.52s (local)
**Delivery:** plain, definitional — client-side, request-level.

    An idempotency key is something the client attaches to a request, a unique ID for that specific logical operation. If the same request gets sent twice, because of a retry, a flaky network, whatever, the server sees the same key and knows to return the original result instead of doing the work again.

## Line 3 — Deduplication skips the repeat message (Frame 3)

**Time:** local segment, 14.75s
**Delivery:** plain, definitional — system-side, message-level.

    Deduplication is the system's own job, not the client's. It's for event and message pipelines, where the same message can arrive more than once through no fault of the sender, and the consumer has to recognize it's already processed that exact message ID and skip it.

## Line 4 — The distributed lock is about concurrency, not duplicates (Frame 4)

**Time:** local segment, 13.48s
**Delivery:** the pivot line — "isn't really about duplicates at all" gets the emphasis.

    A distributed lock isn't really about duplicates at all, it's about concurrency. It makes sure that when multiple processes across multiple machines could all try to do the same critical section of work at the same time, only one of them actually gets to.

## Line 5 — The real distinction (Frame 5)

**Time:** local segment, 14.22s
**Delivery:** the thesis — client side vs consumer side vs colliding processes, each clause gets equal weight.

    So idempotency keys and deduplication both stop the same operation from running twice, one from the client side, one from the consumer side. A distributed lock stops different processes from colliding while doing that operation in the first place.

## Line 6 — When to reach for which (Frame 6)

**Time:** local segment, 18.09s
**Delivery:** practical, a beat between each of the three recommendations.

    Use an idempotency key for any client-initiated write that might get retried, payments especially. Use deduplication in any message or event pipeline where at-least-once delivery is possible. Reach for a distributed lock when multiple workers could pick up the same job simultaneously and you need exactly one of them to win.

## Line 7 — CTA (Frame 7)

**Time:** local segment, 2.53s
**Delivery:** warm, direct address, close on "breakdown."

    Comment guide and I'll send over the full breakdown.
