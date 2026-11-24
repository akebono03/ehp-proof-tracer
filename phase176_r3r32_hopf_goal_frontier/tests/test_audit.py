"""Focused contracts for the non-mutating R3R32 audit package."""
from __future__ import annotations

import importlib.util
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[1] / "audit.py"
spec = importlib.util.spec_from_file_location("phase176_r3r32_audit", AUDIT)
assert spec is not None and spec.loader is not None
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def test_function_names_reads_python_definitions() -> None:
    assert audit.function_names("def first():\n    return 1\n") == ["first"]


def test_review_file_missing_file_reports_not_present(tmp_path: Path) -> None:
    assert audit.review_file(tmp_path, "missing.py") == {"file": "missing.py", "present": False}


def test_review_file_detects_existing_rule_names(tmp_path: Path) -> None:
    source = "def toda_prop22_right_inference_rule():\n    return None\n"
    (tmp_path / "example.py").write_text(source, encoding="utf-8")
    result = audit.review_file(tmp_path, "example.py")
    assert result["present"] is True
    assert result["syntax_error"] is None
    assert result["indicators"]["toda_prop22_right"] is True
    assert result["indicators"]["phase176_r3r31"] is False
