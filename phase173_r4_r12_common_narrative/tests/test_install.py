"""Static source-protection and entire-function replacement regression."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r12_common_narrative import install


def _source():
    return Path(__file__).resolve().parents[1]


def test_full_adapter_is_a_real_complete_function_and_keeps_imports() -> None:
    code = (_source() / "web_adapter_FULL.py.txt").read_text(encoding="utf-8")
    parsed = ast.parse(code)
    assert sum(isinstance(node, ast.FunctionDef)
               and node.name == "build_partial_web_group_proof_view"
               for node in parsed.body) == 1
    assert not any(isinstance(node, ast.Constant) and node.value is Ellipsis
                   for node in ast.walk(parsed))
    assert "project_verified_pi74_narrative(" not in code
    assert "project_verified_toda56_narrative(" in code


def test_unreviewed_imports_are_rejected() -> None:
    source = (_source() / "web_adapter_FULL.py.txt").read_text(encoding="utf-8")
    with pytest.raises(RuntimeError, match="imports or other definitions"):
        install.patched_source(
            source.replace("from __future__ import annotations", "import os").encode(),
            source,
        )


def test_original_narrative_anchor_is_required() -> None:
    source = (_source() / "web_adapter_FULL.py.txt").read_text(encoding="utf-8")
    with pytest.raises(RuntimeError, match="Only the narrative branch may change"):
        install.patched_source(source.encode(), source)


def test_refuse_external_premise_changes() -> None:
    content = (_source() / "projection.py").read_text(encoding="utf-8")
    assert "root.inference_rule.match_guard(root.premises, {})" in content
    assert "display_prior_reference_locator(citation, model)" in content
    assert "model.step_citation_numbers[index]" in content
