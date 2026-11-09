"""Actual R38 public-source and general-provider integration tests."""
from __future__ import annotations

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.audit import (
    inspect_public_chain,
)
from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
    PROVIDER_ID, expand_source_bound_zero_image_chain,
    left_associated, lifted_stable_composition,
)
from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
from proof import ProofRule, ProofStep


def _screened():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    available = tuple(link.step.conclusion for link in bridge.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    return root, bridge, available


def test_cited_source_is_necessary_for_public_zero_image_candidate() -> None:
    prior = exact_prior_database_result(5, 5)
    mapping = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6))
    goal = ImageZeroStatement(mapping)
    assert expand_source_bound_zero_image_chain(goal, ()) == ()
    assert expand_source_bound_zero_image_chain(goal, (prior,)) == ()
    root, bridge, available = _screened()
    assert sum(type(x) is CitedFamilyAnnihilator for x in available) == 1
    options = shared_expansion_provider(bridge, proof_target=root)(goal)
    assert any(item.rule.name ==
               'finite cyclic generator mapped to zero implies zero homomorphism image'
               and item.subgoals[0] == prior for item in options)


def test_full_source_bound_composition_chain_offers_only_subgoals() -> None:
    _, _, available = _screened()
    prior = exact_prior_database_result(5, 5)
    mapping = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6))
    g = prior.rhs.generator
    lifted = lifted_stable_composition(g)
    assert lifted is not None
    left = left_associated(lifted)
    assert left is not None
    goal = GeneratorImage(mapping, g, Zero())
    candidates = expand_source_bound_zero_image_chain(goal, available)
    assert len(candidates) == 1
    assert candidates[0].subgoals[0] == GeneratorImage(mapping, g, left)
    reassociation = expand_source_bound_zero_image_chain(
        GeneratorImage(mapping, g, left), available,
    )
    assert len(reassociation) == 1
    assert reassociation[0].subgoals == (GeneratorImage(mapping, g, lifted),)
    assert not any(isinstance(subgoal, ProofStep) for candidate in candidates
                   for subgoal in candidate.subgoals)


def test_public_audit_does_not_claim_completion_or_sources() -> None:
    result = inspect_public_chain()
    assert result['zero_image_public_proposals'] == 1
    assert result['generator_zero_public_proposals'] == 1
    assert result['associativity_public_proposals'] == 1
    assert result['composition_factorization_public_proposals'] == 1
    assert result['public_provider_id'] == PROVIDER_ID
    assert result['new_givens'] == 0
    assert result['zero_image_proved_by_this_audit'] is False
    assert result['root_complete'] is False
