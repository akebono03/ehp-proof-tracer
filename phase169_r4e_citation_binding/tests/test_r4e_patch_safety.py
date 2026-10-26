"""Patch is scope-limited and rejects text it was not reviewed against."""
from __future__ import annotations

import ast

import pytest

from phase169_r4e_citation_binding.patch import (
    checked_replacement, updated_reference, updated_renderer,
)


def test_r4e_rejects_missing_or_ambiguous_patch_anchors():
    with pytest.raises(RuntimeError, match="baseline mismatch"):
        checked_replacement("unrelated", "source", "new", "unit")
    with pytest.raises(RuntimeError, match="baseline mismatch"):
        checked_replacement("source source", "source", "new", "unit")


def test_r4e_reference_patch_only_renders_guarded_prop44():
    original = (
        'def project_reference_bodies(registry, assertion_ids):\n'
        '    from phase165_r52_r27_r5_literature import Toda52UniversalStatement\n'
        '    if False:\n'
        '            elif isinstance(statement, Toda51BelowDiagonalZeroStatement):\n'
        '                sentence = r"$\\pi_i^n=0\\quad(i<n)$."\n'
    )
    result = updated_reference(original)
    assert "and statement == TodaProp44UniversalStatement()" in result
    assert result.count("from phase165_r52_r27_r5_literature import") == 1


def test_r4e_renderer_patch_only_adds_ancestry_based_tags():
    original = (
        'def render_model_backed_narrative_markdown():\n'
        '    if False:\n'
        '            if sentence.endswith("である."):\n'
        '                pass\n'
        '            if isinstance(step.conclusion, TodaProp42ExactnessStatement):\n'
        '                statement_latex = statement_latex.replace(r" \\text{ is exact}", "")\n'
        '                lines.append(f"{prefix}${statement_latex}$ は完全.")\n'
    )
    result = updated_renderer(original)
    assert "step, TodaProp44UniversalStatement" in result
    assert "step, TodaProp42GeneralExactnessStatement" in result
    assert "literature_reference=" not in result
    ast.parse(result)
