"""Real Web group view checks on the same Narrative Model pipeline."""
from __future__ import annotations

import pytest

from web_group_proof import build_standard_web_group_proof_view
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result


@pytest.mark.parametrize("n,k,complete", ((4, 3, True), (4, 7, True),
                                        (4, 8, False), (4, 31, False)))
def test_one_presentation_contract_for_both_proof_states(
    n: int, k: int, complete: bool,
) -> None:
    goal = None if complete else exact_prior_database_result(n, k)
    view = build_standard_web_group_proof_view(
        n=n, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.partial_result is not complete
    assert view.key == ("generic-complete-proof" if complete
                        else "generic-partial-proof")
    headings = [line.prefix for line in view.rendered_lines
                if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert "証明" not in headings
    assert "証明対象" not in headings
    assert sum(line.kind == "separator" for line in view.rendered_lines) == 1
    if complete:
        assert not any(line.kind == "heading" and line.prefix == "未解決 Goal"
                       for line in view.rendered_lines)
        assert any("[R" in segment.value for line in view.rendered_lines
                   for segment in line.segments)
    else:
        assert headings.count("未解決 Goal") == 1
        assert headings.count("証明済みの抽象群構造") == 1
        assert any("探索状態" in segment.value for line in view.rendered_lines
                   for segment in line.segments)


def test_existing_markdown_api_is_preserved() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=3, bridge=bridge, context_sink=contexts.append,
    )
    model = build_linked_proof_narrative_model(result, contexts[-1])
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "\n証明\n" in markdown
    assert "[R1]" in markdown
