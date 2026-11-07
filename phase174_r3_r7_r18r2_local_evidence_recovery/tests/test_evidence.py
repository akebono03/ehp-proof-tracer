"""Fail-closed tests for missing, present and invalid profile-local R17 records."""
from __future__ import annotations

import ast
import json
import os
import sys
import tempfile
import types
from pathlib import Path
from typing import Any

import pytest

from phase174_r3_r7_r18r2_local_evidence_recovery.patch import (
    EXPECTED_R18R1_SHA256,
    EXPECTED_R18R2_SHA256,
    REPLACEMENT_FUNCTION,
    checked_replacement,
    sha256,
    transform,
)


def _load_validator(monkeypatch: pytest.MonkeyPatch, local: Path, live: dict[str, Any]):
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    fake_parent = types.ModuleType("phase174_r3_r7_r17_typed_map_open_goal")
    fake_parent.__path__ = []
    fake = types.ModuleType("phase174_r3_r7_r17_typed_map_open_goal.audit")
    fake.inspect_public_map_display = lambda: dict(live)
    monkeypatch.setitem(sys.modules, "phase174_r3_r7_r17_typed_map_open_goal", fake_parent)
    monkeypatch.setitem(sys.modules, "phase174_r3_r7_r17_typed_map_open_goal.audit", fake)
    source = REPLACEMENT_FUNCTION.read_text(encoding="utf-8")
    context = {"Any": Any, "Path": Path, "json": json,
               "os": os, "tempfile": tempfile}
    exec(compile(source, "validate_prior_r17.py", "exec"), context)
    return context["validate_prior_r17"]


def _valid_live() -> dict[str, Any]:
    return {
        "public_root_candidates": 1,
        "public_delta_surjectivity_candidates": 0,
        "generic_isomorphism_depends_on_surjectivity": True,
        "direct_given_for_goal_or_delta": False,
        "delta_latex": r"\Delta: \pi_{13}^{13} \twoheadrightarrow \pi_{11}^{6}",
        "search_status": "search_failed",
        "proven_steps": 0,
        "completion_claimed": False,
    }


def _write_report(local: Path, index: int, *, gate: str | None = None) -> None:
    options = (
        ("phase174_r3_r7_r17/typed_map_public_audit.json", "174-R3-R7-R17",
         "PASS_TYPED_DELTA_OPEN_GOAL_SURJECTIVITY_STILL_PENDING"),
        ("phase174_r3_r7_r17r1/historical_contract_audit.json", "174-R3-R7-R17R1",
         "PASS_HISTORICAL_TEST_CONTRACT_CORRECTED_R17_PUBLIC_UNCHANGED"),
    )
    relative, phase, expected_gate = options[index]
    path = local / "EHPProofTracerAudit" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "phase": phase, "gate": expected_gate if gate is None else gate,
        "new_group_given": 0, "full_pytest_run": False,
    }), encoding="utf-8")


def test_exact_function_replacement_changes_no_other_definitions() -> None:
    base, patched = checked_replacement(root=Path(__file__).resolve().parents[2])
    assert sha256(base) == EXPECTED_R18R1_SHA256
    assert sha256(patched) == EXPECTED_R18R2_SHA256
    old_tree = ast.parse(base.decode("utf-8"))
    new_tree = ast.parse(patched.decode("utf-8"))
    for node in old_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "validate_prior_r17":
            old_tree.body.remove(node)
            break
    for node in new_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "validate_prior_r17":
            new_tree.body.remove(node)
            break
    assert ast.dump(old_tree, include_attributes=False) == ast.dump(new_tree, include_attributes=False)


def test_missing_reports_recheck_live_without_creating_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = _load_validator(monkeypatch, tmp_path, _valid_live())
    result = validator()
    assert result["recovery"]["mode"] == "LIVE_REVALIDATED_NO_SYNTHETIC_REPORT"
    assert len(result["recovery"]["missing_local_reports"]) == 2
    assert "LIVE_PUBLIC_BOUNDARY_REVALIDATED" in result["174-R3-R7-R17"]
    assert "CORRECTED_TEST_SOURCE_PINNED" in result["174-R3-R7-R17R1"]
    assert not tuple(tmp_path.rglob("*.json"))


def test_both_valid_reports_no_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _write_report(tmp_path, 0)
    _write_report(tmp_path, 1)
    validator = _load_validator(monkeypatch, tmp_path, _valid_live())
    result = validator()
    assert "recovery" not in result
    assert result["174-R3-R7-R17"].startswith("PASS_")
    assert result["174-R3-R7-R17R1"].startswith("PASS_")


def test_only_one_missing_report_rechecks_public_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_report(tmp_path, 0)
    validator = _load_validator(monkeypatch, tmp_path, _valid_live())
    result = validator()
    assert result["174-R3-R7-R17"].startswith("PASS_")
    assert len(result["recovery"]["missing_local_reports"]) == 1


@pytest.mark.parametrize("key,value", (
    ("public_root_candidates", 0),
    ("public_delta_surjectivity_candidates", 1),
    ("generic_isomorphism_depends_on_surjectivity", False),
    ("direct_given_for_goal_or_delta", True),
    ("search_status", "complete"),
    ("proven_steps", 1),
    ("completion_claimed", True),
    ("delta_latex", "unrecognized"),
))
def test_bad_live_frontier_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, key: str, value: object,
) -> None:
    live = _valid_live()
    live[key] = value
    validator = _load_validator(monkeypatch, tmp_path, live)
    with pytest.raises(RuntimeError, match="Live R17 proof boundary"):
        validator()


def test_existing_bad_report_is_never_silently_recovered(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_report(tmp_path, 0, gate="FORGED_PASS")
    validator = _load_validator(monkeypatch, tmp_path, _valid_live())
    with pytest.raises(RuntimeError, match="Prior R17 evidence inconsistent"):
        validator()


def test_duplicate_or_missing_function_anchor_fails_closed() -> None:
    new = REPLACEMENT_FUNCTION.read_text(encoding="utf-8")
    with pytest.raises(RuntimeError):
        transform(b"def other():\n    pass\n", new)
    with pytest.raises(RuntimeError):
        transform(b"def validate_prior_r17() -> dict[str, Any]:\n    pass\n", new)
