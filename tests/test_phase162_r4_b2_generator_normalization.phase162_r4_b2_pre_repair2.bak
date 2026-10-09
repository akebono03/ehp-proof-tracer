import pytest

from proof import ProofRule, ProofStep
from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_stable_concrete_transport_proof import build_toda_stable_concrete_transport_proof
from toda_stable_eta_generator_normalization import (
    build_toda_stable_eta_normalized_proof,
    toda_eta_concrete_generator_normalization_inference_rule,
)
from toda_rules import toda_eta_family_definition_statement


def _group_result(n, k):
    presentation, _, _, _ = _method_evidence_data(n, k)
    return presentation.source_replay.group_result


@pytest.mark.parametrize("n", [4, 5])
def test_phase162_r4_b2_eta_normalization_has_explicit_three_premises(n):
    target = _group_result(n, 1)
    transport = build_toda_stable_concrete_transport_proof(target, _group_result(3, 1))
    normalized = build_toda_stable_eta_normalized_proof(transport)
    assert normalized.normalized_step.premises == (
        transport.transported_step,
        normalized.base_definition_step,
        normalized.target_definition_step,
    )
    assert normalized.normalized_step.inference_rule is not None
    assert normalized.normalized_step.conclusion == target.proof_step.conclusion
    assert target.proof_step is not normalized.normalized_step
    assert normalized.normalized_step.conclusion.rhs.order == transport.transported_step.conclusion.rhs.order


def test_phase162_r4_b2_eta_normalization_rejects_wrong_target_definition():
    transport = build_toda_stable_concrete_transport_proof(
        _group_result(5, 1), _group_result(3, 1)
    )
    normalized = build_toda_stable_eta_normalized_proof(transport)
    wrong = ProofStep(
        conclusion=toda_eta_family_definition_statement(4),
        premises=(), rule=ProofRule.GIVEN,
    )
    rule = toda_eta_concrete_generator_normalization_inference_rule()
    from proof import run_inference_until_stable_with_history
    result = run_inference_until_stable_with_history(
        rule, (transport.transported_step, normalized.base_definition_step, wrong)
    )
    assert all(step.inference_rule is not rule for step in result.steps)


def test_phase162_r4_b2_eta_normalization_requires_actual_transport():
    with pytest.raises(TypeError, match="transport_proof"):
        build_toda_stable_eta_normalized_proof(None)
