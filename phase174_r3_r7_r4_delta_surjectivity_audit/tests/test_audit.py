"""Focused contracts for the read-only Delta-surjectivity frontier audit."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r4_delta_surjectivity_audit.audit import (
    BASE_HEAD,
    REVIEWED_HEAD,
    SOURCE_BLOBS,
    SOURCE_CLAUSES,
    accepted_source_blob,
    audited_head_pair,
    blob_sha,
    validate_prior_evidence,
)


def sample_reports() -> tuple[dict, dict]:
    r2 = {
        "phase": "174-R3-R7-R2",
        "gate": "PASS_READ_ONLY_TYPED_EHP_CHAIN",
        "live_obligations": {
            "obligations": {
                "delta_surjectivity": {"proposal_count": 0},
                "delta_e_exactness": {"proposal_count": 1},
                "e_h_exactness": {"proposal_count": 1},
            },
            "pi11_6": {
                "search_status": "search_failed",
                "open_goal_types": ["Relation", "Relation"],
                "candidate_frontier": [],
            },
        },
    }
    r3 = {
        "phase": "174-R3-R7-R3",
        "gate": "PASS_ISOLATED_RULE_DELTA_SURJECTIVITY_PENDING",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "new_candidate": {
            "isolated_generic_root_proposals": 1,
            "not_registered_with_production_provider": True,
            "separate_premises": {"delta_surjectivity": {"proposal_count": 0}},
        },
    }
    return r2, r3


def test_git_blob_accepts_crlf_and_rejects_changes() -> None:
    source = b"first\nsecond\n"
    assert accepted_source_blob(source, blob_sha(source))
    assert accepted_source_blob(b"first\r\nsecond\r\n", blob_sha(source))
    assert not accepted_source_blob(source + b"different", blob_sha(source))


def test_valid_git_lineage_same_head() -> None:
    result = audited_head_pair(REVIEWED_HEAD, REVIEWED_HEAD)
    assert result["local_equals_remote"]
    assert not result["reconciliation_before_implementation_required"]


def test_readonly_lineage_prior_head_requires_later_sync() -> None:
    result = audited_head_pair(BASE_HEAD, REVIEWED_HEAD)
    assert not result["local_equals_remote"]
    assert result["reconciliation_before_implementation_required"]


def test_unreviewed_git_head_fails_closed() -> None:
    with pytest.raises(RuntimeError, match="unreviewed"):
        audited_head_pair("a" * 40, REVIEWED_HEAD)
    with pytest.raises(RuntimeError, match="moved behind"):
        audited_head_pair(REVIEWED_HEAD, BASE_HEAD)


def test_nonzero_group_and_zero_suspension_are_distinct() -> None:
    assert r"\pi^{5}_{10}=\mathbb Z_2" in SOURCE_CLAUSES["nonzero_preceding_group"]
    assert SOURCE_CLAUSES["zero_suspension_of_preceding_group"] == r"E\pi_{10}^5=0"


def test_pinned_sources_and_claims_do_not_define_proof() -> None:
    assert len(SOURCE_BLOBS) == 8
    assert "target_zero_is_conclusion" in SOURCE_CLAUSES
    assert "preceding_free_group_is_conclusion" in SOURCE_CLAUSES


def test_previous_evidence_remains_unresolved() -> None:
    r2, r3 = sample_reports()
    result = validate_prior_evidence(r2, r3)
    assert result["delta_surjectivity_candidate_count"] == 0
    assert result["isolated_zero_root_is_not_proof"]


def test_previous_evidence_rejects_forged_delta_candidate() -> None:
    r2, r3 = sample_reports()
    r2["live_obligations"]["obligations"]["delta_surjectivity"]["proposal_count"] = 1
    with pytest.raises(RuntimeError, match="candidate counts"):
        validate_prior_evidence(r2, r3)


def test_previous_evidence_rejects_missing_isolated_rule() -> None:
    r2, r3 = sample_reports()
    r3["new_candidate"]["isolated_generic_root_proposals"] = 0
    with pytest.raises(RuntimeError, match="isolated EHP"):
        validate_prior_evidence(r2, r3)


def test_previous_evidence_rejects_unapproved_given_or_rule() -> None:
    r2, r3 = sample_reports()
    r3["new_group_given"] = 1
    with pytest.raises(RuntimeError, match="Unapproved"):
        validate_prior_evidence(r2, r3)
    r3["new_group_given"] = 0
    r3["new_production_inference_rules"] = 1
    with pytest.raises(RuntimeError, match="Unapproved"):
        validate_prior_evidence(r2, r3)


def test_new_audit_contains_no_write_or_install_function() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "inspect_live_delta_frontier" in names
    assert "verify_toda_proof_chain" in names
    assert "install" not in names
    assert "patch" not in names
    assert "apply" not in names
