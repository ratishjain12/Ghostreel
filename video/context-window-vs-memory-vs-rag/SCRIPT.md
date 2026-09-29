# SCRIPT — context-window-vs-memory-vs-rag

**Voice:** locked recording (`audio/context-window-vs-memory-vs-rag.wav`) — VO_MODE: verbatim/locked. No TTS; this file documents the already-recorded lines and their frame mapping.
**Voice direction:** Plain, direct, explanatory — a builder correcting a common mix-up, not a hype narrator.

---

## Line 1 — The three terms, and what happens if you mix them up (Frame 1)

**Time:** 0.0 – 10.628s

    Context window, memory, RAG. All three end up putting text in front of the model. But confuse them, and you'll build a system that either forgets everything or drowns in irrelevant context.

## Line 2 — The context window is just the space (Frame 2)

**Time:** 10.628 – 20.684s

    The context window is just the raw space, the token budget for a single call. Whatever's inside it, the model can see, whatever's outside it, the model has never heard of, full stop.

## Line 3 — Memory decides what gets carried forward (Frame 3)

**Time:** 20.684 – 35.472s

    Memory is what decides what from past turns, or past sessions, gets carried forward and re-inserted into that window. Without memory, every new call starts from zero, the model has no idea what you said five messages ago unless something explicitly put it back in.

## Line 4 — RAG gates in what the model was never told (Frame 4)

**Time:** 35.472 – 49.668s

    RAG isn't about the past conversation at all, it's about knowledge the model was never told in the first place. It retrieves relevant documents from an external source based on the current query, and injects them into the same context window, right alongside the conversation history.

## Line 5 — Same space, two different gatekeepers (Frame 5)

**Time:** 49.668 – 62.208s

    So the context window is the space. Memory decides what from the conversation's own history earns a spot in that space. RAG decides what from outside the conversation entirely earns a spot in that same space.

## Line 6 — When to reach for which (Frame 6)

**Time:** 62.208 – 75.66s

    You always have a context window, that's just the constraint. Add memory the moment your app needs to remember something across turns or sessions. Add RAG the moment the model needs facts it was never given, from your docs, your database, wherever.

## Line 7 — Comment "guide" (Frame 7)

**Time:** 75.66 – 78.704s

    Comment guide and I'll send over the full breakdown.
