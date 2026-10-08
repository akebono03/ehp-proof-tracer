"""Focused tests of R3-C final-reason provenance and public placement."""

from dataclasses import replace
from types import SimpleNamespace

import pytest

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from audit_phase162_r3d_root_reason import _root_premise_contract, audit_root_reason
from proof import Relation, RelationType
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_structure_transport_reason import render_group_structure_transport_reason


@pytest.fixture(scope='module')
def rendered_fixture():
    _, presentation = build_r3b_presentation()
    markdown = render_toda_group_proof_narrative_markdown(presentation)
    return presentation, markdown


def test_phase162_r3d_root_premises_and_edges_are_identical(rendered_fixture):
    presentation, _ = rendered_fixture
    root = presentation.root_step
    assert _root_premise_contract(root, presentation) == root.premises
    assert len(root.premises) == 3


def test_phase162_r3d_reason_once_immediately_before_final_conclusion(rendered_fixture):
    presentation, markdown = rendered_fixture
    report = audit_root_reason(presentation, markdown)
    assert report['reason_occurrences'] == 1
    assert report['reason_adjacent_to_final_conclusion']
    assert report['final_conclusion_matches_root']
    assert not report['full_proof_semantic_certification']


def test_phase162_r3d_rejects_missing_root_reason(rendered_fixture):
    presentation, markdown = rendered_fixture
    reason = render_group_structure_transport_reason(presentation.root_step)
    with pytest.raises(AssertionError, match='Root reasoning occurs'):
        audit_root_reason(presentation, markdown.replace(reason, '', 1))


def test_phase162_r3d_rejects_reason_after_final_conclusion(rendered_fixture):
    presentation, markdown = rendered_fixture
    reason = render_group_structure_transport_reason(presentation.root_step)
    misplaced = markdown.replace(reason, '', 1)
    misplaced = misplaced.replace('□', reason + '\n\n□', 1)
    with pytest.raises(AssertionError, match='immediately upstream'):
        audit_root_reason(presentation, misplaced)


def test_phase162_r3d_rejects_copied_root_identity(rendered_fixture):
    presentation, _ = rendered_fixture
    root = presentation.root_step
    wrong_conclusion = Relation(
        lhs=root.premises[1].conclusion.lhs,
        rhs=root.conclusion.rhs,
        relation_type=RelationType.EQUALITY,
    )
    tampered = replace(root, conclusion=wrong_conclusion)
    with pytest.raises(AssertionError, match='Presentation root identity changed'):
        _root_premise_contract(tampered, presentation)


def test_phase162_r3d_rejects_incorrect_root_conclusion_after_identity_check(rendered_fixture):
    presentation, _ = rendered_fixture
    root = presentation.root_step
    wrong_conclusion = Relation(
        lhs=root.premises[1].conclusion.lhs,
        rhs=root.conclusion.rhs,
        relation_type=RelationType.EQUALITY,
    )
    tampered = replace(root, conclusion=wrong_conclusion)
    # This minimal audit-facing stand-in tests the conclusion guard independently.
    # It is not presented as a valid TodaGroupProofPresentation.
    identity_aligned_view = SimpleNamespace(root_step=tampered, edges=presentation.edges)
    with pytest.raises(AssertionError, match='Root conclusion'):
        _root_premise_contract(tampered, identity_aligned_view)
