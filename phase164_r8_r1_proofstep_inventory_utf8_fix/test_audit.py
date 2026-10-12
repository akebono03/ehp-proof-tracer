import json
from pathlib import Path
from audit import inventory, write_report


def test_inventory_finds_direct_and_inference(tmp_path):
    (tmp_path / "proof.py").write_text("def f():\n    return ProofStep('x', (), None)\n")
    (tmp_path / "other.py").write_text("def g(match):\n    return apply_inference_match(match)\n")
    report = inventory(tmp_path)
    assert report["counts"]["direct_constructor"] == 1
    assert report["counts"]["inference_application"] == 1


def test_tests_directory_not_counted(tmp_path):
    (tmp_path / "proof.py").write_text("value = 1\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_hidden.py").write_text("ProofStep(None, (), None)\n")
    assert inventory(tmp_path)["counts"].get("direct_constructor", 0) == 0


def test_function_and_line_captured(tmp_path):
    (tmp_path / "proof.py").write_text("def build():\n    return ProofStep('a', (), None)\n")
    result = inventory(tmp_path)
    assert result["sites"][0]["function"] == "build"
    assert result["sites"][0]["line"] == 2


def test_report_files_and_read_only_flag(tmp_path):
    (tmp_path / "proof.py").write_text("value = 1\n")
    result = inventory(tmp_path)
    output = tmp_path / "output"
    write_report(result, output)
    assert json.loads((output / "audit.json").read_text(encoding="utf-8"))["production_modified"] is False
    assert "ProofStep" in (output / "report.md").read_text(encoding="utf-8")


def test_invalid_project_rejected(tmp_path):
    try:
        inventory(tmp_path)
    except FileNotFoundError:
        return
    raise AssertionError("missing project root must be rejected")
