"""Source-first audit and reviewed-HEAD lineage contracts."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r6_cyclic_generator_zero_image.audit import (
    ALLOWED_SUCCESSOR_PREFIX, REVIEWED_HEAD, REVIEWED_R5_SUCCESSOR_HEAD,
    SOURCE_BLOBS, TODA_CLAUSES,
    accepted_source_blob, blob_sha, validate_r5_evidence,
    validate_reviewed_head_lineage,
)


def sample_r5() -> dict:
    return {
        "phase": "174-R3-R7-R5",
        "gate": "PASS_ISOLATED_HOPF_INJECTIVITY_ZERO_IMAGE_PENDING",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "completion_claimed": False,
        "live": {
            "isolated_hopf_injectivity_candidate_count": 1,
            "production_zero_image_frontier": {"proposal_count": 0},
            "production_eh_exactness_frontier": {"proposal_count": 1},
            "no_public_provider_wiring": True,
        },
    }


def test_r5_live_evidence_is_read_without_promotion_to_proof() -> None:
    data = validate_r5_evidence(sample_r5())
    assert data["production_image_zero_proposals"] == 0
    assert data["prior_complete_proof_claimed"] is False


@pytest.mark.parametrize("change", ("gate", "image_zero", "source_ancestry", "given"))
def test_r5_gate_and_evidence_fail_closed(change: str) -> None:
    report = sample_r5()
    if change == "gate":
        report["gate"] = "PASS_PREFLIGHT"
    elif change == "image_zero":
        report["live"]["production_zero_image_frontier"]["proposal_count"] = 1
    elif change == "source_ancestry":
        report["live"]["no_public_provider_wiring"] = False
    else:
        report["new_group_given"] = 1
    with pytest.raises(RuntimeError):
        validate_r5_evidence(report)


def test_reviewed_base_head_is_accepted_only_when_equal() -> None:
    assert validate_reviewed_head_lineage(
        REVIEWED_HEAD, REVIEWED_HEAD, (), (),
    ) == "REVIEWED_BASE"
    with pytest.raises(RuntimeError):
        validate_reviewed_head_lineage(REVIEWED_HEAD, "f" * 40, (), ())


def test_one_r5_only_successor_is_accepted_but_unrelated_files_rejected() -> None:
    next_head = REVIEWED_R5_SUCCESSOR_HEAD
    assert validate_reviewed_head_lineage(
        next_head, next_head, (next_head,),
        (ALLOWED_SUCCESSOR_PREFIX + "audit.py",),
    ) == "REVIEWED_R5_ONLY_SUCCESSOR"
    with pytest.raises(RuntimeError):
        validate_reviewed_head_lineage(
            "a" * 40, "a" * 40, ("a" * 40,),
            (ALLOWED_SUCCESSOR_PREFIX + "audit.py",),
        )
    for changed in (
        ("proof.py",),
        (ALLOWED_SUCCESSOR_PREFIX + "audit.py", "README.md"),
        (),
    ):
        with pytest.raises(RuntimeError):
            validate_reviewed_head_lineage(
                next_head, next_head, (next_head,), changed,
            )
    with pytest.raises(RuntimeError):
        validate_reviewed_head_lineage(
            next_head, next_head, ("b" * 40, next_head),
            (ALLOWED_SUCCESSOR_PREFIX + "audit.py",),
        )


def test_source_blobs_accept_crlf_but_not_modified_content() -> None:
    value = b"ab\ncd\n"
    expected = blob_sha(value)
    assert accepted_source_blob(value, expected)
    assert accepted_source_blob(b"ab\r\ncd\r\n", expected)
    assert not accepted_source_blob(b"ab\nmodified\n", expected)


def test_toda_transcription_does_not_justify_direct_group_given() -> None:
    assert r"\mathbb Z_2" in TODA_CLAUSES["nonzero_group_presentation"]
    assert TODA_CLAUSES["zero_image_conclusion"] == r"E\pi_{10}^5=0"
    assert r"\nu_6" in TODA_CLAUSES["suspended_generator_zero"]
    assert len(SOURCE_BLOBS) >= 12


def test_audit_contains_no_installer_or_public_mutation_function() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    funcs = {
        node.name
        for node in ast.parse(source.read_text(encoding="utf-8")).body
        if isinstance(node, ast.FunctionDef)
    }
    assert "verify_git_and_sources" in funcs
    assert "inspect_screened_cyclic_generator_frontier" in funcs
    assert "make_report" in funcs
    assert not {"install", "patch", "write_production", "register_given"} & funcs
