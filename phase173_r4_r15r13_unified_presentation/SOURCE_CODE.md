# Source and Tests — Full Replacement Units

See `FULL_CHANGED_UNITS.md` for the complete modified function and the new layout function.

## `tests/test_contract.py` (all imports and tests)

```python
"""Pure, status-independent presentation contract tests."""
from __future__ import annotations

from phase173_r4_r15r13_unified_presentation.layout import canonicalize_proof_layout


def test_complete_and_partial_share_one_structure() -> None:
    completed = (
        "使用する結果\n\n**[R1] Proposition 4.4.**\n\n"
        "証明\n\n[R1]を用いて, $\\pi_7^4=\\mathbb{Z}$.\n□\n"
    )
    partial = (
        "## 証明対象\n\n$\\pi_{12}^{4}$\n\n"
        "## 使用する結果\n\n参照情報を持つ ProofStep はありません。\n"
        "---\n\n## 証明\n\n**探索状態：証明未完成**\n"
        "## 未解決 Goal\n\n- $\\pi_{12}^{4}$\n"
    )
    full = canonicalize_proof_layout(completed)
    pending = canonicalize_proof_layout(partial)
    for text in (full, pending):
        assert text.count("## 使用する結果") == 1
        assert "\n証明\n" not in text
        assert "## 証明\n" not in text
        assert text.count("\n---\n") == 1
    assert "**[R1] Proposition 4.4.**" in full
    assert "[R1]を用いて" in full and "□" in full
    assert "**探索状態：証明未完成**" in pending
    assert "## 未解決 Goal" in pending
    assert "## 証明対象" not in pending
    assert r"$\pi_{12}^{4}$" in pending


def test_layout_does_not_infer_or_remove_citations() -> None:
    source = (
        "## 使用する結果\n\n**[R1] Lemma 5.4.**\n\n"
        "$H(\\nu_4)=\\iota_7$.\n\n---\n\n## 証明\n\n"
        "**探索状態：証明未完成**\n\n"
        "## 未解決 Goal\n\n- CyclicStructureStatement（数式表示未対応）\n"
    )
    changed = canonicalize_proof_layout(source)
    assert changed.count("[R1]") == source.count("[R1]")
    assert changed.count(r"$H(\nu_4)=\iota_7$") == 1
    assert changed.count("## 未解決 Goal") == 1
    assert "CyclicStructureStatement（数式表示未対応）" in changed
    assert changed.count("\n---\n") == 1


def test_other_text_is_not_changed() -> None:
    source = "## 未解決 Goal\n\n証明\n"
    assert canonicalize_proof_layout(source) == source


def test_type_guard() -> None:
    try:
        canonicalize_proof_layout(None)
    except TypeError:
        pass
    else:
        raise AssertionError("type guard missing")
```

## `tests/test_integration.py` (all imports and tests)

```python
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
```
