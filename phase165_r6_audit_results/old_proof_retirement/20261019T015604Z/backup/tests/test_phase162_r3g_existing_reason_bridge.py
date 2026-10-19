"""Focused tests for reusing existing typed exactness reasons on R3-F trace."""

import pytest

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3f_recursive_renderer import render_phase162_r3f_recursive_markdown
from phase162_r3g_existing_reason_bridge import (
    _existing_exactness_reason,
    build_phase162_r3g_existing_reason_trace,
)
from proof import ProofRule


@pytest.fixture(scope='module')
def presentation():
    return build_r3b_presentation()[1]


@pytest.fixture(scope='module')
def result(presentation):
    return build_phase162_r3g_existing_reason_trace(presentation)


def test_phase162_r3g_preserves_all_proofstep_identities_and_edges(presentation, result):
    base = render_phase162_r3f_recursive_markdown(presentation)
    assert len(result.records) == len(base.records) == len(presentation.nodes)
    assert result.checked_edge_count == base.checked_edge_count == len(presentation.edges)
    assert all(a.step is b.step and a.premise_indices == b.premise_indices
               for a, b in zip(result.records, base.records))


def test_phase162_r3g_reuses_existing_exactness_without_losing_root(presentation, result):
    assert result.records[-1].step is presentation.root_step
    assert result.records[-1].reason_status == 'EXPLAINED'
    assert sum(record.reason_status == 'EXPLAINED' for record in result.records) >= 1
    assert result.reason_kind_by_index[-1][1] == 'ROOT_GROUP_STRUCTURE_TRANSPORT'


def test_phase162_r3g_all_extra_explanations_use_real_direct_premises(result):
    for record in result.records:
        reason = _existing_exactness_reason(record.step)
        if reason is None:
            continue
        assert reason.conclusion_step is record.step
        assert all(any(premise is actual for actual in record.step.premises)
                   for premise in reason.premise_steps)
        assert len(reason.premise_steps) == 2


def test_phase162_r3g_does_not_claim_all_inferences_are_explained(result):
    assert sum(record.reason_status == 'UNEXPLAINED' for record in result.records) > 0
    assert '推論理由: 未対応' in result.markdown
    assert all(record.reason_status == 'GIVEN' for record in result.records
               if record.step.rule is ProofRule.GIVEN)


def test_phase162_r3g_never_uses_public_markdown(presentation, monkeypatch):
    import toda_group_proof_narrative_renderer

    def forbidden(_):
        raise AssertionError('Public Markdown must not be read')

    monkeypatch.setattr(
        toda_group_proof_narrative_renderer,
        'render_toda_group_proof_narrative_markdown',
        forbidden,
    )
    assert build_phase162_r3g_existing_reason_trace(presentation).records


def test_phase162_r3g_rejects_non_presentation():
    with pytest.raises(TypeError, match='TodaGroupProofPresentation'):
        build_phase162_r3g_existing_reason_trace(None)
