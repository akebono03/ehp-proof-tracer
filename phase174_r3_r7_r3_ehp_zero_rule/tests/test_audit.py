"""Pure guard and evidence checks for the isolated R3-R7-R3 audit."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r3_ehp_zero_rule.audit import (
    BASE_HEAD, EXPECTED_COUNTS, SOURCE_BLOBS,
    accepted_source_blob, blob_sha, verify_r2_evidence,
)


def _report() -> dict:
    return {
        "phase": "174-R3-R7-R2",
        "gate": "PASS_READ_ONLY_TYPED_EHP_CHAIN",
        "previous_audit": {"zero_root_proposal_count": 0},
        "live_obligations": {
            "obligations": {
                k: {"proposal_count": v} for k, v in EXPECTED_COUNTS.items()
            },
            "pi11_6": {
                "search_status": "search_failed",
                "open_goal_types": ["Relation", "Relation"],
                "candidate_frontier": [],
            },
        },
        "new_group_given": 0,
        "new_inference_rules": 0,
    }


def test_evidence_accepts_only_observed_source_screened_counts() -> None:
    data = verify_r2_evidence(_report())
    assert data["proposal_counts"] == EXPECTED_COUNTS
    assert data["delta_isomorphism_candidate_is_not_surjectivity_evidence"]


@pytest.mark.parametrize("changed_name,changed_count", (
    ("delta_surjectivity", 1), ("target_zero", 1),
    ("delta_e_exactness", 0), ("e_h_exactness", 0),
))
def test_evidence_fails_closed_when_candidates_change(
    changed_name: str, changed_count: int,
) -> None:
    report = _report()
    report["live_obligations"]["obligations"][changed_name]["proposal_count"] = changed_count
    with pytest.raises(RuntimeError, match="counts differ"):
        verify_r2_evidence(report)


def test_prior_gate_and_pi11_status_fail_closed() -> None:
    data = _report()
    data["gate"] = "PASS_PREFLIGHT"
    with pytest.raises(RuntimeError, match="not certified"):
        verify_r2_evidence(data)
    data = _report()
    data["live_obligations"]["pi11_6"]["search_status"] = "complete"
    with pytest.raises(RuntimeError, match="blocker differs"):
        verify_r2_evidence(data)


def test_prior_direct_group_claims_are_not_admitted() -> None:
    report = _report()
    report["new_group_given"] = 1
    with pytest.raises(RuntimeError, match="unapproved"):
        verify_r2_evidence(report)


def test_sha_guard_accepts_crlf_without_widening() -> None:
    original = b"line1\nline2\n"
    sha = blob_sha(original)
    assert accepted_source_blob(original, sha)
    assert accepted_source_blob(b"line1\r\nline2\r\n", sha)
    assert not accepted_source_blob(b"line1\nwrong\n", sha)


def test_audit_does_not_mutate_production_code() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    names = {
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    assert "inspect_new_candidate" in names
    assert "verify_git_and_sources" in names
    assert "install" not in names
    assert "modify_production" not in names
    assert len(SOURCE_BLOBS) == 7
    assert len(BASE_HEAD) == 40
