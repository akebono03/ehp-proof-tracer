"""Focused unit tests; no project-wide pytest."""
import ast
from pathlib import Path
from tempfile import TemporaryDirectory

from audit import audit, local_calls, production_files, references_in, review


def test_from_import_call():
    tree = ast.parse("from old import target as t\nt()\n")
    assert {x["kind"] for x in references_in(tree, "old", "target")} == {"import", "call"}


def test_module_import_call():
    tree = ast.parse("import old as obj\nobj.target()\n")
    assert {x["kind"] for x in references_in(tree, "old", "target")} == {"module_import", "call"}


def test_unrelated_symbol_excluded():
    tree = ast.parse("from old import different\ndifferent()\n")
    assert references_in(tree, "old", "target") == []


def test_local_calls():
    tree = ast.parse("def first():\n    target()\n\ndef second():\n    other()\n")
    assert local_calls(tree, "target") == [{"function": "first", "line": 2}]


def test_backup_files_excluded():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "active.py").write_text("pass\n", encoding="utf-8")
        (root / "active.phase165_r48_backup.py").write_text("pass\n", encoding="utf-8")
        selected = [p.name for p, _ in production_files(root)]
        assert selected == ["active.py"]


def test_audit_fail_closed_when_r5_r11_missing():
    with TemporaryDirectory() as tmp:
        result = audit(Path(tmp))
        assert result["status"] == "PRECONDITION_FAILED"
        assert not result["guards"]["r5_r11_shared_file_exists"]


def test_review_contains_decisions():
    with TemporaryDirectory() as tmp:
        result = audit(Path(tmp))
        text = review(result)
        assert "関数別の依存" in text
        assert "PRECONDITION_FAILED" in text
