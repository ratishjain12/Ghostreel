---
version: alpha
name: Signal Path — Frame (video / frame layer)
description: >
  Bespoke design system for "Reverse proxy vs load balancer vs API gateway" — a dark
  network-schematic / blueprint language where the diagram IS the argument. One flat
  void-black canvas, hairline circuit rules, boxes-and-edges built from CSS/SVG, and
  three named signal colors that map 1:1 to the video's three concepts: amber = a
  request simply FORWARDING, teal = a request being ROUTED to a chosen destination,
  violet = a request being GATED through policy checks before it's allowed to continue.
  Fraunces (a characterful serif) carries every display statement against IBM Plex Sans
  body copy and IBM Plex Mono chrome/labels/data — a serif-headline + monospace-label
  pairing deliberately unlike a typical dev-tool sans-only look. Composition is free;
  the atoms (palette, ramp, hairline-only depth, sharp corners) are sacred.
unit: the frame — 1080×1920 (9:16 reel) primary; 1920×1080 and 1080×1080 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  canvas: "#0A0D12"
  canvas-raised: "#12161C"
  canvas-raised-2: "#181D24"
  ink: "#EDEFF3"
  ink-dim: "#8992A1"
  ink-faint: "#4A525E"
  line: "#232B33"
  line-strong: "#2E3742"
  accent: "#FF9F45"
  accent-2: "#4DE8C2"
  accent-3: "#B98CFF"
  danger: "#FF5C7A"

borders: { hairline: "1px solid line", hairline-strong: "1px solid line-strong", node: "1.5px solid ink-dim@40%" }
shadows: { none: "none (flat plane — no shadow anywhere)" }

typography:
  # — reading + chrome ramp (IBM Plex Sans body, IBM Plex Mono chrome/data) —
  body:      { fontFamily: "IBM Plex Sans", cqw: 1.5, weight: 400, lineHeight: 1.5 }
  lead:      { fontFamily: "IBM Plex Sans", cqw: 2.0, weight: 400, lineHeight: 1.5 }
  label:     { fontFamily: "IBM Plex Mono", cqw: 1.1, weight: 500, tracking: "0.14em", upper: true }
  node-tag:  { fontFamily: "IBM Plex Mono", cqw: 1.3, weight: 500, tracking: "0.04em" }
  micro:     { fontFamily: "IBM Plex Mono", px: 20, weight: 500, tracking: "0.16em", upper: true }
  status:    { fontFamily: "IBM Plex Mono", cqw: 1.2, weight: 500, tracking: "0.06em" }
  # — display ramp (Fraunces, sentence case, tight, the video's one expressive voice) —
  kicker:      { fontFamily: "Fraunces", cqw: 2.0, weight: 500, italic: true, lineHeight: 1.1 }
  h3:          { fontFamily: "Fraunces", cqw: 3.2, weight: 600, lineHeight: 1.15 }
  h2:          { fontFamily: "Fraunces", cqw: 4.4, weight: 600, lineHeight: 1.08, tracking: "-0.01em" }
  h1:          { fontFamily: "Fraunces", cqw: 6.6, weight: 600, lineHeight: 1.0, tracking: "-0.015em" }
  display:     { fontFamily: "Fraunces", cqw: 9.5, weight: 600, lineHeight: 0.96, tracking: "-0.02em" }
  display-italic: { fontFamily: "Fraunces", cqw: 8.0, weight: 500, italic: true, lineHeight: 1.0, tracking: "-0.01em" }
  number-hero: { fontFamily: "Fraunces", cqw: 10.5, weight: 600, lineHeight: 0.94, tracking: "-0.02em" }

spacing:
  pad-x: "6cqw"
  pad-y: "5cqw"
  gap-lg: "3.5cqw"
  gap-md: "2cqw"
  gap-sm: "1cqw"
  radius-sm: "4px"
  radius-md: "8px"
  hairline: "1px"

components:
  node-box:
    backgroundColor: "{colors.canvas-raised}"
    border: "1.5px solid {colors.ink-dim}@40%"
    rounded: "{spacing.radius-sm}"
    typography: "{typography.node-tag}"
    description: "A diagram box — client / proxy / server / service. Sharp-ish corners (4px), hairline border, no fill gradient, no shadow. The label sits inside in mono, uppercase micro caption below it (role)."
  edge-forward:
    stroke: "{colors.accent}"
    style: "solid 3px, single path, no branch"
    description: "The reverse-proxy signature: ONE path in, ONE path out. A request simply forwards — the edge never splits and nothing gates it."
  edge-choose:
    stroke: "{colors.accent-2}"
    style: "solid 3px, ONE path branches into 2-4, exactly one lit at a time"
    description: "The load-balancer signature: the edge forks toward several destination nodes; per beat, exactly one branch is lit (the chosen destination), the rest sit dim at 25%."
  edge-gate:
    stroke: "{colors.accent-3}"
    style: "solid 3px, interrupted by 1-4 gate-ticks before continuing"
    description: "The API-gateway signature: the edge is interrupted by small perpendicular gate-ticks (auth / rate-limit / transform / route) that must resolve (flip from hollow to filled) before the path continues onward. The request visibly WAITS at the gate."
  gate-tick:
    shape: "a short perpendicular tick or small square badge sitting ON the edge"
    states: "hollow (pending, ink-dim) → filled (checked, accent-3) with its label in mono micro"
    description: "One policy check. Never a full card — a small mark directly on the path, so policy reads as friction on the SAME line, not a separate panel."
  station-label:
    typography: "{typography.label}"
    color: "{colors.ink-dim}"
    description: "A small mono uppercase tag pinned near a node (CLIENT / PROXY / ORIGIN / GATEWAY) — chrome, not narration."
  hairline-grid:
    stroke: "{colors.line}@10-16%"
    description: "An extremely faint fixed-pitch grid across the canvas — the one ambient texture, evokes graph paper / a schematic sheet. Never brighter than 16% alpha."
  console-caption:
    description: "This project's caption treatment — see frame's caption-skin. A slim monospace 'log line' rail, not a rounded karaoke pill."
---

# Signal Path — Frame (video / frame layer)

## Overview

Signal Path is a **network-schematic / blueprint system**: the video's whole argument is
"these three things sit in the same place in the request path but do different amounts
of work to it," so the frame's job is to make that difference **visually literal** —
boxes (client / proxy / servers) connected by edges, where the EDGE ITSELF changes
character per concept. There is no cream, no paper, no light mode: the canvas is a
**void-black schematic sheet** (`{colors.canvas}`) with an almost-invisible hairline
grid, so every lit edge and node reads like a signal on a dark board.

**The three signal colors are the whole thesis, worn as color:**

- **Amber (`{colors.accent}`)** — a reverse proxy: the edge just **forwards**. One line in, one line out, nothing branches, nothing gates.
- **Teal (`{colors.accent-2}`)** — a load balancer: the edge **forks and chooses** — several possible destinations, one lit branch per beat.
- **Violet (`{colors.accent-3}`)** — an API gateway: the edge is **interrupted by gate-ticks** (auth, rate limit, transform, route) that must resolve before the request continues.

Every frame that shows a diagram reuses these exact three colors for these exact three
roles — never swapped, never used for anything else. A rare fourth, rose (`{colors.danger}`),
exists only for a blocked/denied request at the gate.

**Type is a two-voice system:** **Fraunces** (a warm, slightly idiosyncratic serif with
real character) carries every big statement — the hook words, the thesis line, the CTA —
at sentence case with tight negative tracking, so the video reads as an argued essay, not
a slide deck. **IBM Plex Sans** carries any longer reading copy. **IBM Plex Mono** is the
diagram's own voice — node tags, station labels, gate-tick labels, status readouts, and
the caption rail — because a monospace grid is what a request log / schematic actually
looks like. Display serif for the THESIS, mono for the MACHINERY.

**Key characteristics at frame scale:**

- **Void-black canvas**, near-invisible hairline grid — one texture, never brighter than 16% alpha.
- **Three signal colors, fixed roles**: amber = forward, teal = choose, violet = gate. Never remapped, never combined loosely.
- **Diagrams are boxes + edges**, built in CSS/SVG — sharp 4px corners, 1.5px hairline node borders, zero shadow, zero gradient fill.
- **Fraunces sentence-case display** (the argued-essay voice) + **IBM Plex Sans** body + **IBM Plex Mono** chrome/diagram-labels/captions.
- **The build IS the teaching** — an edge assembles, forks, or gates on-screen as the voiceover names that behavior; nothing is a static finished diagram dropped in whole.
- **Low density outside the diagram** — let the schematic breathe; chrome (station labels, mono tags) stays quiet and small.

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — the diagram's ONE lit edge (or the frame's one display statement) dominates; everything else reads as quiet schematic chrome.
- **Signal discipline** — amber/teal/violet never appear together doing the SAME job in one frame; each frame's beat commits to the one signal color its concept owns (recap frames may show all three side by side, each still in its own lane).
- **Flat + hairline** — zero shadow, zero gradient fill, zero blur-glow except the sanctioned ambient bloom behind a held hero; borders are always 1-1.5px hairlines.

- **Primary:** 1080×1920 (9:16 reel). **Landscape:** 1920×1080. **Square:** 1080×1080 (documented, not primary for this project).
- **Safe area:** this project's own reel safe zone — nothing (including the caption band) below **y ≈ 1670** (last ~250px) on the 1920-tall canvas, and no load-bearing content above **y ≈ 150** (top chrome). Content plans into **y ≈ 150–1480**; the caption rail sits at **y 1480–1630**, itself clear of the 1670 line.
- **The container law (load-bearing).** Every frame ground sets `container-type: size`; all frame-relative units are `cqw`/`cqh` against it — never `vw`.

## Colors

Tokens identical to the source. Ground is always `{colors.canvas}`; a diagram's boxes and
any card-like surface sit on `{colors.canvas-raised}` / `{colors.canvas-raised-2}` (a half-step
lighter panel, never a hard light patch). Text is `{colors.ink}` primary / `{colors.ink-dim}`
secondary / `{colors.ink-faint}` chrome-only. The three signal colors (`accent` amber /
`accent-2` teal / `accent-3` violet) are reserved for the diagram's edges, gate-ticks, and the
matching word emphasis in captions/type — never decorative. `{colors.danger}` (rose) is the
one exception color, for a denied/blocked request only.

## Typography

Two ramps. The **reading/chrome ramp** (IBM Plex Sans `body` 1.5cqw / `lead` 2.0cqw; IBM
Plex Mono `label`/`node-tag`/`status` for diagram chrome) carries copy and diagram labels;
the **display ramp** (Fraunces `h3` 3.2cqw → `display` 9.5cqw, weight 500-600, sentence
case, negative-tracked) carries every hook word, thesis line, and CTA.

- **Legibility floor:** any load-bearing line ≥ 1.4cqw; mono micro labels are chrome only.
- **Fraunces is sentence case**, never uppercase, weight 500 (italic kicker) or 600 (everything else); reach for **`display-italic`** for a single reflective/aside line. **IBM Plex Mono chrome is uppercase**, 0.06-0.16em tracked.

## Depth & Surface

Flat plane, hairline-only. No box-shadow, no elevation, no gradient fill on a node or
card — a node's only "lift" is its 1.5px hairline border against the void canvas. The
**one sanctioned glow** is a soft ambient bloom (`ambient-glow-bloom`) behind a held hero
number or the final brand mark — never on a diagram node (nodes stay flat and precise).

## Shapes

- **4px** node-box corners, **8px** any larger card/panel. Never a true pill, never a circle save a gate-tick dot or a small connector node. Sharp, drafted, schematic — not soft.

## Components

- **node-box** — client/proxy/server/service boxes. **edge-forward** / **edge-choose** / **edge-gate** — the three signature edge behaviors (this is the whole visual argument). **gate-tick** — one policy check riding on a gate edge. **station-label** — a quiet mono tag pinned to a node. **hairline-grid** — the one ambient texture. **console-caption** — this project's caption rail (see caption-skin).

## Frame Treatments

> Recipe: ground · diagram-state · composes · focal · chrome · accent · Fixed/Free · density.
> Every diagram frame reuses the SAME client→proxy→server(s) stage; only the edge behavior and the labels change per concept.

### 1 · Hook (identity · move: hard-cut term flashes · void canvas)

**Ground** `{colors.canvas}` + faint hairline grid. **Composes** kicker, three hard-cut Fraunces `display`/`h1` term flashes, a settling stamp line. **Focal** the three terms themselves, each flashed then replaced. **Chrome** none (declarative). **Accent** each term flash briefly borrows its own signal color as an underline tick (proxy=amber / balancer=teal / gateway=violet) — a preview of the thesis before it's explained. **Free** exact words, timing. **Density** low, type-only.

### 2 · Diagram-Build (mechanism · move: stations traversed by camera / edge assembling · void canvas)

**Ground** `{colors.canvas}` + hairline grid. **Composes** node-box × (client, proxy/LB/gateway, server×N), one edge type, station-labels, a small Fraunces `h3` or `kicker` caption of the beat's one-line takeaway. **Focal** the edge behavior (forward / choose / gate) assembling as the VO names it. **Chrome** station-labels, mono micro tags. **Accent** the ONE signal color this beat owns. **Free** node count, layout, which station the camera lands on. **Density** the dense exception — this is the video's core, let the diagram fill 45-60%.

### 3 · Recap Triptych (synthesis · move: three cards self-assemble side by side · void canvas)

**Ground** `{colors.canvas}`. **Composes** 3 stacked mini-diagram cards (portrait = vertical stack), each a tiny node+edge glyph in its own signal color + a short Fraunces label ("just forwards" / "picks a destination" / "makes policy decisions"). **Focal** the three cards landing one by one, then held together. **Chrome** mono micro captions. **Accent** all three signal colors together, each staying in its own lane. **Free** exact glyph size, stagger order. **Density** moderate, the payoff beat.

### 4 · Guidance List (practical · move: rule-of-three statements land in sequence · void canvas)

**Ground** `{colors.canvas}`. **Composes** kicker, 3 short Fraunces statements landing top-to-bottom (portrait stack), each prefixed by a small mono index tag + its signal-color tick. **Focal** the statement currently landing. **Chrome** mono index. **Accent** the matching signal color per line. **Free** wording, stagger. **Density** low-moderate.

### 5 · Brand/CTA (closer · move: single card, one clean move, held · void canvas)

**Ground** `{colors.canvas}`. **Composes** a short Fraunces sign-off line, one emphasized quoted word, a small mono sub-line. **Focal** the sign-off. **Chrome** none. **Accent** amber (the video's primary/first-named signal) as the one CTA voltage. **Free** exact words. **Density** low, calm hold.

## Composition Rules

### Do

- Reuse the **same client → proxy/LB/gateway → server(s)** stage across the diagram-build frames (2-5 of the storyboard) so the video reads as one evolving schematic, not disconnected slides.
- Keep the **three signal colors' roles fixed** everywhere they appear (diagram edges AND caption emphasis words AND the recap triptych).
- Build every diagram **live** — edges draw/fork/gate on their VO cue; never drop in a finished diagram at t=0.
- Keep depth to **hairline + flat fill** only; the one glow is reserved for a held hero moment.

### Don't

- No shadow, no gradient fill, no card glow on a diagram node.
- No color other than the three signal colors (+ rare `danger`) on an edge or gate-tick.
- No pill-shaped node, no rounded-blob diagram — sharp 4px corners only.
- Never uppercase Fraunces; never a sans headline; never a serif diagram label (labels are always mono).
- Don't let a diagram frame sit static after ~25% — the edge must still be resolving into the second half of the frame's duration.

## Aspect-Ratio Behavior

| Treatment       | 9:16 (primary)              | 16:9                       | 1:1                    |
| --------------- | ---------------------------- | --------------------------- | ----------------------- |
| Hook            | term stack, centered         | term row, centered          | centered                |
| Diagram-Build    | stations stacked vertically  | stations left-to-right      | stations in an arc      |
| Recap Triptych  | 3 cards stacked vertically   | 3 cards in a row            | 2+1                      |
| Guidance List    | 3 lines stacked              | 3 lines stacked, wider      | 3 lines stacked          |
| Brand/CTA       | centered                     | centered                    | centered                 |

## Approved Real Entities

No real customers, vendors, or logos — every node is a generic labeled box (CLIENT /
PROXY / ORIGIN / SERVICE-A / SERVICE-B …). No placeholder imagery is needed; every visual
is CSS/SVG diagram geometry or type.

## Numerals & Claims (hard rule)

Never invent figures beyond what the script states. The only numeral in the script is
"ten microservices" (API-gateway frame) — render exactly that; do not invent latency
numbers, percentages, or server counts beyond what a frame's script line supports.

## Pre-Render Self-Audit

- **Squint** — one lit edge / one display statement dominates per frame.
- **Signal discipline** — amber/teal/violet roles held fixed; no stray fourth hue.
- **Type** — Fraunces sentence-case display; IBM Plex Sans body; IBM Plex Mono uppercase chrome + diagram labels.
- **Depth** — hairline + flat only; the one ambient glow reserved for a held hero.
- **Build** — diagrams assemble on VO cue, never dropped in whole; safe zone respected (nothing below y≈1670, nothing load-bearing above y≈150).
- **Fabrication** — the only numeral is "ten microservices"; nothing else invented.

## Font loading (staged locally — paste into every frame's `<template>`)

Fraunces and IBM Plex Sans ship as variable fonts (one file covers their whole weight
range); IBM Plex Mono ships as two static weights. All five files are staged in this
project's `assets/fonts/`. Paste this exact block into every frame's `<template>` (root-relative
paths, matching `frame-worker-core.md`'s `font_family_without_font_face` rule):

```html
<style>
  @font-face { font-family: 'Fraunces'; src: url('assets/fonts/Fraunces-Variable.woff2') format('woff2'); font-weight: 400 700; font-style: normal; font-display: block; }
  @font-face { font-family: 'Fraunces'; src: url('assets/fonts/Fraunces-Italic.woff2') format('woff2'); font-weight: 400 700; font-style: italic; font-display: block; }
  @font-face { font-family: 'IBM Plex Sans'; src: url('assets/fonts/IBMPlexSans-Variable.woff2') format('woff2'); font-weight: 300 700; font-style: normal; font-display: block; }
  @font-face { font-family: 'IBM Plex Mono'; src: url('assets/fonts/IBMPlexMono-400.woff2') format('woff2'); font-weight: 400; font-style: normal; font-display: block; }
  @font-face { font-family: 'IBM Plex Mono'; src: url('assets/fonts/IBMPlexMono-500.woff2') format('woff2'); font-weight: 500; font-style: normal; font-display: block; }
</style>
```

## Known Gaps

- **Motion intentionally out of scope here.** frame.md specifies composition/palette/type only; per-frame motion is authored in `STORYBOARD.md` (Step 4) and built in Step 5 from `hyperframes-animation`'s rule library.
- **Fraunces + IBM Plex Sans + IBM Plex Mono ship as local files** in `assets/fonts/` (staged for this project) — do NOT link Google Fonts; use the `@font-face` block above verbatim in every frame.
- **9:16 is this project's actual primary** (a portrait reel), documented above the 16:9/1:1 rows the preset lineage otherwise leads with.
