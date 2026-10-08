"""Focused contracts for Phase 162 R3-A, without Narrative changes."""

import pytest

from audit_phase162_r3a_presentation import audit_presentation, build_r2_fixture
from proof import ProofRule


@pytest.fixture(scope="module")
def r2_fixture():
    return build_r2_fixture()


@pytest.fixture(scope="module")
def audit_report():
    return audit_presentation()


def test_phase162_r3a_r2_root_is_fresh_inference(r2_fixture):
    result = r2_fixture
    final = result.reconstruction.final_step
    assert final.rule is ProofRule.INFERENCE
    assert final.inference_rule.name == "phase162_group_structure_transport"
    assert final.premises[1] is result.source_structure_step
    assert final.premises[2] is result.generator_image_step
    assert result.provenance.verified_inferences >= 1


def test_phase162_r3a_complete_presentation_preserves_nodes_and_edges(audit_report):
    report = audit_report
    assert report["status"] == "PASS"
    assert report["node_count"] > 0
    assert report["edge_count"] > 0
    assert report["all_nodes_preserved"]
    assert report["all_edges_preserved"]
    assert report["max_depth"] >= 2


def test_phase162_r3a_presentation_preserves_exact_step_identity(audit_report):
    report = audit_report
    assert report["root_and_entry_identity"]
    assert report["premise_object_identity_preserved"]
    assert report["root_premise_count"] == 3
    assert report["given_count"] + report["inference_count"] == report["node_count"]
