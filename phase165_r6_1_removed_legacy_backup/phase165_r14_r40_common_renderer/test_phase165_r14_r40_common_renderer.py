"""Tests use real common replay and common narrative, not R39 text."""
from pathlib import Path

from phase165_r14_r38_direct_registry import reconstruct_registered_pi32
from phase164_r5_r2_common_replay import build_phase164_r5_r2_common_replay
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from web_group_proof import build_standard_web_group_proof_view


def _group_result():
    report = build_standard_toda_report(n=2, k=1)
    assert len(report.candidates) == 1
    return report.candidates[0].source_candidate.group_result


def test_common_replay_root_is_r38_registered_proof():
    result = _group_result()
    replay = build_phase164_r5_r2_common_replay(2, 1, result, 2, "narrative")
    _, r38_root = reconstruct_registered_pi32(Path(__file__).with_name("phase165_r14_r39_toda51.tex"))
    assert replay.root_step.conclusion == r38_root.conclusion
    assert replay.root_step.rule == r38_root.rule
    assert replay.root_step.premises
    assert replay.source_entry.key == "phase165:registered:pi3_2"


def test_common_presentation_builds_for_registered_proof():
    replay = build_phase164_r5_r2_common_replay(2, 1, _group_result(), 2, "narrative")
    presentation = build_toda_group_proof_presentation(replay)
    assert presentation.root_step is replay.root_step
    assert presentation.edges


def test_common_renderer_generates_narrative():
    replay = build_phase164_r5_r2_common_replay(2, 1, _group_result(), 2, "narrative")
    markdown = render_toda_group_proof_narrative_markdown(build_toda_group_proof_presentation(replay))
    assert isinstance(markdown, str) and markdown.strip()
    assert "eta" in markdown or "\\eta" in markdown


def test_web_narrative_uses_common_renderer(monkeypatch):
    import web_group_proof
    real = web_group_proof.render_toda_group_proof_narrative_markdown
    calls = []
    def record(presentation):
        calls.append(presentation)
        return real(presentation)
    monkeypatch.setattr(web_group_proof, "render_toda_group_proof_narrative_markdown", record)
    view = build_standard_web_group_proof_view(2, 1, max_depth=2, mode="narrative")
    assert len(calls) == 1
    assert view.rendered_lines
    assert view.key == "phase165:registered:pi3_2"


def test_web_trace_uses_same_registered_root():
    view = build_standard_web_group_proof_view(2, 1, max_depth=2, mode="trace")
    assert view.key == "phase165:registered:pi3_2"
    assert view.steps
    assert view.rendered_lines == ()
