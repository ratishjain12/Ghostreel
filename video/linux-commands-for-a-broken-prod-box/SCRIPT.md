# SCRIPT: linux-commands-for-a-broken-prod-box

**Voice:** locked recording (verbatim, source of truth: `audio/linux-commands-for-a-broken-prod-box.wav`)
**Voice settings:** n/a, pre-recorded, not synthesized by this workflow
**Voice direction:** Fast, calm, on-call engineer talking you through an incident.

---

## Line 1: Hook (Frame 1)

**Time:** 0.00 to 9.08s
**Delivery:** Urgent, direct address, fast.

    The server is slow, the alert is firing, and you just SSH'd in. There are thousands of Linux commands. These are the ones you run in the first five minutes, in order.

## Line 2: uptime (Frame 2)

**Time:** 9.08 to 16.97s
**Delivery:** Plain, procedural.

    First, uptime. Load average tells you in one second whether the box is actually overloaded, or whether the problem is somewhere else.

## Line 3: top / htop (Frame 3)

**Time:** 16.97 to 22.72s
**Delivery:** Quick, procedural.

    Second, top, or htop. Which process is eating CPU or memory right now.

## Line 4: free -h (Frame 4)

**Time:** 22.72 to 30.28s
**Delivery:** Procedural, lands the consequence.

    Third, free minus h. Is memory full, and is the machine swapping. Swapping is why everything suddenly got a hundred times slower.

## Line 5: df -h (Frame 5)

**Time:** 30.28 to 37.31s
**Delivery:** Procedural, wry on 'completely unrelated'.

    Fourth, df minus h. A full disk breaks logging, databases, and deploys in ways that look completely unrelated.

## Line 6: dmesg (Frame 6)

**Time:** 37.31 to 43.43s
**Delivery:** Grave on 'the only place it says so'.

    Fifth, dmesg. If the kernel killed your process for using too much memory, this is the only place it says so.

## Line 7: journalctl (Frame 7)

**Time:** 43.43 to 48.48s
**Delivery:** Quick, procedural.

    Sixth, journalctl, or your app logs, for the error right before it all started.

## Line 8: ss -tulpn (Frame 8)

**Time:** 48.48 to 54.01s
**Delivery:** Procedural, closing the list.

    And seventh, ss minus tulpn. Is the port actually listening, and who is connected to it.

## Line 9: Recap (Frame 9)

**Time:** 54.01 to 58.44s
**Delivery:** Rhythmic roll-call, then firm.

    CPU, memory, disk, kernel, logs, network. Same order, every incident.

## Line 10: CTA (Frame 10)

**Time:** 58.44 to 61.22s
**Delivery:** Warm sign-off.

    Comment guide and I'll send you the full incident checklist.
