#!/usr/bin/env python3
"""Wrapper: run build/tests/run_acceptance.py from idea root."""
import runpy
from pathlib import Path

target = Path(__file__).resolve().parents[1] / "build" / "tests" / "run_acceptance.py"
runpy.run_path(str(target), run_name="__main__")
