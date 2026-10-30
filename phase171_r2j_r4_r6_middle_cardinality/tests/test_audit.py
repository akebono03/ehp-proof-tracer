"""Focused mathematical, matcher, source-boundary and replay checks for R4-R6."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_E_MAP, EHP_H_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r5_short_exact_sequence.source import short_exact_from_ehp
from phase171_r2j_r4_r6_middle_cardinality.audit import (
    _git,
    build_middle_cardinality_proof,
    screened_prior_pi52,
)
from phase171_r2j_r4_r6_middle_cardinality.source import (
    FiniteGroupCardinality,
    cardinality_from_short_exact,
    expand_finite_cardinality_from_short_exact,
    finite_cardinality_from_short_exact_rule,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement


def _fixture():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    c = TodaPrimaryGroup(6, 5)
    element_a = HomotopyElement(
        name="a", dimension=2, source=5, target=2,
        generator=GeneratorSymbol(family="a", index=2),
    )
    element_c = HomotopyElement(
        name="c", dimension=5, source=6, target=5,
        generator=GeneratorSymbol(family="c", index=5),
    )
    left = Relation(a, FiniteCyclicGroup(2, element_a), RelationType.EQUALITY)
    right = Relation(c, FiniteCyclicGroup(2, element_c), RelationType.EQUALITY)
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        a, b, c, EHP_E_MAP, EHP_H_MAP,
    ))
    sequence = short_exact_from_ehp(
        MapInjective(TodaSuspensionMap(a, b)),
        exact,
        MapSurjective(TodaHopfInvariantMap(b, c)),
    )
    assert sequence is not None
    return left, sequence, right


def test_generic_cardinality_product_without_middle_group_presentation():
    left, sequence, right = _fixture()
    value = cardinality_from_short_exact(left, sequence, right)
    assert value == FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    assert value.group == sequence.middle_group
    assert len(expand_finite_cardinality_from_short_exact(value, left, sequence, right)) == 1


def test_mixed_source_and_inference_steps_produce_real_inference():
    left, sequence, right = _fixture()
    goal = cardinality_from_short_exact(left, sequence, right)
    assert goal is not None
    steps = (
        ProofStep(left, (), ProofRule.GIVEN),
        ProofStep(sequence, (), ProofRule.INFERENCE),
        ProofStep(right, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(
        finite_cardinality_from_short_exact_rule(goal), steps,
    )
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == steps
    assert result.conclusion == goal


def test_permuted_available_premises_match_in_canonical_order():
    left, sequence, right = _fixture()
    goal = cardinality_from_short_exact(left, sequence, right)
    assert goal is not None
    steps = (
        ProofStep(left, (), ProofRule.GIVEN),
        ProofStep(sequence, (), ProofRule.INFERENCE),
        ProofStep(right, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(
        finite_cardinality_from_short_exact_rule(goal),
        (steps[2], steps[0], steps[1]),
    )
    assert len(matches) == 1
    assert matches[0].premises == steps


def test_bad_end_group_coordinates_and_fake_cardinality_are_rejected():
    left, sequence, right = _fixture()
    wrong_left = replace(left, lhs=TodaPrimaryGroup(6, 2))
    wrong_right = replace(right, lhs=TodaPrimaryGroup(7, 5))
    assert cardinality_from_short_exact(wrong_left, sequence, right) is None
    assert cardinality_from_short_exact(left, sequence, wrong_right) is None
    goal = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 5)
    assert expand_finite_cardinality_from_short_exact(goal, left, sequence, right) == ()


def test_wrong_sequence_map_endpoints_are_rejected():
    left, sequence, right = _fixture()
    bad = replace(sequence, injection=TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    ))
    assert cardinality_from_short_exact(left, bad, right) is None
    bad = replace(sequence, projection=TodaHopfInvariantMap(
        TodaPrimaryGroup(6, 4), TodaPrimaryGroup(6, 5),
    ))
    assert cardinality_from_short_exact(left, bad, right) is None


def test_unproved_short_exact_or_forged_group_leaf_is_rejected():
    left, sequence, right = _fixture()
    goal = cardinality_from_short_exact(left, sequence, right)
    assert goal is not None
    rule = finite_cardinality_from_short_exact_rule(goal)
    valid = (
        ProofStep(left, (), ProofRule.GIVEN),
        ProofStep(sequence, (), ProofRule.INFERENCE),
        ProofStep(right, (), ProofRule.INFERENCE),
    )
    assert find_inference_matches_for_rule(rule, (
        valid[0], ProofStep(sequence, (), ProofRule.GIVEN), valid[2],
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        valid[0], valid[1], ProofStep(right, (), ProofRule.RELATION),
    )) == ()


def test_positive_integer_cardinality_and_cyclic_orders_required():
    left, sequence, right = _fixture()
    assert cardinality_from_short_exact(
        replace(left, rhs=FiniteCyclicGroup(True, left.rhs.generator)),
        sequence, right,
    ) is None
    assert cardinality_from_short_exact(
        left, sequence, replace(right, rhs=FiniteCyclicGroup(0, right.rhs.generator)),
    ) is None
    with pytest.raises(ValueError):
        finite_cardinality_from_short_exact_rule(FiniteGroupCardinality(
            TodaPrimaryGroup(6, 3), 0,
        ))
    assert expand_finite_cardinality_from_short_exact(object(), left, sequence, right) == ()


def test_real_prior_proposition56_source_is_unique_and_earlier():
    screened, goal, citing = _screened_context()
    link = screened_prior_pi52(screened, citing)
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.conclusion.lhs == TodaPrimaryGroup(5, 2)
    assert link.step.conclusion.rhs.order == 2
    assert precedes_citing_assertion(screened, link.assertion_id, citing)
    assert link.step.conclusion != goal


def test_read_only_git_guard_rejects_mutating_commands():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_replay_uses_prior_source_and_inferred_cyclic_codomain():
    root, nodes, report = build_middle_cardinality_proof()
    assert root.rule is ProofRule.INFERENCE
    assert root.conclusion == FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    assert root.premises[0].rule is ProofRule.GIVEN
    assert root.premises[1].rule is ProofRule.INFERENCE
    assert root.premises[2].rule is ProofRule.INFERENCE
    assert report["status"] == "INFERRED"
    assert report["cardinality"] == 4
    assert report["new_given_added"] == 0
    assert report["nu_prime_order_four_proven"] is False
    assert report["pi63_group_proven"] is False
    assert sum(node.rule is ProofRule.GIVEN for node in nodes) >= 3
