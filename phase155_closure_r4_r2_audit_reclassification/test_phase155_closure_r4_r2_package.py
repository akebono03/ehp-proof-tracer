from pathlib import Path
import ast

def test_scripts_parse():
    root = Path(__file__).parent
    for name in (
        "apply_phase155_closure_r4_r2.py",
        "run_phase155_closure_r4_r2_audits.py",
        "update_phase155_closure_r4_r2_docs.py",
        "verify_phase155_closure_r4_r2.py",
    ):
        ast.parse((root / name).read_text(encoding="utf-8"))

def test_readme_has_final_boundary():
    text = (Path(__file__).parent / "README.txt").read_text(encoding="utf-8")
    assert "10384 total" in text
    assert "10382 routine" in text
    assert "2 audit-only" in text
    assert "117" in text

def test_no_monolithic_pytest_command():
    text = (Path(__file__).parent / "run_phase155_closure_r4_r2.ps1").read_text(encoding="utf-8")
    assert "python -m pytest tests -q" not in text
