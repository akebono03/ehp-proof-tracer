"""Public projection of a separately verified tree through the common renderer."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    render_certified_abstract_section,
)
from phase173_r4_r15r16r3_staged_guard_fix.tree_adapter import (
    render_verified_tree_progress,
    verified_tree_postorder,
)
from web_group_proof import build_standard_web_group_proof_view


@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_real_abstract_tree_reuses_common_renderer(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    structure = result.abstract_structure
    assert structure is not None
    ordered = verified_tree_postorder(structure.proof_step)
    assert ordered[-1] is structure.proof_step
    assert len(ordered) >= 4
    assert structure.proof_step not in result.proven_steps
    lines = render_verified_tree_progress(result.target, structure.proof_step)
    joined = "\n".join(lines)
    assert "### 検証済み証明木の Reference" in joined
    assert "### 検証済み ProofStep" in joined
    assert "Proposition 4.4" in joined
    assert "Lemma 5.4" in joined
    assert "DB prior: sphere.csv" in joined
    assert "- 与件:" in joined or "- 推論:" in joined
    assert "Relation(lhs=" not in joined
    assert "数式表示未対応" not in joined
    assert "先行データベースの " not in joined
    assert "4つの前提" not in joined
    rendered = render_certified_abstract_section(result)
    assert "## 検証済みの途中経過" in rendered
    assert "### 検証済み ProofStep" in rendered

    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.partial_result and view.abstract_structure_certified
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("検証済みの途中経過") == 1
    assert headings.count("証明済みの抽象群構造") == 1
    assert headings.count("未解決 Goal") == 1
    shown = "\n".join(segment.value for line in view.rendered_lines
                       for segment in line.segments)
    assert "Proposition 4.4" in shown
    assert "sphere.csv" in shown
    assert "Lemma 5.4" in shown
    assert "、" not in shown and "。" not in shown
    assert result.conclusion is None and result.open_goals


def test_completed_proof_does_not_receive_abstract_progress() -> None:
    view = build_standard_web_group_proof_view(
        n=4, k=4, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert not view.abstract_structure_certified
    assert not any(line.kind == "heading" and line.prefix == "検証済みの途中経過"
                   for line in view.rendered_lines)
