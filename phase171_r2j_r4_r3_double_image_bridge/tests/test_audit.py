"""Focused typed-double substitution, source-screening and live replay tests."""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

from expression import (
    Composition,
    GeneratorSymbol,
    HomotopyElement,
    MapApplication,
    Multiple,
)
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_E_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import GeneratorImage
from phase171_r2j_r4_r3_double_image_bridge.audit import (
    build_double_image_proof,
    screened_double_proof_step,
)
from phase171_r2j_r4_r3_double_image_bridge.source import (
    typed_double_image_conclusion,
    typed_double_image_rule,
)
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    find_inference_matches_for_rule,
)


def _eta(n: int) -> HomotopyElement:
    return HomotopyElement(
        name="η" + str(n),
        dimension=n,
        source=n + 1,
        target=n,
        generator=GeneratorSymbol(family="η", index=n),
    )


def _triple(n: int) -> Composition:
    return Composition(_eta(n), Composition(_eta(n + 1), _eta(n + 2)))


def _inputs() -> tuple[Relation, GeneratorImage]:
    nu = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    double = Relation(Multiple(2, nu), _triple(3), RelationType.EQUALITY)
    image = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3)),
        _triple(2), _triple(3),
    )
    return double, image


def test_type_checked_double_image_has_exact_expected_structure():
    double, image = _inputs()
    target = typed_double_image_conclusion(double, image)
    assert target == Relation(
        double.lhs, MapApplication(EHP_E_MAP, image.source_generator),
        RelationType.EQUALITY,
    )
    assert target.lhs.coefficient == 2
    assert target.rhs.expression == _triple(2)


def test_actual_matcher_builds_inference_step_with_both_ancestors():
    double, image = _inputs()
    cited_fixture = ProofStep(double, (), ProofRule.GIVEN)
    inferred_fixture = ProofStep(image, (), ProofRule.INFERENCE)
    rule = typed_double_image_rule(double, image)
    matches = find_inference_matches_for_rule(rule, (cited_fixture, inferred_fixture))
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.premises == (cited_fixture, inferred_fixture)
    assert step.conclusion == typed_double_image_conclusion(double, image)


def test_wrong_target_composition_is_rejected_not_string_matched():
    double, image = _inputs()
    wrongly_ordered = Composition(_eta(3), Composition(_eta(5), _eta(4)))
    assert typed_double_image_conclusion(
        double, replace(image, target_generator=wrongly_ordered),
    ) is None
    assert typed_double_image_conclusion(
        replace(double, rhs=wrongly_ordered), image,
    ) is None


def test_wrong_map_domain_and_codomain_are_rejected():
    double, image = _inputs()
    wrong_source = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    wrong_target = TodaSuspensionMap(TodaPrimaryGroup(5, 2), TodaPrimaryGroup(7, 3))
    assert typed_double_image_conclusion(double, replace(image, map=wrong_source)) is None
    assert typed_double_image_conclusion(double, replace(image, map=wrong_target)) is None


def test_wrong_nu_degree_is_rejected():
    double, image = _inputs()
    bad_nu = replace(double.lhs.expression, source=7)
    assert typed_double_image_conclusion(
        replace(double, lhs=Multiple(2, bad_nu)), image,
    ) is None


def test_nonpositive_or_boolean_multiple_cannot_produce_relation():
    double, image = _inputs()
    for coefficient in (0, -2, True):
        assert typed_double_image_conclusion(
            replace(double, lhs=Multiple(coefficient, double.lhs.expression)), image,
        ) is None


def test_rule_does_not_accept_noninferred_image_or_uncited_relation_fixture():
    double, image = _inputs()
    rule = typed_double_image_rule(double, image)
    given_double = ProofStep(double, (), ProofRule.GIVEN)
    inferred_image = ProofStep(image, (), ProofRule.INFERENCE)
    assert find_inference_matches_for_rule(
        rule, (given_double, ProofStep(image, (), ProofRule.GIVEN)),
    ) == ()
    assert find_inference_matches_for_rule(
        rule, (ProofStep(double, (), ProofRule.INFERENCE), inferred_image),
    ) == ()
    assert find_inference_matches_for_rule(
        rule, (given_double, ProofStep(replace(image, source_generator=_eta(2)), (), ProofRule.INFERENCE)),
    ) == ()


def test_no_unregistered_double_relation_can_be_screened():
    empty = SimpleNamespace(proof_links=())
    with pytest.raises(RuntimeError):
        screened_double_proof_step(empty, "unused")


def test_real_source_bound_tree_builds_double_image_without_group_theorem():
    root, ancestry, report = build_double_image_proof()
    assert root.rule is ProofRule.INFERENCE
    assert report["status"] == "INFERRED"
    assert report["given_leaves"] == 2
    assert report["new_given_added"] == 0
    assert report["pi63_group_proven"] is False
    assert sum(step.rule is ProofRule.INFERENCE for step in ancestry) >= 2
    assert len(root.premises) == 2
