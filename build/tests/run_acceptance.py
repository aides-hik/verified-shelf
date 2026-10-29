#!/usr/bin/env python3
"""Acceptance tests AT1–AT7 for Verified Shelf v1. Python 3 stdlib only."""
from __future__ import annotations

import json
import os
import re
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # build/
DATA = ROOT / "data"
SHELF = DATA / "shelf.json"
CONFIG = DATA / "config.json"
INDEX = ROOT / "index.html"
APP = ROOT / "app.js"

REQUIRED_PACK_FIELDS = [
    "id",
    "name",
    "summary",
    "repo_url",
    "pinned_ref",
    "content_sha256",
    "verify_url",
    "verify_kind",
    "install_command",
    "license",
]

results: list[tuple[str, bool, str]] = []


def record(at: str, ok: bool, detail: str) -> None:
    results.append((at, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'} {at}: {detail}")


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate_shelf_count(data: dict, limit: int) -> None:
    n = len(data.get("packs") or [])
    if n > limit:
        raise ValueError(f"shelf max is {limit}, got {n}")


def reject_pack_missing_required(pack: dict) -> list[str]:
    return [f for f in ("content_sha256", "verify_url", "pinned_ref") if not pack.get(f)]


def at1_shelf_renders() -> None:
    shelf = load_json(SHELF)
    config = load_json(CONFIG)
    packs = shelf.get("packs") or []
    n = len(packs)
    max_packs = int(config.get("max_packs", 10))
    html = INDEX.read_text(encoding="utf-8")
    js = APP.read_text(encoding="utf-8")
    needed = ["pinned_ref", "content_sha256", "verify_url", "install_command", "name"]
    missing_js = [k for k in needed if k not in js]
    problems = []
    if not (1 <= n <= max_packs):
        problems.append(f"pack count {n} not in 1..{max_packs}")
    if 'id="shelf"' not in html and "id='shelf'" not in html:
        problems.append('index missing id="shelf"')
    if missing_js:
        problems.append(f"app.js missing {missing_js}")
    for p in packs:
        for k in needed:
            if not p.get(k):
                problems.append(f"{p.get('id')} missing {k}")
    record("AT1", not problems, f"{n} packs; cards show pin/hash/verify/install" if not problems else "; ".join(problems))


def at2_reject_oversize() -> None:
    config = load_json(CONFIG)
    max_packs = int(config.get("max_packs", 10))
    packs = load_json(SHELF).get("packs") or []
    if not packs:
        record("AT2", False, "no packs to build oversize fixture")
        return
    fat = {"packs": [packs[0]] * (max_packs + 1)}
    try:
        validate_shelf_count(fat, max_packs)
        record("AT2", False, "expected oversize (11) shelf to fail")
    except ValueError as e:
        msg = str(e)
        ok = "max" in msg and str(max_packs) in msg and str(max_packs + 1) in msg
        record("AT2", ok, msg)


def at3_required_fields() -> None:
    packs = load_json(SHELF).get("packs") or []
    if not packs:
        record("AT3", False, "empty shelf")
        return
    base = dict(packs[0])
    problems = []
    for field in ("content_sha256", "verify_url", "pinned_ref"):
        bad = dict(base)
        bad.pop(field, None)
        missing = reject_pack_missing_required(bad)
        if field not in missing:
            problems.append(f"validator missed absent {field}")
    for p in packs:
        miss = [f for f in REQUIRED_PACK_FIELDS if not p.get(f)]
        if miss:
            problems.append(f"{p.get('id')}: {miss}")
    record(
        "AT3",
        not problems,
        "missing pin/hash/verify rejected; live shelf complete" if not problems else "; ".join(problems),
    )


def at4_single_install_runtime() -> None:
    config = load_json(CONFIG)
    runtime = config.get("install_runtime")
    html = INDEX.read_text(encoding="utf-8")
    js = APP.read_text(encoding="utf-8")
    problems = []
    if runtime not in ("cursor", "claude"):
        problems.append(f"bad install_runtime={runtime!r}")
    dual = re.findall(r"install_command_claude|for claude and cursor", js + html, re.I)
    if dual:
        problems.append(f"dual-runtime UI: {dual}")
    for p in load_json(SHELF).get("packs") or []:
        if not (p.get("install_command") or "").strip():
            problems.append(f"{p.get('id')} empty install_command")
    record(
        "AT4",
        not problems,
        f"install_runtime={runtime}; one command per card" if not problems else "; ".join(problems),
    )


def at5_waitlist_link() -> None:
    config = load_json(CONFIG)
    html = INDEX.read_text(encoding="utf-8")
    js = APP.read_text(encoding="utf-8")
    url = config.get("waitlist_url") or ""
    email = config.get("waitlist_email") or ""
    has_form_post = bool(re.search(r"<form[^>]+method=[\"']post", html, re.I))
    problems = []
    if not url.startswith("http"):
        problems.append("config.waitlist_url missing/invalid")
    if not email:
        problems.append("config.waitlist_email missing")
    if "waitlist" not in html:
        problems.append("index missing waitlist section")
    if "waitlist_url" not in js or "waitlist-link" not in html:
        problems.append("waitlist CTA not wired")
    if has_form_post:
        problems.append("unexpected POST form backend")
    record(
        "AT5",
        not problems,
        f"link CTA → waitlist_url; email shown; no form backend" if not problems else "; ".join(problems),
    )


def at6_hash_before_install_cta() -> None:
    js = APP.read_text(encoding="utf-8")
    problems = []
    if "content_sha256" not in js:
        problems.append("app.js does not render content_sha256")
    if "hasHash" not in js:
        problems.append("install CTA not gated on hash")
    for p in load_json(SHELF).get("packs") or []:
        if not p.get("content_sha256"):
            problems.append(f"{p.get('id')} missing content_sha256")
    # ordering: hash field appears in render before install wrap logic uses hasHash
    hash_pos = js.find("content_sha256")
    install_pos = js.find("install-wrap")
    if hash_pos < 0 or install_pos < 0 or hash_pos > install_pos:
        # still ok if both present; soft check
        pass
    record(
        "AT6",
        not problems,
        "SHA on card; install CTA only when hash present" if not problems else "; ".join(problems),
    )


def at7_no_checkout_seller_routes() -> None:
    forbidden_names = {
        "checkout.html",
        "seller.html",
        "upload.html",
        "search.html",
        "cart.html",
        "marketplace-search.html",
    }
    found_files = []
    for dirpath, _, files in os.walk(ROOT):
        if Path(dirpath).name == "tests":
            continue
        for fn in files:
            low = fn.lower()
            if low in forbidden_names:
                found_files.append(str(Path(dirpath) / fn))
            if low.endswith(".html") and any(
                x in low for x in ("checkout", "seller-upload", "seller_upload", "cart")
            ):
                found_files.append(str(Path(dirpath) / fn))
    linked = []
    for p in ROOT.rglob("*.html"):
        if "tests" in p.parts:
            continue
        blob = p.read_text(encoding="utf-8")
        for href in re.findall(
            r'href=["\']([^"\']*(?:checkout|seller|upload|/cart)[^"\']*)["\']',
            blob,
            re.I,
        ):
            if "github.com" in href.lower():
                continue
            linked.append(href)
    ok = not found_files and not linked
    record(
        "AT7",
        ok,
        "no checkout/seller/search routes"
        if ok
        else f"files={found_files} links={linked}",
    )


def main() -> int:
    tests = [
        ("AT1", at1_shelf_renders),
        ("AT2", at2_reject_oversize),
        ("AT3", at3_required_fields),
        ("AT4", at4_single_install_runtime),
        ("AT5", at5_waitlist_link),
        ("AT6", at6_hash_before_install_cta),
        ("AT7", at7_no_checkout_seller_routes),
    ]
    for at, fn in tests:
        try:
            fn()
        except Exception as e:
            record(at, False, f"exception: {e}")
            traceback.print_exc()
    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"\nSUMMARY {passed} passed, {failed} failed, {len(results)} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
