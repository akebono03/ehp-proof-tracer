from dataclasses import dataclass

import pytest

from map_property_rules import SurjectiveMapStatement
from phase165_r12_r2_quotient_rules import (
    CyclicStructureStatement,
    HomomorphismPresentationStatement,
    KernelMultipleStatement,
    QuotientIsomorphismStatement,
    first_isomorphism_quotient_inference_rule,
    infinite_cyclic_quotient_structure_inference_rule,
)
from phase165_r8_rule_provider import build_production_rule_provider, create_rule_expansion_provider
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


@dataclass(frozen=True)
class Label:
    name: str


def premise(statement):
    return ProofStep(conclusion=statement, premises=(), rule=ProofRule.RELATION)


def example():
    f, a, b, x, y = (Label(s) for s in ("E", "pi3_2", "pi4_3", "eta2", "eta3"))
    target = QuotientIsomorphismStatement(f, a, b, x, y, 2)
    known = (
        premise(HomomorphismPresentationStatement(f, a, b, x, y)),
        premise(KernelMultipleStatement(f, a, x, 2)),
        premise(SurjectiveMapStatement(f)),
    )
    return f, a, b, x, y, target, known


def test_first_iso_inverse_has_fully_bound_subgoals():
    f, a, b, x, y, target, known = example()
    rule = first_isomorphism_quotient_inference_rule()
    expansions = create_rule_expansion_provider((rule,))(target)
    assert len(expansions) == 1
    assert expansions[0].subgoals == tuple(step.conclusion for step in known)


def test_first_iso_forward_reconstructs_target_from_matching_premises():
    f, a, b, x, y, target, known = example()
    matches = find_inference_matches_for_rule(first_isomorphism_quotient_inference_rule(), known)
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.conclusion == target
    assert step.premises == known
    assert step.rule == ProofRule.INFERENCE


def test_cyclic_quotient_forward_requires_infinite_cyclic_source():
    f, a, b, x, y, target, known = example()
    rule = infinite_cyclic_quotient_structure_inference_rule()
    inputs = (premise(target), premise(CyclicStructureStatement(a, x, None)))
    matches = find_inference_matches_for_rule(rule, inputs)
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.conclusion == CyclicStructureStatement(b, y, 2)
    assert find_inference_matches_for_rule(
        rule, (premise(target), premise(CyclicStructureStatement(a, x, 4)))
    ) == ()


def test_cyclic_quotient_backward_refuses_to_invent_map_and_domain():
    f, a, b, x, y, target, known = example()
    goal = CyclicStructureStatement(b, y, 2)
    assert create_rule_expansion_provider((infinite_cyclic_quotient_structure_inference_rule(),))(goal) == ()


def test_positive_kernel_index_validation():
    f, a, b, x, y, target, known = example()
    with pytest.raises(ValueError):
        KernelMultipleStatement(f, a, x, 0)
    with pytest.raises(ValueError):
        QuotientIsomorphismStatement(f, a, b, x, y, -1)
    with pytest.raises(ValueError):
        CyclicStructureStatement(b, y, 0)


def test_production_registry_includes_both_shared_rules():
    provider, report = build_production_rule_provider()
    names = set(report.rule_names)
    assert "first isomorphism theorem for generated kernel" in names
    assert "infinite cyclic quotient structure" in names
    assert len(provider(example()[5])) >= 1
