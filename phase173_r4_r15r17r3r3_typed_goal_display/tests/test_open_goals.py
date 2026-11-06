"""Real typed pending goals and public Narrative across status boundaries."""
from __future__ import annotations

import pytest

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import (
    project_typed_open_goal_displays,
    render_model_backed_narrative_markdown,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from proof import Relation, RelationType
from web_group_proof import build_standard_web_group_proof_view


@pytest.mark.parametrize('n,k,expected', ((4, 8, 3), (4, 9, 2)))
def test_real_typed_pending_goals_are_grouped_only_in_public_display(
    n: int, k: int, expected: int,
) -> None:
    typed = exact_prior_database_result(n, k)
    assert typed is not None
    result = search_group_from_registered_goal(n=n, k=k, goal=typed)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    original = result.open_goals
    assert len(original) == expected
    model = build_proof_narrative_model(result)
    assert model.open_goals == original
    groups = project_typed_open_goal_displays(original)
    assert len(groups) == 1
    assert groups[0][0] is original[0]
    assert groups[0][1] == expected
    markdown = render_model_backed_narrative_markdown(result, model)
    block = markdown.split('## 未解決 Goal', 1)[1].split('## 探索診断', 1)[0]
    goal_lines = [line for line in block.splitlines() if line.startswith('- ')]
    assert len(goal_lines) == 1
    assert f'未解決 Goal {expected} 件' in goal_lines[0]
    assert result.open_goals == original
    assert model.open_goals == original
    assert result.conclusion is None
    assert len(model.steps) >= len(result.proven_steps)
    view = build_standard_web_group_proof_view(
        n=n, k=k, goal=typed, mode='narrative', citation_source='model',
    )
    assert view.partial_result
    assert view.key == 'generic-partial-proof'
    assert any(line.kind == 'heading' and line.prefix == '未解決 Goal'
               for line in view.rendered_lines)


def test_pi8_5_completed_case_is_not_reported_as_an_open_goal() -> None:
    """The formerly partial (n=5,k=3) case must retain its completed proof."""
    typed = exact_prior_database_result(5, 3)
    assert typed is not None
    result = search_group_from_registered_goal(n=5, k=3, goal=typed)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == typed
    assert result.open_goals == ()
    assert any(step.conclusion == typed for step in result.proven_steps)
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    assert model.root_index is not None
    assert project_typed_open_goal_displays(result.open_goals) == ()
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "## 未解決 Goal" not in markdown
    view = build_standard_web_group_proof_view(
        n=5, k=3, goal=typed, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert not any(line.kind == "heading" and line.prefix == "未解決 Goal"
                   for line in view.rendered_lines)


def test_same_latex_is_not_sufficient_to_merge_distinct_typed_structures() -> None:
    target = TodaPrimaryGroup(12, 4)
    first = Relation(target, FiniteCyclicGroup(2, 'g'), RelationType.EQUALITY)
    distinct = Relation(target, FiniteCyclicGroup(4, 'g'), RelationType.EQUALITY)
    entries = project_typed_open_goal_displays((first, distinct, first))
    assert len(entries) == 2
    assert entries[0] == (first, 2)
    assert entries[1] == (distinct, 1)


def test_untyped_strings_remain_distinct_even_when_equal() -> None:
    goals = ('unproved', 'unproved')
    assert project_typed_open_goal_displays(goals) == (('unproved', 1), ('unproved', 1))


def test_completed_proof_remains_unchanged() -> None:
    result = search_group_from_registered_goal(n=4, k=4)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    model = build_proof_narrative_model(result)
    assert project_typed_open_goal_displays(result.open_goals) == ()
    markdown = render_model_backed_narrative_markdown(result, model)
    assert '未解決 Goal' not in markdown
    assert model.steps == result.proven_steps
    assert model.root_index is not None


def test_non_equality_relation_is_never_grouped_into_structure_goal() -> None:
    target = TodaPrimaryGroup(12, 4)
    structure = FiniteCyclicGroup(2, 'g')
    equality = Relation(target, structure, RelationType.EQUALITY)
    other = Relation(target, structure, RelationType.ORDER)
    assert project_typed_open_goal_displays((equality, other)) == (
        (equality, 1), (other, 1),
    )
