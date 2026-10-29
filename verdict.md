# Verdict · skill-pack-marketplace

**Top pain:** Malicious / supply-chain skill panic — install like npm, get stealer or injection (score **100** in pain.md)

**Date:** 2026-10-29 15:53 Asia/Shanghai  
**Judge:** Judge  
**Verdict:** **HOLD** · score **6**/8

| dimension | score (0-2) | note |
| --- | ---: | --- |
| real pain | 2 | Unit 42 / ClawHavoc / 341 malicious ClawHub skills; intensity 5 |
| 10x number | 1 | Unified “verify then install” vs hand-read SKILL.md is strong; vs SkillzBench+SkillSpector+PromptSign not clearly 10× |
| 7-day v1 | 1 | Curated shelf of ~10 pinned packs + reports yes; full marketplace + continuous re-verify + sandbox Lift farm no |
| first 50 users | 2 | Exact reach: ClawHub/malware X threads, PH Agent Skills, Show HN PromptSign/AcidTest |
| **total** | **6** | **HOLD** (do not hand Builder a full marketplace yet) |

---

## 1. Who has this problem

Agent builders and coding-agent users who install skill packs from ClawHub / GitHub / `npx skills add` and treat them like npm — then hit stealers, injection, or silent tampering.

Complaints:
- [Unit 42 · OpenClaw supply-chain](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/) — skills that bypassed ClawScan/VirusTotal
- [The Hacker News · 341 malicious ClawHub skills](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [X @zhou_xiaoma](https://x.com/zhou_xiaoma/status/2114953884447711550) — don’t `npx skills add` blindly / SkillSpector narrative

## 2. What they use today (and why it fails)

| today | fails because |
| --- | --- |
| Pre-install scanners (NVIDIA SkillSpector, ClawScan/VT, AcidTest) | Unit 42 still found skills that bypassed ClawScan/VT; scan ≠ continuous proof; one-liner install UX unchanged |
| Big indexes (agentskill.sh, SkillsGate) | Discovery-only or optional scores; PH: stars = weak signal ([PH Agent Skills](https://www.producthunt.com/products/agent-skills-3)) |
| [SkillzBench](https://skillzbench.com/methodology) Trust Score + Lift | New / incomplete coverage; not the default install path |
| [PromptSign](https://promptsign.ai/posts/what-signing-proves) Sigstore identity | Author: signed ≠ safe; markdown writable after install; almost all packs unsigned ([Show HN](https://news.ycombinator.com/item?id=49647883)) |
| Seller self TEST-REPORT on paid kits | Seller-controlled; indie posts show $0 / pending checkout ([SkillHammer](https://x.com/SkillHammerUK/status/2113875828874297463)) |

## 3. Is our fix 10x on ONE number?

**Number: steps (or minutes) from “found a pack” → “pinned version + scan result + comparable quality gate visible before install.”**

- vs hand-reading SKILL.md across 100k+ indexes: clear order-of-magnitude cut in vetting time. GUESS on realized UX.
- vs nearest substitutes (SkillzBench + SkillSpector + PromptSign): they already cover scan / trust / sign as **separate** tools. A shelf that only rebundles them is **not** 10× unless it becomes the **default install hook** for at least one major agent.

Score: **1**

## 4. 7-day v1 — what we cut

**Ship (narrow):** curated **Verified Shelf** of ≤10 packs in one vertical (e.g. design anti-slop **or** security-audit), each with: pinned content hash, link to scan output (SkillSpector or manual checklist), one install path (Cursor **or** Claude), static landing + waitlist.

**Cut from v1:**
- Full crawler of 100k+ skills / replace VirusTotal
- Own Sigstore / continuous post-install re-verify hooks
- Sandbox Lift farm / SkillzBench-class scoring engine
- Multi-agent path matrix / paid checkout + refunds
- Cross-pack AI-slop benchmark suite (keep as later gate)

**7-day full marketplace: no. 7-day curated verified shelf: yes** → score **1**

## 5. First 50 users — where exactly

| who | where |
| --- | --- |
| People scared by ClawHub / `npx skills add` | Reply/quote [Unit 42](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/), [THN 341](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html), [X SkillSpector threads](https://x.com/rainwaterJay/status/2115319098590785922) |
| PH / index shoppers who distrust stars | [PH Agent Skills](https://www.producthunt.com/products/agent-skills-3) comments; [agentskill.sh](https://agentskill.sh/) users |
| Identity / scan early adopters | [Show HN PromptSign](https://news.ycombinator.com/item?id=49647883), [AcidTest HN](https://news.ycombinator.com/item?id=46907328), SkillzBench waiters |
| Indie pack sellers needing buyer trust | [SkillHammer](https://x.com/SkillHammerUK/status/2113875828874297463), [AgenttaskAtlas](https://x.com/AgenttaskAtlas/status/2113810583934136773) — offer “listed on Verified Shelf” |

Channels are concrete → score **2**. Conversion still fights SkillzBench/agentskill defaults.

## 6. Strongest reason this fails

**Scan + sign + trust-score products already exist as separate defaults-in-waiting (SkillSpector, PromptSign, SkillzBench, agentskill.sh).** A new “marketplace” without becoming the **install path** for Cursor/Claude/OpenClaw is another directory. Signed ≠ safe and scanners still get bypassed — so trust marketing without a hook into `npx skills add` (or agent-native install) does not stop the panic. Small team cannot out-crawl or out-scan NVIDIA/VirusTotal in 7 days; without distribution into install UX, shelf stays unread.

---

## Evidence that would flip HOLD → GO

1. **Install-path commitment** (even informal): one agent runtime or popular `skills add` wrapper will call our verify API / badge before install.
2. **Paid preorders ≥20** for “Verified Shelf” listing or buyer seat — not free index signups.
3. **Side-by-side:** for 20 popular packs, our pin+scan+gate catches ≥1 class of issue SkillzBench/public indexes miss **or** publishes comparable Lift where they only list stars.

(1) alone or (2)+(3) → re-score; likely GO on a **shelf** not a full market.

---

## Kill list (rejected this round)

| rejected | why |
| --- | --- |
| Free forever / undercut paid packs | Pricing ≠ trust gap (pain.md Rejected) |
| Brand hate ClawHub / OpenClaw / Anthropic | Evidence is missing verification defaults, not kill-brand |
| Full VirusTotal replacement / 50-engineer scanner | Scanners exist; pain is packaging into install UX |
| “Just read every SKILL.md” as product | Does not scale at 100k+ |
| AI-slop taste packs as standalone v1 without gates | Packs exist (MotionSites/taste); missing piece is shared pass/fail, not another download |
| Cross-agent path unifier as v1 | Real but lower volume (score 21); not top panic |
| Paid indie kit store without third-party verify | Sellers already attach self TEST-REPORT; trust infra missing — store alone fails |
| inbox-digest-for-builders (prior) | Separate idea; already HOLD 6/8 waiting evidence |

---

## Next

- **HOLD** — do **not** hand Builder a marketplace SPEC yet.
- Optional narrow re-brief: Verified Shelf (≤10) + waitlist for install-hook partners → then re-Judge.
- LEDGER next: Chief (HOLD — evidence / narrow scope before Builder).
