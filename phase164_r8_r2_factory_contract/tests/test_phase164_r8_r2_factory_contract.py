"""Focused R8-R2 contract tests; no production callers migrated yet."""
import pytest

from phase164_r8_proofstep_factory import (
    create_relation_proof_step,
    derive_inference_proof_step,
    retain_existing_proof_step,
)
from proof import InferenceMatch, InferenceRule, ProofRule, ProofStep, Relation


def test_relation_uses_existing_checked_constructor():
    relation = Relation(lhs="a", rhs="b")
    step = create_relation_proof_step(relation)
    assert type(step) is ProofStep
    assert step.conclusion is relation
    assert step.rule is ProofRule.RELATION
    assert step.premises == ()


def test_relation_rejects_wrong_input():
    with pytest.raises(TypeError, match="relation"):
        create_relation_proof_step("a=b")


def test_inference_uses_existing_rule_with_same_premise_objects():
    premise = ProofStep(conclusion="input", premises=(), rule=ProofRule.GIVEN)
    rule = InferenceRule(
        name="phase164_r8_r2_fixture",
        conclusion_builder=lambda premises: ("derived", premises[0].conclusion),
    )
    match = InferenceMatch(inference_rule=rule, premises=(premise,))
    step = derive_inference_proof_step(match)
    assert step.rule is ProofRule.INFERENCE
    assert step.inference_rule is rule
    assert step.premises == (premise,)
    assert step.premises[0] is premise
    assert step.conclusion == ("derived", "input")


def test_inference_rejects_unchecked_argument():
    with pytest.raises(TypeError, match="match"):
        derive_inference_proof_step(object())


def test_replay_preserves_identity():
    step = ProofStep(conclusion="existing", premises=(), rule=ProofRule.GIVEN)
    assert retain_existing_proof_step(step) is step


def test_replay_rejects_non_proof_step():
    with pytest.raises(TypeError, match="ProofStep"):
        retain_existing_proof_step(object())
