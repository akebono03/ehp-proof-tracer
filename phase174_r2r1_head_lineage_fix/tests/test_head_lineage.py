"""Validate the separate HEADs for R1 evidence and the R2 audit."""
from __future__ import annotations

import json

import pytest

from phase174_r2_source_math_audit.audit import (
    REVIEWED_HEAD,
    R1_BASELINE_HEAD,
    TARGETS,
    audit_prior_record,
)


def _r1_record(head: str) -> dict[str, object]:
    counts = {(5, 3): 3, (4, 8): 3, (4, 9): 2}
    abstract_keys = {(4, 8), (4, 9)}
    return {
        "local_head": head,
        "rows": [
            {
                "n": n,
                "k": k,
                "runtime_error": None,
                "result": {
                    "status": "search_failed",
                    "open_goal_count": counts[(n, k)],
                    "open_goals": [
                        {"type": "RecordedGoal", "repr": "recorded"}
                        for _ in range(counts[(n, k)])
                    ],
                    "proven_step_count": 0,
                    "abstract_certificate": (
                        {"verified": True}
                        if (n, k) in abstract_keys else None
                    ),
                },
            }
            for n, k in TARGETS
        ],
    }


def _write_record(monkeypatch, tmp_path, record):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    destination = tmp_path / "EHPProofTracerAudit" / "phase174_r1"
    destination.mkdir(parents=True)
    (destination / "audit.json").write_text(
        json.dumps(record, ensure_ascii=False), encoding="utf-8"
    )


def test_r2_head_changes_but_r1_evidence_preserves_its_original_head():
    assert REVIEWED_HEAD == "3558d713fd7939ded656f2458aacc62d71c7e0b3"
    assert R1_BASELINE_HEAD == "cb85913905b2f7452bda2a2c4428e6fe5a3a793a"
    assert REVIEWED_HEAD != R1_BASELINE_HEAD


def test_r1_record_from_previous_committed_ancestor_is_accepted(monkeypatch, tmp_path):
    _write_record(monkeypatch, tmp_path, _r1_record(R1_BASELINE_HEAD))
    result = audit_prior_record()
    assert result["verified_head"] == R1_BASELINE_HEAD
    assert len(result["rows"]) == 3
    assert [row["open_goal_count"] for row in result["rows"]] == [3, 3, 2]
    assert [row["abstract_certified"] for row in result["rows"]] == [False, True, True]


def test_r1_evidence_is_not_retroactively_rewritten(monkeypatch, tmp_path):
    _write_record(monkeypatch, tmp_path, _r1_record(REVIEWED_HEAD))
    with pytest.raises(ValueError, match="R1 audit report HEAD differs"):
        audit_prior_record()
