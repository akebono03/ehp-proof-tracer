"""Phase 162 R3-I focused tests; do not run the full repository suite."""
from types import SimpleNamespace

import pytest

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3g_existing_reason_bridge import build_phase162_r3g_existing_reason_trace
from phase162_r3h_reason_inventory import build_phase162_r3h_inventory
from phase162_r3i_semantic_sidecar_audit import (
    build_phase162_r3i_sidecar_audit,
    classify_r3i_sidecar_entry,
)
from toda_group_proof_narrative_reasons import TodaGroupProofNarrativeReasonKind


@pytest.fixture(scope='module')
def presentation():
    return build_r3b_presentation()[1]


@pytest.fixture(scope='module')
def audit(presentation):
    return build_phase162_r3i_sidecar_audit(presentation)


def test_phase162_r3i_covers_every_r3h_unexplained_step(presentation, audit):
    inventory, prior = build_phase162_r3h_inventory(presentation)
    entries, report = audit
    assert [item.index for item in entries] == [item.index for item in inventory]
    assert len(entries) == prior['unexplained_count']
    assert sum(report['r3i_category_counts'].values()) == len(entries)


def test_phase162_r3i_keeps_baseline_status_and_graph(presentation, audit):
    entries, report = audit
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    assert report['node_count'] == len(presentation.nodes)
    assert report['edge_count'] == len(presentation.edges)
    assert report['prior_explained_count'] == sum(r.reason_status == 'EXPLAINED' for r in baseline.records)
    assert report['unexplained_status_preserved']
    assert all(r.reason_status == 'UNEXPLAINED' for r in baseline.records if r.index in {e.index for e in entries})


def test_phase162_r3i_result_label_is_not_a_verified_reason(presentation):
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    record = next(r for r in baseline.records if r.reason_status == 'UNEXPLAINED')
    prior = SimpleNamespace(index=record.index, category='GENERIC_RESULT_LABEL_ONLY',
                            statement_type=type(record.step.conclusion).__name__, inference_rule=None)
    fake = SimpleNamespace(conclusion_step=record.step,
                           kind=TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION)
    entry = classify_r3i_sidecar_entry(prior, record, (fake,), ())
    assert entry.category == 'GENERIC_RESULT_LABEL_ONLY'
    assert entry.direct_premise_reason_kinds == ()


def test_phase162_r3i_requires_same_step_identity(presentation):
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    record = next(r for r in baseline.records if r.reason_status == 'UNEXPLAINED')
    entry = SimpleNamespace(index=record.index, category='NO_DIRECT_MATCH_REVIEW_REQUIRED',
                            statement_type='Relation', inference_rule=None)
    fake = SimpleNamespace(conclusion_step=object(),
                           kind=TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION)
    with pytest.raises(ValueError, match='identical ProofStep'):
        classify_r3i_sidecar_entry(entry, record, (fake,), ())


def test_phase162_r3i_preserves_unmatched_semantic_hints(presentation):
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    record = next(r for r in baseline.records if r.reason_status == 'UNEXPLAINED')
    prior = SimpleNamespace(index=record.index, category='NO_DIRECT_MATCH_REVIEW_REQUIRED',
                            statement_type='Relation', inference_rule=None)
    entry = classify_r3i_sidecar_entry(prior, record, (), ('step:definition_introduction',))
    assert entry.category == 'SEMANTIC_HINT_ONLY'
    assert entry.semantic_hints == ('step:definition_introduction',)


def test_phase162_r3i_does_not_call_public_renderer(presentation, monkeypatch):
    import toda_group_proof_narrative_renderer

    def forbidden(_):
        raise AssertionError('Public narrative renderer must not be used')

    monkeypatch.setattr(toda_group_proof_narrative_renderer,
                        'render_toda_group_proof_narrative_markdown', forbidden)
    _, report = build_phase162_r3i_sidecar_audit(presentation)
    assert report['historical_markdown_used_as_input'] is False


def test_phase162_r3i_rejects_bad_input():
    with pytest.raises(TypeError, match='TodaGroupProofPresentation'):
        build_phase162_r3i_sidecar_audit(None)
