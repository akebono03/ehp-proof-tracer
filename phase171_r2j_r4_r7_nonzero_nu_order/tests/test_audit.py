"""Focused type, provenance, negative and end-to-end proof tests for R4-R7."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_E_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapInjective
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r7_nonzero_nu_order.audit import (
    _git,
    build_nonzero_nu_order_proof,
)
from phase171_r2j_r4_r7_nonzero_nu_order.source import (
    FiniteElementOrder,
    NonZeroGroupElement,
    inferred_nonzero_double_rule,
    inferred_order_four_rule,
    injected_generator_nonzero_rule,
    nonzero_cyclic_generator_image,
    nonzero_double_from_equality,
    order_four_from_nonzero_double,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _eta(n: int, *, typed: bool = True) -> HomotopyElement:
    return HomotopyElement(
        name="η_" + str(n), dimension=n,
        source=n + 1 if typed else None,
        target=n if typed else None,
        generator=GeneratorSymbol(family="η", index=n),
    )


def _triple(n: int, *, typed: bool = True) -> Composition:
    return Composition(
        _eta(n, typed=typed),
        Composition(_eta(n + 1, typed=typed), _eta(n + 2, typed=typed)),
    )


def _fixture():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    source = Relation(a, FiniteCyclicGroup(2, _triple(2)), RelationType.EQUALITY)
    injective = MapInjective(TodaSuspensionMap(a, b))
    image = MapApplication(EHP_E_MAP, _triple(2))
    nu = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    equality = Relation(Multiple(2, nu), image, RelationType.EQUALITY)
    finite = FiniteGroupCardinality(b, 4)
    return source, injective, equality, finite


def test_injective_nonzero_from_a_real_finite_cyclic_generator():
    source, injective, equality, _ = _fixture()
    value = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    assert value == NonZeroGroupElement(TodaPrimaryGroup(6, 3), equality.rhs)
    rule = injected_generator_nonzero_rule(value, source, injective)
    parents = (
        ProofStep(source, (), ProofRule.GIVEN),
        ProofStep(injective, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    root = derive_inference_proof_step(matches[0])
    assert root.rule is ProofRule.INFERENCE
    assert root.conclusion == value
    assert root.premises == parents


def test_prior_untyped_eta_composition_is_matched_by_registered_identity():
    source, injective, equality, _ = _fixture()
    untyped = replace(source, rhs=FiniteCyclicGroup(2, _triple(2, typed=False)))
    assert source.rhs.generator != untyped.rhs.generator
    assert nonzero_cyclic_generator_image(
        untyped, injective, equality.rhs,
    ) == NonZeroGroupElement(TodaPrimaryGroup(6, 3), equality.rhs)


def test_wrong_generator_map_and_cyclic_order_are_rejected():
    source, injective, equality, _ = _fixture()
    wrong_gen = replace(source, rhs=FiniteCyclicGroup(2, _triple(3)))
    wrong_e = MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    ))
    assert nonzero_cyclic_generator_image(wrong_gen, injective, equality.rhs) is None
    assert nonzero_cyclic_generator_image(source, wrong_e, equality.rhs) is None
    assert nonzero_cyclic_generator_image(
        replace(source, rhs=FiniteCyclicGroup(1, source.rhs.generator)),
        injective, equality.rhs,
    ) is None
    assert nonzero_cyclic_generator_image(
        replace(source, rhs=FiniteCyclicGroup(True, source.rhs.generator)),
        injective, equality.rhs,
    ) is None


def test_nonzero_image_rule_rejects_fabricated_given_injectivity():
    source, injective, equality, _ = _fixture()
    goal = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    assert goal is not None
    rule = injected_generator_nonzero_rule(goal, source, injective)
    assert find_inference_matches_for_rule(rule, (
        ProofStep(source, (), ProofRule.GIVEN),
        ProofStep(injective, (), ProofRule.GIVEN),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(source, (), ProofRule.RELATION),
        ProofStep(injective, (), ProofRule.INFERENCE),
    )) == ()


def test_typed_equality_transfers_nonzero_to_exact_double():
    source, injective, equality, _ = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    assert nonzero is not None
    value = nonzero_double_from_equality(equality, nonzero)
    assert value == NonZeroGroupElement(TodaPrimaryGroup(6, 3), equality.lhs)
    rule = inferred_nonzero_double_rule(value, equality, nonzero)
    parents = (
        ProofStep(equality, (), ProofRule.INFERENCE),
        ProofStep(nonzero, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    root = derive_inference_proof_step(matches[0])
    assert root.conclusion == value
    assert root.premises == parents


def test_wrong_double_coefficient_equality_and_group_fail_closed():
    source, injective, equality, _ = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    assert nonzero is not None
    for bad in (0, 1, 3, True):
        altered = replace(equality, lhs=Multiple(bad, equality.lhs.expression))
        assert nonzero_double_from_equality(altered, nonzero) is None
    assert nonzero_double_from_equality(
        replace(equality, rhs=MapApplication(EHP_E_MAP, _triple(3))),
        nonzero,
    ) is None
    assert nonzero_double_from_equality(
        equality,
        replace(nonzero, group=TodaPrimaryGroup(6, 4)),
    ) is None


def test_nonzero_double_must_have_inferred_equality_and_image():
    source, injective, equality, _ = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    assert nonzero is not None
    value = nonzero_double_from_equality(equality, nonzero)
    assert value is not None
    rule = inferred_nonzero_double_rule(value, equality, nonzero)
    assert find_inference_matches_for_rule(rule, (
        ProofStep(equality, (), ProofRule.GIVEN),
        ProofStep(nonzero, (), ProofRule.INFERENCE),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(equality, (), ProofRule.INFERENCE),
        ProofStep(nonzero, (), ProofRule.GIVEN),
    )) == ()


def test_order_four_uses_cardinality_and_nonzero_double():
    source, injective, equality, finite = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    doubled = nonzero_double_from_equality(equality, nonzero)
    assert doubled is not None
    goal = order_four_from_nonzero_double(finite, doubled)
    assert goal == FiniteElementOrder(TodaPrimaryGroup(6, 3), equality.lhs.expression, 4)
    rule = inferred_order_four_rule(goal, finite, doubled)
    parents = (
        ProofStep(finite, (), ProofRule.INFERENCE),
        ProofStep(doubled, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(rule, (parents[1], parents[0]))
    assert len(matches) == 1
    assert matches[0].premises == parents
    assert derive_inference_proof_step(matches[0]).conclusion == goal


def test_cardinality_and_nonzero_double_must_match():
    source, injective, equality, finite = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    doubled = nonzero_double_from_equality(equality, nonzero)
    assert doubled is not None
    assert order_four_from_nonzero_double(
        replace(finite, order=2), doubled,
    ) is None
    assert order_four_from_nonzero_double(
        replace(finite, order=True), doubled,
    ) is None
    assert order_four_from_nonzero_double(
        finite, replace(doubled, group=TodaPrimaryGroup(7, 3)),
    ) is None
    assert order_four_from_nonzero_double(
        finite, replace(doubled, element=Multiple(3, equality.lhs.expression)),
    ) is None


def test_order_four_rule_requires_two_inferences():
    source, injective, equality, finite = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    doubled = nonzero_double_from_equality(equality, nonzero)
    assert doubled is not None
    goal = order_four_from_nonzero_double(finite, doubled)
    assert goal is not None
    rule = inferred_order_four_rule(goal, finite, doubled)
    assert find_inference_matches_for_rule(rule, (
        ProofStep(finite, (), ProofRule.GIVEN),
        ProofStep(doubled, (), ProofRule.INFERENCE),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(finite, (), ProofRule.INFERENCE),
        ProofStep(doubled, (), ProofRule.GIVEN),
    )) == ()


def test_git_guard_rejects_write_operations():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_live_proof_replay_is_source_bound_and_not_a_cyclic_group_claim():
    double_nonzero_root, order_root, nodes, report = build_nonzero_nu_order_proof()
    assert double_nonzero_root.rule is ProofRule.INFERENCE
    assert order_root.rule is ProofRule.INFERENCE
    assert order_root.conclusion.order == 4
    assert report["status"] == "INFERRED"
    assert report["nu_prime_double_nonzero_proven"] is True
    assert report["nu_prime_order_four_proven"] is True
    assert report["pi63_cyclic_presentation_proven"] is False
    assert report["new_given_added"] == 0
    assert len(report["verified_source_ids"]) >= 3
    assert sum(step.rule is ProofRule.GIVEN for step in nodes) >= 3
