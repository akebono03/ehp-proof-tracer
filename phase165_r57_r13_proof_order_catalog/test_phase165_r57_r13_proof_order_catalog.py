"""R57-R13: lookup earlier completed proofs from reviewed catalog records."""
import pytest

from phase165_r52_r17_internal_dependency import CompletedInternalProof
from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog, ProofOrderRecord
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep


def _complete(statement):
    source = ProofStep(conclusion="sourced premise: " + statement, premises=(), rule=ProofRule.GIVEN)
    rule = InferenceRule(
        name="test generic deduction",
        premise_patterns=(PremisePattern(statement_type=str),),
        conclusion_builder=lambda steps: statement,
    )
    return CompletedInternalProof(ProofStep(
        conclusion=statement, premises=(source,), rule=ProofRule.INFERENCE,
        inference_rule=rule,
    ))


def test_catalog_selects_earlier_completed_proofs_without_query_order():
    catalog = ProofOrderCatalog()
    earlier = _complete("earlier result")
    later = _complete("later result")
    catalog.register(ProofOrderRecord("earlier result", 4, earlier))
    catalog.register(ProofOrderRecord("target result", 5))
    catalog.register(ProofOrderRecord("later result", 6, later))
    reusable, target_position = catalog.select_prior("target result")
    assert target_position == 5
    assert reusable == (earlier,)


def test_catalog_fails_closed_when_target_order_missing():
    catalog = ProofOrderCatalog()
    catalog.register(ProofOrderRecord("earlier result", 4, _complete("earlier result")))
    with pytest.raises(ValueError, match="registered proof order"):
        catalog.select_prior("unknown target")


def test_catalog_rejects_duplicates_and_unverified_positions():
    catalog = ProofOrderCatalog()
    catalog.register(ProofOrderRecord("A", 0))
    with pytest.raises(ValueError, match="duplicate proof position"):
        catalog.register(ProofOrderRecord("B", 0))
    with pytest.raises(ValueError, match="duplicate target"):
        catalog.register(ProofOrderRecord("A", 1))
    with pytest.raises(ValueError, match="position"):
        ProofOrderRecord("B", True)


def test_catalog_rejects_mismatched_proof_conclusion():
    with pytest.raises(ValueError, match="does not prove"):
        ProofOrderRecord("goal", 2, _complete("other goal"))


def test_shared_search_has_catalog_parameter_after_install():
    from inspect import signature
    from phase165_r52_r9_shared_math import search_shared_group_goal
    assert "proof_order_catalog" in signature(search_shared_group_goal).parameters


def test_shared_search_rejects_unknown_catalog_order_before_search():
    from phase165_r52_r9_shared_math import search_shared_group_goal
    with pytest.raises(ValueError, match="registered proof order"):
        search_shared_group_goal(n=4, k=1, group_structure="unregistered candidate",
                                 proof_order_catalog=ProofOrderCatalog())
