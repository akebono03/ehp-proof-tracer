import pytest

from proof import ProofRule, ProofStep
from phase165_r52_partial_proof import (
    GroupStructureStatus,
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)


def test_r52_arbitrary_range_and_unknown():
    result = make_partial_proof_result(n=200, k=90, status=ProofSearchStatus.NOT_SEARCHED)
    text = render_partial_proof_markdown(result)
    assert r"\pi_{290}^{200}" in text
    assert "unknown" in text
    assert "□" not in text


def test_r52_partial_preserves_steps_and_goals():
    step = ProofStep(conclusion="typed_known", premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.PARTIAL,
        structure_status=GroupStructureStatus.KNOWN,
        references=("Toda Proposition 5.1",),
        proven_steps=(step,), open_goals=("typed_missing",),
    )
    text = render_partial_proof_markdown(result)
    assert "typed_known" in text and "typed_missing" in text
    assert text.index("Reference") < text.index("Proof（導出済み）") < text.index("未解決 Goal")
    assert "□" not in text


def test_r52_complete_requires_matching_step():
    step = ProofStep(conclusion="final", premises=(), rule=ProofRule.GIVEN)
    valid = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.COMPLETE,
        proven_steps=(step,), conclusion="final",
    )
    assert "□" in render_partial_proof_markdown(valid)
    with pytest.raises(ValueError):
        make_partial_proof_result(n=3, k=2, status=ProofSearchStatus.COMPLETE, conclusion="final")
    with pytest.raises(ValueError):
        make_partial_proof_result(n=3, k=2, status=ProofSearchStatus.PARTIAL, conclusion="final")


def test_r52_failed_search_preserves_diagnostics():
    result = make_partial_proof_result(
        n=99, k=14, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("missing_rule",), diagnostics=("no matching inference rule",),
    )
    text = render_partial_proof_markdown(result)
    assert "missing_rule" in text and "no matching inference rule" in text
    assert "□" not in text


def test_r52_invalid_inputs():
    for n, k in ((1, 1), (2, -1), (True, 2)):
        with pytest.raises(ValueError):
            make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)
    with pytest.raises(ValueError):
        make_partial_proof_result(n=2, k=1, status=ProofSearchStatus.SEARCH_FAILED)
