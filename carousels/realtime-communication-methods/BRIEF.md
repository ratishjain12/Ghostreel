---
workflow: faceless-explainer
content_type: carousel
flow: automation
storyboard: no
message: "4 ways systems talk in real time, and the tradeoff each one hides. Save this cheat sheet, and follow @ratish.ai for more system design breakdowns."

#systemdesign #webdevelopment #api #softwareengineering"
destination: carousel
aspect: 1080x1080
slide_count: 7
language: en
angle: concept
---

## Intent

Explain, one idea per slide: 4 ways systems talk in real time, and the tradeoff each one hides. Comment 'GUIDE' for the full breakdown.

#systemdesign #webdevelopment #api #softwareengineering

## Assets

- No voiceover, no captions — a carousel carries no narration or audio.

## Customizations

- 7 static scenes, one per carousel slide, in the order they should appear.
- No motion — every scene is a single still composition (no GSAP timeline, no keyframes).
  Design each scene as a self-contained graphic slide (headline/stat/diagram + supporting text),
  not a frame of a continuous animation.

## Notes

- Carousel safe zone: keep content clear of the outer ~80px on all sides so platform chrome
  (Instagram's rounded corners, LinkedIn's card padding) never crops it.
- Design system is pre-seeded: frame.md and assets/fonts/ are already in this project, copied from the house style. Skip Step 2 (design invention) entirely and go straight from Setup to the storyboard/script step. Every frame's @font-face block must reuse these exact files verbatim (same family names, same weights, same assets/fonts/ paths).
