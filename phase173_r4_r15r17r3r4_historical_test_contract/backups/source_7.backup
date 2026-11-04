"""Real certified partial proofs display their checked intermediate premises."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    render_certified_abstract_model_section,
    render_certified_abstract_section,
)
from web_group_proof import build_standard_web_group_proof_view


@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_abstract_certificate_displays_actual_verified_milestones(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    assert result.abstract_structure is not None
    assert result.abstract_structure.proof_step not in result.proven_steps

    model = build_proof_narrative_model(result)
    progress = render_certified_abstract_model_section(model)
    assert progress == render_certified_abstract_section(result)
    assert "## 検証済みの途中経過" in progress
    assert "### 検証済み証明木の Reference" in progress
    assert "### 検証済み ProofStep" in progress
    assert "Proposition 4.4" in progress
    assert "Lemma 5.4" in progress
    assert progress.count("DB prior: sphere.csv") >= 2
    assert "## 証明済みの抽象群構造" in progress
    assert "記名生成元の対応は未証明" in progress
    assert "先行データベースの " not in progress
    assert "Proposition 4.4 の適用前提となる定理を検証した" not in progress
    assert progress in render_model_backed_narrative_markdown(result, model)

    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.partial_result and view.abstract_structure_certified
    assert view.key == "generic-partial-proof"
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("検証済みの途中経過") == 1
    assert headings.count("証明済みの抽象群構造") == 1
    assert headings.count("未解決 Goal") == 1
    shown = "\n".join(
        seg.value for line in view.rendered_lines for seg in line.segments
    )
    assert "sphere.csv" in shown and "Lemma 5.4" in shown
    assert "Relation(lhs=" not in shown
    assert "、" not in shown and "。" not in shown
    assert result.conclusion is None and result.open_goals

def test_completed_view_has_no_abstract_progress_sidecar() -> None:
    view = build_standard_web_group_proof_view(
        n=4, k=4, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert not view.abstract_structure_certified
    assert not any(
        line.kind == "heading" and line.prefix == "検証済みの途中経過"
        for line in view.rendered_lines
    )
    assert not any(
        "、" in seg.value or "。" in seg.value
        for line in view.rendered_lines for seg in line.segments
    )


def test_legacy_and_model_paths_share_abstract_progress() -> None:
    goal = exact_prior_database_result(4, 8)
    assert goal is not None
    views = (
        build_standard_web_group_proof_view(
            n=4, k=8, goal=goal, mode="narrative", citation_source=source,
        )
        for source in ("model", "legacy")
    )
    for view in views:
        assert view.key == "generic-partial-proof"
        assert any(
            line.kind == "heading" and line.prefix == "検証済みの途中経過"
            for line in view.rendered_lines
        )
