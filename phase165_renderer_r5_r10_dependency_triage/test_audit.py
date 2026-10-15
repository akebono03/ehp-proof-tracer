"""Focused tests for R5-R10 ownership attribution; no application code changed."""
from pathlib import Path
import ast
from audit import TARGETS, imported_usage, owner, analyze


def test_r10_owner_separates_app_audit_tests(tmp_path):
    (tmp_path / "tests").mkdir()
    assert owner(tmp_path / "phase162_pi5_3_web_replay.py", tmp_path) == "application"
    assert owner(tmp_path / "audit_phase144.py", tmp_path) == "audit"
    assert owner(tmp_path / "tests" / "test_case.py", tmp_path) == "test"


def test_r10_imported_symbol_alias_records_real_target():
    tree = ast.parse("from phase162_web_narrative_integration import _phase162_ehp_leaves as leaves\nleaves()\n")
    refs = imported_usage(tree,TARGETS)
    assert any(r["symbol"] == "_phase162_ehp_leaves" and r["kind"] == "call" for r in refs)


def test_r10_module_alias_is_recognized():
    tree = ast.parse("import phase162_r3_narrative_connection as old\nold.render_phase162_r3_narrative(None)\n")
    refs = imported_usage(tree,TARGETS)
    assert any(r["symbol"] == "render_phase162_r3_narrative" and r["kind"] == "call" for r in refs)


def test_r10_unrelated_functions_not_misattributed():
    tree = ast.parse("from math import sqrt\nsqrt(4)\n")
    assert imported_usage(tree,TARGETS) == []


def test_r10_fixture_declares_application_dependency(tmp_path):
    root=tmp_path
    for module in TARGETS:
        (root/(module+".py")).write_text("def example():\n    return 1\n",encoding="utf-8")
    (root / "phase162_pi5_3_web_replay.py").write_text(
        "from phase162_web_narrative_integration import _phase162_ehp_leaves\n"
        "_phase162_ehp_leaves()\n",encoding="utf-8")
    result=analyze(root)
    assert result["checks"]["shared_leaf_dependency_retained"]
    assert result["status"] == "REVIEW_REQUIRED"


def test_r10_bom_is_accepted(tmp_path):
    for module in TARGETS:
        (tmp_path/(module+".py")).write_bytes(b"\xef\xbb\xbfdef example():\n    return 1\n")
    (tmp_path / "phase162_pi5_3_web_replay.py").write_text(
        "from phase162_web_narrative_integration import _phase162_ehp_leaves\n",encoding="utf-8")
    result=analyze(tmp_path)
    assert result["checks"]["no_ast_errors"]


def test_r10_removal_requires_no_application_ref(tmp_path):
    for module in TARGETS:
        (tmp_path/(module+".py")).write_text("pass\n",encoding="utf-8")
    (tmp_path / "phase162_pi5_3_web_replay.py").write_text(
        "from phase162_web_narrative_integration import _phase162_ehp_leaves\n",encoding="utf-8")
    result=analyze(tmp_path)
    assert result["targets"]["phase162_web_narrative_integration"]["disposition"] == "RETAIN_UNTIL_APPLICATION_DEPENDENCIES_MIGRATED"
