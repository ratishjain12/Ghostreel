---
format: 1080x1920
duration: 61s
message: "The server is on fire and you just SSH'd in. The 7 Linux commands to run in the first five minutes, in order: CPU, memory, disk, kernel, logs, network."
arc: how-to-process (numbered incident runbook, one command per frame on one stage)
audience: backend and DevOps engineers who get paged and freeze at a blank prompt on a broken production box
mode: autonomous
music: none
---

## Video direction

**Design system:** `frame.md` (code-editorial preset), reused verbatim. Warm cream `colors.cream` #FAF9F5 ground on every frame, content gathers on `colors.tile` #EFE9DE half-step surfaces, ink #141413 voice. The terminal is the warm-navy **code-surface** (`colors.navy` #181715 body, `colors.navy-elev` #252320 title bar, cream@14% hairline, 8px radius). Coral #CC785C is rationed to **one moment per frame**; on the command frames (2 to 8) that one moment is the **current step chip in the progress rail**. Inside the terminal, the fixed syntax decoration applies: command name in cream, flags in amber #E8A55A, highlighted output fields in teal #5DB8A6, the warn/fail read in #C64545, the success/listening read in #5DB872. These are decoration, not brand hues.

**Type:** EB Garamond 400 sentence case (negative-tracked) for every display line, takeaway and numeral; Inter 400 for any body/lead copy; JetBrains Mono for kickers (UPPERCASE, 0.16em, coral ✱ prefix), the progress rail, and everything inside the terminal. Fonts come ONLY from the canonical `@font-face` block at the bottom of `frame.md` (paths `assets/fonts/...`), copied verbatim. No other family, no Google Fonts link. Only weights 400 and 700 exist.

**The stage (frames 2 to 8, identical skeleton, the "runbook page"):** one layout repeats so seven frames read as one continuous runbook being worked top to bottom:
- **Top band (y ≈ 170 to 330):** left: a number-lockup: the step numeral in EB Garamond number-hero (e.g. "1") + JetBrains Mono unit "/ 7". Right of it: a mono kicker `✱ CPU` (the category from the recap: uptime and top = CPU, free = MEMORY, df = DISK, dmesg = KERNEL, journalctl = LOGS, ss = NETWORK). Below both, full-width: the **progress rail**: seven small mono chips `01` to `07` in a row on hairlines; completed steps ink-filled on tile, the current step coral-filled (the frame's one coral), future steps outline only.
- **Middle (y ≈ 400 to 1150):** the navy terminal panel, near full width (~920px), title bar with three hairline dots + mono `prod · ssh`. The command types in behind a caret on its VO cue, then schematic output prints. **No invented numbers**: output rows are real field labels the script names (e.g. `load average`, `Mem:`, `Swap:`, `LISTEN`) with values drawn as bars/blocks or `—`, never fabricated digits, PIDs, timestamps, or hostnames beyond the generic `prod` chrome.
- **Lower (y ≈ 1200 to 1560):** the takeaway: one EB Garamond display line (italic when it's a stance) that reveals word-group by word-group on the VO, the frame's teaching sentence.
- Nothing load-bearing above y 150 or below y 1574 (caption band). Band-safe.

**Terminal mechanism:** `compositions/components/code-terminal-run.html` is installed as a **reference only**. Do NOT mount it (it registers a fixed timeline key that collides across frames). Reproduce its mechanism inline in your frame: typed-prompt law (row table of text-at-time built synchronously, reveal by character count, deterministic human cadence seeded per frame), integer-cycle blinking caret driven from timeline time, output lines printing one per cue. All inside your frame's own timeline.

**Motion grammar:** long-tail `power3.out` settles, no bounce/overshoot/elastic. Every reveal fires on its spoken word (times below are frame-relative seconds, taken from the locked VO word timings). At t=0 only what the VO is saying enters. Holds are still; the only sanctioned aliveness is the blinking caret and at most a subtle jitter. Coral is the only draw-on color (rail chip fill, section rule).

**Hook energy (growth note):** the account's latest growth analysis recommends testing a **number-promise** hook over the contrarian hooks used lately. This script is already a number promise ("the ones you run in the first five minutes, in order"), so the hook frame lands a big "7" numeral and "first 5 minutes" as its payoff, and every command frame carries the "N / 7" counter so the promise is paid off visibly step by step. The numeral 7 is the script's own count of commands, not an invented figure.

**Rhythm / held frames:** frames 2 to 8 are fast (5 to 8s), each a quick type-run-read. Frame 9 (recap) is the **held breather**: the six categories stack, then stillness. Frame 10 is the final still CTA.

**Transitions:** frame 1 `cut`; frames 2 to 8 `push-slide LEFT` (turning the runbook page, same direction every step); frames 9 and 10 `crossfade` (stepping back from the runbook to the summary).

**Negative list:** no em dashes in any visible text. No pure white/black/cool gray. No gradients, glows, heavy shadows, tilts. No bokeh or "AI" gradients. No fake metrics, PIDs, timestamps, IPs, or percentages beyond "full". No slideshow (front-load then freeze), no screensaver (independent floating), no lazy breathing, no slow back-half pan/push. No `document.currentScript.closest(...)`; get your root with `document.querySelector('[data-composition-id="<frame-id>"]')`, never `#root`. No overlapping elements in screen space at any moment.

## Frame 1 — Hook

- scene: Cream page. "The server is slow." slams in as big serif type with a mono alert pill "ALERT FIRING"; a terminal prompt appears "you just SSH'd in"; a wall of faint command names floods the page ("thousands of Linux commands"), then clears to a big "7" + "first 5 minutes, in order".
- voiceover: "The server is slow, the alert is firing, and you just SSH'd in. There are thousands of Linux commands. These are the ones you run in the first five minutes, in order."
- duration: 9.08s
- transition_in: cut
- status: outline
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Imagine / scenario (direct address) + number promise
- beat: tension + recognition, then relief of a plan
- blueprint: kinetic-type-beats (Adapt)
- focal: the hero line "The server is slow." then the payoff numeral "7"
- roles: hero serif lines = foreground subject · alert pill + ssh prompt = supporting · faint command-name wall = background (dim ~35%) · "7 / first 5 minutes / in order" lockup = foreground payoff
- sfx: none

narrativeRole: Drops the viewer into the page-at-3am moment, then promises a short ordered plan.
keyMessage: You don't need thousands of commands, you need seven, in order.

Adapt: keep the statement-builds-across-beats signature; the final payoff is a number-lockup instead of a logo.
Scene 1 (0.0–1.3s): visible within the first second: EB Garamond display "The server is slow." sets upper third (y ≈ 380), per-word reveal from 0.0 ("The" 0.0, "server" 0.24, "slow" 0.8). Centered, ~80% width.
Scene 2 (1.3–2.3s): on "alert… firing" (1.34/1.72) a tile pill with mono `✱ ALERT FIRING` and a small #C64545 status dot snaps in beneath the headline; the dot is the warn read (decoration), the coral ✱ is the frame's single coral.
Scene 3 (2.3–3.9s): on "you just SSH'd in" (2.34/2.74) a compact navy terminal strip slides up into the middle (y ≈ 900) and types `$ ssh prod` behind a caret, a fresh prompt caret blinks after.
Scene 4 (3.9–5.9s): on "thousands of Linux commands" (4.4/4.94) the upper content scale-swaps out and a dense wall of ~40 real command names in JetBrains Mono (ls, grep, awk, sed, find, tar, curl, chmod, ps, kill, lsof, vmstat, iostat, netstat, ping, dig, rsync, crontab, systemctl, strace, tcpdump, du, …) cascades in as a background texture at ~35% ink, filling y 250 to 1500. Do not include the seven featured commands in the wall.
Scene 5 (5.9–7.9s): on "These are the ones" (6.04) the wall blurs and dims further (depth-of-field-blur) and seven chips `01`–`07` land in a row; on "first five minutes" (7.38/7.58) a number-lockup rises center: EB Garamond number-hero "7" huge (~ 520px tall), JetBrains Mono unit "commands", with a mono line "FIRST 5 MINUTES" beneath.
Scene 6 (7.9–9.08s): on "in order" (8.52) the seven chips fill ink left to right in a quick stagger, then hold still.

## Frame 2 — uptime

- scene: Runbook page, step 1 / 7, CPU. Terminal types `uptime`; the `load average` field lights teal; two verdict chips below: "the box is overloaded" vs "the problem is somewhere else".
- voiceover: "First, uptime. Load average tells you in one second whether the box is actually overloaded, or whether the problem is somewhere else."
- duration: 7.89s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/02-uptime.html
- type: feature_showcase
- persuasion: Numbered enumeration + question→answer pairing
- beat: focus + momentum
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the terminal running `uptime` with the `load average` field highlighted
- roles: terminal = foreground subject · numeral "1 / 7" + `✱ CPU` kicker + rail (chip 01 coral) = supporting chrome · two verdict chips + serif takeaway = foreground lower · cream/tile ground = background
- sfx: none

narrativeRole: Step one: a one-second triage that tells you whether to keep digging on this box at all.
keyMessage: uptime's load average says, in one second, whether this box is overloaded or the problem is elsewhere.

Adapt: keep "watch me ask, watch it answer" (command types, output prints); the answer is one highlighted field plus a two-way verdict instead of a streaming answer.
Scene 1 (0.0–0.7s): the stage chrome is already seated (numeral "1", unit "/ 7", `✱ CPU`, rail with 01 coral), the terminal panel settles; nothing else.
Scene 2 (0.7–1.7s): on "uptime" (0.72) the command `uptime` types in after `$`.
Scene 3 (1.7–3.3s): on "Load average" (1.72) one output row prints: mono `load average:` in teal followed by three placeholder value blocks (bars, no digits); a teal hairline underline draws under `load average`. A mono tag `1 SECOND` appears at the row's end on "one second" (2.86/3.08).
Scene 4 (3.3–5.4s): on "whether the box is actually overloaded" (3.38/4.96) the serif takeaway starts below the terminal: left verdict card (tile, hairline) "The box is overloaded" reveals.
Scene 5 (5.4–7.89s): on "or whether the problem is somewhere else" (5.5/7.24) a mono "or" sits between and the right/second verdict card "The problem is somewhere else" reveals; stacked vertically (portrait), not side by side if width is tight. Hold.

## Frame 3 — top / htop

- scene: Runbook page, step 2 / 7, CPU. Terminal types `top` then "or htop"; a schematic process table prints with CPU and MEM columns; one row rises to the top and highlights: the process eating it.
- voiceover: "Second, top, or htop. Which process is eating CPU or memory right now."
- duration: 5.75s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/03-top.html
- type: feature_showcase
- persuasion: Numbered enumeration + demonstration
- beat: momentum + aha
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the process table with the one guilty row highlighted
- roles: terminal/table = foreground subject · numeral "2 / 7" + `✱ CPU` + rail (02 coral, 01 ink) = supporting · serif takeaway = foreground lower
- sfx: none

narrativeRole: Step two: from "is it overloaded" to "who is doing it".
keyMessage: top or htop shows which process is eating CPU or memory right now.

Adapt: keep type → answer; the answer is a table whose rows re-sort.
Scene 1 (0.0–0.6s): stage chrome seated (numeral "2", `✱ CPU`, rail 02 coral), terminal settles.
Scene 2 (0.6–2.6s): on "top" (1.27) `top` types; on "or htop" (1.61) a small mono `or  htop` tag appears beside the command line (both are valid commands).
Scene 3 (2.6–3.9s): on "Which process" (2.61) a header row prints: mono `PROCESS   CPU   MEM`; five process rows print quickly beneath, names as generic mono placeholders (`process-a` … `process-e`), CPU/MEM values drawn as short bars of differing length (no digits).
Scene 4 (3.9–5.0s): on "eating CPU or memory" (3.57/3.97/4.63) one row (the one with the longest bars) slides up to the top slot and its bars fill teal; row outline in #C64545 warn. The CPU header lights on "CPU", MEM on "memory".
Scene 5 (5.0–5.75s): on "right now" (4.81/5.21) the serif takeaway "Who is eating it, right now." lands below. Hold.

## Frame 4 — free -h

- scene: Runbook page, step 3 / 7, MEMORY. Terminal types `free -h`; `Mem:` bar fills to full, `Swap:` bar starts filling; then a serif number-lockup "100×" with mono unit "slower".
- voiceover: "Third, free minus h. Is memory full, and is the machine swapping. Swapping is why everything suddenly got a hundred times slower."
- duration: 7.56s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/04-free.html
- type: feature_showcase
- persuasion: Numbered enumeration + causal chain (memory full → swapping → slow)
- beat: comprehension + unease
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the Mem/Swap bars, then the "100×" lockup
- roles: terminal = foreground subject · numeral "3 / 7" + `✱ MEMORY` + rail (03 coral) = supporting · "100× slower" number-lockup = foreground lower
- sfx: none

narrativeRole: Step three: explains the most common reason "everything got slow" at once.
keyMessage: free -h tells you if memory is full and the box is swapping, and swapping makes everything a hundred times slower.

Adapt: keep type → answer; the answer is two fill bars plus a stat payoff.
Scene 1 (0.0–0.6s): stage chrome seated (numeral "3", `✱ MEMORY`, rail 03 coral), terminal settles.
Scene 2 (0.6–1.5s): on "free minus h" (0.6/1.16) `free -h` types (`-h` in amber).
Scene 3 (1.5–2.8s): on "Is memory full" (1.52/2.42) row `Mem:` prints with a horizontal bar that fills to the end (stat-bars-and-fills), end tag `FULL` in #C64545.
Scene 4 (2.8–4.1s): on "is the machine swapping" (3.18/3.78) row `Swap:` prints and its bar begins filling teal→warn.
Scene 5 (4.1–6.3s): on "Swapping is why everything suddenly" (4.18/5.74) the serif line "Swapping is why everything got slow." reveals below the terminal.
Scene 6 (6.3–7.56s): on "a hundred times slower" (6.4/6.84) number-lockup lands at the right of / under the line: EB Garamond "100×" + JetBrains Mono unit "slower", counting up 1→100 fast (counting-dynamic-scale). Hold.

## Frame 5 — df -h

- scene: Runbook page, step 4 / 7, DISK. Terminal types `df -h`; a `Use%` bar fills to full; three unrelated-looking breakages stack: logging, databases, deploys, each struck through.
- voiceover: "Fourth, df minus h. A full disk breaks logging, databases, and deploys in ways that look completely unrelated."
- duration: 7.03s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/05-df.html
- type: feature_showcase
- persuasion: Numbered enumeration + counterexample (the symptom is not where the cause is)
- beat: recognition + unease
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the three broken things list
- roles: terminal = foreground subject (upper) · numeral "4 / 7" + `✱ DISK` + rail (04 coral) = supporting · three breakage cards + serif line = foreground lower
- sfx: none

narrativeRole: Step four: warns that a full disk disguises itself as three different failures.
keyMessage: A full disk breaks logging, databases, and deploys in ways that look unrelated; df -h catches it.

Adapt: keep type → answer; the answer fans out into three consequence cards.
Scene 1 (0.0–0.5s): stage chrome seated (numeral "4", `✱ DISK`, rail 04 coral), terminal settles.
Scene 2 (0.5–1.7s): on "df minus h" (0.38/1.0) `df -h` types (`-h` amber).
Scene 3 (1.7–2.4s): on "A full disk" (1.74/2.04) row `/   Use%` prints with a bar filling to the end, tag `FULL` #C64545.
Scene 4 (2.4–4.9s): three tile cards stack below the terminal, each revealing on its word and getting a #C64545 strike line: "Logging" (2.44), "Databases" (3.3), "Deploys" (4.3).
Scene 5 (4.9–7.03s): on "look completely unrelated" (5.48/6.1) serif italic line "…in ways that look completely unrelated." lands under the cards. Hold.

## Frame 6 — dmesg

- scene: Runbook page, step 5 / 7, KERNEL. Terminal types `dmesg`; one kernel line prints and highlights: "Out of memory: Killed process"; serif "The only place it says so."
- voiceover: "Fifth, dmesg. If the kernel killed your process for using too much memory, this is the only place it says so."
- duration: 6.12s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/06-dmesg.html
- type: feature_showcase
- persuasion: Numbered enumeration + demonstration of the evidence
- beat: surprise + gravity
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the highlighted kernel line "Out of memory: Killed process"
- roles: terminal = foreground subject · numeral "5 / 7" + `✱ KERNEL` + rail (05 coral) = supporting · serif takeaway = foreground lower
- sfx: none

narrativeRole: Step five: reveals the hidden place a silent process death is recorded.
keyMessage: If the kernel killed your process for using too much memory, dmesg is the only place that says so.

Adapt: keep type → answer; the answer is one evidence line among faint noise lines.
Scene 1 (0.0–0.6s): stage chrome seated (numeral "5", `✱ KERNEL`, rail 05 coral), terminal settles.
Scene 2 (0.6–1.3s): on "dmesg" (0.72) `dmesg` types.
Scene 3 (1.3–2.6s): on "If the kernel" (1.33/1.61) several faint output lines print as muted mono bars (noise, no text).
Scene 4 (2.6–4.1s): on "killed your process for using too much memory" (1.85/3.67) one line prints in full text: `Out of memory: Killed process` with "Killed process" in #C64545 and a hairline highlight band behind the whole row.
Scene 5 (4.1–6.12s): on "the only place it says so" (4.61/5.55) the serif italic takeaway "The only place it says so." reveals below. Hold.

## Frame 7 — journalctl

- scene: Runbook page, step 6 / 7, LOGS. Terminal types `journalctl`, "or your app logs" tag; log lines scroll up; one ERROR line locks in with a marker "right before it all started".
- voiceover: "Sixth, journalctl, or your app logs, for the error right before it all started."
- duration: 5.05s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/07-journalctl.html
- type: feature_showcase
- persuasion: Numbered enumeration + signposting (the moment before)
- beat: focus + momentum
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the ERROR log line with the "before it started" marker
- roles: terminal = foreground subject · numeral "6 / 7" + `✱ LOGS` + rail (06 coral) = supporting · serif takeaway = foreground lower
- sfx: none

narrativeRole: Step six: points at the one log line that matters, the first error before the incident.
keyMessage: Read journalctl or your app logs for the error right before it all started.

Adapt: keep type → answer; the answer is a scrolling log that stops on one line.
Scene 1 (0.0–0.5s): stage chrome seated (numeral "6", `✱ LOGS`, rail 06 coral), terminal settles.
Scene 2 (0.5–1.9s): on "journalctl" (1.03) `journalctl` types; on "or your app logs" (1.65/2.47) a mono tag `or  app logs` appears beside it.
Scene 3 (1.9–3.2s): log rows print quickly as mono level tags + muted bars: `INFO ▬▬▬`, `INFO ▬▬`, `WARN ▬▬▬`, … (no timestamps, no fabricated text).
Scene 4 (3.2–4.3s): on "the error" (3.25) one row `ERROR` prints in #C64545 and a hairline highlight band locks on it; the rows after it dim.
Scene 5 (4.3–5.05s): on "right before it all started" (3.43/4.35) a small mono marker `▲ RIGHT BEFORE IT STARTED` pins under that row, and the serif line "Find the error right before it started." lands below. Hold.

## Frame 8 — ss -tulpn

- scene: Runbook page, step 7 / 7, NETWORK. Terminal types `ss -tulpn`; a port row prints with a `LISTEN` state badge; connection rows stack below it: "who is connected".
- voiceover: "And seventh, ss minus tulpn. Is the port actually listening, and who is connected to it."
- duration: 5.53s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/08-ss.html
- type: feature_showcase
- persuasion: Numbered enumeration + question→answer pairing
- beat: momentum + completion
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the `LISTEN` port row with its connections
- roles: terminal = foreground subject · numeral "7 / 7" + `✱ NETWORK` + rail (07 coral, 01–06 ink: the rail is now complete) = supporting · serif takeaway = foreground lower
- sfx: none

narrativeRole: Step seven: closes the list at the network edge, is it listening and who is on it.
keyMessage: ss -tulpn shows whether the port is actually listening and who is connected to it.

Adapt: keep type → answer; the answer is a state badge plus a growing list.
Scene 1 (0.0–0.6s): stage chrome seated (numeral "7", `✱ NETWORK`, rail 07 coral with all prior chips ink), terminal settles.
Scene 2 (0.6–2.4s): on "ss minus tulpn" (1.56/1.84) `ss -tulpn` types (`-tulpn` amber), fast cadence.
Scene 3 (2.4–3.6s): on "Is the port actually listening" (2.48/3.4) a row prints: mono `:port` + state badge `LISTEN` in #5DB872 (a pill) that pops on "listening".
Scene 4 (3.6–5.53s): on "who is connected to it" (4.1/4.46/5.0) three connection rows stack beneath, each a mono `ESTAB` tag + a muted bar (no IPs), and the serif line "Is it listening, and who is on it?" lands below. Hold.

## Frame 9 — Recap

- scene: The runbook collapses to a one-page summary: six category words stack vertically in big serif, each with its command in mono beside it, revealing on the roll-call; then "Same order, every incident."
- voiceover: "CPU, memory, disk, kernel, logs, network. Same order, every incident."
- duration: 4.43s
- transition_in: crossfade
- status: outline
- src: compositions/frames/09-recap.html
- type: branding
- persuasion: Distillation + rule-driven mnemonic (the order is the tool)
- beat: clarity + mastery
- blueprint: grid-card-assemble (Adapt)
- focal: the six-word stacked roll-call
- roles: category words (EB Garamond display) = foreground subject · commands (mono, muted) = supporting · coral section rule = the frame's one coral · closing italic line = foreground lower
- sfx: none

narrativeRole: Compresses seven commands into a six-word order the viewer can remember at 3am.
keyMessage: CPU, memory, disk, kernel, logs, network: same order, every incident.

Adapt: keep the staggered vertical list self-assembling and holding; the cascade is paced to the roll-call instead of one fast stagger.
Scene 1 (0.0–2.3s): a vertical list, left-aligned at x ≈ 120, y ≈ 240 to 1250, each row = EB Garamond display word + right-aligned mono commands muted: "CPU" `uptime · top` (0.27), "Memory" `free -h` (0.4), "Disk" `df -h` (0.75), "Kernel" `dmesg` (1.19), "Logs" `journalctl` (1.63), "Network" `ss -tulpn` (1.97). Each row slides up + fades in on its word, hairline rule between rows. (CPU and memory are spoken almost together; stagger them by ~0.15s.)
Scene 2 (2.3–4.43s): on "Same order" (2.47) a coral 1px section rule draws on under the list, then EB Garamond italic "Same order, every incident." reveals by word group (2.47/3.43/3.87) at y ≈ 1380. Hold still.

## Frame 10 — CTA

- scene: Cream page. EB Garamond sign-off "The full incident checklist" with the one coral callout: "Comment GUIDE".
- voiceover: "Comment guide and I'll send you the full incident checklist."
- duration: 2.777s
- transition_in: crossfade
- status: outline
- src: compositions/frames/10-cta.html
- type: cta
- persuasion: Direct ask + reciprocity (the checklist)
- beat: resolve
- blueprint: titlecard-reveal (Adapt)
- focal: the coral "Comment GUIDE" callout
- roles: coral callout = foreground subject (the one coral) · serif line = foreground · mono kicker = supporting
- sfx: none

narrativeRole: Converts the viewer into a comment with a concrete reward.
keyMessage: Comment GUIDE to get the full incident checklist.

Adapt: one restrained move then a still hold; two elements instead of one.
Scene 1 (0.0–1.0s): on "Comment guide" (0.22/0.48) the coral callout (coral fill, cream JetBrains Mono text `COMMENT "GUIDE"`, 8px radius, ~780px wide) slide-up-fades in at y ≈ 700.
Scene 2 (1.0–2.777s): on "the full incident checklist" (1.5/1.98) a mono kicker `✱ I'LL SEND YOU` and EB Garamond display "The full incident checklist." reveal below the callout (y ≈ 900 to 1200). Hold still to the end.
