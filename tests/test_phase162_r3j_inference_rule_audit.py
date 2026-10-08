"""Phase 162 R3-J focused tests only; never run the full suite here."""
from dataclasses import replace
from types import SimpleNamespace

import pytest

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3g_existing_reason_bridge import build_phase162_r3g_existing_reason_trace
from phase162_r3i_semantic_sidecar_audit import build_phase162_r3i_sidecar_audit
from phase162_r3j_inference_rule_audit import (
    build_phase162_r3j_inference_rule_audit,
    classify_r3j_inference_rule,
)


@pytest.fixture(scope='module')
def presentation():
    return build_r3b_presentation()[1]


@pytest.fixture(scope='module')
def audit(presentation):
    return build_phase162_r3j_inference_rule_audit(presentation)


def test_phase162_r3j_covers_only_r3i_no_sidecar_steps(presentation, audit):
    r3i, _ = build_phase162_r3i_sidecar_audit(presentation)
    entries, report = audit
    expected = [e.index for e in r3i if e.category == 'NO_SIDECAR_REASON_OR_HINT']
    assert [e.index for e in entries] == expected
    assert report['target_no_sidecar_count'] == len(expected)
    assert sum(report['classification_counts'].values()) == len(expected)


def test_phase162_r3j_preserves_proof_graph(presentation, audit):
    entries, report = audit
    assert report['node_count'] == len(presentation.nodes)
    assert report['edge_count'] == len(presentation.edges)
    assert report['all_nodes_once']
    assert report['dependency_first']
    assert report['root_is_last']
    assert len({e.index for e in entries}) == len(entries)


def test_phase162_r3j_replayed_rule_is_not_counted_as_prose(presentation, audit):
    entries, report = audit
    assert report['inference_explanations_added'] == 0
    assert report['unexplained_status_preserved']
    assert not report['full_proof_semantic_certification']
    assert all(e.classification != 'EXPLAINED' for e in entries)


def test_phase162_r3j_detects_tampered_conclusion(presentation):
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    r3i, _ = build_phase162_r3i_sidecar_audit(presentation)
    target_index = next(e.index for e in r3i if e.category == 'NO_SIDECAR_REASON_OR_HINT')
    record = next(r for r in baseline.records if r.index == target_index)
    wrong = replace(record.step, conclusion=object())
    changed = replace(record, step=wrong)
    result = classify_r3j_inference_rule(changed)
    assert result.classification in ('RULE_CONCLUSION_MISMATCH', 'RULE_NO_EXACT_PREMISE_MATCH', 'RULE_REPLAY_ERROR_REVIEW')
    assert result.matching_conclusion_count == 0


def test_phase162_r3j_requires_inference_step(presentation):
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    given = next(r for r in baseline.records if r.reason_status == 'GIVEN')
    with pytest.raises(TypeError, match='INFERENCE'):
        classify_r3j_inference_rule(given)


def test_phase162_r3j_rejects_bad_presentation():
    with pytest.raises(TypeError, match='TodaGroupProofPresentation'):
        build_phase162_r3j_inference_rule_audit(None)


def test_phase162_r3j_does_not_use_public_renderer(presentation, monkeypatch):
    import toda_group_proof_narrative_renderer

    def forbidden(_presentation):
        raise AssertionError('Public Renderer should not run in R3-J')

    monkeypatch.setattr(
        toda_group_proof_narrative_renderer,
        'render_toda_group_proof_narrative_markdown',
        forbidden,
    )
    _, report = build_phase162_r3j_inference_rule_audit(presentation)
    assert report['historical_markdown_used_as_input'] is False
