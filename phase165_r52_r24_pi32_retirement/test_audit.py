"""Focused regression checks for the R24 read-only retirement gate."""
from pathlib import Path

from audit import _references, audit


def test_name_reference_scan(tmp_path: Path):
    path = tmp_path / "example.py"
    path.write_text("def f():\n    return foo()\n", encoding="utf-8")
    refs = _references(path, "foo")
    assert len(refs) == 1
    assert refs[0]["kind"] == "Load"


def test_reference_scan_ignores_comments_and_strings(tmp_path: Path):
    path = tmp_path / "example.py"
    path.write_text("# foo\nx = 'foo'\n", encoding="utf-8")
    assert _references(path, "foo") == []


def test_audit_fails_closed_on_missing_sources(tmp_path: Path):
    import pytest
    with pytest.raises(FileNotFoundError):
        audit(tmp_path)


def test_audit_reports_real_legacy_dependency():
    root = Path(__file__).resolve().parent.parent
    if not (root / "toda_rules.py").is_file():
        import pytest
        pytest.skip("Run inside EHP Proof Tracer repository")
    report = audit(root)
    assert report["active_legacy_bootstrap_reference"]
    assert report["status"] == "DELETION_BLOCKED_BY_LEGACY_CONSUMERS"
    assert report["production_modified"] is False
