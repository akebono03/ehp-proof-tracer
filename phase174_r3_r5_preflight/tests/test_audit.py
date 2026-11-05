"""Focused tests of the R3-R5 read-only preimplementation audit."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r5_preflight.audit import (
    check_transcription,
    inspect_public_frontier,
    inspect_source_provider,
)


def test_toda48_and_toda55_original_conditions_are_present() -> None:
    root = Path(__file__).resolve().parents[2]
    checks = check_transcription(root)
    assert len(checks) == 5
    assert all(checks.values())


def test_r3r4_provider_remains_connected_without_edits() -> None:
    root = Path(__file__).resolve().parents[2]
    contract = inspect_source_provider(root)
    assert contract["delta_provider_hook_present"] is True
    assert contract["production_source_changed_by_this_audit"] is False
    assert contract["state"] in ("COMMITTED", "WORKTREE_PATCHED")


def test_public_frontier_has_no_premature_certificate() -> None:
    inspected = inspect_public_frontier()
    assert inspected["root_goal_type"] == "Relation"
    assert inspected["cyclic_child_type"] == "CyclicStructureStatement"
    assert inspected["delta_zero_proposal_count"] == 1
    assert inspected["new_given"] == 0
    assert inspected["new_proof_steps"] == 0
    assert inspected["proven_named_group"] is False


def test_transcription_refuses_missing_zero_delta_condition(tmp_path: Path) -> None:
    original = Path(__file__).resolve().parents[2]
    for chapter in ("04", "05"):
        source = original / f"sources/toda/Toda_{chapter}_2.tex"
        destination = tmp_path / f"sources/toda/Toda_{chapter}_2.tex"
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_text(encoding="utf-8-sig")
        if chapter == "04":
            data = data.replace(r"\Delta(\iota_{2n-1})=0", "condition omitted")
        destination.write_text(data, encoding="utf-8")
    with pytest.raises(ValueError, match="toda48_delta_zero_condition"):
        check_transcription(tmp_path)
