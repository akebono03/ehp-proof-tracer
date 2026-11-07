"""Focused R25 tests; fabricated premises are test fixtures, not public proof."""
from __future__ import annotations

import pytest

from homotopy_groups import TodaPrimaryGroup
from proof import (
    InferenceRule, LiteratureReference, ProofRule, ProofStep,
    find_inference_match, run_inference_until_stable_with_history,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    PROP27_REFERENCE, Prop27GeneralTheoremPremise,
    Prop27TypedHopfDeltaStatement, prop27_typed_specialization_rule,
    typed_specialization,
)


def fixture_step(*, locator="Proposition 2.7", rule=ProofRule.INFERENCE,
                 sign=True):
    parent = InferenceRule(
        name="test-only independent cited schema premise",
        literature_reference=LiteratureReference(
            label="Toda Proposition 2.7", locator=locator,
        ),
    )
    return ProofStep(
        conclusion=Prop27GeneralTheoremPremise(sign_undetermined=sign),
        premises=(), rule=rule, inference_rule=parent,
    )


def test_n6_correct_groups_and_sign():
    result = typed_specialization(6)
    assert isinstance(result, Prop27TypedHopfDeltaStatement)
    assert result.delta.source_group == TodaPrimaryGroup(13, 13)
    assert result.delta.target_group == TodaPrimaryGroup(11, 6)
    assert result.hopf.source_group == TodaPrimaryGroup(11, 6)
    assert result.hopf.target_group == TodaPrimaryGroup(11, 11)
    assert (result.source_iota_dimension, result.target_iota_dimension) == (13, 11)
    assert result.absolute_coefficient == 2
    assert result.sign_undetermined is True


@pytest.mark.parametrize("n", [0, 1, 3, 5, -2, 6.0, True, "6"])
def test_reject_invalid_dimensions(n):
    with pytest.raises(ValueError):
        typed_specialization(n)


def test_valid_even_generalization():
    for n in (2, 4, 6, 8, 10):
        value = typed_specialization(n)
        assert value.delta.target_group == value.hopf.source_group
        assert value.sign_undetermined


def test_no_premise_no_proof():
    assert find_inference_match(prop27_typed_specialization_rule(6), ()) is None


def test_given_premise_rejected():
    rule = prop27_typed_specialization_rule(6)
    assert find_inference_match(rule, (fixture_step(rule=ProofRule.GIVEN),)) is None


def test_wrong_source_rejected():
    rule = prop27_typed_specialization_rule(6)
    assert find_inference_match(rule, (fixture_step(locator="Proposition 5.9"),)) is None


def test_missing_sign_preservation_rejected():
    rule = prop27_typed_specialization_rule(6)
    assert find_inference_match(rule, (fixture_step(sign=False),)) is None


def test_synthetic_cited_fixture_produces_inference_not_given():
    premise = fixture_step()
    rule = prop27_typed_specialization_rule(6)
    result = run_inference_until_stable_with_history(rule, (premise,))
    derived = [s for s in result.steps if isinstance(s.conclusion, Prop27TypedHopfDeltaStatement)]
    assert len(derived) == 1
    assert derived[0].rule is ProofRule.INFERENCE
    assert derived[0].premises == (premise,)
    assert derived[0].inference_rule.literature_reference == PROP27_REFERENCE
    assert derived[0].conclusion == typed_specialization(6)


def test_rule_does_not_create_premise():
    rule = prop27_typed_specialization_rule(6)
    assert len(rule.premise_patterns) == 1
    assert rule.premise_patterns[0].statement_type is Prop27GeneralTheoremPremise
    assert rule.premise_patterns[0].proof_rule is ProofRule.INFERENCE
