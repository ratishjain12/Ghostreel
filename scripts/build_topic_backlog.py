import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PILLARS = ["ai-engineering", "system-design", "dev-lessons", "ai-news", "engineering-opinions"]
HOOK_STYLES = ["bold-claim", "question", "number-promise", "contrarian", "before-after"]

PROMPT = f"""Read growth/competitor-outliers.json in this repository. Each entry is a post from a \
competitor Instagram account (field "handle") that performed at least 3x that account's own median \
on "score_metric" (view_count if available, otherwise like_count); "outlier_ratio" is how many \
times the median. Reels and feed posts are scored against separate per-type medians (see \
"medians" in growth/competitors/<handle>.json); treat a ratio from a group with fewer than 5 \
posts as noise. Also skim growth/competitors/*.json for each account's full post list, and read \
growth/analysis-latest.md for this account's own results. growth/competitors/transcripts/*.json \
holds whisper transcripts of competitor reels that beat their median by 1.5x+ ("has_voiceover" false \
means a music/on-screen-text reel); use them for hooks, structure, length and pacing \
("words_per_minute", "duration"). Meta withholds media for reels with licensed music, so a missing \
transcript says nothing about quality.

Ignore outliers that aren't educational content (birthdays, weddings, personal milestones, \
event photos, course/product announcements): they spike on the creator's personal audience, not \
on topic, and tell us nothing about what to make. Note how many you excluded.

This account's already-made topics are the filenames in scripts/reels/*.txt and \
scripts/carousels/. Never propose a topic that duplicates one of those.

Saves/bookmarks are NOT available for competitor accounts (Instagram only exposes them to the \
owner), so never claim a competitor post had a high save rate. Say "outperformed its account's \
median by Nx" instead.

Write growth/topic-backlog.md:
1. "What's working elsewhere": group the outliers into recurring topic clusters and formats \
(e.g. "X vs Y vs Z comparisons", "how <company> built <system>", "interview question \
breakdowns"). For each cluster: how many distinct accounts had an outlier in it, the best \
outlier_ratio, and 1-2 permalinks as evidence. Clusters confirmed across 2+ accounts rank above \
single-account ones.
2. "Hooks that travel": the opening-line patterns from the top outlier captions, mapped to this \
repo's hook styles ({", ".join(HOOK_STYLES)}), or labeled "new: <name>" if none fits.
3. "Backlog": 15 concrete reel topics for THIS account, ranked. Each line: \
`- [ ] <kebab-case-name> | <pillar> | <hook style> | <one-sentence angle> | evidence: <cluster>`. \
Pillar is one of {", ".join(PILLARS)}. Prefer topics where competitor evidence and this \
account's own analysis-latest.md agree. Our own versions with our own angle, never a \
restatement of a competitor's script. No em dashes.

Only write growth/topic-backlog.md; don't modify any other file. If \
growth/competitor-outliers.json is empty or missing, say so and stop. This is unattended \
automation, no one will answer questions: write the file and finish. Today is {date.today().isoformat()}."""


def main():
    if not (ROOT / "growth" / "competitor-outliers.json").exists():
        raise SystemExit("run scripts/scrape_competitors.py first")
    cmd = ["claude", "-p", PROMPT, "--permission-mode", "bypassPermissions"]
    sys.exit(subprocess.run(cmd, cwd=ROOT).returncode)


if __name__ == "__main__":
    main()
