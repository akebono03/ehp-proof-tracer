"""Targeted Web adapter tests: no mathematical certification implied."""

import pytest

from phase165_r52_partial_proof import (
    GroupStructureStatus,
    ProofSearchStatus,
    make_partial_proof_result,
)
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from proof import ProofRule, ProofStep
from web_group_proof import WebGroupProofView, build_web_partial_group_proof_view


def _visible_text(view: WebGroupProofView) -> str:
    return "\n".join(
        line.prefix + (line.statement_latex or "") + line.suffix
        for line in view.rendered_lines
    )


def test_outside_legacy_112_groups_is_renderable():
    result = make_partial_proof_result(
        n=100, k=20, status=ProofSearchStatus.NOT_SEARCHED,
        open_goals=("target",),
    )
    view = build_web_partial_group_proof_view(result)
    assert isinstance(view, WebGroupProofView)
    assert (view.n, view.k) == (100, 20)
    assert view.conclusion_latex == r"\pi_{120}^{100}"
    assert "未解決 Goal" in _visible_text(view)
    assert "□" not in _visible_text(view)


def test_partial_result_keeps_observed_steps_and_unresolved_goals():
    step = ProofStep(conclusion="observed", premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.PARTIAL,
        proven_steps=(step,), open_goals=("unknown",),
        references=("General theorem",),
    )
    view = build_partial_web_group_proof_view(result)
    assert len(view.steps) == 1
    assert "Reference" in _visible_text(view)
    assert "未解決 Goal" in _visible_text(view)
    assert "□" not in _visible_text(view)


def test_failed_and_unknown_state_does_not_claim_completion():
    result = make_partial_proof_result(
        n=17, k=4, status=ProofSearchStatus.SEARCH_FAILED,
        structure_status=GroupStructureStatus.UNKNOWN,
        open_goals=("no-rule",), diagnostics=("No applicable typed rule",),
    )
    view = build_partial_web_group_proof_view(result)
    text = _visible_text(view)
    assert "探索診断" in text
    assert "No applicable typed rule" in text
    assert "□" not in text


def test_complete_result_retains_qed():
    step = ProofStep(conclusion="proved", premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=4, k=2, status=ProofSearchStatus.COMPLETE,
        proven_steps=(step,), conclusion="proved",
    )
    view = build_partial_web_group_proof_view(result)
    assert "□" in _visible_text(view)


def test_rejects_invalid_mode_and_depth():
    result = make_partial_proof_result(n=2, k=0, status=ProofSearchStatus.NOT_SEARCHED)
    with pytest.raises(ValueError, match="mode"):
        build_partial_web_group_proof_view(result, mode="unknown")
    with pytest.raises(ValueError, match="nonnegative"):
        build_partial_web_group_proof_view(result, max_depth=-1)
    with pytest.raises(TypeError, match="max_depth"):
        build_partial_web_group_proof_view(result, max_depth=True)
