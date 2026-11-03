"""Pure AST detector tests; no proof-search or renderer edits."""
from __future__ import annotations

from phase173_r4_r12r3_architecture_audit.audit import scan_source


def _codes(source: str, path: str) -> set[str]:
    return {finding.code for finding in scan_source(source, path)}


def test_dedicated_pi_narrative_function_is_detected() -> None:
    source = (
        "def project_verified_pi74_narrative(result, model, markdown):\n"
        "    return markdown\n"
    )
    codes = _codes(source, "phase173_r4_r12_common_narrative/projection.py")
    assert "DEDICATED_NARRATIVE_FUNCTION" in codes


def test_numeric_dispatch_is_detected_without_source_text_matching() -> None:
    source = (
        "def render(result):\n"
        "    if 7 == result.target.group_dimension:\n"
        "        return 'custom'\n"
        "    return 'generic'\n"
    )
    codes = _codes(source, "phase173_r4_r12_common_narrative/projection.py")
    assert "LITERAL_DIMENSION_DISPATCH" in codes


def test_legacy_rule_dispatch_is_detected() -> None:
    source = (
        "LEGACY_ROOT = 'previous'\n"
        "def project(result):\n"
        "    if root_name == LEGACY_ROOT:\n"
        "        return 'custom'\n"
        "    return 'generic'\n"
    )
    codes = _codes(source, "phase173_r4_r12_common_narrative/projection.py")
    assert "LEGACY_RULE_DISPATCH" in codes


def test_adapter_rewriting_derived_markdown_is_detected() -> None:
    source = (
        "def build(result, model):\n"
        "    markdown = render_model_backed_narrative_markdown(result, model)\n"
        "    markdown = project_verified_toda56_narrative(result, model, markdown)\n"
        "    return markdown\n"
    )
    codes = _codes(source, "phase165_r52_r3_web_adapter.py")
    assert "POST_RENDER_NARRATIVE_OVERRIDE" in codes


def test_generic_model_renderer_has_no_false_dimension_dispatch() -> None:
    source = (
        "def render(result, model):\n"
        "    for step in model.steps:\n"
        "        if step.rule == ProofRule.GIVEN:\n"
        "            return format_step(step)\n"
        "    return ''\n"
    )
    codes = _codes(source, "phase168_r3_5_model_renderer.py")
    assert "LITERAL_DIMENSION_DISPATCH" not in codes
    assert "DEDICATED_NARRATIVE_FUNCTION" not in codes


def test_test_contract_that_freezes_legacy_wording_is_detected() -> None:
    source = (
        "def test_pi74_existing_projection_remains_byte_equal():\n"
        "    assert shown == expected\n"
    )
    codes = _codes(
        source, "phase173_r4_r12_common_narrative/tests/test_projection.py",
    )
    assert "LEGACY_TEST_CONTRACT" in codes


def test_fixed_sphere_dimension_in_central_renderer_is_detected() -> None:
    source = (
        "def render(mapping, i):\n"
        "    if mapping.target_group == TodaPrimaryGroup(i, 4):\n"
        "        return 'custom'\n"
        "    return 'generic'\n"
    )
    codes = _codes(source, "phase168_r3_5_model_renderer.py")
    assert "FIXED_SPHERE_CONSTRUCTOR" in codes
