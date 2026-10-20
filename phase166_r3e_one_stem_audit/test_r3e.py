"""Targeted production regressions: pi4_3 first, then pi5_4."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from proof import ProofRule


def test_pi43_is_complete_with_inferred_root():
    result = search_group_from_registered_goal(n=3, k=1)
    assert result.status is ProofSearchStatus.COMPLETE, result.diagnostics
    assert result.conclusion is not None
    assert not result.open_goals
    assert any(step.rule is ProofRule.INFERENCE and step.conclusion == result.conclusion
               for step in result.proven_steps)


def test_pi43_existing_reference_and_quotient_narrative():
    result = search_group_from_registered_goal(n=3, k=1)
    assert result.status is ProofSearchStatus.COMPLETE, result.diagnostics
    markdown = render_partial_proof_markdown(result)
    assert "(5.1)" in markdown
    assert "Proposition 5.1" in markdown
    assert r"\pi_{4}^{3}" in markdown
    assert r"\ker E" in markdown
    assert r"\cong" in markdown
    assert "□" in markdown


def test_pi43_web_complete():
    view = build_group_proof_progress_view(n=3, k=1, max_depth=2)
    assert view.key == "generic-complete-proof"
    assert view.mode == "narrative"
    assert not view.partial_result
    assert view.rendered_lines


def test_pi54_search_returns_observed_proof_status():
    result = search_group_from_registered_goal(n=4, k=1)
    assert isinstance(result.status, ProofSearchStatus)
    if result.status is ProofSearchStatus.COMPLETE:
        assert result.conclusion is not None
        assert not result.open_goals
        assert any(step.conclusion == result.conclusion for step in result.proven_steps)
    else:
        assert result.conclusion is None
        assert result.open_goals or result.diagnostics


def test_pi54_web_agrees_with_search_status():
    result = search_group_from_registered_goal(n=4, k=1)
    view = build_group_proof_progress_view(n=4, k=1, max_depth=2)
    assert view.mode == "narrative"
    assert bool(view.rendered_lines)
    assert (view.key == "generic-complete-proof") == (result.status is ProofSearchStatus.COMPLETE)
    assert view.partial_result == (result.status is not ProofSearchStatus.COMPLETE)


def test_pi54_completion_requirement():
    result = search_group_from_registered_goal(n=4, k=1)
    assert result.status is ProofSearchStatus.COMPLETE, (
        "pi5_4 NOT COMPLETE; inspect audit_result.json for goals and diagnostics: "
        f"status={result.status.value}; open_goals={result.open_goals!r}; "
        f"diagnostics={result.diagnostics!r}"
    )
    markdown = render_partial_proof_markdown(result)
    assert r"\pi_{5}^{4}" in markdown
    assert r"\eta_{4}" in markdown
    assert "□" in markdown
