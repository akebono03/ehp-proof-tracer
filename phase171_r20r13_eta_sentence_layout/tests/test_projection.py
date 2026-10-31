"""Sentence layout unit checks and canonical public-search integration."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase171_r20r13_eta_sentence_layout.projection import (
    _split_outside_math_at_period,
    combine_adjacent_verified_eta_sentences,
    format_complete_proof_sentences,
    split_completed_proof_sentences,
    verified_eta_display_sentences,
)


def test_periods_are_newlines_only_in_proof_body():
    lines = [
        "使用する結果", "", "[R1] Proposition 5.6.", "",
        "証明", "", "最初の理由. 次の理由. $E(\\eta_{2})=\\eta_{3}$.",
        "", "□",
    ]
    actual = split_completed_proof_sentences(lines)
    assert "[R1] Proposition 5.6." in actual
    assert "最初の理由." in actual
    assert "次の理由." in actual
    assert r"$E(\eta_{2})=\eta_{3}$." in actual
    assert "最初の理由. 次の理由." not in actual


def test_periods_inside_math_and_decimals_remain_intact():
    assert _split_outside_math_at_period(r"$x=1. 2$ を用いる. 次を示す.") == [
        r"$x=1. 2$ を用いる.", "次を示す."
    ]
    assert _split_outside_math_at_period("値は3.14である. 次を示す.") == [
        "値は3.14である.", "次を示す."
    ]
    assert _split_outside_math_at_period("位数は2. また群は有限.") == [
        "位数は2.", "また群は有限."
    ]


def test_uncertified_eta_lines_are_not_merged():
    model = SimpleNamespace(steps=(), root_index=None)
    lines = ["証明", "", r"[R3]より, $E(\eta_{2})=\eta_{3}$.", "",
             r"[R3]より, $E(\eta_{3}^{2})=\eta_{4}^{2}$."]
    assert combine_adjacent_verified_eta_sentences(lines, model) == lines
    assert format_complete_proof_sentences(lines, model) == lines


@pytest.fixture(scope="module")
def canonical_pi63():
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    original = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=original, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(original, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    return result, build_linked_proof_narrative_model(result, contexts[0])


def test_real_derived_eta_prose_has_verified_citation(canonical_pi63):
    _, model = canonical_pi63
    eligible = verified_eta_display_sentences(model)
    assert len(eligible) >= 3
    assert sum(line.startswith("[R3]より, $E(") for line in eligible) >= 3


def test_real_public_proof_joins_eta_and_retains_order_four(canonical_pi63):
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    result, model = canonical_pi63
    markdown = render_model_backed_narrative_markdown(result, model)
    refs, body = markdown.split("\n証明\n", 1)
    eligible = verified_eta_display_sentences(model)
    assert len(model.citations) == 8
    assert "[R3] Chapter V, i)." in refs
    assert r"\operatorname{ord}" in body
    assert r"\neq0" in body
    assert r"\quad E(" in body
    assert any(source not in body for source in eligible if source.startswith("[R3]より,"))
    assert "による導出も同じ群構造を示す" not in body
