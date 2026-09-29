# SCRIPT — replication-vs-sharding-vs-partitioning

**Voice:** locked voiceover recording (audio/replication-vs-sharding-vs-partitioning.wav) — VO_MODE: verbatim/locked, no TTS
**Voice settings:** n/a — pre-recorded
**Voice direction:** Plain, precise, dev-to-dev — a colleague correcting a common mix-up, not narrating a slide.

---

## Line 1 — The denial (Frame 1)

**Time:** 0.0 – 8.5s

    Replication, sharding, partitioning. Say we need to scale the database and someone will suggest all three like they solve the same problem. They don't.

## Line 2 — Replication (Frame 2)

**Time:** 8.5 – 20.57s

    Replication copies your entire dataset onto multiple servers. Every replica has the same data. It's for availability and read scale — if one node dies, another has everything, and you can spread reads across all of them.

## Line 3 — Partitioning (Frame 3)

**Time:** 20.57 – 33.88s

    Partitioning does the opposite. Instead of copying everything everywhere, you split your data into smaller chunks — by date range, by customer ID, whatever — so no single piece gets too big to manage. It doesn't add copies, it divides the original.

## Line 4 — Sharding (Frame 4)

**Time:** 33.88 – 45.91s

    Sharding is partitioning taken one level further. Each partition doesn't just live on a different table — it lives on a completely different database server. Now write load is split across machines too, not just read load.

## Line 5 — The divide (Frame 5)

**Time:** 45.91 – 55.04s

    So replication solves what if one server dies or gets too many reads. Partitioning and sharding solve what if the dataset itself is too big for one server to hold or write to.

## Line 6 — The punchline (Frame 6)

**Time:** 55.04 – 57.67s

    Different problems, often used together, never interchangeable.

## Line 7 — The guidance list (Frame 7)

**Time:** 57.67 – 70.18s

    Add replication first — almost every production database needs it for availability alone. Partition when a single table gets too large to query efficiently. Shard when write throughput on a single server becomes the actual bottleneck.

## Line 8 — The ask (Frame 8)

**Time:** 70.18 – 73.5s

    Comment guide and I'll send over the full breakdown.
