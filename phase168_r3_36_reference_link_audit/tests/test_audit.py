from pathlib import Path

from audit import audit_repository, inspect_file


def test_inspect_file_extracts_complete_named_definition(tmp_path: Path) -> None:
    source = tmp_path / "sample.py"
    source.write_text("class A:\n    def f(self):\n        return 1\n", encoding="utf-8")
    result = inspect_file(source, ("A",))
    assert result["definitions"] == [{"name": "A", "first_line": 1, "last_line": 3}]
    assert result["missing_definitions"] == []


def test_audit_repository_rejects_incomplete_checkout(tmp_path: Path) -> None:
    try:
        audit_repository(tmp_path)
    except FileNotFoundError as exc:
        assert "phase168_r3_3_proof_narrative_model.py" in str(exc)
    else:
        raise AssertionError("Incomplete repository must not be silently accepted")
