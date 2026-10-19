import pytest

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup
from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_stable_concrete_transport_proof import build_toda_stable_concrete_transport_proof
from toda_rules import Toda45IsomorphismStatement


def _result(n, k):
    presentation, _, _, _ = _method_evidence_data(n, k)
    return presentation.source_replay.group_result


@pytest.mark.parametrize("n, count", [(4, 1), (5, 2)])
def test_phase162_r4_b2_1stem_concrete_transport_keeps_rule_ancestry(n, count):
    target = _result(n, 1)
    base = _result(3, 1)
    proof = build_toda_stable_concrete_transport_proof(target, base)
    transported = proof.transported_step
    assert proof.base_step is base.proof_step
    assert transported.premises == (proof.base_step, proof.isomorphism_step)
    assert isinstance(proof.isomorphism_step.conclusion, Toda45IsomorphismStatement)
    assert len(proof.isomorphism_step.premises) == 3
    assert transported.inference_rule is not None
    assert transported.conclusion.rhs.order == base.group_structure.order
    assert isinstance(transported.conclusion.rhs.generator, IteratedSuspension)
    assert transported.conclusion.rhs.generator.expression == base.group_structure.generator
    assert transported.conclusion.lhs.sphere_dimension == n
    exponent = proof.isomorphism_step.conclusion.map.exponent
    assert exponent.left == n
    assert exponent.right.right == 3


def test_phase162_r4_b2_does_not_modify_original_repository_root():
    target = _result(5, 1)
    original_root = target.proof_step
    proof = build_toda_stable_concrete_transport_proof(target, _result(3, 1))
    assert target.proof_step is original_root
    assert proof.transported_step is not original_root
    assert isinstance(proof.transported_step.conclusion.rhs, FiniteCyclicGroup)


def test_phase162_r4_b2_rejects_noncanonical_base():
    with pytest.raises(ValueError, match="canonical stable base"):
        build_toda_stable_concrete_transport_proof(_result(5, 1), _result(4, 1))


def test_phase162_r4_b2_base_and_unstable_are_not_transport_targets():
    base = _result(3, 1)
    with pytest.raises(ValueError, match="strictly above"):
        build_toda_stable_concrete_transport_proof(base, base)
    with pytest.raises(ValueError, match="strictly above"):
        build_toda_stable_concrete_transport_proof(_result(2, 1), base)


def test_phase162_r4_b2_requires_actual_base_evidence():
    with pytest.raises(TypeError, match="base_result"):
        build_toda_stable_concrete_transport_proof(_result(5, 1), None)
