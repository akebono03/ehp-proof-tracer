"""Real Web regression after historical test expectations follow the unified model."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from web_group_proof import build_standard_web_group_proof_view


@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_model_web_keeps_one_source_list_and_unproved_named_goals(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    assert result.abstract_structure is not None
    model = build_proof_narrative_model(result)
    assert model.open_goals == result.open_goals
    assert any(step is result.abstract_structure.proof_step for step in model.steps)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, citation_source="model", mode="narrative",
    )
    assert view.partial_result and view.abstract_structure_certified
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("未解決 Goal") == 1
    assert headings.count("確認済み ProofStep（与件を含む）") == 1
    assert "検証済み証明木の Reference" not in headings
    assert "検証済みの途中経過" not in headings
    assert "証明済みの抽象群構造" not in headings
    shown = "\n".join(segment.value for line in view.rendered_lines
                       for segment in line.segments)
    assert "Proposition 4.4" in shown
    assert "Lemma 5.4" in shown
    assert r"\cong" in shown
    assert "数式表示未対応" not in shown
    assert "Relation(lhs=" not in shown
    assert "、" not in shown and "。" not in shown


def test_uncertified_group_keeps_no_fabricated_references() -> None:
    result = search_group_from_registered_goal(n=5, k=3)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    assert not model.citations
    assert result.open_goals and result.conclusion is None
    view = build_standard_web_group_proof_view(n=5, k=3, mode="narrative")
    assert view.key == "generic-partial-proof"
    assert not view.abstract_structure_certified
    assert not view.steps


def test_named_complete_proof_stays_complete() -> None:
    result = search_group_from_registered_goal(n=4, k=4)
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    view = build_standard_web_group_proof_view(n=4, k=4, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert not view.partial_result and not view.abstract_structure_certified
