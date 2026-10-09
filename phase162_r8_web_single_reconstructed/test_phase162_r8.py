from proof import ProofRule
from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from web_group_proof import build_standard_web_group_proof_view


def test_phase162_r8_web_replay_has_reconstructed_root():
    replay = build_phase162_pi5_3_web_replay()
    assert replay.root_step.rule is ProofRule.INFERENCE
    assert replay.source_entry.phase == "162"
    assert len(replay.steps) > 10
    assert replay.root_step.premises[1].rule is ProofRule.INFERENCE


def test_phase162_r8_web_shows_only_one_narrative():
    view = build_standard_web_group_proof_view(3, 2, mode="narrative")
    assert view.phase == "162"
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("証明") == 1
    assert "群構造の検証済み証明" not in headings
    assert view.max_depth >= 40


def test_phase162_r8_other_group_keeps_original_route():
    view = build_standard_web_group_proof_view(3, 1, mode="narrative")
    assert view.phase != "162"


def test_phase162_r8_trace_keeps_original_route():
    view = build_standard_web_group_proof_view(3, 2, mode="trace")
    assert view.phase != "162"
