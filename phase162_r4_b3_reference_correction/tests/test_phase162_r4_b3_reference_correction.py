"""Verify that the R4-B3 dedicated renderer is no longer used by the common entry."""

import inspect

import pytest

from toda_group_proof_narrative_renderer import (
    _phase158_baseline_render_toda_group_proof_narrative_markdown,
)
from toda_stable_eta_proof_replay import build_toda_stable_eta_proof_replay
from tests.test_phase143_19_method_evidence import _method_evidence_data


def test_phase162_r4_b3_common_entry_does_not_call_dedicated_renderer():
    source = inspect.getsource(_phase158_baseline_render_toda_group_proof_narrative_markdown)
    assert 'render_concrete_transport_proof_from_steps' not in source
    assert 'build_toda_group_proof_narrative_semantic_closure_presentation' in source
    assert 'render_toda_group_proof_narrative_multi_argument_with_contributions_markdown' in source


@pytest.mark.parametrize('n', [4, 5])
def test_phase162_r4_b3_derived_proof_uses_common_entry_without_fixed_reference_prose(n):
    target = _method_evidence_data(n, 1)[0].source_replay.group_result
    base = _method_evidence_data(3, 1)[0].source_replay.group_result
    presentation = build_toda_stable_eta_proof_replay(target, base, max_depth=3).presentation
    markdown = _phase158_baseline_render_toda_group_proof_narrative_markdown(presentation)
    assert '# Group proof narrative' in markdown
    assert 'Toda (4.5) の安定範囲における懸垂同型.' not in markdown
    assert '基準群の証明より' not in markdown
