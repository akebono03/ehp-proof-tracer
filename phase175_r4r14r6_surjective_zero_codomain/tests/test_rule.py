"""General surjective-and-zero-image zero-codomain proof contract."""
from __future__ import annotations

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapSurjective
from phase175_r4r14r6_surjective_zero_codomain.rule import (
    RULE_NAME, expand_surjective_zero_codomain,
    surjective_zero_codomain_inputs, surjective_zero_codomain_rule,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule


def root(i: int, n: int) -> TodaPrimaryGroupZeroStatement:
    return TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(i, n))


def test_pi106_has_typed_surjectivity_and_zero_image_goals() -> None:
    claim = root(10, 6)
    mapping = TodaSuspensionMap(TodaPrimaryGroup(9, 5), TodaPrimaryGroup(10, 6))
    required = surjective_zero_codomain_inputs(claim)
    assert required == (MapSurjective(mapping), ImageZeroStatement(mapping))
    options = expand_surjective_zero_codomain(claim)
    assert len(options) == 1
    assert options[0].subgoals == required
    assert options[0].rule.name == RULE_NAME


@pytest.mark.parametrize("i,n", [(9, 5), (10, 6), (12, 7), (15, 8)])
def test_root_candidate_is_not_stem_specific(i: int, n: int) -> None:
    claim = root(i, n)
    required = surjective_zero_codomain_inputs(claim)
    assert required is not None
    assert required[0].map == required[1].map
    assert required[0].map.target_group == claim.group


@pytest.mark.parametrize("invalid", [root(1, 2), root(3, 2), root(2, 3), root(5, 7), "zero", None])
def test_invalid_or_below_diagonal_goals_fail_closed(invalid: object) -> None:
    assert surjective_zero_codomain_inputs(invalid) is None
    assert expand_surjective_zero_codomain(invalid) == ()


def test_rule_needs_two_independently_inferred_premises() -> None:
    claim = root(10, 6)
    required = surjective_zero_codomain_inputs(claim)
    assert required is not None
    rule = surjective_zero_codomain_rule(claim)
    parents = tuple(ProofStep(x, (), ProofRule.INFERENCE) for x in required)
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == claim
    assert derived.premises == parents
    assert find_inference_matches_for_rule(rule, parents[:1]) == ()
    assert find_inference_matches_for_rule(rule, (ProofStep(required[0], (), ProofRule.GIVEN), parents[1])) == ()
    assert find_inference_matches_for_rule(rule, (parents[0], ProofStep(required[1], (), ProofRule.GIVEN))) == ()


def test_wrong_map_cannot_close_zero_group() -> None:
    claim = root(10, 6)
    required = surjective_zero_codomain_inputs(claim)
    assert required is not None
    wrong = TodaSuspensionMap(TodaPrimaryGroup(10, 6), TodaPrimaryGroup(11, 7))
    rule = surjective_zero_codomain_rule(claim)
    assert find_inference_matches_for_rule(rule, (
        ProofStep(MapSurjective(wrong), (), ProofRule.INFERENCE),
        ProofStep(required[1], (), ProofRule.INFERENCE),
    )) == ()


def test_backward_expansion_creates_no_given_or_proof_step() -> None:
    options = expand_surjective_zero_codomain(root(10, 6))
    assert len(options) == 1
    assert all(not isinstance(x, ProofStep) for x in options[0].subgoals)
