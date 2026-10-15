"""R57-R12: ordered prior proofs only; no fabricated stable isomorphism."""
import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r17_internal_dependency import CompletedInternalProof
from phase165_r57_r12_ordered_proofs import OrderedCompletedProof, validate_prior_internal_proofs
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep, Relation, RelationType


def _earlier_proof():
    eta3 = HomotopyElement(name="η_3", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3))
    conclusion = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta3), RelationType.EQUALITY)
    given = ProofStep(conclusion="registered premise", premises=(), rule=ProofRule.GIVEN)
    rule = InferenceRule(name="test prior inference", premise_patterns=(PremisePattern(statement_type=str),),
        conclusion_builder=lambda premises: conclusion)
    root = ProofStep(conclusion=conclusion, premises=(given,), rule=ProofRule.INFERENCE, inference_rule=rule)
    return OrderedCompletedProof(CompletedInternalProof(root), 1)


def test_prior_proof_requires_strictly_earlier_position():
    prior = _earlier_proof()
    assert validate_prior_internal_proofs((prior,), 2) == (prior.proof,)
    with pytest.raises(ValueError, match="precede"):
        validate_prior_internal_proofs((prior,), 1)
    with pytest.raises(ValueError, match="precede"):
        validate_prior_internal_proofs((prior,), 0)


def test_unknown_order_and_unranked_proofs_fail_closed():
    prior = _earlier_proof()
    with pytest.raises(ValueError, match="target_order"):
        validate_prior_internal_proofs((prior,), None)
    with pytest.raises(ValueError, match="unranked"):
        validate_prior_internal_proofs((), 2, (prior.proof,))


def test_invalid_order_metadata_is_rejected():
    prior = _earlier_proof()
    with pytest.raises(ValueError):
        OrderedCompletedProof(prior.proof, True)
    with pytest.raises(ValueError):
        validate_prior_internal_proofs((prior, prior), 5)


def test_shared_provider_without_registered_toda45_does_not_invent_transport():
    bridge = expand_cited_given_components(build_adopted_prop51_reference())
    earlier = _earlier_proof().proof.root.conclusion
    provider = shared_expansion_provider(bridge, prior_conclusions=(earlier,))
    eta4 = HomotopyElement(name="η_4", dimension=4, source=5, target=4,
        generator=GeneratorSymbol(family="η", index=4))
    target = Relation(TodaPrimaryGroup(5,4), FiniteCyclicGroup(2, eta4), RelationType.EQUALITY)
    expansions = provider(target)
    assert not any("Toda 4.5" in x.rule.name for x in expansions)


def test_shared_search_rejects_unranked_prior_without_running_exploration():
    from phase165_r52_r9_shared_math import search_shared_group_goal
    prior = _earlier_proof()
    with pytest.raises(ValueError, match="unranked"):
        search_shared_group_goal(n=4, k=1, group_structure=prior.proof.root.conclusion.rhs,
            completed_internal_proofs=(prior.proof,))
