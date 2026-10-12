"""R8-R3: delegation must preserve the production inference contract."""
import pytest

import phase161_r5_backward_proof_reconstruction as backward
from phase164_r8_proofstep_factory import derive_inference_proof_step
from proof import ProofRule, ProofStep
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data


def test_backward_reconstruction_uses_shared_factory_for_seven_derivations(monkeypatch):
    calls = []

    def recording_factory(match):
        result = derive_inference_proof_step(match)
        calls.append((match, result))
        return result

    monkeypatch.setattr(backward, 'derive_inference_proof_step', recording_factory)
    leaves = build_phase59_3_data()['premise_steps']
    result = backward.reconstruct_phase161_r5_goal(backward.phase161_r5_target_goal(), leaves)
    assert len(calls) == 7
    assert len(result.derived_steps) == 7
    assert all(derived is recorded[1] for derived, recorded in zip(result.derived_steps, calls))
    assert all(step.rule is ProofRule.INFERENCE for step in result.derived_steps)
    assert all(step.inference_rule is match.inference_rule and step.premises == match.premises for match, step in calls)
    assert result.final_step is result.derived_steps[-1]


def test_backward_reconstruction_retains_original_leaf_identity():
    leaves = build_phase59_3_data()['premise_steps']
    result = backward.reconstruct_phase161_r5_goal(backward.phase161_r5_target_goal(), leaves)
    assert all(any(used is leaf for leaf in leaves) for used in result.leaf_steps)
    assert not any(derived is leaf for derived in result.derived_steps for leaf in leaves)


def test_backward_reconstruction_rejects_bad_factory_result(monkeypatch):
    original = derive_inference_proof_step

    def damaged_factory(match):
        valid = original(match)
        return ProofStep(conclusion=object(), premises=valid.premises, rule=ProofRule.INFERENCE, inference_rule=valid.inference_rule)

    monkeypatch.setattr(backward, 'derive_inference_proof_step', damaged_factory)
    leaves = build_phase59_3_data()['premise_steps']
    with pytest.raises(ValueError, match='conclusion|goal'):
        backward.reconstruct_phase161_r5_goal(backward.phase161_r5_target_goal(), leaves)
