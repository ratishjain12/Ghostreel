import argparse
import json
from pathlib import Path

from gen_reel_batch import THEME_SOURCE_DEFAULT, init_project, seed_theme

REPO_ROOT = Path(__file__).resolve().parent.parent

MIN_SLIDES = 2
MAX_SLIDES = 10
DEFAULT_SLIDES = 6

# The account these carousels are grown for — the CTA slide always closes on a save+follow ask
# naming this handle. Carousels are never published through this pipeline's Graph API automation
# (that's reel-only), so a "comment X and I'll DM you" CTA has nothing behind it and must not be
# used here — save/follow are the only asks this pipeline can actually make good on.
ACCOUNT_HANDLE = "@ratish.ai"

# Square is the one aspect ratio both Instagram and LinkedIn carousels render natively with
# zero cropping — no new hyperframes resolution preset needed, "square" already exists.
CAROUSEL_ASPECT = "1080x1080"

THEMED_NOTE = (
    "- Design system is pre-seeded: frame.md and assets/fonts/ are already in this project, "
    "copied from the house style. Skip Step 2 (design invention) entirely and go straight from "
    "Setup to the storyboard/script step. Every frame's @font-face block must reuse these exact "
    "files verbatim (same family names, same weights, same assets/fonts/ paths)."
)
UNTHEMED_NOTE = "- No design system pre-seeded for this project. Step 2 (design invention) runs normally."

BRIEF_TEMPLATE = """---
workflow: faceless-explainer
content_type: carousel
flow: automation
storyboard: no
message: "{message}"
destination: {destination}
aspect: {aspect}
slide_count: {slide_count}
language: {language}
angle: {angle}
---

## Intent

{intent}

## Assets

- No voiceover, no captions. A carousel carries no narration or audio.

## Customizations

- {slide_count} static scenes, one per carousel slide, in the order they should appear.
- No motion. Every scene is a single still composition (no GSAP timeline, no keyframes).
  Design each scene as a self-contained graphic slide (headline/stat/diagram + supporting text),
  not a frame of a continuous animation.
- Every scene needs a real supporting graphic, not just headline + subhead typography on a flat
  or gradient background: an icon, a small diagram (boxes/arrows for a flow, side-by-side columns
  for a comparison, a numbered/checklist layout for a listicle item), or a simple data element.
  Typography-only slides read as unfinished.
- Compose every scene so its content fills and balances the full 1080x1080 frame vertically, not
  clustered in the top half with dead empty space below (or vice versa). Vertically center the
  whole content block, or if a scene has a headline block and a separate supporting-graphic block,
  distribute them across the frame's height so the composition reads as intentional at a glance,
  not top-heavy with an empty bottom half.
- One idea per slide, always. Never cram two concepts, two comparisons, or two data points onto
  a single scene, that is what the next slide is for.
- Max ~35 words of body text per scene (headline not counted). If a point needs more than that to
  land, cut it down or split it across two scenes rather than shrinking the type to fit more text.
- Visual consistency across every scene, the CTA slide included: the same base canvas background
  color, the same font choices, the same margins, and the same accent color throughout. A carousel
  should look like one post, not a set of differently-designed slides stitched together. The CTA
  slide must never invert to a full accent-color background, that reads as a different post
  spliced onto the end.
- If scenes are numbered (step X of N, question X of N, etc.), use the exact same number format
  and placement on every scene that has one, do not switch styles partway through.
- No em dashes anywhere in any visible text (headlines, subheads, labels, captions). Use a
  period, comma, or colon instead, and rewrite the sentence around it rather than just deleting
  the dash and leaving a run-on.
- Slide 1 (the hook) is the single highest-leverage slide, most of a carousel's engagement rides
  on it. It must be a bold claim, a sharp question, or a number + promise, never a flat topic
  label, and it needs a visible swipe cue (an arrow icon or "Swipe" label) so it reads as the
  start of a sequence, not a standalone graphic.
- The last slide is the CTA. Keep the same base canvas background as every other slide clearly
  visible, covering meaningfully more than half the frame; the accent-color card sitting on top of
  it is a headline-sized banner, not a near-full-bleed rectangle with a thin border around it. A
  card that covers ~90% of the frame with the base color reduced to a sliver at the edges fails
  this instruction just as much as a true full-bleed background does, both still read as a
  different post spliced onto the end. Concretely: the accent-color card should hold only the
  headline and, optionally, the subhead, roughly the top third to top half of the frame; the two
  CTA buttons then sit below it directly on the visible base canvas background (as solid
  accent-color pills is fine for the buttons themselves, that is not the same as the whole slide
  going accent-color), with the base canvas's color clearly the dominant color of the slide overall,
  not an afterthought margin. Its ask is always save + follow, phrased and designed as two
  distinct, visually highlighted calls to action (each in its own bordered/filled button-like shape
  with a small icon, a bookmark icon for save, a profile/plus icon for follow), not plain
  sentences: save this post, and follow {handle} for more. Never use a "comment a keyword and I'll
  send/DM you something" CTA on a carousel; nothing in this pipeline can actually deliver on that
  promise.

## Notes

- Carousel safe zone: keep content clear of the outer ~80px on all sides so platform chrome
  (Instagram's rounded corners, LinkedIn's card padding) never crops it.
{theme_note}
"""


def first_sentence(text):
    text = text.strip().strip('"').strip()
    for sep in (". ", "! ", "? "):
        if sep in text:
            return text.split(sep, 1)[0].strip() + sep.strip()
    return text


def build_brief(name, outline_text, meta, themed):
    message = (meta.get("message") or first_sentence(outline_text)).replace('"', "'")
    slide_count = int(meta.get("slide_count", DEFAULT_SLIDES))
    if not (MIN_SLIDES <= slide_count <= MAX_SLIDES):
        raise SystemExit(f"{name}: slide_count must be between {MIN_SLIDES} and {MAX_SLIDES}, got {slide_count}")
    return BRIEF_TEMPLATE.format(
        message=message,
        destination=meta.get("destination", "carousel"),
        aspect=CAROUSEL_ASPECT,
        slide_count=slide_count,
        language=meta.get("language", "en"),
        angle=meta.get("angle", "concept"),
        intent=meta.get("intent") or f"Explain, one idea per slide: {message}",
        theme_note=THEMED_NOTE if themed else UNTHEMED_NOTE,
        handle=ACCOUNT_HANDLE,
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Batch-generate a pre-filled BRIEF.md for a folder of carousel outlines, one .txt per "
            "post. Each outline may have a sibling <name>.meta.json with overrides: message, "
            "intent, destination, slide_count (2-10), language, angle."
        )
    )
    parser.add_argument("--scripts-dir", required=True, type=Path, help="Directory of .txt carousel outlines")
    parser.add_argument("--carousel-out", default=Path("carousels"), type=Path)
    parser.add_argument("--names", help="Comma-separated outline stems to process (default: all .txt files in --scripts-dir)")
    parser.add_argument(
        "--theme-source",
        default=THEME_SOURCE_DEFAULT,
        help="Where to copy frame.md + fonts/ from — same convention as gen_reel_batch.py's --theme-source.",
    )
    args = parser.parse_args()

    outlines = sorted(args.scripts_dir.glob("*.txt"))
    if args.names:
        wanted = {n.strip() for n in args.names.split(",") if n.strip()}
        outlines = [o for o in outlines if o.stem in wanted]
        missing = wanted - {o.stem for o in outlines}
        if missing:
            raise SystemExit(f"No outline found for: {', '.join(sorted(missing))}")
    if not outlines:
        raise SystemExit(f"No .txt outlines found in {args.scripts_dir}")

    print(f"Found {len(outlines)} outline(s): {[o.stem for o in outlines]}\n")

    for outline_path in outlines:
        name = outline_path.stem
        print(f"=== {name} ===")
        text = outline_path.read_text().strip()
        meta_path = outline_path.with_suffix(".meta.json")
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}

        project_dir = args.carousel_out / name
        hf_marker = project_dir / "hyperframes.json"
        if hf_marker.exists():
            print(f"  {project_dir} already initialized — skipping init/BRIEF.md")
            continue

        init_project(project_dir, CAROUSEL_ASPECT)

        themed = seed_theme(project_dir, args.carousel_out, args.theme_source)
        if themed:
            source_label = "assets/" if args.theme_source == "assets" else f"video/{args.theme_source}/"
            print(f"  seeded frame.md + fonts from {source_label}")

        brief_path = project_dir / "BRIEF.md"
        brief_path.write_text(build_brief(name, text, meta, themed))
        print(f"  wrote {brief_path}")

    print("\nDone. Each carousels/<name>/ with a BRIEF.md is ready for the carousel authoring step.")


if __name__ == "__main__":
    main()
