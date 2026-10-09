"""Focused R3-K tests: replay evidence is never promoted to a proof reason."""
from dataclasses import replace

import pytest

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3g_existing_reason_bridge import build_phase162_r3g_existing_reason_trace
from phase162_r3j_inference_rule_audit import build_phase162_r3j_inference_rule_audit
from phase162_r3k_rule_meaning_audit import (
    build_phase162_r3k_rule_meaning_audit,
    compose_r3k_explanation_draft,
    render_phase162_r3k_rule_meaning_markdown,
)


@pytest.fixture(scope='module')
def presentation():
    return build_r3b_presentation()[1]


@pytest.fixture(scope='module')
def audit(presentation):
    return build_phase162_r3k_rule_meaning_audit(presentation)


def test_r3k_preserves_exact_r3j_scope(presentation, audit):
    previous, _ = build_phase162_r3j_inference_rule_audit(presentation)
    entries, groups, report = audit
    assert [e.index for e in entries] == [e.index for e in previous]
    assert sum(group['count'] for group in groups) == len(entries)
    assert len(entries) == report['target_count']


def test_r3k_does_not_promote_description_to_certified_reason(audit):
    entries, _, report = audit
    assert all(e.prose_status == 'RULE_DESCRIPTION_ONLY_NOT_A_PROOF_REASON' for e in entries)
    assert report['new_certified_reason_count'] == 0
    assert report['unexplained_status_preserved']
    assert not report['full_proof_semantic_certification']


def test_r3k_drafts_preserve_real_premise_labels_and_conclusion(presentation, audit):
    entries, _, _ = audit
    by_index = {r.index: r for r in build_phase162_r3g_existing_reason_trace(presentation).records}
    for entry in entries:
        record = by_index[entry.index]
        assert record.mathematical_fact in entry.explanation_draft
        assert entry.description in entry.explanation_draft
        for index in entry.premise_indices:
            assert '[S' + str(index).zfill(3) + ']' in entry.explanation_draft


def test_r3k_detects_changed_premise_indices(presentation):
    previous, _ = build_phase162_r3j_inference_rule_audit(presentation)
    first = previous[0]
    by_index = {r.index: r for r in build_phase162_r3g_existing_reason_trace(presentation).records}
    record = by_index[first.index]
    altered = replace(first, premise_indices=(9999,))
    with pytest.raises(ValueError, match='Premise indices'):
        compose_r3k_explanation_draft(record, altered, by_index)


def test_r3k_detects_non_verified_replay(presentation):
    previous, _ = build_phase162_r3j_inference_rule_audit(presentation)
    by_index = {r.index: r for r in build_phase162_r3g_existing_reason_trace(presentation).records}
    first = previous[0]
    with pytest.raises(ValueError, match='replay-verified'):
        compose_r3k_explanation_draft(
            by_index[first.index], replace(first, classification='RULE_CONCLUSION_MISMATCH'), by_index
        )


def test_r3k_grouping_and_proof_order(presentation, audit):
    entries, groups, report = audit
    assert len(groups) == report['structural_group_count']
    assert report['all_nodes_once']
    assert report['dependency_first']
    assert report['root_is_last']
    assert all(all(p < entry.index for p in entry.premise_indices) for entry in entries)


def test_r3k_markdown_explicitly_disclaims_certification(audit):
    text = render_phase162_r3k_rule_meaning_markdown(audit[0])
    assert '証明本文ではありません' in text
    assert 'PROSE_NOT_CERTIFIED' in text
    assert '規則の登録説明' in text


def test_r3k_rejects_invalid_input():
    with pytest.raises(TypeError, match='TodaGroupProofPresentation'):
        build_phase162_r3k_rule_meaning_audit(None)
    with pytest.raises(TypeError, match='entries'):
        render_phase162_r3k_rule_meaning_markdown(None)
