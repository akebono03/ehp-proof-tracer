from pathlib import Path
import ast

def test_runner_parses():
    ast.parse(
        (Path(__file__).parent / "run_phase155_closure_r4_r1_audits.py")
        .read_text(encoding="utf-8")
    )

def test_explicit_bypass_is_present():
    text = (
        Path(__file__).parent / "run_phase155_closure_r4_r1_audits.py"
    ).read_text(encoding="utf-8")
    assert '"PYTEST_ADDOPTS"' in text
    assert '"--noconftest"' in text
    assert '"addopts="' in text

def test_exact_five_remain_fixed():
    text = (
        Path(__file__).parent / "run_phase155_closure_r4_r1_audits.py"
    ).read_text(encoding="utf-8")
    assert "EXPECTED_AUDIT_NODEIDS" in text
    assert "range(\n      1,\n      6," in text
