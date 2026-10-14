"""Targeted tests for read-only R27-R12 audit; no production tests are run."""
import ast
from pathlib import Path
from audit import SCANNED, PROTECTED, classify, collect, scan_file


def test_scope_and_protection_are_distinct():
    assert "proof_repository.py" in SCANNED
    assert "unified_statement_registry.py" in PROTECTED
    assert classify("tests/test_repository.py") == "TEST_REFERENCE"
    assert classify("standard_production_repository.py") == "ACTIVE_OR_UNCLASSIFIED_REVIEW"


def test_ast_records_constructor_references(tmp_path):
    target = tmp_path / "sample.py"
    target.write_text("from standard_repository import build_standard_proof_repository\n"
                      "def f():\n    return build_standard_proof_repository()\n", encoding="utf-8")
    entries = scan_file(target)["references"]
    assert any(e["kind"] == "import" for e in entries)
    assert any(e["kind"] == "use" for e in entries)


def test_required_sources_missing_fail_closed(tmp_path):
    try:
        collect(tmp_path)
    except FileNotFoundError as error:
        assert "Required source files missing" in str(error)
    else:
        raise AssertionError("missing files must not silently pass")
