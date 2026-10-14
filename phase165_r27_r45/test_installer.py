import ast
from pathlib import Path
import tempfile

import pytest

from apply import apply, replace_function, WEB_FUNCTION, NEW_MODULE


def test_execution_module_has_no_legacy_import():
    source = (Path(__file__).parent / NEW_MODULE).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert not any(isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("repository_") for node in ast.walk(tree))


def test_execution_uses_real_inference_engine():
    source = (Path(__file__).parent / NEW_MODULE).read_text(encoding="utf-8")
    assert "apply_inference_match(match)" in source
    assert "find_typed_applicable_rules(proven_steps, rules=rules)" in source


def test_invalid_candidate_rejected():
    assert "candidate_number < 1" in (Path(__file__).parent / NEW_MODULE).read_text()


def test_web_function_is_valid_python():
    ast.parse(WEB_FUNCTION)
    assert "TypedGeneratorExecutionStatus.EXECUTED" in WEB_FUNCTION
    assert "provenance=WebGeneratorExecutionProvenanceView(" in WEB_FUNCTION


def test_replace_function_keeps_other_code():
    source = "def build_standard_web_generator_execution_view():\n    return 5\n\ndef keep():\n    return 3\n"
    changed = replace_function(source, "build_standard_web_generator_execution_view", WEB_FUNCTION)
    assert "def keep():\n    return 3" in changed


def test_installer_stages_and_is_idempotent():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "toda_typed_applicability.py").write_text("pass\n")
        (root / "web_generator_execution.py").write_text("def build_standard_web_generator_execution_view():\n    search_typed_generator_statements('x')\n    return None\n")
        first = apply(root)
        assert first["status"] == "CHANGED"
        second = apply(root)
        assert second["status"] == "ALREADY_INSTALLED"


def test_installer_rejects_unmigrated_entry():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "toda_typed_applicability.py").write_text("pass\n")
        (root / "web_generator_execution.py").write_text("def build_standard_web_generator_execution_view():\n    return None\n")
        with pytest.raises(RuntimeError, match="R36"):
            apply(root)
        assert not (root / NEW_MODULE).exists()
