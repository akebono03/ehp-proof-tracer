"""R13 audit contracts, source guards and no-public-wiring checks."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r13_cited_annihilator_bridge.audit import (
    REVIEWED_HEAD, SOURCE_BLOBS, git_blob_sha, matches_source_blob,
    validate_r12_report,
)


def sample_r12() -> dict:
    return {
        "phase": "174-R3-R7-R12",
        "gate": "PASS_ISOLATED_CITED_ANNIHILATOR_SOURCE_UNWIRED",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "live": {
            "independent_source_candidate_count": 1,
            "production_source_given_count": 0,
            "production_cited_specialization_count": 0,
            "production_left_zero_proposals": {"proposal_count": 1},
            "production_left_zero_rule_names": ["equality symmetry"],
            "source_as_proof_leaf_created": False,
            "new_verified_steps": 0,
            "public_provider_unchanged": True,
        },
    }


def test_valid_r12_report_is_a_gate_not_cited_source() -> None:
    result = validate_r12_report(sample_r12())
    assert result["gate"] == "PASS_ISOLATED_CITED_ANNIHILATOR_SOURCE_UNWIRED"
    assert result["public_source_count"] == 0


@pytest.mark.parametrize("field,bad", (
    ("gate", "PASS_PREFLIGHT"), ("new_group_given", 1),
    ("new_production_inference_rules", 1), ("public_provider_changed", True),
    ("completion_claimed", True), ("full_pytest_run", True),
))
def test_changed_r12_trust_boundary_fails_closed(field: str, bad: object) -> None:
    report = sample_r12()
    report[field] = bad
    with pytest.raises(RuntimeError):
        validate_r12_report(report)


@pytest.mark.parametrize("field,bad", (
    ("independent_source_candidate_count", 0),
    ("production_source_given_count", 1),
    ("production_cited_specialization_count", 1),
    ("new_verified_steps", 1),
    ("source_as_proof_leaf_created", True),
    ("public_provider_unchanged", False),
    ("production_left_zero_rule_names", ["cited Toda (5.9)"]),
))
def test_unproved_r12_live_claims_cannot_be_promoted(field: str, bad: object) -> None:
    report = sample_r12()
    report["live"][field] = bad
    with pytest.raises(RuntimeError):
        validate_r12_report(report)


def test_unexpected_left_zero_candidate_count_rejected() -> None:
    report = sample_r12()
    report["live"]["production_left_zero_proposals"]["proposal_count"] = 2
    with pytest.raises(RuntimeError):
        validate_r12_report(report)


def test_40_character_blob_guard_with_crlf_and_mutation() -> None:
    value = b"one\ntwo\n"
    sha = git_blob_sha(value)
    assert matches_source_blob(value, sha)
    assert matches_source_blob(b"one\r\ntwo\r\n", sha)
    assert not matches_source_blob(value, sha[:-1])
    assert not matches_source_blob(value + b"modified", sha)
    assert all(len(sha) == 40 for sha in SOURCE_BLOBS.values())
    assert len(REVIEWED_HEAD) == 40


def test_registry_does_not_import_narrative_or_public_patcher() -> None:
    registry_file = Path(__file__).resolve().parents[1] / "registry.py"
    tree = ast.parse(registry_file.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {"build_isolated_toda59_annihilator_bridge", "reviewed_toda59_source_position", "join_isolated_source_bridge"} <= functions
    assert not {"patch", "install", "write_production"} & functions
    names = registry_file.read_text(encoding="utf-8")
    assert "TodaPrimaryGroupZeroStatement" not in names
    assert "pi_12" not in names
    assert "ProofRule.GIVEN" in names


def test_audit_contains_no_production_installer() -> None:
    audit_file = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(audit_file.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {"verify_git_and_sources", "validate_r12_report", "inspect_isolated_registration_and_proof"} <= functions
    assert not {"install", "patch", "mutate_production", "register_group_given"} & functions
