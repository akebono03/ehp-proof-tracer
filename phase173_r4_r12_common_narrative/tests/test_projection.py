"""Focused live verified-proof narrative tests; no production edits."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase173_r4_r12_common_narrative.projection import (
    project_verified_toda56_narrative,
)
from phase173_r4_r1_narrative_source_fix.projection import (
    project_verified_pi74_narrative,
)
from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result


def _proof(dimension: int):
    original = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=dimension - 4, bridge=original, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    assert len(contexts) == 1
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    return result, model, markdown


def test_pi74_existing_projection_remains_byte_equal() -> None:
    result, model, markdown = _proof(7)
    expected = project_verified_pi74_narrative(result, model, markdown)
    assert project_verified_toda56_narrative(result, model, markdown) == expected


@pytest.mark.parametrize("dimension", (8, 9, 10, 11))
def test_common_projector_uses_proven_model_sources(dimension: int) -> None:
    result, model, markdown = _proof(dimension)
    shown = project_verified_toda56_narrative(result, model, markdown)
    assert "使用する結果" in shown
    assert shown.count("\n証明\n") == 1
    assert "Proposition 4.4" in shown
    assert rf"\pi_{{{dimension - 1}}}^3\oplus\pi_{{{dimension}}}^7" in shown
    assert rf"\Phi_{{{dimension}}}" in shown
    assert rf"i={dimension}" in shown
    assert r"\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}" in shown
    assert r"\nu_4\circ\gamma" in shown
    assert "先行データベース結果" in shown or "DB prior: sphere.csv" in shown
    assert shown.endswith("□\n")
    if dimension == 11:
        assert "零群" in shown
        assert r"\pi_{11}^{4} = 0" in shown
    else:
        assert "生成元の対応" in shown
        assert rf"\Phi_{{{dimension}}}(" in shown


def test_incomplete_result_is_not_projected() -> None:
    result, model, markdown = _proof(8)
    partial = replace(
        result, status=ProofSearchStatus.PARTIAL,
        conclusion=None, open_goals=(result.target,),
    )
    assert project_verified_toda56_narrative(partial, model, markdown) == markdown


def test_unproven_epsilon_never_selected_by_general_root() -> None:
    candidate = exact_prior_database_result(4, 8)
    assert candidate is not None
    assert checked_general_inputs(candidate) is None
