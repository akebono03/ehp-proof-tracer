"""Actual typed inference tests; run against the current GitHub checkout."""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

pytest.importorskip("homotopy_groups")

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import MapInjective
from phase175_r3_pi73_hopf_lift.rule import (
    RULE_NAME,
    expand_cited_hopf_lift,
    hopf_lift_inputs,
    hopf_lift_rule,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)


def fixture():
    nu = HomotopyElement("ν'", 3, source=6, target=3, generator=GeneratorSymbol(r"\nu'"))
    eta6 = HomotopyElement("η₆", 6, source=7, target=6, generator=GeneratorSymbol("η", 6))
    eta5 = HomotopyElement("η₅", 5, source=6, target=5, generator=GeneratorSymbol("η", 5))
    x = Composition(nu, eta6)
    g = Composition(eta5, eta6)
    domain = TodaPrimaryGroup(7, 3)
    codomain = TodaPrimaryGroup(7, 5)
    goal = CyclicStructureStatement(domain, x, 2)
    group = Relation(codomain, FiniteCyclicGroup(2, g), RelationType.EQUALITY)
    image = Relation(MapApplication(EHP_H_MAP, x), g, RelationType.EQUALITY)
    return goal, group, image


def inferred(value: object, kind: ProofRule = ProofRule.INFERENCE) -> ProofStep:
    return ProofStep(value, (), kind, inference_rule=InferenceRule("synthetic test fixture only"))


def test_hopf_generator_lift_three_typed_premises() -> None:
    goal, group, image = fixture()
    required = hopf_lift_inputs(goal, group, image)
    assert required == (
        MapInjective(TodaHopfInvariantMap(goal.group, group.lhs)), group, image,
    )
    rule = hopf_lift_rule(goal, group, image)
    assert rule.name == RULE_NAME
    parents = tuple(inferred(value) for value in required)
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.conclusion == goal
    assert step.rule is ProofRule.INFERENCE
    assert step.premises == parents


@pytest.mark.parametrize("index", (0, 1, 2))
def test_no_missing_proof_can_prove_cyclic_lift(index: int) -> None:
    goal, group, image = fixture()
    required = hopf_lift_inputs(goal, group, image)
    parents = tuple(inferred(value) for j, value in enumerate(required) if j != index)
    assert not find_inference_matches_for_rule(hopf_lift_rule(goal, group, image), parents)


@pytest.mark.parametrize("index", (0, 1, 2))
def test_given_instead_of_inference_does_not_prove_lift(index: int) -> None:
    goal, group, image = fixture()
    required = hopf_lift_inputs(goal, group, image)
    parents = tuple(inferred(value, ProofRule.GIVEN if j == index else ProofRule.INFERENCE)
                    for j, value in enumerate(required))
    assert not find_inference_matches_for_rule(hopf_lift_rule(goal, group, image), parents)


def test_wrong_hopf_image_is_rejected() -> None:
    goal, group, image = fixture()
    bad = replace(image, lhs=MapApplication(EHP_H_MAP, group.rhs.generator))
    assert hopf_lift_inputs(goal, group, bad) is None


def test_wrong_group_order_is_rejected() -> None:
    goal, group, image = fixture()
    bad = replace(group, rhs=FiniteCyclicGroup(4, group.rhs.generator))
    assert hopf_lift_inputs(goal, bad, image) is None


def test_below_hopf_dimension_is_rejected() -> None:
    goal, group, image = fixture()
    bad = replace(goal, group=TodaPrimaryGroup(7, 6))
    assert hopf_lift_inputs(bad, group, image) is None


def cited_nu_prime_image():
    """Actual (5.3) nu-prime notation differs from the DB TeX ID spelling."""
    goal, group, image = fixture()
    from_source = HomotopyElement(
        "ν′", 3, source=6, target=3,
        generator=GeneratorSymbol("ν", decoration="′"),
    )
    cited_generator = Composition(from_source, image.lhs.expression.right)
    return goal, group, replace(
        image, lhs=MapApplication(EHP_H_MAP, cited_generator),
    )


def test_cited_unicode_nu_prime_and_db_tex_id_are_same_registered_generator() -> None:
    goal, group, image = cited_nu_prime_image()
    assert image.lhs.expression != goal.generator
    required = hopf_lift_inputs(goal, group, image)
    assert required is not None
    parents = tuple(inferred(value) for value in required)
    matches = find_inference_matches_for_rule(hopf_lift_rule(goal, group, image), parents)
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == goal


def test_registered_alias_candidate_offered_without_creating_proof(monkeypatch) -> None:
    import phase175_r3_pi73_hopf_lift.rule as module
    goal, group, image = cited_nu_prime_image()
    source = Relation("earlier-general-source", "general-cyclic-claim")
    monkeypatch.setattr(
        module, "eligible_eta_hopf_chains",
        lambda available: (SimpleNamespace(conclusion=image),),
    )
    monkeypatch.setattr(
        module, "specialize_registered_higher_stem",
        lambda statement, dimension: group if statement == source and dimension == 5 else None,
    )
    monkeypatch.setattr(
        module, "_eligible_group_instance",
        lambda statement, concrete: statement == source and concrete == group,
    )
    proposals = expand_cited_hopf_lift(goal, (source,))
    assert len(proposals) == 1
    assert proposals[0].subgoals == hopf_lift_inputs(goal, group, image)
    assert not any(isinstance(value, ProofStep) for value in proposals[0].subgoals)


def test_unregistered_or_false_nu_prime_alias_rejected() -> None:
    goal, group, image = cited_nu_prime_image()
    wrong_nu = HomotopyElement(
        "ν′", 3, source=6, target=3,
        generator=GeneratorSymbol("ν", index=3),
    )
    wrong = replace(image, lhs=MapApplication(
        EHP_H_MAP, Composition(wrong_nu, image.lhs.expression.right),
    ))
    assert hopf_lift_inputs(goal, group, wrong) is None
    wrong_sphere = replace(goal, group=TodaPrimaryGroup(7, 4))
    assert hopf_lift_inputs(wrong_sphere, group, image) is None


def test_alias_is_not_inferred_from_a_printable_name_only() -> None:
    goal, group, image = cited_nu_prime_image()
    spoofed = HomotopyElement(
        "ν′", 3, source=6, target=3,
        generator=GeneratorSymbol("unregistered-nu-prime", index=3),
    )
    false = replace(image, lhs=MapApplication(
        EHP_H_MAP, Composition(spoofed, image.lhs.expression.right),
    ))
    assert hopf_lift_inputs(goal, group, false) is None
