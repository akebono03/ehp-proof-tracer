"""Focused R3R19 read-only inventory contracts."""
from __future__ import annotations

import json

import pytest

from phase176_r3r19_cyclic_structure_frontier import audit


def test_source_guard_rejects_missing_file(tmp_path):
    with pytest.raises(RuntimeError, match="SOURCE_MISSING"):
        audit.check_sources(tmp_path)


def test_source_guard_rejects_changed_anchor(tmp_path):
    for name, anchors in audit.REQUIRED_SOURCES.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(anchors), encoding="utf-8")
    assert len(audit.check_sources(tmp_path)) == len(audit.REQUIRED_SOURCES)
    first = tmp_path / next(iter(audit.REQUIRED_SOURCES))
    first.write_text("changed", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_MISSING"):
        audit.check_sources(tmp_path)


def test_summarize_preserves_subgoal_identity():
    class Rule:
        name = "fixture"
    class Option:
        rule = Rule()
        subgoals = ("child",)
    assert audit.summarize((Option(),)) == [
        {"rule": "fixture", "subgoals": ["'child'"], "subgoal_count": 1}
    ]


def test_dry_run_does_not_call_worker(monkeypatch, tmp_path):
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "fixture"})
    monkeypatch.setattr(audit, "worker", lambda timeout: pytest.fail("worker called"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 1) == 0
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["root_proof_complete"] is False
    assert report["gate"] == "PASS_R3R19_READ_ONLY_DRYRUN"
    assert report["full_pytest"] == "NOT_RUN"
