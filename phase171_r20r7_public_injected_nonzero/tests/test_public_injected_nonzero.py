"""Only source-screened prior cyclic facts and proven injectivity may imply nonzero E."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_E_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r7_nonzero_nu_order.audit import build_nonzero_nu_order_proof
from phase171_r2j_r4_r7_nonzero_nu_order.source import (
    NonZeroGroupElement,
    expand_public_injected_generator_nonzero,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _eta(n: int, typed: bool) -> HomotopyElement:
    return HomotopyElement(
        name="η_" + str(n), dimension=n,
        source=n + 1 if typed else None,
        target=n if typed else None,
        generator=GeneratorSymbol(family="η", index=n),
    )


def _triple(typed: bool) -> Composition:
    return Composition(
        _eta(2, typed), Composition(_eta(3, typed), _eta(4, typed)),
    )


def _case():
    source = TodaPrimaryGroup(5, 2)
    target = TodaPrimaryGroup(6, 3)
    earlier = Relation(
        source, FiniteCyclicGroup(2, _triple(False)), RelationType.EQUALITY,
    )
    goal = NonZeroGroupElement(target, MapApplication(EHP_E_MAP, _triple(True)))
    injection = MapInjective(TodaSuspensionMap(source, target))
    return earlier, goal, injection


def test_public_nonzero_image_from_cited_group_and_injective_e() -> None:
    earlier, goal, injection = _case()
    routes = expand_public_injected_generator_nonzero(goal, (earlier,))
    assert len(routes) == 1
    assert routes[0].subgoals == (earlier, injection)
    assert routes[0].rule.name == "injective map preserves nonzero finite-cyclic generator"
    assert not any(isinstance(item, ProofStep) for item in routes[0].subgoals)
    parents = (
        ProofStep(earlier, (), ProofRule.GIVEN),
        ProofStep(injection, (), ProofRule.INFERENCE),
    )
    matching = find_inference_matches_for_rule(routes[0].rule, parents)
    assert len(matching) == 1
    assert derive_inference_proof_step(matching[0]).conclusion == goal


def test_public_nonzero_requires_cited_group_and_valid_goal() -> None:
    earlier, goal, _ = _case()
    assert expand_public_injected_generator_nonzero(goal, ()) == ()
    assert expand_public_injected_generator_nonzero("unrelated", (earlier,)) == ()
    with pytest.raises(TypeError):
        expand_public_injected_generator_nonzero(goal, [earlier])
    wrong_generator = replace(earlier, rhs=FiniteCyclicGroup(2, _eta(3, False)))
    assert expand_public_injected_generator_nonzero(goal, (wrong_generator,)) == ()
    wrong_order = replace(earlier, rhs=FiniteCyclicGroup(1, earlier.rhs.generator))
    assert expand_public_injected_generator_nonzero(goal, (wrong_order,)) == ()
    wrong_target = replace(goal, group=TodaPrimaryGroup(7, 3))
    assert expand_public_injected_generator_nonzero(wrong_target, (earlier,)) == ()
    wrong_e = replace(goal, element="not a suspension image")
    assert expand_public_injected_generator_nonzero(wrong_e, (earlier,)) == ()


def test_public_nonzero_fails_closed_on_competing_prior_presentations() -> None:
    earlier, goal, _ = _case()
    assert len(expand_public_injected_generator_nonzero(goal, (earlier, earlier))) == 1
    rival = replace(earlier, rhs=FiniteCyclicGroup(4, earlier.rhs.generator))
    assert expand_public_injected_generator_nonzero(goal, (earlier, rival)) == ()


def test_shared_provider_matches_real_r4r7_proved_parents() -> None:
    screened, target, _ = _screened_context()
    doubled, order_four, _, prior = build_nonzero_nu_order_proof()
    assert prior["new_given_added"] == 0
    assert order_four.rule is ProofRule.INFERENCE
    real = doubled.premises[1]
    assert real.rule is ProofRule.INFERENCE
    proposals = shared_expansion_provider(screened, proof_target=target)(real.conclusion)
    matches = tuple(
        candidate for candidate in proposals
        if candidate.rule.name == real.inference_rule.name
        and candidate.subgoals == tuple(item.conclusion for item in real.premises)
    )
    assert len(matches) == 1
    admissible = find_inference_matches_for_rule(matches[0].rule, real.premises)
    assert any(
        derive_inference_proof_step(item).conclusion == real.conclusion
        and item.premises == real.premises
        for item in admissible
    )
