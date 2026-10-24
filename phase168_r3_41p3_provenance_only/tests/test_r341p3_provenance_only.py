"""R3-41P3: Rendering reuses proof provenance and does not replay specialization."""
from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import patch

import pytest

import phase168_r3_5_model_renderer as renderer
from phase168_r3_38_frozen_fulltext_audit.audit import sections
from phase168_r3_39f_frozen_comparison.audit import assess
from web_group_proof import build_standard_web_group_proof_view

PACKAGE = Path(__file__).resolve().parents[1]
CASE_IDS = (("pi3_2", 2, 1, 18, 4), ("pi4_3", 3, 1, 25, 4),
            ("pi5_4", 4, 1, 10, 3))


@pytest.mark.parametrize("name,n,k,count,reference_count", CASE_IDS)
def test_existing_fulltext_and_citation_provenance_without_rule_replay(
    name, n, k, count, reference_count
):
    seen = []
    original_renderer = renderer.render_model_backed_narrative_markdown

    def render_without_revalidating(result, model):
        before = repr((model.steps, model.citations, model.step_citation_numbers))
        with patch(
            "phase165_r57_r20_general_specialization.specialize_typed_statement",
            side_effect=AssertionError("renderer replayed a proof specialization"),
        ):
            text = original_renderer(result, model)
        after = repr((model.steps, model.citations, model.step_citation_numbers))
        assert before == after
        seen.append((text, model))
        return text

    with patch.object(renderer, "render_model_backed_narrative_markdown",
                      side_effect=render_without_revalidating):
        view = build_standard_web_group_proof_view(n=n, k=k)
    assert len(seen) == 1
    text, model = seen[0]
    baseline = (PACKAGE / "fixtures" / (name + "_current.md")).read_text(
        encoding="utf-8-sig"
    )
    assert text == baseline
    assert len(model.steps) == count
    assert len(model.citations) == reference_count
    assert all(c.statement_bodies for c in model.citations)
    assert all(i in model.citations[num-1].step_indices
               for i, nums in enumerate(model.step_citation_numbers)
               for num in nums)
    _, proof = sections(text)
    assert all(check["present"] for check in assess(name, proof))
    assert "□" in proof
    if name == "pi5_4":
        assert "(n,m,k)=(3,4,1)" in proof
        assert "[R3]を " in proof


def test_source_contains_no_specialization_validator_in_renderer_projection():
    for name in ("phase168_r3_5_model_renderer.py",
                 "phase168_r3_27_typed_statement_projection.py"):
        root = PACKAGE.parent
        tree = ast.parse((root / name).read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                function = node.func
                if isinstance(function, ast.Name):
                    assert function.id != "specialize_typed_statement"
                elif isinstance(function, ast.Attribute):
                    assert function.attr != "specialize_typed_statement"
