"""R3 focused routing and evidence-preservation checks."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase165_r52_partial_proof import (
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)
from phase165_renderer_narrative_model import build_narrative_proof_model
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative
from toda_group_proof_narrative_renderer import (
    render_narrative_proof_model,
    render_toda_partial_proof_narrative_markdown,
)


def test_r3_completed_public_uses_original_narrative():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    assert render_partial_proof_markdown(result) == render_completed_shared_narrative(result)


def test_r3_incomplete_public_uses_original_partial_narrative():
    result = search_group_from_registered_goal(n=3, k=1)
    assert result.status is not ProofSearchStatus.COMPLETE
    assert render_partial_proof_markdown(result) == render_toda_partial_proof_narrative_markdown(result)


def test_r3_large_unsearched_target_preserved():
    result = make_partial_proof_result(n=200, k=90, status=ProofSearchStatus.NOT_SEARCHED)
    markdown = render_partial_proof_markdown(result)
    assert r"\pi_{290}^{200}" in markdown
    assert "□" not in markdown


def test_r3_model_dispatch_identity():
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.SEARCH_FAILED,
        diagnostics=("missing premise",), open_goals=("goal",),
    )
    model = build_narrative_proof_model(result)
    assert model.source is result
    assert render_narrative_proof_model(model) == render_partial_proof_markdown(result)


def test_r3_dispatch_rejects_non_model():
    with pytest.raises(TypeError):
        render_narrative_proof_model(object())


def test_r3_public_only_dispatches_through_model():
    text = (Path(__file__).resolve().parent.parent / "phase165_r52_partial_proof.py").read_text(encoding="utf8")
    assert "render_narrative_proof_model(build_narrative_proof_model(result))" in text


def test_r3_does_not_restore_duplicate_generic_file():
    project = Path(__file__).resolve().parent.parent
    assert not (project / "toda_group_proof_generic_narrative_renderer.py").exists()
