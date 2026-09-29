---
format: 1080x1080
duration: n/a — static carousel, no assembled runtime
message: "4 ways systems talk in real time, and the tradeoff each one hides."
arc: listicle
audience: backend/full-stack engineers and system-design learners on IG/LinkedIn
mode: autonomous
music: none
---

## Video direction

**This is a static carousel, not an assembled video.** Every frame below is one independent
still composition — no GSAP timeline, no keyframes, no voiceover, no captions, no
transitions between slides (the platform's swipe gesture is the only "transition"). Motion
is out of scope by `frame.md`'s own design (see its "Known Gaps"); each frame renders one
settled, held layout for its full `data-duration` and is snapshotted at the midpoint.

- **Palette / type** — pull only from `frame.md`: warm cream ground (`#fdfae7`), single
  cobalt accent (`#1e2bfa`), near-black headlines, muted-gray body. Space Grotesk for
  display/numerals/chrome, Inter for body. No second accent color, no invented colors.
- **Safe zone (carries every slide, all four sides)** — keep all content, including chrome
  (progress bar, counter, tag pills), clear of the outer **80px** on every edge so IG's
  rounded corners and LinkedIn's card padding never crop it. This supersedes the pack's
  normal bottom-only caption keep-out — there are no captions here, so the constraint is
  symmetric on all sides instead.
- **Progress / counter chrome** — every content frame (2-6) carries the pack's slide-header
  rhythm (eyebrow + tag-pill) and bottom progress bar per `frame.md`'s "Chrome" convention,
  so the viewer always knows "where am I in the swipe." The cover (1) and closing (7)
  frames use `frame.md`'s cover/closing chrome instead (counter + progress bar, no
  slide-header).
- **Consistent stage** — frames 2-5 (the four methods) share one composition idea: an
  Inter body column beside a cobalt-tinted highlight callout (`frame.md`'s "Split +
  Highlight" treatment), so the run of four reads as one system, not four unrelated
  slides. Each swaps only its label, mechanism copy, and tradeoff callout.
- **Negative list** — no shadows on content, no square corners (save the progress bar), no
  second accent hue, no fabricated numbers/logos (`frame.md`'s "Numerals & Claims" rule —
  none of these frames need a number, so none is invented), no motion/animation of any
  kind, no captions, no off-brand textures.

## Frame 1 — Hook / cover

- scene: cover treatment — the thesis as a two-line headline, left-aligned, under a cobalt
  accent-line, with the diagonal cobalt-tint panel holding the right third
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Direct address + concept announcement
- beat: curiosity

narrativeRole: Opens the cognitive gap — names that there are exactly four ways real-time
systems talk, and that each hides a cost the viewer doesn't usually see.
keyMessage: There are 4 common real-time patterns, and picking one always means trading
something away.

Layout: `frame.md` **Cover** treatment. Cream ground; clipped diagonal cobalt-tint panel on
the right ~36% with the 3×3 cobalt dot grid inside it. Left column: cobalt accent-line (60×4)
above a small cobalt eyebrow ("SYSTEM DESIGN"), then a 2-line Space Grotesk `h1` near-black —
"4 ways systems talk in real time" — then an Inter body sub-line — "…and the tradeoff each
one hides." Bottom-left: counter "1/7" + the persistent cobalt progress bar (bar fill ~1/7
width). Focal: the h1. Roles: h1 = foreground subject; diagonal panel + dot grid =
background; accent-line + eyebrow + sub-line = supporting.

## Frame 2 — Polling

- scene: split + highlight — left column explains the ask-on-a-timer mechanism, right
  highlight card names the tradeoff it hides
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/02-polling.html
- type: feature_showcase
- persuasion: Contrast (mechanism vs. hidden cost) + numbered enumeration ("1/4")
- beat: recognition

narrativeRole: Introduces the first, simplest pattern and immediately pairs it with the
cost it hides, establishing the slide's repeatable "mechanism → tradeoff" rhythm.
keyMessage: Polling is dead simple and works everywhere, but it wastes requests and caps
your latency at the poll interval.

Layout: `frame.md` **Split + Highlight**. Slide-header: cobalt eyebrow "METHOD 1 OF 4" left,
tag-pill "POLLING" right; `h2` "Ask on a timer" below. Left column (Inter body, ~55% width):
3-line mechanism description — client requests on a fixed interval; server answers even
when nothing changed; repeat forever. Right: a cobalt-8%-tint highlight block (4px cobalt
left rule) holding the tradeoff as a short pull-quote-style line: "Hides: wasted requests +
latency capped at your poll interval." Bottom: counter "2/7" + progress bar (~2/7). Focal:
the highlight block. Roles: highlight block = foreground subject; body column = supporting;
slide-header = chrome.

## Frame 3 — Long polling

- scene: split + highlight — same stage as Frame 2, now the server holds the request open
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/03-long-polling.html
- type: feature_showcase
- persuasion: Contrast (mechanism vs. hidden cost) + build-up (one step past polling)
- beat: comprehension

narrativeRole: Shows the natural next step past polling — the same request/response shape,
but held open — and pairs it with the resource cost that improvement introduces.
keyMessage: Long polling cuts latency by holding the request open, but every held-open
request ties up a server connection, and the client must re-ask immediately after each reply.

Layout: identical stage to Frame 2 (`frame.md` **Split + Highlight**, same slide-header
rhythm). Eyebrow "METHOD 2 OF 4", tag-pill "LONG POLLING", `h2` "Ask, then wait". Left
column: client sends one request; server holds it open until there's news (or a timeout);
client immediately re-requests. Right highlight block: "Hides: a held-open connection per
waiting client, and an instant re-request loop." Counter "3/7" + progress bar (~3/7). Focal:
the highlight block. Roles: same as Frame 2.

## Frame 4 — WebSockets

- scene: split + highlight — same stage, now a persistent two-way connection
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/04-websockets.html
- type: feature_showcase
- persuasion: Contrast (mechanism vs. hidden cost) + build-up (full duplex, the strongest form)
- beat: momentum

narrativeRole: Presents the strongest real-time form — instant two-way messaging — and
pairs it with the operational complexity that strength introduces.
keyMessage: WebSockets give you real instant two-way communication, but the connection is
stateful, which complicates scaling — sticky sessions or a pub-sub backplane.

Layout: identical stage to Frames 2-3. Eyebrow "METHOD 3 OF 4", tag-pill "WEBSOCKETS", `h2`
"One open line, both ways". Left column: a single persistent full-duplex connection opens
once; either side pushes messages over it at any time. Right highlight block: "Hides:
stateful connections complicate horizontal scaling — sticky sessions or a pub-sub
backplane." Counter "4/7" + progress bar (~4/7). Focal: the highlight block. Roles: same
pattern as Frames 2-3.

## Frame 5 — Server-Sent Events

- scene: split + highlight — same stage, now one-way server push over plain HTTP
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/05-sse.html
- type: feature_showcase
- persuasion: Contrast (mechanism vs. hidden cost) + counterexample (closes the set of four)
- beat: clarity

narrativeRole: Closes the four-item body with the lightest-weight option, pairing its
HTTP-native simplicity with the one direction it can't cover.
keyMessage: SSE streams events to the client over plain HTTP with built-in reconnect, but
it's one-way only — the client can't push data back on the same channel.

Layout: identical stage to Frames 2-4. Eyebrow "METHOD 4 OF 4", tag-pill "SSE", `h2` "The
server keeps talking". Left column: one long-lived HTTP connection; server streams events;
browser auto-reconnects natively; plays cleanly with existing HTTP infra (caches, proxies).
Right highlight block: "Hides: one-way only — no client-to-server channel on the same
connection." Counter "5/7" + progress bar (~5/7). Focal: the highlight block. Roles: same
pattern as Frames 2-4.

## Frame 6 — The comparison

- scene: dashboard — a 2×2 grid of tinted cards, one per method, each naming its one-line
  tradeoff so the four sit side by side for the first time
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/06-comparison.html
- type: benefit_highlight
- persuasion: Rule of three extended to four + distillation (each tradeoff compressed to
  one line)
- beat: "aha" + orientation

narrativeRole: Lands the payoff of the whole run — seeing all four tradeoffs at once turns
four separate facts into one comparative mental model.
keyMessage: Every real-time pattern trades something for its speed — the right pick depends
on your direction (one-way vs. two-way) and your connection budget.

Layout: `frame.md` **Dashboard** treatment, square variant = 2×2 grid (per its
Aspect-Ratio-Behavior table). Slide-header: eyebrow "THE TRADEOFF, SIDE BY SIDE", `h2`
"Pick your cost". Four tinted metric-cards, one per method (Polling / Long Polling /
WebSockets / SSE), each: Space Grotesk method name (cobalt) + one Inter line naming its
tradeoff (reusing each method frame's "Hides:" line, shortened to fit the card). Counter
"6/7" + progress bar (~6/7). Focal: the 2×2 card grid. Roles: cards = foreground subject;
slide-header = chrome; grid gutter = supporting.

## Frame 7 — Closing / CTA

- scene: closing treatment — centered sign-off line plus the comment-to-unlock CTA pill
- voiceover:
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/frames/07-cta.html
- type: cta
- persuasion: Distillation + direct call to act
- beat: resolve

narrativeRole: Converts the understanding just built into one concrete next action.
keyMessage: Comment "GUIDE" to get the full breakdown of all four patterns.

Layout: `frame.md` **Closing / CTA** treatment. Cream ground + faint concentric cobalt
closing-rings centered behind. Cobalt accent-line above a centered Space Grotesk `h1` —
"Which one is your system using?" — then an Inter body line repeating the CTA verbatim:
"Comment 'GUIDE' for the full breakdown." — then the one solid cobalt `cta-button` pill:
"COMMENT 'GUIDE'". Hashtag line in muted Inter beneath the pill: "#systemdesign
#webdevelopment #api #softwareengineering". Counter "7/7" + full progress bar. Focal: the
h1 + CTA pill pairing. Roles: h1 = foreground subject; CTA pill = foreground subject
(secondary); rings = background; hashtag line = supporting.
