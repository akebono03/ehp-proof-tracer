"""Focused 1-stem + existing 2-stem verified-projection regressions."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10a2_unified_one_stem.one_stem_projection import (
    project_verified_one_stem_notation_chain,
)
from phase169_r10a_verified_stable_chain_projection.projection import (
    project_verified_stable_image_chain,
)
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def screened_bridge():
    return build_shared_typed_bridge()


def _complete(n: int, k: int, bridge):
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    return result, model


def test_r10a2_one_stem_certified_projection_and_single_equation(screened_bridge):
    result, model = _complete(8, 1, screened_bridge)
    original_steps = tuple(model.steps)
    order = tuple(range(len(model.steps)))
    projection = project_verified_one_stem_notation_chain(model, order)
    assert projection is not None
    assert projection.root_index == model.root_index
    assert projection.exponent == 5
    assert projection.citation_numbers
    assert all(model.steps[i].rule is ProofRule.INFERENCE for i in projection.hidden_indices)
    assert len(projection.hidden_indices) >= 2
    narrative = render_model_backed_narrative_markdown(result, model)
    assert tuple(model.steps) == original_steps
    assert narrative.count(r"$E^{5}(\eta_{3})=\eta_{8}$") == 1
    assert r"E(\eta_{7})=\eta_{8}" not in narrative
    assert r"\mathbb{Z}/2\{E^{5}" not in narrative
    assert r"\pi_{9}^{8} = \mathbb{Z}/2\{\eta_{8}\}" in narrative
    assert narrative.rstrip().endswith("□")
    web = build_standard_web_group_proof_view(8, 1, mode="narrative")
    assert web.key == "generic-complete-proof"
    assert not web.partial_result
    assert len(web.steps) == len(result.proven_steps)


@pytest.mark.parametrize("n,k", [(6,2), (7,2), (8,2)])
def test_r10a2_two_stem_proof_display_unchanged(n, k, screened_bridge):
    result, model = _complete(n, k, screened_bridge)
    assert project_verified_one_stem_notation_chain(
        model, tuple(range(len(model.steps))),
    ) is None
    narrative = render_model_backed_narrative_markdown(result, model)
    assert narrative.rstrip().endswith("□")
    assert len(model.steps) == len(result.proven_steps)
    if n == 8:
        chain = project_verified_stable_image_chain(model, tuple(range(len(model.steps))))
        assert chain is not None and chain.exponent == 4
        assert narrative.count(r"$E^{4}(\eta_{4}^{2})=\eta_{8}^{2}$") == 1


def test_r10a2_premature_partial_model_never_compresses(screened_bridge):
    result, model = _complete(8, 1, screened_bridge)
    from dataclasses import replace
    from phase165_r52_partial_proof import ProofSearchStatus
    invalid = replace(model, root_index=None)
    assert project_verified_one_stem_notation_chain(
        invalid, tuple(range(len(model.steps))),
    ) is None
    invalid = replace(model, step_citation_numbers=tuple(() for _ in model.steps))
    assert project_verified_one_stem_notation_chain(
        invalid, tuple(range(len(model.steps))),
    ) is None


def test_r10a2_patch_preserves_full_renderer_and_refuses_unreviewed_changes():
    from phase169_r10a2_unified_one_stem.patch import (
        OLD_IMPORT, NEW_IMPORT, OLD_TRANSITION, NEW_TRANSITION,
        replacement_content,
    )
    import pytest
    sample = (
        'def render_model_backed_narrative_markdown(result, model):\n'
        + OLD_IMPORT + OLD_TRANSITION
        + '    return "verified"\n'
    ).encode("utf-8")
    changed, full = replacement_content(sample, sample)
    assert NEW_IMPORT in full and NEW_TRANSITION in full
    assert changed.count(b"project_verified_one_stem_notation_chain") == 2
    assert "def render_model_backed_narrative_markdown" in full
    with pytest.raises(RuntimeError, match="differs"):
        replacement_content(sample + b"#dirty\n", sample)
    with pytest.raises(RuntimeError, match="missing or duplicated"):
        replacement_content(changed, changed)
