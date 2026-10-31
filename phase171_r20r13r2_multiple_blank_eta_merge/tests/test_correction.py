"""Focused separator-only fix; real proof still verifies via R20R13 audit."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase171_r20r13_eta_sentence_layout.projection import (
    combine_adjacent_verified_eta_sentences,
    verified_eta_display_sentences,
)


@pytest.fixture
def eligible(monkeypatch):
    values = {
        r"[R3]より, $E(\eta_{2})=\eta_{3}$.":
            ("[R3]より, ", r"E(\eta_{2})=\eta_{3}"),
        r"[R3]より, $E(\eta_{3}^{2})=\eta_{4}^{2}$.":
            ("[R3]より, ", r"E(\eta_{3}^{2})=\eta_{4}^{2}"),
        r"[R3]より, $E(\eta_{2}^{3})=\eta_{3}^{3}$.":
            ("[R3]より, ", r"E(\eta_{2}^{3})=\eta_{3}^{3}"),
    }
    monkeypatch.setattr(
        "phase171_r20r13_eta_sentence_layout.projection.verified_eta_display_sentences",
        lambda model: values,
    )
    return values


def test_orphan_blank_lines_do_not_break_three_verified_eta_equations(eligible):
    a, b, c = tuple(eligible)
    lines = ["証明", "", a, "", "", "", b, "", c, "", "□"]
    actual = combine_adjacent_verified_eta_sentences(lines, SimpleNamespace())
    merged = r"[R3]より, $E(\eta_{2})=\eta_{3},\quad E(\eta_{3}^{2})=\eta_{4}^{2},\quad E(\eta_{2}^{3})=\eta_{3}^{3}$."
    assert merged in actual
    assert sum(line.startswith("[R3]より, ") for line in actual) == 1
    assert a not in actual and b not in actual and c not in actual
    assert actual[-1] == "□"


def test_no_merge_across_other_proof_sentence(eligible):
    a, b, c = tuple(eligible)
    barrier = r"[R5]より, $2\nu'=\eta_{3}^{3}$."
    original = [a, "", "", barrier, "", b, "", c]
    actual = combine_adjacent_verified_eta_sentences(original, SimpleNamespace())
    assert a in actual
    assert barrier in actual
    assert not any(r"E(\eta_{2})=\eta_{3},\quad" in s for s in actual)
    assert any(r"E(\eta_{3}^{2})=\eta_{4}^{2},\quad E(\eta_{2}^{3})=\eta_{3}^{3}" in s for s in actual)


def test_no_merge_across_different_citation(eligible, monkeypatch):
    a, b, c = tuple(eligible)
    other_line = "[R4]より, $" + eligible[b][1] + "$."
    differing = dict(eligible)
    differing[other_line] = ("[R4]より, ", eligible[b][1])
    monkeypatch.setattr(
        "phase171_r20r13_eta_sentence_layout.projection.verified_eta_display_sentences",
        lambda model: differing,
    )
    original = [a, "", "", other_line, "", "", c]
    actual = combine_adjacent_verified_eta_sentences(original, SimpleNamespace())
    assert actual == original


def test_uncertified_lines_stay_unchanged(eligible):
    a, b, c = tuple(eligible)
    unknown = r"[R3]より, $E(\kappa)=\lambda$."
    original = [a, "", "", unknown, "", b, "", c]
    actual = combine_adjacent_verified_eta_sentences(original, SimpleNamespace())
    assert a in actual
    assert unknown in actual


def test_complete_real_pi63_three_eta_equations_in_one_line():
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    reference, body = markdown.split("\n証明\n", 1)
    lines = body.splitlines()
    grouped = [line for line in lines
               if line.startswith("[R3]より, $E(") and r",\quad E(" in line]
    assert any(
        all(eta in line for eta in (
            r"E(\eta_{2})=\eta_{3}",
            r"E(\eta_{3}^{2})=\eta_{4}^{2}",
            r"E(\eta_{2}^{3})=\eta_{3}^{3}",
        )) for line in grouped
    )
    assert r"\operatorname{ord}" in body
    assert r"\neq0" in body
    assert "短完全列となる. 両端" not in body
    assert len(model.citations) == 8
    assert "[R3] Chapter V, i)." in reference
