# TEST_REPORT · skill-pack-marketplace Verified Shelf v1

**When:** 2026-10-29 16:02 Asia/Shanghai  
**Runner:** `python3 build/tests/run_acceptance.py` (stdlib only)  
**Result:** **7 passed, 0 failed, 7 total**

## Per AT

| AT | result | notes |
| --- | --- | --- |
| AT1 | PASS | 8 packs; cards show name, pinned_ref, content_sha256, verify_url, install_command |
| AT2 | PASS | fixture with 11 packs fails: `shelf max is 10, got 11` |
| AT3 | PASS | missing content_sha256 / verify_url / pinned_ref rejected; live shelf complete |
| AT4 | PASS | install_runtime=cursor; one install_command per card |
| AT5 | PASS | waitlist_url + email CTA; no POST form backend |
| AT6 | PASS | SHA on card; install CTA gated on hash (`hasHash`) |
| AT7 | PASS | no checkout / seller / search routes under build/ |

## Command output

```
$ python3 build/tests/run_acceptance.py
PASS AT1: 8 packs; cards show pin/hash/verify/install
PASS AT2: shelf max is 10, got 11
PASS AT3: missing pin/hash/verify rejected; live shelf complete
PASS AT4: install_runtime=cursor; one command per card
PASS AT5: link CTA → waitlist_url; email shown; no form backend
PASS AT6: SHA on card; install CTA only when hash present
PASS AT7: no checkout/seller/search routes

SUMMARY 7 passed, 0 failed, 7 total
```

## Hash provenance

Content SHA-256 values were computed with `sha256sum` on raw GitHub files at the pinned commit (not invented). Spot-check: `pbakaus/impeccable` `.cursor/skills/impeccable/SKILL.md` matches shelf entry.
