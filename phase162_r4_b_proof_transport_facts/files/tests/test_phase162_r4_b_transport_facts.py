from dataclasses import replace

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_transport_facts import (
    extract_suspension_transport_facts,
)


def test_phase162_r4_b_pi5_4_extracts_tree_backed_transport():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    facts = extract_suspension_transport_facts(presentation.root_step)
    assert facts is not None
    assert facts.isomorphism_step in facts.transported_group_step.premises
    assert facts.source_group_step in facts.transported_group_step.premises
    assert facts.generator_bridge_step.conclusion.rhs == (
        presentation.root_step.conclusion.rhs.generator
    )


def test_phase162_r4_b_removed_isomorphism_cannot_be_reconstructed():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    root = presentation.root_step
    facts = extract_suspension_transport_facts(root)
    assert facts is not None
    # A copied dependency tree with the isomorphism removed must not
    # be misinterpreted as a complete proof.
    removed = replace(
        facts.transported_group_step,
        premises=(facts.source_group_step,),
    )
    assert extract_suspension_transport_facts(removed) is None
