"""Focused tests for the R3-41I pytest import-collection repair package."""
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]

def test_full_runner_keeps_focused_test_targets():
    runner = (PACKAGE / "full_files" / "phase168_r3_41i_renderer_closure_audit" / "run.ps1").read_text(encoding="utf-8")
    assert "python -m pytest -q --import-mode=importlib `" in runner
    assert runner.count("phase168_r3_41i_renderer_closure_audit\\tests\\test_audit.py") == 1
    assert runner.count("phase168_r3_39f_frozen_comparison\\tests\\test_audit.py") == 1
    assert runner.count("phase168_r3_19_web_model_default\\tests\\test_phase168_r3_19_web_model_default.py") == 1
    assert "python -m phase168_r3_41i_renderer_closure_audit.audit" in runner


def test_fix_package_preserves_rollback_and_read_only_checks():
    fixer = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "[System.IO.File]::WriteAllBytes($Target, $OriginalBytes)" in fixer
    assert "Read-only verification failed:" in fixer
    assert "phase168_narrative_baseline_frozen\\pi5_4_original.txt" in fixer
    assert "review_bundle.zip" in fixer
    assert "Repository-wide pytest: NOT RUN" in fixer


def test_replacement_changes_only_one_pytest_command():
    full = (PACKAGE / "full_files" / "phase168_r3_41i_renderer_closure_audit" / "run.ps1").read_text(encoding="utf-8")
    old = full.replace("python -m pytest -q --import-mode=importlib `", "python -m pytest -q `")
    assert old != full
    assert old.replace("python -m pytest -q `", "python -m pytest -q --import-mode=importlib `") == full
    assert "R3-41I read-only frozen quality audit complete. Full pytest NOT run." in full
