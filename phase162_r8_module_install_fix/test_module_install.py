"""Regression: the production Web module is importable from the repository root."""
from pathlib import Path

from proof import ProofRule
from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from web_group_proof import build_standard_web_group_proof_view


def test_r8_module_resolves_from_repository_root():
    import phase162_pi5_3_web_replay

    repo = Path(__file__).resolve().parent.parent
    assert Path(phase162_pi5_3_web_replay.__file__).resolve() == (
        repo / "phase162_pi5_3_web_replay.py"
    ).resolve()


def test_r8_reconstructed_web_narrative_is_single():
    view = build_standard_web_group_proof_view(3, 2, mode="narrative")
    assert view.phase == "162"
    assert view.max_depth >= 40
    headings = [item.prefix for item in view.rendered_lines if item.kind == "heading"]
    assert headings.count("証明") == 1
    assert "群構造の検証済み証明" not in headings


def test_r8_reconstructed_root_is_inferred():
    replay = build_phase162_pi5_3_web_replay()
    assert replay.root_step.rule is ProofRule.INFERENCE
    assert len(replay.root_step.premises) == 3


def test_r8_unrelated_web_route_remains_unchanged():
    view = build_standard_web_group_proof_view(3, 1, mode="narrative")
    assert view.phase != "162"
