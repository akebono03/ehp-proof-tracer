"""Tests for frozen public narratives on the canonical group-query route."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase165_r4_golden_baseline.golden import CASES, baseline_path, capture, compare


def test_pi3_2_golden_narrative() -> None:
    name, n, k = CASES[0]
    expected = json.loads(baseline_path(name).read_text(encoding="utf-8"))
    compare(capture(name, n, k), expected)


def test_pi4_3_golden_narrative() -> None:
    name, n, k = CASES[1]
    expected = json.loads(baseline_path(name).read_text(encoding="utf-8"))
    compare(capture(name, n, k), expected)


def test_golden_comparison_rejects_drift() -> None:
    name, n, k = CASES[0]
    expected = json.loads(baseline_path(name).read_text(encoding="utf-8"))
    changed = dict(expected)
    changed["markdown"] = changed["markdown"] + "\nUNINTENDED CHANGE"
    try:
        compare(changed, expected)
    except AssertionError as error:
        assert "golden baseline mismatch" in str(error)
    else:
        raise AssertionError("golden baseline comparison accepted a mutation")
