# SCRIPT: what-happens-after-you-hit-send-on-an-llm

**Voice:** locked / pre-recorded: `audio/what-happens-after-you-hit-send-on-an-llm.wav`, verbatim, source of truth for timing. Sliced per frame into `assets/voice/NN.wav`.
**Voice settings:** n/a. VO_MODE is verbatim/locked; no TTS in this workflow.
**Voice direction:** brisk, plain explainer register.

---

## Line 1 (Frame 1, Hook) 0.00 – 6.36s

    You type a prompt and hit send. In the two seconds before the first word appears, your message goes through six systems.

## Line 2 (Frame 2, Gateway) 6.36 – 12.06s

    First, an API gateway. It checks your key, your rate limit, and how many tokens you're allowed to spend.

## Line 3 (Frame 3, Cache) 12.06 – 21.86s

    Second, a cache lookup. If the start of your prompt matches something the provider has already processed, like a long system prompt, that work gets reused instead of recomputed.

## Line 4 (Frame 4, Router) 21.86 – 28.75s

    Third, a router picks which model and which GPU cluster handles you, based on load and on the model you asked for.

## Line 5 (Frame 5, Batching) 28.75 – 37.36s

    Fourth, a batching queue. Your request waits a few milliseconds so it can share a GPU pass with dozens of others. That's how inference stays affordable.

## Line 6 (Frame 6, Prefill) 37.36 – 43.96s

    Fifth, prefill. The model reads your entire prompt in one parallel pass. This is the pause before the first token.

## Line 7 (Frame 7, Decode) 43.96 – 51.26s

    And sixth, decode. The model generates one token at a time, and each one is streamed back to you the moment it exists.

## Line 8 (Frame 8, Diagnose) 51.26 – 56.16s

    So when an LLM feels slow, ask which of those six steps is slow.

## Line 9 (Frame 9, CTA) 56.16 – 59.01s

    Comment guide and I'll send you the full request path.
