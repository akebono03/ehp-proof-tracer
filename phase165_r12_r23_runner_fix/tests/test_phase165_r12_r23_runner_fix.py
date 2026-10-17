"""Ensure PowerShell executes tests shipped in its own package."""
from pathlib import Path


def test_runner_uses_installed_package_name():
    root = Path(__file__).resolve().parents[1]
    runner = (root / "run.ps1").read_text(encoding="utf-8")
    assert "$package = Join-Path $project 'phase165_r12_r23_runner_fix'" in runner
    for filename in (
        "test_phase165_r12_r23_public_narrative.py",
        "test_phase165_r12_r23_path_fix.py",
    ):
        assert (root / "tests" / filename).is_file()


def test_both_audit_scripts_are_present():
    root = Path(__file__).resolve().parents[2]
    assert (root / "phase165_r12_r22_quotient_closure" / "audit.py").is_file()
    assert (root / "phase165_r12_r23_runner_fix" / "audit.py").is_file()
