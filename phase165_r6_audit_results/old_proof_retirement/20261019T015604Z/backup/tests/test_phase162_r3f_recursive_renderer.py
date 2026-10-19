"""Lightweight focused checks for dependency-first recursive proof trace."""

from dataclasses import replace

import pytest

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3f_recursive_renderer import (
    build_phase162_r3f_recursive_records,
    render_phase162_r3f_recursive_markdown,
)


@pytest.fixture(scope='module')
def presentation():
    return build_r3b_presentation()[1]


@pytest.fixture(scope='module')
def result(presentation):
    return render_phase162_r3f_recursive_markdown(presentation)


def test_phase162_r3f_visits_each_node_once_and_keeps_all_edges(presentation, result):
    assert len(result.records) == len(presentation.nodes)
    assert result.checked_edge_count == len(presentation.edges)
    assert len({id(record.step) for record in result.records}) == len(result.records)
    assert result.records[-1].step is presentation.root_step


def test_phase162_r3f_premises_precede_dependents(result):
    assert all(
        premise_index < record.index
        for record in result.records
        for premise_index in record.premise_indices
    )
    assert sum(len(record.premise_indices) for record in result.records) == result.checked_edge_count


def test_phase162_r3f_unexplained_inferences_are_explicit(result):
    assert sum(r.reason_status == 'EXPLAINED' for r in result.records) == 1
    assert sum(r.reason_status == 'UNEXPLAINED' for r in result.records) > 0
    assert '推論理由: 未対応' in result.markdown
    assert result.records[-1].reason_status == 'EXPLAINED'


def test_phase162_r3f_does_not_use_legacy_markdown(presentation, monkeypatch):
    import toda_group_proof_narrative_renderer as old

    def prohibited(_presentation):
        raise AssertionError('Legacy Markdown unexpectedly called')

    monkeypatch.setattr(old, 'render_toda_group_proof_narrative_markdown', prohibited)
    assert render_phase162_r3f_recursive_markdown(presentation).records


def test_phase162_r3f_detects_missing_edge(presentation):
    removed = next(e for e in presentation.edges if e.parent_step is presentation.root_step)
    broken = replace(presentation, edges=tuple(e for e in presentation.edges if e is not removed))
    with pytest.raises(ValueError, match='dependency edges differ'):
        build_phase162_r3f_recursive_records(broken)


def test_phase162_r3f_rejects_nonpresentation():
    with pytest.raises(TypeError, match='TodaGroupProofPresentation'):
        build_phase162_r3f_recursive_records(None)
