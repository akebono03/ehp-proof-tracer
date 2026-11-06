"""Source, reviewed-HEAD, evidence and non-promotion contracts for R12."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r12_toda59_annihilator_source.audit import (
    ALLOWED_SUCCESSOR, BASE_HEAD, REVIEWED_R11_HEAD, SOURCE_BLOBS,
    git_blob_sha, reviewed_head_lineage, source_blob_matches,
    validate_r11_evidence,
)


def certified_r11_fixture() -> dict:
    return {
        "phase": "174-R3-R7-R11",
        "gate": "PASS_READ_ONLY_CANONICAL_FIXTURE_GAP",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "canonical_full_composite_candidate_count": 1,
            "diagnostic_symbols_are_not_verified_aliases": True,
            "canonical_source_from_explicit_database_goal": True,
            "canonical_left_rule_names": ["equality symmetry"],
            "transcription_not_promoted_to_proof": True,
            "public_provider_unchanged": True,
            "new_verified_steps": 0,
            "public_canonical_full_image": {"proposal_count": 1},
            "public_canonical_nu_image": {"proposal_count": 1},
            "public_canonical_eta_square_image": {"proposal_count": 1},
            "public_canonical_left_zero": {"proposal_count": 1},
        },
    }


def test_valid_r11_report_is_evidence_not_an_installed_source() -> None:
    checked = validate_r11_evidence(certified_r11_fixture())
    assert checked["canonical_left_zero_only_symmetry"] is True


@pytest.mark.parametrize("field,value", (
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_production_inference_rules", 1),
    ("public_provider_changed", True),
    ("completion_claimed", True),
))
def test_invalid_r11_certification_never_opens_r12(field: str, value: object) -> None:
    report = certified_r11_fixture()
    report[field] = value
    with pytest.raises(RuntimeError):
        validate_r11_evidence(report)


@pytest.mark.parametrize("field,value", (
    ("canonical_full_composite_candidate_count", 0),
    ("diagnostic_symbols_are_not_verified_aliases", False),
    ("canonical_left_rule_names", ["cited Toda (5.9)"]),
    ("transcription_not_promoted_to_proof", False),
    ("new_verified_steps", 1),
    ("public_provider_unchanged", False),
))
def test_r11_partial_proof_cannot_be_promoted(field: str, value: object) -> None:
    report = certified_r11_fixture()
    report["live"][field] = value
    with pytest.raises(RuntimeError):
        validate_r11_evidence(report)


@pytest.mark.parametrize("field", (
    "public_canonical_full_image", "public_canonical_nu_image",
    "public_canonical_eta_square_image", "public_canonical_left_zero",
))
def test_r11_root_counts_cannot_change_silently(field: str) -> None:
    report = certified_r11_fixture()
    report["live"][field]["proposal_count"] = 0
    with pytest.raises(RuntimeError):
        validate_r11_evidence(report)


def test_source_guard_accepts_normal_crlf_but_not_truncated_sha() -> None:
    text = b"one\ntwo\n"
    sha = git_blob_sha(text)
    assert source_blob_matches(text, sha)
    assert source_blob_matches(b"one\r\ntwo\r\n", sha)
    assert not source_blob_matches(text, sha[:-1])
    assert not source_blob_matches(text, "f" * 40)
    assert all(len(value) == 40 for value in SOURCE_BLOBS.values())
    assert len(SOURCE_BLOBS) == 14


def test_only_reviewed_base_or_r11_successor_is_allowed() -> None:
    assert reviewed_head_lineage(BASE_HEAD, BASE_HEAD, (), ()) == "REVIEWED_BASE"
    assert reviewed_head_lineage(
        REVIEWED_R11_HEAD, REVIEWED_R11_HEAD,
        (REVIEWED_R11_HEAD,), (ALLOWED_SUCCESSOR + "audit.py",),
    ) == "REVIEWED_R11_ONLY_SUCCESSOR"
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(BASE_HEAD, "f" * 40, (), ())
    with pytest.raises(RuntimeError):
        reviewed_head_lineage("f" * 40, "f" * 40, ("f" * 40,),
                              (ALLOWED_SUCCESSOR + "audit.py",))
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(REVIEWED_R11_HEAD, REVIEWED_R11_HEAD,
                              (REVIEWED_R11_HEAD,), ("proof.py",))
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(REVIEWED_R11_HEAD, REVIEWED_R11_HEAD,
                              (REVIEWED_R11_HEAD,), ())


def test_audit_cannot_install_provider_or_mutate_existing_code() -> None:
    file = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(file.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {"verify_git_and_sources", "inspect_source_and_frontier", "make_report"} <= functions
    assert not {"install", "patch", "register_given", "mutate_production"} & functions


def test_inference_requires_source_step_not_relation_leaf() -> None:
    file = Path(__file__).resolve().parents[1] / "rule.py"
    code = file.read_text(encoding="utf-8")
    assert "proof_rule=ProofRule.GIVEN" in code
    assert "source_options" in code
    assert "subgoals=(source,)" in code
    assert "ProofStep(" not in code
