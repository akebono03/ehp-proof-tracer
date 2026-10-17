"""Runner must point at this ZIP's installed folder."""
from pathlib import Path


def test_runner_targets_current_package_and_tests():
    root = Path(__file__).resolve().parents[1]
    text = (root / 'run.ps1').read_text(encoding='utf-8')
    assert "$package = Join-Path $project 'phase165_r12_r23_self_contained_fix'" in text
    for name in ('test_phase165_r12_r23_public_narrative.py', 'test_phase165_r12_r23_path_fix.py', 'test_phase165_r12_r23_runner_fix.py'):
        assert (root / 'tests' / name).is_file()


def test_audit_writes_output_without_prior_script():
    root = Path(__file__).resolve().parents[1]
    text = (root / 'audit.py').read_text(encoding='utf-8')
    assert 'build_verified_pi43_narrative()' in text
    assert "public_narrative.md" in text
