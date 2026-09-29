# SCRIPT — api-gateway-vs-service-mesh-vs-sidecar-proxy

**Voice:** locked recording (`audio/api-gateway-vs-service-mesh-vs-sidecar-proxy.wav`) — VO_MODE verbatim/locked, per BRIEF.md. Not synthesized by this project; segmented here at paragraph boundaries only, words unchanged. Word-level timing re-derived via `hyperframes transcribe` on the locked wav, aligned back onto the exact script words (the raw ASR pass mis-heard a few terms — "API" as "IP", "sidecar" as "sideguard" — timing kept, text corrected to the source script).
**Voice settings:** n/a (pre-recorded)
**Voice direction:** measured, confident, explanatory — a system-design debrief, matching the account's best-performing pillar (system-design) and hook style (contrarian: "you need all three, not just one").

---

## Line 1 — The three terms, together (Frame 1)

**Time:** 0.07 – 11.38s
**Delivery:** the hook; no warm-up, states the contrarian claim immediately.

    API gateway, service mesh, sidecar proxy. All three sit in the request path of a microservices system, and it's easy to think you only need one. You usually need all three, doing different jobs.

## Line 2 — The API gateway gates (Frame 2)

**Time:** 11.38 – 23.40s
**Delivery:** plain, definitional — the edge/front-door concept.

    An API gateway sits at the edge, the single door external clients come through. It's the one place handling auth, rate limiting, and routing requests to the right service, before anything is internal traffic yet.

## Line 3 — The sidecar proxy forwards (Frame 3)

**Time:** 23.40 – 36.19s
**Delivery:** plain, definitional — the per-instance, local-layer concept.

    A sidecar proxy is a small proxy deployed next to a single service instance, intercepting everything that service sends and receives. It's not about the edge, it's about every individual service having its own local traffic layer.

## Line 4 — The service mesh coordinates (Frame 4)

**Time:** 36.19 – 50.12s
**Delivery:** the densest line — enumerate retries / timeouts / encryption / observability distinctly, don't rush the list.

    A service mesh is what you get when every service has its own sidecar, and a control plane manages all of them together, retries, timeouts, encryption, and observability, for every service-to-service call, consistently, without each team building it themselves.

## Line 5 — Front door vs hallways (Frame 5)

**Time:** 50.19 – 62.48s
**Delivery:** the synthesis / thesis line — land "front door" and "hallways" as the payoff pair.

    So the gateway handles traffic coming into your system from outside. The mesh, built out of sidecars, handles traffic moving between your own services once it's already inside. One's the front door, the other is the hallways.

## Line 6 — When to reach for which (Frame 6)

**Time:** 62.63 – 75.88s
**Delivery:** practical, a beat between the two thresholds.

    You need an API gateway as soon as external clients talk to more than one backend service. Add a service mesh once you have enough internal services that retries, mTLS, and observability between them can't be handled per-team anymore.

## Line 7 — CTA (Frame 7)

**Time:** 76.03 – 78.46s
**Delivery:** warm, direct address, close on "breakdown."

    Comment guide and I'll send over the full breakdown.
