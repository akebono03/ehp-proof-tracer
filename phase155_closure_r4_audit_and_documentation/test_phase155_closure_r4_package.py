from pathlib import Path
import ast

def test_all_python_scripts_parse():
    root = Path(__file__).parent
    for name in (
        "run_phase155_closure_r4_audits.py",
        "update_phase155_closure_docs.py",
        "verify_phase155_closure_docs.py",
    ):
        ast.parse((root / name).read_text(encoding="utf-8"))

def test_readme_documents_phase156_boundary():
    text = (Path(__file__).parent / "README.txt").read_text(encoding="utf-8")
    assert "Phase156" in text
    assert "Reference statement relevance / minimal display" in text

def test_no_monolithic_runner_is_requested():
    text = (Path(__file__).parent / "run_phase155_closure_r4.ps1").read_text(encoding="utf-8")
    assert "python -m pytest tests -q" not in text
    assert "run_phase155_closure_r4_audits.py" in text
