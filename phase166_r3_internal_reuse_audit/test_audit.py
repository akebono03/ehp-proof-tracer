"""Targeted safety checks for existing internal-proof reuse APIs."""
import pytest

from proof import ProofRule, ProofStep
from phase165_r52_r17_internal_dependency import CompletedInternalProof, find_reusable_internal_proof
from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog, ProofOrderRecord
from phase166_r3_internal_reuse_audit.audit import inspect


def make_completed(label, premise="axiom"):
    leaf = ProofStep(conclusion=premise, premises=(), rule=ProofRule.GIVEN)
    return CompletedInternalProof(ProofStep(conclusion=label, premises=(leaf,), rule=ProofRule.INFERENCE))


def test_unregistered_current_goal_cannot_select_catalog_proofs():
    catalog = ProofOrderCatalog()
    catalog.register(ProofOrderRecord("earlier", 1, make_completed("earlier")))
    with pytest.raises(ValueError, match="no unique registered proof order"):
        catalog.select_prior("unregistered")


def test_catalog_selects_only_strictly_earlier_proofs():
    catalog = ProofOrderCatalog()
    catalog.register(ProofOrderRecord("earlier", 1, make_completed("earlier")))
    catalog.register(ProofOrderRecord("goal", 2, make_completed("goal")))
    catalog.register(ProofOrderRecord("later", 3, make_completed("later")))
    completed, position = catalog.select_prior("goal")
    assert position == 2
    assert len(completed) == 1
    assert completed[0].root.conclusion == "earlier"


def test_reuse_rejects_current_goal_and_dependent_premise():
    completed = make_completed("earlier", premise="current")
    assert find_reusable_internal_proof("earlier", "current", (completed,)) is None
    assert find_reusable_internal_proof("earlier", "earlier", (completed,)) is None


def test_non_inference_root_is_not_accepted_as_completed():
    with pytest.raises(ValueError, match="inference root"):
        CompletedInternalProof(ProofStep(conclusion="answer", premises=(), rule=ProofRule.GIVEN))


def test_direct_search_order_gate_is_reported_without_granting_permission():
    report = inspect()
    assert report["search_calls_internal_reuse"]
    assert report["proof_permission_granted"] == 0
    assert not report["production_code_modified"]
