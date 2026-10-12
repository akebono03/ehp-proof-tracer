"""R5-R1: pi_5^3 uses the same group proof presentation and renderer as other groups."""
from pathlib import Path

import pytest

from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof
from proof import ProofRule
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def proof():
    return build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_group_root_still_derived_from_registry_isomorphism(proof):
    replay, _ = proof
    assert replay.source_entry.phase == "164 R5"
    assert replay.root_step.rule is ProofRule.INFERENCE
    assert len(replay.root_step.premises) == 3
    assert replay.root_step.premises[1].rule is ProofRule.INFERENCE


def test_exact_common_renderer_output_without_pi53_appended_text(proof):
    replay, markdown = proof
    expected = render_toda_group_proof_narrative_markdown(
        build_toda_group_proof_presentation(replay)
    )
    assert markdown == expected
    assert "既存の (5.2) に基づく" not in markdown
    assert "生成元の Suspension（懸垂）に関する内部導出を用いる" not in markdown


def test_web_narrative_uses_shared_presentation(proof):
    view = build_standard_web_group_proof_view(3, 2, max_depth=2, mode="narrative")
    assert view.phase == "164 R5"
    assert view.mode == "narrative"
    assert view.rendered_lines
    assert view.conclusion_latex


def test_web_trace_and_other_group_unaffected():
    view = build_standard_web_group_proof_view(3, 2, max_depth=0, mode="trace")
    assert view.mode == "trace"
    assert view.phase != "164 R5"


def test_invalid_depth_rejected():
    with pytest.raises((TypeError, ValueError)):
        build_phase164_r5_web_pi5_3_proof(max_depth=-1)
