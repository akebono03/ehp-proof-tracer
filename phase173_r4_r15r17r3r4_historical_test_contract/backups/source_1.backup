"""Real source-first abstract evidence through the one canonical Narrative Model."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import (
    render_model_backed_narrative_markdown,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    render_certified_abstract_section,
    render_certified_abstract_model_section,
)
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _build_group_proof_rendered_lines


@pytest.mark.parametrize("k", (8, 31))
def test_source_first_certificate_is_owned_by_model_and_rendered_once(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    model = build_proof_narrative_model(result)
    assert result.abstract_structure is not None
    assert model.abstract_structure is result.abstract_structure
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    abstract = render_certified_abstract_model_section(model)
    assert abstract == render_certified_abstract_section(result)
    after = render_model_backed_narrative_markdown(result, model)
    assert after.count("## 証明済みの抽象群構造") == 1
    assert abstract in after
    assert "## 未解決 Goal" in after
    direct_view = build_partial_web_group_proof_view(
        result, mode="narrative", narrative_model=model,
    )
    assert direct_view.rendered_lines == _build_group_proof_rendered_lines(after)
    assert direct_view.key == "generic-partial-proof" and direct_view.partial_result
    assert result.abstract_structure.proof_step not in result.proven_steps
    assert model.open_goals == result.open_goals
    assert model.diagnostics == result.diagnostics


@pytest.mark.parametrize("k", (8, 31))
def test_public_default_path_and_legacy_path_keep_one_abstract_section(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    for citation_source in ("model", "legacy"):
        view = build_standard_web_group_proof_view(
            n=4, k=k, goal=goal, mode="narrative", citation_source=citation_source,
        )
        headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
        assert headings.count("証明済みの抽象群構造") == 1
        if citation_source == "model":
            assert headings.count("未解決 Goal") == 1
        assert view.key == "generic-partial-proof"
        assert view.partial_result


def test_mismatched_narrative_model_fails_closed() -> None:
    goal = exact_prior_database_result(4, 8)
    result = search_group_from_registered_goal(n=4, k=8, goal=goal)
    model = build_proof_narrative_model(result)
    assert model.abstract_structure is not None
    with pytest.raises(ValueError, match="abstract certificate must match"):
        render_model_backed_narrative_markdown(
            result, replace(model, abstract_structure=None),
        )
    with pytest.raises(ValueError, match="partial state must match"):
        render_model_backed_narrative_markdown(
            result, replace(model, status=ProofSearchStatus.COMPLETE),
        )
    with pytest.raises(ValueError, match="unverified Model abstract"):
        render_certified_abstract_model_section(replace(model, root_index=0))


@pytest.mark.parametrize("n,k", ((3, 3), (4, 3)))
def test_existing_completed_web_proofs_remain_complete(n: int, k: int) -> None:
    view = build_standard_web_group_proof_view(
        n=n, k=k, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert view.rendered_lines
    assert not any(
        line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
        for line in view.rendered_lines
    )
