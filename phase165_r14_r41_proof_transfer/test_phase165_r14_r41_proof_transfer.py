"""R41 targeted tests against real R38/R40 proof reconstruction."""
from phase165_r14_r41_proof_transfer import (
    _registered_reference_leaves,
    audit_r41,
    build_phase165_r41_pi32_common_replay,
)
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def _result():
    report = build_standard_toda_report(n=2, k=1)
    assert len(report.candidates) == 1
    return report.candidates[0].source_candidate.group_result


def test_full_ancestry_retains_nine_reference_leaves():
    replay = build_phase165_r41_pi32_common_replay(_result(), 2, "narrative")
    assert len(_registered_reference_leaves(replay.root_step)) == 9


def test_narrative_depth_expands_past_user_depth_when_needed():
    result = _result()
    trace = build_phase165_r41_pi32_common_replay(result, 2, "trace")
    narrative = build_phase165_r41_pi32_common_replay(result, 2, "narrative")
    assert len(narrative.steps) >= len(trace.steps)
    assert narrative.max_depth >= trace.max_depth
    assert trace.max_depth == 2


def test_same_proof_goal_and_real_common_presentation():
    replay = build_phase165_r41_pi32_common_replay(_result(), 2, "narrative")
    presentation = build_toda_group_proof_presentation(replay)
    assert presentation.root_step is replay.root_step
    assert presentation.edges


def test_common_renderer_handles_complete_replay():
    replay = build_phase165_r41_pi32_common_replay(_result(), 2, "narrative")
    text = render_toda_group_proof_narrative_markdown(
        build_toda_group_proof_presentation(replay))
    assert isinstance(text, str) and text.strip()


def test_transfer_audit_has_no_false_reference_display_claim():
    report = audit_r41(_result())
    assert report["full_registered_leaf_count"] == 9
    assert report["root_equal"]
    assert not report["reference_text_rendering_fixed"]
    assert not report["full_pytest_run"]
