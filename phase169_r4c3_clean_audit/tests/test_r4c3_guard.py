"""R4C3: preserve tracked output bytes; never weaken verified proof checks."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase169_r4c3_clean_audit.runner import (
    restore_files,
    snapshot_files,
    validated_report,
)


def _good_report() -> dict:
    return {
        "iso_derived": True,
        "pi6_4_status": "complete",
        "pi6_4_open_goals": [],
        "pi6_4_steps": 18,
        "toda45_stable_range_relaxed": False,
        "cited_source_ancestors": {
            "TodaProp44UniversalStatement": True,
            "TodaProp42GeneralExactnessStatement": True,
            "Toda51BelowDiagonalZeroStatement": True,
        },
    }


def test_r4c3_restore_exact_tracked_output_bytes(tmp_path: Path) -> None:
    md = tmp_path / "audit.md"
    data = tmp_path / "audit.json"
    original_md = "検査前\r\n".encode("utf-8")
    original_json = b'{"old": true}\r\n'
    md.write_bytes(original_md)
    data.write_bytes(original_json)
    snap = snapshot_files((md, data))
    md.write_text("changed\n", encoding="utf-8")
    data.write_text('{"new": true}\n', encoding="utf-8")
    restore_files(snap)
    assert md.read_bytes() == original_md
    assert data.read_bytes() == original_json


def test_r4c3_restore_previously_missing_report(tmp_path: Path) -> None:
    md = tmp_path / "audit.md"
    data = tmp_path / "audit.json"
    data.write_bytes(b"original")
    snap = snapshot_files((md, data))
    md.write_bytes(b"new")
    data.write_bytes(b"modified")
    restore_files(snap)
    assert not md.exists()
    assert data.read_bytes() == b"original"


def test_r4c3_accepts_complete_source_backed_proof(tmp_path: Path) -> None:
    report = tmp_path / "audit.json"
    original = _good_report()
    report.write_text(json.dumps(original), encoding="utf-8")
    assert validated_report(report) == original


def test_r4c3_rejects_partial_and_missing_ancestor(tmp_path: Path) -> None:
    report = tmp_path / "audit.json"
    original = _good_report()
    original["pi6_4_status"] = "partial"
    report.write_text(json.dumps(original), encoding="utf-8")
    with pytest.raises(RuntimeError, match="completed proof"):
        validated_report(report)
    original = _good_report()
    original["cited_source_ancestors"]["TodaProp44UniversalStatement"] = False
    report.write_text(json.dumps(original), encoding="utf-8")
    with pytest.raises(RuntimeError, match="completed proof"):
        validated_report(report)


def test_r4c3_rejects_relaxed_stable_range_and_open_goals(tmp_path: Path) -> None:
    report = tmp_path / "audit.json"
    original = _good_report()
    original["toda45_stable_range_relaxed"] = True
    report.write_text(json.dumps(original), encoding="utf-8")
    with pytest.raises(RuntimeError, match="completed proof"):
        validated_report(report)
    original = _good_report()
    original["pi6_4_open_goals"] = ["unsupported"]
    report.write_text(json.dumps(original), encoding="utf-8")
    with pytest.raises(RuntimeError, match="completed proof"):
        validated_report(report)
