# SCRIPT — thundering-herd

**Voice:** locked voiceover recording (audio/thundering-herd.wav) — VO_MODE: verbatim/locked, no TTS
**Voice settings:** n/a — pre-recorded
**Voice direction:** Plain, precise, dev-to-dev — a colleague explaining a failure mode, not narrating a slide.

---

## Line 1 — The question (Frame 1)

**Time:** 0.0 – 6.62s

    Ever wonder what happens when your cache entry expires at the exact same moment 10,000 requests hit your server?

## Line 2 — Naming it (Frame 2)

**Time:** 6.62 – 8.76s

    That's the thundering herd problem.

## Line 3 — The trigger (Frame 3)

**Time:** 8.76 – 15.36s

    One cache key expires every request that needed that data, suddenly find it missing all at once.

## Line 4 — The stampede (Frame 4)

**Time:** 15.36 – 20.44s

    So all 10,000 requests go straight to the database to recompute the same value,

## Line 5 — The overload (Frame 5)

**Time:** 20.44 – 27.42s

    your database which was handling light load a second ago, just got hit with 10,000 queries at the same time.

## Line 6 — The fix (Frame 6)

**Time:** 27.42 – 31.82s

    The fix is simple, only one request is allowed to recompute the value,

## Line 7 — The payoff (Frame 7)

**Time:** 31.82 – 35.34s

    every other request waits for that result then reads it from cache.

## Line 8 — The term (Frame 8)

**Time:** 35.34 – 40.6s

    This is usually called request coalescing or a distributed lock around the recompute step.
