"""Focused verification of the live accepted proof, without old checkout pins."""
from __future__ import annotations

from phase175_r4r14r10_complete_proof_audit.audit import audit_live_proof, walk_proof
from proof import ProofRule, ProofStep


def test_live_literature_zero_image_is_part_of_completed_proof() -> None:
    report = audit_live_proof()
    assert report["search_status"] == "complete"
    assert report["open_goals"] == []
    assert report["literature_reference"] == "Proposition 5.8"
    assert report["literature_fixed_origin"] is True
    assert report["literature_step_is_verified_db"] is False
    assert "(5.9)" in report["given_leaf_locators"]
    assert report["new_given"] == 0


def test_walk_proof_collects_parent_first_without_duplication() -> None:
    parent = ProofStep(conclusion="source", premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(conclusion="inferred", premises=(parent, parent), rule=ProofRule.INFERENCE)
    assert walk_proof(root) == (parent, root)
