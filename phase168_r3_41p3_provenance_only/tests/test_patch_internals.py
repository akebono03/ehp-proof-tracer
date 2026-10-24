"""Lightweight structure/guard tests; standalone and application-independent."""
from __future__ import annotations

import ast

import pytest

from phase168_r3_41p3_provenance_only.apply import compute_patches, replaced_function
from phase168_r3_41p3_provenance_only.replacements import RENDERER_HELPER, TODA45_EVIDENCE


def test_replacement_functions_are_complete_python_and_have_expected_names():
    module = ast.parse("from __future__ import annotations\n" + TODA45_EVIDENCE)
    functions = [n for n in module.body if isinstance(n, ast.FunctionDef)]
    assert len(functions) == 1
    assert functions[0].name == "toda45_specialization_evidence"
    outer = ast.parse("def sample():\n" + RENDERER_HELPER)
    helper = outer.body[0].body[0]
    assert isinstance(helper, ast.FunctionDef)
    assert helper.name == "direct_given_premise_citation_numbers"


def test_ast_function_replacement_preserves_other_functions():
    source = "def a():\n    return 1\n\ndef b():\n    return 2\n"
    modified = replaced_function(source, "a", "def a():\n    return 3\n")
    assert "    return 3" in modified
    assert "def b():\n    return 2" in modified


def test_missing_or_duplicate_function_is_rejected():
    with pytest.raises(ValueError):
        replaced_function("def other():\n    pass\n", "wanted", "def wanted():\n    pass\n")
    with pytest.raises(ValueError):
        replaced_function("def a():\n    pass\ndef a():\n    pass\n", "a", "def a():\n    pass\n")


def test_unexpected_project_source_is_rejected_without_changing_files():
    inputs = {
        "phase168_r3_5_model_renderer.py": "def other():\n    pass\n",
        "phase168_r3_27_typed_statement_projection.py": "def other():\n    pass\n",
    }
    before = inputs.copy()
    with pytest.raises(ValueError):
        compute_patches(inputs)
    assert inputs == before


def test_patcher_replaces_nested_and_top_level_functions_atomically():
    renderer = (
        "from __future__ import annotations\n"
        "def render_model_backed_narrative_markdown(result, model):\n"
        "    def validated_specialization_citation_numbers(step):\n"
        "        return specialize_typed_statement(step, step)\n"
        "    sources = validated_specialization_citation_numbers(step)\n"
        "    return sources\n"
    )
    projection = (
        "def toda45_specialization_evidence(step):\n"
        "    bindings = specialize_typed_statement(parent.conclusion, step.conclusion)\n"
        "    return bindings\n"
        "\n"
        "def typed_sentence(statement, step):\n"
        "    return None\n"
    )
    modified = compute_patches({
        "phase168_r3_5_model_renderer.py": renderer,
        "phase168_r3_27_typed_statement_projection.py": projection,
    })
    assert "sources = direct_given_premise_citation_numbers(step)" in modified[
        "phase168_r3_5_model_renderer.py"
    ]
    assert "def typed_sentence(statement, step):" in modified[
        "phase168_r3_27_typed_statement_projection.py"
    ]
    assert all("specialize_typed_statement" not in content for content in modified.values())
    for content in modified.values():
        ast.parse(content)
