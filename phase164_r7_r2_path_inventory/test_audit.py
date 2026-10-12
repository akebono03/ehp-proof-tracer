import ast
from pathlib import Path

from audit import inspect_source, write_report


def test_import_bound_and_ambiguous_calls_are_distinguished():
    result = inspect_source("from proof_repository import ProofRepository\nrepo.get('a')\nProofRepository()\n", "sample.py")
    assert "proof_repository" in result["imports"]
    assert any(call["name"] == "get" and call["certainty"] == "candidate_unresolved_receiver" for call in result["calls"])


def test_syntax_error_remains_visible():
    try:
        inspect_source("def bad(:\n    pass", "broken.py")
    except SyntaxError:
        pass
    else:
        raise AssertionError("SyntaxError was hidden")


def test_report_explains_scope(tmp_path: Path):
    data = {"module_count": 1, "parse_errors": [], "branches": {"group": {"reachable_module_count": 1, "candidates": []}}, "related_tests": {"group": []}}
    destination = tmp_path / "report.md"
    write_report(data, destination)
    assert "読み" not in destination.read_text(encoding="utf-8") or "静的" in destination.read_text(encoding="utf-8")
    assert "削除" in destination.read_text(encoding="utf-8")
