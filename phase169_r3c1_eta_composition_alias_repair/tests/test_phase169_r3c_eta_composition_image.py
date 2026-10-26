"""R3C: derive a composition image only from verified eta suspensions."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r21_eta_generator_chain import (
    _composition_eta_suspensions,
    composition_eta_suspension_image_rule,
    expand_cited_eta_generator,
)
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule
from toda_rules import toda_eta_family_definition_statement


def _image(n=2):
    eta_n = toda_eta_family_definition_statement(n).element
    eta_n1 = toda_eta_family_definition_statement(n + 1).element
    eta_n2 = toda_eta_family_definition_statement(n + 2).element
    suspension = TodaSuspensionMap(
        TodaPrimaryGroup(n + 2, n), TodaPrimaryGroup(n + 3, n + 1)
    )
    return GeneratorImage(
        suspension,
        Composition(eta_n, eta_n1),
        Composition(eta_n1, eta_n2),
    )


def test_pi53_composition_creates_two_proof_subgoals():
    goal = _image(2)
    proposals = expand_cited_eta_generator(goal)
    assert len(proposals) == 1
    assert proposals[0].rule.name == "suspension preserves composition of proved eta generators"
    first, second = proposals[0].subgoals
    assert first.source_generator == goal.source_generator.left
    assert first.target_generator == goal.target_generator.left
    assert second.source_generator == goal.source_generator.right
    assert second.target_generator == goal.target_generator.right
    assert len(expand_cited_eta_generator(first)) == 1
    assert len(expand_cited_eta_generator(second)) == 1


def test_consecutive_composition_is_not_special_cased_to_pi53():
    for n in (2, 3, 4):
        goal = _image(n)
        witness = _composition_eta_suspensions(goal)
        assert witness is not None
        assert len(expand_cited_eta_generator(goal)) == 1


def test_verified_component_suspensions_derive_exact_composite_image():
    goal = _image()
    expansion, = expand_cited_eta_generator(goal)
    two_proved = tuple(
        ProofStep(item, (), ProofRule.INFERENCE)
        for item in expansion.subgoals
    )
    matches = find_inference_matches_for_rule(expansion.rule, two_proved)
    assert len(matches) == 1
    derived = apply_inference_match(matches[0])
    assert derived.conclusion == goal
    assert derived.rule is ProofRule.INFERENCE
    assert derived.premises == two_proved


def test_missing_or_given_component_suspensions_are_rejected():
    goal = _image()
    expansion, = expand_cited_eta_generator(goal)
    derived = tuple(ProofStep(item, (), ProofRule.INFERENCE) for item in expansion.subgoals)
    assert not find_inference_matches_for_rule(expansion.rule, ())
    assert not find_inference_matches_for_rule(expansion.rule, derived[:1])
    given = tuple(ProofStep(item, (), ProofRule.GIVEN) for item in expansion.subgoals)
    assert not find_inference_matches_for_rule(expansion.rule, given)


def test_wrong_component_image_cannot_prove_requested_goal():
    goal = _image()
    expansion, = expand_cited_eta_generator(goal)
    witnesses = expansion.subgoals
    mismatched = replace(witnesses[1], target_generator=witnesses[0].target_generator)
    steps = (ProofStep(witnesses[0], (), ProofRule.INFERENCE),
             ProofStep(mismatched, (), ProofRule.INFERENCE))
    assert not find_inference_matches_for_rule(expansion.rule, steps)


def test_noncomposable_or_wrong_suspension_map_does_not_expand():
    goal = _image()
    swapped = replace(goal, target_generator=Composition(
        goal.target_generator.right, goal.target_generator.left,
    ))
    assert expand_cited_eta_generator(swapped) == ()
    unrelated = replace(goal, map=TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3),
    ))
    assert expand_cited_eta_generator(unrelated) == ()
    assert expand_cited_eta_generator("generator image") == ()


def test_existing_single_eta_image_route_still_works():
    n = 3
    eta2 = toda_eta_family_definition_statement(n - 1).element
    eta3 = toda_eta_family_definition_statement(n).element
    mapping = TodaSuspensionMap(TodaPrimaryGroup(n, n - 1), TodaPrimaryGroup(n + 1, n))
    goal = GeneratorImage(mapping, eta2, eta3)
    options = expand_cited_eta_generator(goal)
    assert len(options) == 1
    assert options[0].rule.name == "proved suspension of generator supplies generator image"
    with pytest.raises(ValueError):
        composition_eta_suspension_image_rule(goal)
