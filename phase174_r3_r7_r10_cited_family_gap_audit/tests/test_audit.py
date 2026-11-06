"""R10 source-first lineage, evidence and no-proof-promotion contracts."""
from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r10_cited_family_gap_audit.audit import (
    REVIEWED_HEAD,
    SOURCE_BLOBS,
    TODA_59,
    git_blob_sha,
    reviewed_head_pair,
    source_blob_matches,
    summarize_expression,
    validate_r9_report,
    verify_toda_transcription,
)


def sample_r9() -> dict:
    return {
        "phase": "174-R3-R7-R9",
        "gate": "PASS_ISOLATED_ASSOCIATIVITY_CHILDREN_PENDING",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "production_files_changed": False,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "isolated_rebracket_candidate_count": 1,
            "old_composite_candidate_count": 0,
            "right_associated_composite_candidate_count": 1,
            "public_right_associated_image_frontier": {"proposal_count": 1},
            "public_left_associated_image_frontier": {"proposal_count": 0},
            "left_factor_root_rule": "equality symmetry",
            "left_factor_symmetry_is_not_proof": True,
            "public_provider_unchanged": True,
            "new_verified_steps": 0,
        },
    }


def test_previous_r9_report_is_only_evidence_not_proof() -> None:
    data = validate_r9_report(sample_r9())
    assert data["left_image_public_options"] == 0
    assert data["right_image_public_options"] == 1
    assert data["left_zero_is_symmetry_only"] is True


@pytest.mark.parametrize("field,bad", (
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_production_inference_rules", 1),
    ("production_files_changed", True),
    ("public_provider_changed", True),
    ("completion_claimed", True),
))
def test_r9_rejects_modified_gate_or_trust_contract(field: str, bad: object) -> None:
    report = sample_r9()
    report[field] = bad
    with pytest.raises(RuntimeError):
        validate_r9_report(report)


@pytest.mark.parametrize("key,bad", (
    ("isolated_rebracket_candidate_count", 0),
    ("old_composite_candidate_count", 1),
    ("right_associated_composite_candidate_count", 0),
    ("left_factor_root_rule", "Toda source GIVEN"),
    ("left_factor_symmetry_is_not_proof", False),
    ("new_verified_steps", 1),
))
def test_r9_rejects_fabricated_completions(key: str, bad: object) -> None:
    report = sample_r9()
    report["live"][key] = bad
    with pytest.raises(RuntimeError):
        validate_r9_report(report)


def test_r9_rejects_wrong_public_goal_counts() -> None:
    report = sample_r9()
    report["live"]["public_left_associated_image_frontier"]["proposal_count"] = 1
    with pytest.raises(RuntimeError, match="public candidate count"):
        validate_r9_report(report)


def test_source_sha_requires_all_40_characters_and_content_match() -> None:
    source = b"line one\nline two\n"
    sha = git_blob_sha(source)
    assert source_blob_matches(source, sha)
    assert source_blob_matches(b"line one\r\nline two\r\n", sha)
    assert not source_blob_matches(source, sha[:-1])
    assert not source_blob_matches(source + b"changed", sha)
    assert all(len(value) == 40 for value in SOURCE_BLOBS.values())
    assert len(SOURCE_BLOBS) == 14


def test_head_must_equal_one_reviewed_develop_commit() -> None:
    assert reviewed_head_pair(REVIEWED_HEAD, REVIEWED_HEAD)
    assert not reviewed_head_pair(REVIEWED_HEAD, "f" * 40)
    assert not reviewed_head_pair("f" * 40, "f" * 40)


def test_source_claims_are_distinct_not_target_proof() -> None:
    assert "nu_n" in TODA_59["general_annihilator"]
    assert "nu_5" in TODA_59["generator_suspension"]
    assert TODA_59["zero_image_conclusion"] != TODA_59["general_annihilator"]


def test_toda_excerpt_requires_three_ordered_lines(tmp_path: Path) -> None:
    source = tmp_path / "sources" / "toda"
    source.mkdir(parents=True)
    (source / "Toda_05_2.tex").write_text(
        "prefix\\begin{proposition}\\label{prop:5.9}\n"
        + TODA_59["general_annihilator"] + "\n"
        + TODA_59["generator_suspension"] + "\n"
        + TODA_59["zero_image_conclusion"] + "\n\\qed\n",
        encoding="utf-8",
    )
    result = verify_toda_transcription(tmp_path)
    assert result["transcription_is_not_a_proof_step"] is True
    (source / "Toda_05_2.tex").write_text(
        "\\begin{proposition}\\label{prop:5.9}\n"
        + TODA_59["zero_image_conclusion"] + "\n"
        + TODA_59["general_annihilator"] + "\n"
        + TODA_59["generator_suspension"] + "\n\\qed\n",
        encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="transcription changed"):
        verify_toda_transcription(tmp_path)


def test_expression_descriptor_checks_full_generator_metadata() -> None:
    element = SimpleNamespace(
        name="ν₆", dimension=6, source=9, target=6,
        generator=SimpleNamespace(family="ν", index=6),
    )
    descriptor = summarize_expression(element)
    assert descriptor["name"] == "ν₆"
    assert descriptor["symbol_family"] == "ν"
    assert descriptor["symbol_index"] == 6


def test_source_only_audit_has_no_public_registration() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {"verify_git_and_sources", "validate_r9_report", "inspect_live_frontier"} <= functions
    assert not {"install", "patch", "register_given", "mutate_production"} & functions
