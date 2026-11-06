"""R7 read-only source, lineage and prior-R6 evidence contracts."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r7_composite_zero_audit.audit import (
    ALLOWED_SUCCESSOR_PREFIX,
    BASE_HEAD,
    REVIEWED_R6_HEAD,
    SOURCE_BLOBS,
    TODA_CLAUSES,
    accepted_source_blob,
    blob_sha,
    reviewed_head_lineage,
    validate_r6_evidence,
)


def sample_r6() -> dict:
    return {
        "phase": "174-R3-R7-R6",
        "gate": "PASS_ISOLATED_CYCLIC_ZERO_IMAGE_CHILDREN_UNPROVEN",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "isolated_zero_image_candidate_count": 1,
            "registered_presentation_is_not_proof": True,
            "public_provider_unchanged": True,
            "production_image_zero_frontier": {"proposal_count": 0},
            "production_presentation_frontier": {"proposal_count": 3},
            "production_generator_zero_frontier": {"proposal_count": 0},
        },
    }


def test_r6_certified_counts_are_not_promoted_to_proof() -> None:
    result = validate_r6_evidence(sample_r6())
    assert result["production_generator_zero_proposals"] == 0
    assert result["completion_claimed"] is False


@pytest.mark.parametrize("field", ("gate", "direct_given", "candidate", "presentation", "generator", "wiring"))
def test_r6_mismatch_fails_closed(field: str) -> None:
    report = sample_r6()
    if field == "gate":
        report["gate"] = "PASS_PREFLIGHT"
    elif field == "direct_given":
        report["new_group_given"] = 1
    elif field == "candidate":
        report["live"]["isolated_zero_image_candidate_count"] = 0
    elif field == "presentation":
        report["live"]["production_presentation_frontier"]["proposal_count"] = 4
    elif field == "generator":
        report["live"]["production_generator_zero_frontier"]["proposal_count"] = 1
    else:
        report["public_provider_changed"] = True
    with pytest.raises(RuntimeError):
        validate_r6_evidence(report)


def test_reviewed_base_and_successor_lineage_are_strict() -> None:
    assert reviewed_head_lineage(BASE_HEAD, BASE_HEAD, (), ()) == "REVIEWED_BASE"
    assert reviewed_head_lineage(
        REVIEWED_R6_HEAD, REVIEWED_R6_HEAD,
        (REVIEWED_R6_HEAD,),
        (ALLOWED_SUCCESSOR_PREFIX + "audit.py",),
    ) == "REVIEWED_R6_ONLY_SUCCESSOR"


@pytest.mark.parametrize("local,remote,successors,paths", (
    ("x" * 40, "x" * 40, (), ()),
    (BASE_HEAD, REVIEWED_R6_HEAD, (), ()),
    (REVIEWED_R6_HEAD, REVIEWED_R6_HEAD, (), ()),
    (REVIEWED_R6_HEAD, REVIEWED_R6_HEAD, (REVIEWED_R6_HEAD,), ("proof.py",)),
    (REVIEWED_R6_HEAD, REVIEWED_R6_HEAD, ("x" * 40,), (ALLOWED_SUCCESSOR_PREFIX + "a",)),
))
def test_unreviewed_or_mismatched_git_lineage_is_rejected(
    local: str, remote: str, successors: tuple[str, ...], paths: tuple[str, ...],
) -> None:
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(local, remote, successors, paths)


def test_transcription_general_annihilator_is_distinct_from_target_conclusion() -> None:
    assert r"\nu_n" in TODA_CLAUSES["annihilator_family"]
    assert r"n\ge6" in TODA_CLAUSES["annihilator_family"]
    assert r"\nu_6\circ\eta_9" in TODA_CLAUSES["suspension_equals_composite_zero"]
    assert TODA_CLAUSES["zero_image_is_later_conclusion"] == r"E\pi_{10}^5=0"
    assert len(SOURCE_BLOBS) >= 10
    assert len(REVIEWED_R6_HEAD) == 40


def test_source_blob_accepts_newline_normalization_only() -> None:
    value = b"alpha\nbeta\n"
    expected = blob_sha(value)
    assert accepted_source_blob(value, expected)
    assert accepted_source_blob(value.replace(b"\n", b"\r\n"), expected)
    assert not accepted_source_blob(b"alpha\ngamma\n", expected)


def test_isolated_audit_never_writes_production() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    funcs = {
        node.name for node in ast.parse(source.read_text(encoding="utf-8")).body
        if isinstance(node, ast.FunctionDef)
    }
    assert {"make_report", "verify_git_and_sources", "inspect_composite_frontier"} <= funcs
    assert not {"install", "apply_patch", "register_given", "change_public_provider"} & funcs
