import pytest
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaHopfInvariantMap
from proof import ProofStep, ProofRule, Relation, RelationType
from phase165_r14_r6_generic_iso import (
    MapInjective, MapSurjective, MapIsomorphism, GeneratorImage,
    map_isomorphism_rule, free_cyclic_transport_rule, expand_generic_iso_goal,
)
from proof import find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step


def _step(value):
    return ProofStep(value, (), ProofRule.GIVEN)


def test_generic_mono_epi_is_iso():
    a = TodaPrimaryGroup(3, 2)
    b = TodaPrimaryGroup(3, 3)
    h = TodaHopfInvariantMap(a, b)
    matches = find_inference_matches_for_rule(
        map_isomorphism_rule(), (_step(MapInjective(h)), _step(MapSurjective(h)))
    )
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.conclusion == MapIsomorphism(h)
    assert derived.rule is ProofRule.INFERENCE


def test_different_maps_do_not_form_isomorphism():
    a = TodaPrimaryGroup(3, 2)
    b = TodaPrimaryGroup(3, 3)
    c = TodaPrimaryGroup(5, 3)
    h = TodaHopfInvariantMap(a, b)
    other = TodaHopfInvariantMap(c, b)
    assert not find_inference_matches_for_rule(
        map_isomorphism_rule(), (_step(MapInjective(h)), _step(MapSurjective(other)))
    )


def test_generic_cyclic_transport():
    a = TodaPrimaryGroup(3, 2)
    b = TodaPrimaryGroup(3, 3)
    h = TodaHopfInvariantMap(a, b)
    premises = (
        _step(MapIsomorphism(h)),
        _step(Relation(lhs=a, rhs=FreeCyclicGroup("g"), relation_type=RelationType.EQUALITY)),
        _step(GeneratorImage(h, "g", "h")),
    )
    matches = find_inference_matches_for_rule(free_cyclic_transport_rule(), premises)
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.conclusion == Relation(lhs=b, rhs=FreeCyclicGroup("h"))


def test_mismatched_generator_is_rejected():
    a = TodaPrimaryGroup(3, 2)
    b = TodaPrimaryGroup(3, 3)
    h = TodaHopfInvariantMap(a, b)
    premises = (
        _step(MapIsomorphism(h)),
        _step(Relation(lhs=a, rhs=FreeCyclicGroup("g"))),
        _step(GeneratorImage(h, "wrong", "h")),
    )
    assert not find_inference_matches_for_rule(free_cyclic_transport_rule(), premises)


def test_iso_backward_goals_are_generic():
    a = TodaPrimaryGroup(3, 2)
    b = TodaPrimaryGroup(3, 3)
    h = TodaHopfInvariantMap(a, b)
    options = expand_generic_iso_goal(MapIsomorphism(h))
    assert len(options) == 1
    assert options[0].subgoals == (MapInjective(h), MapSurjective(h))


def test_group_goal_is_not_fabricated_from_missing_isomorphism():
    group = TodaPrimaryGroup(3, 2)
    assert expand_generic_iso_goal(Relation(lhs=group, rhs=FreeCyclicGroup("g"))) == ()


def test_conclusion_builders_follow_existing_single_argument_contract():
    import inspect
    from phase165_r14_r6_generic_iso import (
        map_isomorphism_rule, free_cyclic_transport_rule,
    )
    for rule in (map_isomorphism_rule(), free_cyclic_transport_rule()):
        assert len(inspect.signature(rule.conclusion_builder).parameters) == 1
