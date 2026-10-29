# Verified Shelf v1 · build/

Static curated shelf (≤10 design anti-slop packs) with pin + SHA-256 + verify link before Cursor install.

## Open the site

From this `build/` directory:

```bash
python3 -m http.server 8765
```

Then open http://127.0.0.1:8765/ (file:// may block `fetch` of JSON in some browsers).

## Run acceptance tests (AT1–AT7)

```bash
python3 tests/run_acceptance.py
# or from idea root:
python3 ../tests/run_acceptance.py
```

Stdlib only. Expect `SUMMARY 7 passed, 0 failed, 7 total`.

## Data

- `data/shelf.json` — pack catalog (edit + refresh)
- `data/config.json` — vertical, install_runtime, waitlist_url/email, max_packs
- `verify/manual-checklist.html` — shared `manual_checklist` verify page

## Out of scope (intentionally absent)

Search marketplace · seller upload · checkout · multi-runtime install matrix
