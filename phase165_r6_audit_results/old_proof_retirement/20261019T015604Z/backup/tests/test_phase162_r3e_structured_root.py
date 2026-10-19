"""Phase 162 R3-E scoped root-only structured renderer tests."""

from dataclasses import replace

import pytest

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3e_structured_root_renderer import (
    render_phase162_r3e_structured_root_markdown,
)
from proof import Relation, RelationType
from toda_group_structure_transport_reason import render_group_structure_transport_reason


@pytest.fixture(scope='module')
def presentation():
    return build_r3b_presentation()[1]


def test_phase162_r3e_uses_actual_root_premises_in_order(presentation):
    root = presentation.root_step
    result = render_phase162_r3e_structured_root_markdown(presentation)
    assert isinstance(result, str)
    assert len(root.premises) == 3
    reason = render_group_structure_transport_reason(root)
    assert result.count(reason) == 1
    assert result.index(r'\xrightarrow{\cong}') < result.index(reason)
    assert result.index(reason) < result.rfind('以上より,')
    assert result.rstrip().endswith('□')


def test_phase162_r3e_no_existing_markdown_marker_needed(presentation, monkeypatch):
    # Proof is composed from root and edges only; no baseline Renderer is called.
    import toda_group_proof_narrative_renderer as legacy

    def forbid_legacy(_):
        raise AssertionError('Legacy Markdown must not be read')

    monkeypatch.setattr(legacy, 'render_toda_group_proof_narrative_markdown', forbid_legacy)
    assert render_phase162_r3e_structured_root_markdown(presentation)


def test_phase162_r3e_rejects_missing_identity_edge(presentation):
    # Use replace to avoid modifying the original frozen presentation.
    root = presentation.root_step
    removed = next(e for e in presentation.edges if e.parent_step is root)
    broken = replace(
        presentation,
        edges=tuple(e for e in presentation.edges if e is not removed),
    )
    with pytest.raises(ValueError, match='edge is absent'):
        render_phase162_r3e_structured_root_markdown(broken)


def test_phase162_r3e_rejects_inconsistent_root_conclusion(presentation):
    root = presentation.root_step
    wrong = Relation(
        lhs=root.premises[1].conclusion.lhs,
        rhs=root.conclusion.rhs,
        relation_type=RelationType.EQUALITY,
    )
    tampered = replace(root, conclusion=wrong)
    # Direct reason validates altered root without reusing any output text.
    with pytest.raises(ValueError, match='conclusion does not follow'):
        render_group_structure_transport_reason(tampered)


def test_phase162_r3e_does_not_claim_recursive_ancestry_is_narrated(presentation):
    assert len(presentation.nodes) > 3
    text = render_phase162_r3e_structured_root_markdown(presentation)
    assert '以下の3つの事実' in text
    assert '123' not in text
