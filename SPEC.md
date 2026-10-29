# SPEC · skill-pack-marketplace (Verified Shelf v1)

## Problem (3 sentences)

Agent builders install skill packs like npm (`npx skills add`, ClawHub, GitHub) and hit stealers, injection, or silent post-install tampering — scanners and indexes exist but are separate and not the default install gate. ([Unit 42](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/), [THN 341 malicious ClawHub skills](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)). Stars and seller self TEST-REPORTs are weak trust signals ([PH Agent Skills](https://www.producthunt.com/products/agent-skills-3)). v1 is **not** a 100k marketplace: it is a curated **Verified Shelf** of ≤10 packs where each listing shows pinned version + content hash + scan/checklist link **before** install.

## User stories

1. As a coding-agent user scared by ClawHub malware news, I can open one static shelf page, see ≤10 packs with pin hash + verify artifact, and copy a single install command for one agent runtime.
2. As a buyer comparing packs, I can see the same verify fields on every card (name, vertical, pinned commit/tag, content SHA-256, scan/checklist URL, install path) so stars alone are not the signal.
3. As a waitlist visitor, I can leave an email for “notify when shelf grows / install-hook partners” without creating an account.
4. As an operator (us), I can add/edit shelf entries by editing one JSON/YAML data file and rebuilding — no admin UI in v1.

## Out of scope (v1)

- Crawling or indexing 100k+ skills / replacing VirusTotal
- Own Sigstore / continuous post-install re-verify hooks
- Sandbox Lift farm / SkillzBench-class scoring engine
- Multi-agent install matrix (pick **one** runtime for v1)
- Paid checkout, refunds, seller dashboards
- Cross-pack AI-slop automated benchmark suite
- Browser extension or patching `npx skills add` itself

## Product shape (v1)

| piece | choice |
| --- | --- |
| Surface | Static site under `build/` (HTML+CSS+JS or minimal static generator) |
| Catalog size | ≤10 packs, one vertical |
| Vertical | **design anti-slop** (resolved) |
| Install path | **Cursor** only (resolved) |
| Per-pack fields | `id`, `name`, `summary`, `repo_url`, `pinned_ref`, `content_sha256`, `verify_url`, `verify_kind` (`skillspector` \| `manual_checklist` \| `acidtest`), `install_command`, `license` |
| Waitlist | Link to existing waitlist canvas + show `paininbox+waitlist@mail.grokbot.com` (resolved) |
| Languages | UI: English primary; Chinese secondary labels OK |

## Acceptance tests (Given / When / Then)

### AT1 · Shelf renders ≤10 verified cards
- **Given** `build/data/shelf.json` contains N packs where 1 ≤ N ≤ 10  
- **When** I open the shelf index page  
- **Then** I see exactly N cards, each showing name, pinned_ref, content_sha256 (or truncated with full in detail), verify_url link, and install_command

### AT2 · Reject oversize catalog at build/test time
- **Given** `shelf.json` contains 11 packs  
- **When** validation / tests run  
- **Then** the check fails with a clear error that the shelf max is 10

### AT3 · Required verify fields
- **Given** a pack missing `content_sha256` or `verify_url` or `pinned_ref`  
- **When** validation runs  
- **Then** that pack is rejected (test fails)

### AT4 · Single install path documented
- **Given** site config `install_runtime` is set to one of `cursor` \| `claude`  
- **When** I view any pack card  
- **Then** the install command matches that runtime only (no second runtime commands on the card)

### AT5 · Waitlist capture
- **Given** I am on the landing/shelf page  
- **When** I submit a valid email on the waitlist form  
- **Then** I see a success state (and in test: handler records the email or returns 204/200 stub)

### AT6 · Hash pin displayed before install CTA
- **Given** a pack with known `content_sha256`  
- **When** I view its card  
- **Then** the SHA is visible above or beside the install command (install CTA is not shown without the hash field present in data)

### AT7 · Out-of-scope pages absent
- **Given** the built site  
- **When** I look for marketplace search, seller upload, or checkout routes  
- **Then** none exist (404 or not linked)

## Dependencies policy

- Original code only under `build/`
- Open-source dependencies only; list name + license in `DEPENDENCIES.md`
- Prefer zero or minimal runtime deps (static files + Node/Python test runner)

## Success for Builder DONE

- `SPEC.md` (this file) + answered open questions reflected in SPEC
- `build/` v1 implementing ATs
- `DEPENDENCIES.md`
- Tests for every AT → `TEST_REPORT.md`
- One PR opened (never merge); routine on that PR for failing checks
- LEDGER: Builder DONE → `build/` → next: Pitch, Buyer

## Resolved answers (2026-10-29 Asia/Shanghai)

| Q | Answer |
| --- | --- |
| Q1 vertical | `design anti-slop` |
| Q2 install_runtime | `cursor` |
| Q3 initial packs | A — public GitHub hot packs + real repo + content hash |
| Q4 waitlist | C — existing waitlist page https://cursor.com/canvas/store-ee6f3732-a655-4ad3-9b18-3885346d8283/433e4d1a-fe1c-4541-9466-8deeede412fd · email `paininbox+waitlist@mail.grokbot.com` |

Site config defaults: `vertical=design-anti-slop`, `install_runtime=cursor`. Waitlist CTA links to the canvas above (and shows the signup email); no new form backend.

