"""Source guards and syntactic contracts before installing a production patch."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r11_model_abstract_integration.install import preflight
from phase173_r4_r15r11_model_abstract_integration.patch import (
    EXPECTED_BLOBS,
    apply_to_source,
    changed_units,
)

ROOT = Path(__file__).resolve().parents[2]


def test_reviewed_source_can_be_replaced_atomically_and_parses() -> None:
    proposal = preflight(ROOT)
    assert set(proposal) == set(EXPECTED_BLOBS)
    for rel, (original, changed) in proposal.items():
        assert changed != original
        ast.parse(changed.decode("utf-8"), filename=rel)
        full = changed_units(rel, changed)
        assert "### Complete" in full
        assert "```python" in full


def test_patch_is_fail_closed_on_repetition_and_crlf() -> None:
    for rel, (original, updated) in preflight(ROOT).items():
        with pytest.raises(RuntimeError, match="Unreviewed"):
            apply_to_source(rel, updated)
        if b"\r\n" not in original:
            crlf = original.replace(b"\n", b"\r\n")
            rewritten = apply_to_source(rel, crlf)
            assert b"\r\n" in rewritten
            assert rewritten.count(b"\n") == rewritten.count(b"\r\n")
            ast.parse(rewritten.decode("utf-8"))


def test_renderer_reapplication_rejected_when_old_anchor_survives() -> None:
    """An inserted block must not be duplicated if it contains the old anchor."""
    source = (
        "def render_model_backed_narrative_markdown(result, model):\n"
        "    incomplete = result.status is not ProofSearchStatus.COMPLETE\n"
        "    if incomplete:\n"
        '        lines.extend(("", "未解決 Goal は証明済みの結論ではありません。"))\n'
        "    else:\n"
        '        lines.append("□")\n'
    ).encode("utf-8")
    relative = "phase168_r3_5_model_renderer.py"
    updated = apply_to_source(relative, source)
    assert updated.count(b"if model.abstract_structure is not result.abstract_structure:") == 1
    with pytest.raises(RuntimeError, match="already patched"):
        apply_to_source(relative, updated)


def test_model_and_web_have_no_dimension_specific_branches() -> None:
    proposal = preflight(ROOT)
    for rel in (
        "phase165_r52_r3_web_adapter.py",
        "phase168_r3_3_proof_narrative_model.py",
        "phase173_r4_r15r9_shared_abstract_renderer/projection.py",
    ):
        new_source = proposal[rel][1].decode("utf-8")
        tree = ast.parse(new_source)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare):
                continue
            operands = (node.left, *node.comparators)
            has_nk = any(
                isinstance(term, ast.Name) and term.id in ("n", "k")
                for operand in operands for term in ast.walk(operand)
            )
            has_integer = any(
                isinstance(term, ast.Constant) and type(term.value) is int
                for operand in operands for term in ast.walk(operand)
            )
            assert not (has_nk and has_integer), f"Specialized display: {rel}:{node.lineno}"


def test_old_adapter_model_branch_does_not_append_abstract_twice() -> None:
    web_source = preflight(ROOT)["phase165_r52_r3_web_adapter.py"][1].decode("utf-8")
    assert web_source.count("render_certified_abstract_section(result)") == 1
    assert web_source.count("render_model_backed_narrative_markdown(result, narrative_model)") == 1
    renderer = preflight(ROOT)["phase168_r3_5_model_renderer.py"][1].decode("utf-8")
    assert renderer.count("render_certified_abstract_model_section(model)") == 1
    assert web_source.count("_build_group_proof_rendered_lines(markdown)") == 1
    assert '"generic-complete-proof"' in web_source
    assert '"generic-partial-proof"' in web_source
