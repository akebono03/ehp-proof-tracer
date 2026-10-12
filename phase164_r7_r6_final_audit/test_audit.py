from pathlib import Path

from audit import audit, calls, find_function, parse_file, write_report


def test_ast_call_detection(tmp_path):
    p = tmp_path / "x.py"
    p.write_text("def func():\n    repository.entries()\n    validate_repository_internal_proof_roots(repository)\n", encoding="utf-8")
    fn = find_function(parse_file(tmp_path, "x.py"), "func")
    assert [c["name"] for c in calls(fn)] == ["entries", "validate_repository_internal_proof_roots"]


def test_missing_entries_fail_closed(tmp_path):
    data = audit(tmp_path)
    assert data["summary"]["guarded_entrypoints"] == 0
    assert data["r7_closure_status"] == "NOT_CERTIFIED_BY_STATIC_AUDIT"
    assert data["missing_files"]


def test_report_created(tmp_path):
    data = audit(tmp_path)
    output = tmp_path / "output"
    write_report(output, data)
    assert (output / "audit.json").is_file()
    assert "静的" in (output / "report.md").read_text(encoding="utf-8")
