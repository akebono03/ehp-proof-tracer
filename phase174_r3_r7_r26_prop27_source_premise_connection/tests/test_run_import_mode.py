from pathlib import Path

RUN_SCRIPT = Path(__file__).resolve().parents[1] / "run.ps1"

def test_focused_pytest_uses_importlib_mode():
    content = RUN_SCRIPT.read_text(encoding="utf-8-sig")
    assert "& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider" in content

def test_both_conflicting_test_audit_modules_remain_selected():
    content = RUN_SCRIPT.read_text(encoding="utf-8-sig")
    assert "phase174_r3_r7_r24_prop27_general_typed_design/tests/test_audit.py" in content
    assert "phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_audit.py" in content

def test_source_guard_still_precedes_pytest():
    content = RUN_SCRIPT.read_text(encoding="utf-8-sig")
    assert content.index("phase174_r3_r7_r26_prop27_source_premise_connection.audit --dry-run") < content.index("& python -B -m pytest")
    assert "if ($LASTEXITCODE -ne 0) { throw 'R26 Source Guard failed' }" in content

def test_full_suite_not_invoked():
    content = RUN_SCRIPT.read_text(encoding="utf-8-sig")
    assert "-p no:cacheprovider" in content
    assert "tests/test_phase50_prop27_theorem_semantics.py" in content
