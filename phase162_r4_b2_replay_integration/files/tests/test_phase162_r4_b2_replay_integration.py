import pytest

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_stable_eta_proof_replay import build_toda_stable_eta_proof_replay


def _result(n, k):
    presentation, _, _, _ = _method_evidence_data(n, k)
    return presentation.source_replay.group_result


@pytest.mark.parametrize("n", [4, 5])
def test_phase162_r4_b2_replay_uses_derived_root_and_existing_base(n):
    target = _result(n, 1)
    base = _result(3, 1)
    integrated = build_toda_stable_eta_proof_replay(target, base, max_depth=3)
    root = integrated.presentation.root_step
    assert root is integrated.derived_proof.normalized_step
    assert root is integrated.derived_result.proof_step
    assert root is integrated.replay.root_step
    assert integrated.derived_result.source_entry.step is root
    assert root is not target.proof_step
    assert root.premises[0] is integrated.derived_proof.transport_proof.transported_step
    assert root.premises[0].premises[0] is base.proof_step
    assert root.premises[0].premises[1] is integrated.derived_proof.transport_proof.isomorphism_step
    assert integrated.derived_result.target == target.target
    assert integrated.derived_result.group_structure.order == target.group_structure.order
    assert target.proof_step is target.source_entry.step


@pytest.mark.parametrize("n", [4, 5])
def test_phase162_r4_b2_replay_depth_and_presented_edges(n):
    integrated = build_toda_stable_eta_proof_replay(_result(n, 1), _result(3, 1), 3)
    assert integrated.replay.steps[0].proof_step is integrated.replay.root_step
    assert any(node.proof_step is integrated.derived_proof.transport_proof.transported_step for node in integrated.replay.steps)
    assert any(node.proof_step is integrated.derived_proof.transport_proof.isomorphism_step for node in integrated.replay.steps)
    assert any(node.proof_step is integrated.derived_proof.transport_proof.base_step for node in integrated.replay.steps)
    edges = integrated.presentation.edges
    assert any(edge.parent_step is integrated.replay.root_step and edge.premise_step is integrated.derived_proof.transport_proof.transported_step for edge in edges)
    assert all(node.depth <= 3 for node in integrated.replay.steps)


def test_phase162_r4_b2_replay_rejects_unstable_and_base_targets():
    base = _result(3, 1)
    for n in [2, 3]:
        with pytest.raises(ValueError):
            build_toda_stable_eta_proof_replay(_result(n, 1), base)


def test_phase162_r4_b2_replay_rejects_wrong_base():
    with pytest.raises(ValueError):
        build_toda_stable_eta_proof_replay(_result(5, 1), _result(4, 1))


def test_phase162_r4_b2_replay_rejects_invalid_depth():
    with pytest.raises(ValueError, match="max_depth"):
        build_toda_stable_eta_proof_replay(_result(4, 1), _result(3, 1), True)
