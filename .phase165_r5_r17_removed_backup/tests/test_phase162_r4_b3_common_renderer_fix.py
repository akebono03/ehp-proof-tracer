import pytest

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_stable_eta_proof_replay import build_toda_stable_eta_proof_replay
from toda_group_proof_narrative_renderer import _phase158_baseline_render_toda_group_proof_narrative_markdown
from toda_group_proof_narrative_concrete_transport import render_concrete_transport_proof_from_steps


@pytest.mark.parametrize("n,exponent", [(4, "E"), (5, "E^{2}")])
def test_phase162_r4_b3_derived_replay_uses_concrete_proof_steps(n, exponent):
    original = _method_evidence_data(n, 1)[0].source_replay.group_result
    base = _method_evidence_data(3, 1)[0].source_replay.group_result
    integrated = build_toda_stable_eta_proof_replay(original, base, max_depth=3)
    result = _phase158_baseline_render_toda_group_proof_narrative_markdown(integrated.presentation)
    body = result.split("## 証明\n", 1)[1]
    assert "**[R1] (4.5).**" in result
    assert exponent + ":" in body
    assert "\\eta_{n}" not in body
    assert "\\pi_{n + 1}^{n}" not in body
    assert "証明木に記録された群構造の移送について" not in body
    assert "これより, これより" not in body
    assert body.count(r"$\square$") == 1


def test_phase162_r4_b3_previous_root_keeps_existing_common_renderer():
    presentation = _method_evidence_data(4, 1)[0]
    assert render_concrete_transport_proof_from_steps(presentation.root_step) is None
    assert "## 証明" in _phase158_baseline_render_toda_group_proof_narrative_markdown(presentation)


def test_phase162_r4_b3_missing_evidence_does_not_render():
    original = _method_evidence_data(5, 1)[0].source_replay.group_result
    base = _method_evidence_data(3, 1)[0].source_replay.group_result
    root = build_toda_stable_eta_proof_replay(original, base, max_depth=3).presentation.root_step
    from dataclasses import replace
    missing = replace(root, premises=root.premises[:2])
    assert render_concrete_transport_proof_from_steps(missing) is None
