"""Focused contracts for Phase 175 R4R14R13; no full suite is run."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r4r14r13_final_gate_preflight import audit


def test_six_groups_are_in_review_scope() -> None:
    assert audit.PAIRS == tuple((n, 4) for n in range(2, 8))


def test_document_change_paths_are_allowed_only_for_reviewed_files() -> None:
    result = audit.classify_dirty_paths(
        ("README.md", "docs/proof_records.md"),
        ("README.md", "docs/proof_records.md"),
    )
    assert result["modified_documents"] == ["README.md", "docs/proof_records.md"]
    assert result["unexpected_tracked"] == []


def test_changed_source_code_blocks_preflight() -> None:
    result = audit.classify_dirty_paths(
        ("phase165_r52_r9_shared_math.py",), ("README.md",),
    )
    assert result["unexpected_tracked"] == ["phase165_r52_r9_shared_math.py"]


def test_cache_changes_are_reported_not_erased() -> None:
    result = audit.classify_dirty_paths(
        (".pytest_cache/v/cache/nodeids",), ("README.md",),
    )
    assert result["tracked_pytest_cache"] == [".pytest_cache/v/cache/nodeids"]
    assert result["cache_requires_explicit_cleanup_decision"] is True


def test_documents_are_complete_and_match_r12_output() -> None:
    result = audit.validate_documents(audit.ROOT)
    assert len(result) == 5
    assert all(row["history_retained"] and row["r12_full_output_verified"] for row in result.values())


def test_document_mutation_is_detected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from phase175_r4r14r12_closeout_documents.build_documents import DOCUMENT_BLOBS
    repo = tmp_path
    name = "README.md"
    (repo / name).write_text("# Incorrect document\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="MISSING_COMPLETE_DOCUMENT_OR_R12_ARCHIVE"):
        audit.validate_documents(repo)
    assert name in DOCUMENT_BLOBS


def test_checkout_preflight_preserves_known_guard_failures() -> None:
    status = audit.preflight()
    assert status["document_count"] == 5
    assert len(status["historical_test_names"]) == 4
    assert status["legacy_guard_policy_resolved"] is False
    assert status["full_pytest"] == "NOT_RUN"


def test_audit_never_closes_phase(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(audit, "collect_worker", lambda n, k, timeout: {
        "n": n, "k": k, "status": "complete", "open_goals": 0,
    })
    result = audit.audit(30)
    assert result["complete_groups"] == 6
    assert result["phase175_formally_closed"] is False
    assert result["final_gate_requires_full_pytest"] is True


def test_incomplete_group_is_not_promoted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(audit, "collect_worker", lambda n, k, timeout: {
        "n": n, "k": k, "status": "partial" if n == 5 else "complete",
        "open_goals": 1 if n == 5 else 0,
    })
    with pytest.raises(RuntimeError, match="SIX_K4_COMPLETED_GROUPS_REQUIRED"):
        audit.audit(30)
