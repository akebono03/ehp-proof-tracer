import pytest

from homotopy_groups import TodaPrimaryGroup, FreeCyclicGroup
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import GeneratorImage, MapIsomorphism
from phase165_r14_r7_map_discovery import (
    discover_hopf_map_candidates, expand_discovered_group_goal,
    inverse_free_cyclic_transport_rule,
)


def _goal(i=3, n=2):
    return Relation(lhs=TodaPrimaryGroup(i, n), rhs=FreeCyclicGroup('eta'))


def test_generic_hopf_map_candidate_from_dimensions():
    found = discover_hopf_map_candidates(_goal())
    assert len(found) == 1
    h = found[0].map
    assert h.source_group == TodaPrimaryGroup(3, 2)
    assert h.target_group == TodaPrimaryGroup(3, 3)
    assert found[0].status == 'STRUCTURAL_CANDIDATE_NOT_VERIFIED'


def test_generic_discovery_works_for_other_dimensions():
    candidate = discover_hopf_map_candidates(_goal(i=7, n=4))[0].map
    assert candidate.target_group == TodaPrimaryGroup(7, 7)


def test_no_invented_premises_from_map_candidate():
    assert expand_discovered_group_goal(_goal()) == ()


def test_external_catalog_creates_only_expansion():
    goal = _goal()
    h = discover_hopf_map_candidates(goal)[0].map
    image = GeneratorImage(h, 'eta', 'iota')
    target = Relation(lhs=h.target_group, rhs=FreeCyclicGroup('iota'))
    expanded = expand_discovered_group_goal(
        goal, generator_images=(image,), target_group_claims=(target,),
    )
    assert len(expanded) == 1
    assert expanded[0].subgoals == (MapIsomorphism(h), target, image)


def test_inverse_transport_uses_verified_steps_only_when_provided():
    goal = _goal()
    h = discover_hopf_map_candidates(goal)[0].map
    image = GeneratorImage(h, 'eta', 'iota')
    target = Relation(lhs=h.target_group, rhs=FreeCyclicGroup('iota'))
    steps = tuple(ProofStep(x, (), ProofRule.GIVEN) for x in (
        MapIsomorphism(h), target, image,
    ))
    matches = find_inference_matches_for_rule(inverse_free_cyclic_transport_rule(), steps)
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.conclusion == goal


def test_wrong_generator_cannot_transfer():
    goal = _goal()
    h = discover_hopf_map_candidates(goal)[0].map
    image = GeneratorImage(h, 'eta', 'wrong')
    target = Relation(lhs=h.target_group, rhs=FreeCyclicGroup('iota'))
    assert expand_discovered_group_goal(
        goal, generator_images=(image,), target_group_claims=(target,),
    ) == ()


def test_invalid_range_does_not_discover_map():
    assert discover_hopf_map_candidates(_goal(i=2, n=3)) == ()
    assert discover_hopf_map_candidates(_goal(i=1, n=1)) == ()


def test_catalog_types_are_checked():
    with pytest.raises(TypeError):
        expand_discovered_group_goal(_goal(), generator_images=[])
