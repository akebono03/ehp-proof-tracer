from dataclasses import replace

from tests.test_phase143_19_method_evidence import (
    _method_evidence_data,
)
from toda_group_proof_narrative_transport_facts import (
    extract_suspension_transport_facts,
)


def test_phase162_r4_b_pi5_4_extracts_tree_backed_transport():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    facts = extract_suspension_transport_facts(presentation.root_step)
    assert facts is not None
    assert facts.target_step is presentation.root_step
    assert facts.isomorphism_step in facts.transported_group_step.premises
    assert facts.source_group_step in facts.transported_group_step.premises
    family_step = next(
        step
        for step in presentation.root_step.premises
        if facts.transported_group_step in step.premises
    )
    assert facts.generator_bridge_step in family_step.premises
    assert facts.generator_bridge_step.conclusion.rhs == (
        family_step.conclusion.rhs.generator
    )


def test_phase162_r4_b_removed_isomorphism_cannot_be_reconstructed():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    facts = extract_suspension_transport_facts(presentation.root_step)
    assert facts is not None
    removed = replace(
        facts.transported_group_step,
        premises=(facts.source_group_step,),
    )
    # An isolated modified subtree must not produce a transport witness.
    assert extract_suspension_transport_facts(removed) is None


def test_phase162_r4_b_unconnected_generator_bridge_fails_closed():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    root = presentation.root_step
    facts = extract_suspension_transport_facts(root)
    assert facts is not None
    family = root.premises[0]
    detached_family = replace(
        family,
        premises=(facts.transported_group_step,),
    )
    detached_root = replace(root, premises=(detached_family,))
    assert extract_suspension_transport_facts(detached_root) is None
