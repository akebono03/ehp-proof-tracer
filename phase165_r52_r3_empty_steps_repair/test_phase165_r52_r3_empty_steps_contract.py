"""R52-R3 regression: completed views retain legacy invariant."""

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from web_group_proof import WebGroupProofView


def test_legacy_completed_view_rejects_empty_steps():
    with pytest.raises(ValueError, match="steps must not be empty"):
        WebGroupProofView(
            n=3, k=2, conclusion_latex=r"\pi_{5}^{3}",
            theorem=None, phase=None, key="legacy", steps=(), max_depth=0,
        )


def test_explicit_partial_view_accepts_empty_steps():
    result = make_partial_proof_result(
        n=100, k=20, status=ProofSearchStatus.NOT_SEARCHED,
    )
    view = build_partial_web_group_proof_view(result)
    assert view.partial_result is True
    assert view.steps == ()
    assert view.rendered_lines


def test_partial_view_flag_rejects_non_bool():
    with pytest.raises(TypeError, match="partial_result"):
        WebGroupProofView(
            n=3, k=2, conclusion_latex=r"\pi_{5}^{3}",
            theorem=None, phase=None, key="invalid", steps=(),
            max_depth=0, partial_result="true",
        )
