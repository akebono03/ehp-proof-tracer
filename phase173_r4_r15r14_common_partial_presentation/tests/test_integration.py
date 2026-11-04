"""Focused real typed partial and complete view regression tests."""
from __future__ import annotations

import pytest

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _group_proof_statement_latex


@pytest.mark.parametrize("k", (8, 15))
def test_typed_cyclic_open_goal_reuses_registered_latex(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None and isinstance(goal.rhs, FiniteCyclicGroup)
    typed = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    shown, fallback = _group_proof_statement_latex(typed)
    expected, expected_fallback = _group_proof_statement_latex(goal)
    assert fallback is None and expected_fallback is None
    assert shown == expected
    assert shown.startswith(r"\pi_{")
    assert r"\mathbb{Z}/2\{" in shown


def test_infinite_cyclic_statement_reuses_general_group_renderer() -> None:
    goal = exact_prior_database_result(4, 3)
    assert goal is not None
    free = next(component for component in goal.rhs.summands
                if isinstance(component, FreeCyclicGroup))
    typed = CyclicStructureStatement(goal.lhs, free.generator, None)
    result, fallback = _group_proof_statement_latex(typed)
    assert fallback is None
    assert r"\mathbb{Z}\{" in result
    assert r"\pi_{7}^{4}" in result


@pytest.mark.parametrize("k", (8, 15))
def test_real_partial_web_does_not_leak_internal_diagnostics(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None and len(result.open_goals) == 3
    assert result.abstract_structure is not None
    assert any("Relation(" in item for item in result.diagnostics)
    model = build_proof_narrative_model(result)
    # Preserve the internal model for audits; only the public view is projected.
    raw = render_model_backed_narrative_markdown(result, model)
    assert "expected a verified registered derivation" in raw
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-partial-proof" and view.partial_result
    assert sum(line.kind == "heading" and line.prefix == "未解決 Goal"
               for line in view.rendered_lines) == 1
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("確認済み ProofStep（与件を含む）") == 1
    assert view.abstract_structure_certified
    rendered = "\n".join(
        segment.value for line in view.rendered_lines for segment in line.segments
    )
    assert "CyclicStructureStatement（数式表示未対応）" not in rendered
    assert "Relation(lhs=" not in rendered
    assert "導出候補 0 件" in rendered
    assert r"\mathbb{Z}/2\{" in rendered
    assert r"\pi_{" in rendered


def test_multi_summand_pending_diagnostic_is_public_prose() -> None:
    goal = exact_prior_database_result(4, 9)
    result = search_group_from_registered_goal(n=4, k=9, goal=goal)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None and len(result.open_goals) == 2
    assert result.abstract_structure is not None
    view = build_standard_web_group_proof_view(
        n=4, k=9, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-partial-proof" and view.partial_result
    diagnostic_lines = []
    in_diagnostics = False
    for line in view.rendered_lines:
        if line.kind == "heading":
            in_diagnostics = line.prefix == "探索診断"
        elif in_diagnostics:
            diagnostic_lines.extend(segment.value for segment in line.segments)
    diagnostic = "\n".join(diagnostic_lines)
    assert "導出候補 0 件" in diagnostic
    assert "Relation(" not in diagnostic


def test_named_complete_proof_is_unchanged() -> None:
    view = build_standard_web_group_proof_view(
        n=4, k=4, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof" and not view.partial_result
    assert view.rendered_lines
    assert any("[R" in segment.value for line in view.rendered_lines
               for segment in line.segments)
    assert not any(line.kind == "heading" and line.prefix == "未解決 Goal"
                   for line in view.rendered_lines)
