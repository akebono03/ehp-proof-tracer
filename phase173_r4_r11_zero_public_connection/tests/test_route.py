"""Focused mathematical, source and Web checks prior to production patch."""
from __future__ import annotations

from pathlib import Path

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import (
    exact_prior_database_result,
    verified_db_step,
)
from phase173_r4_r10_general_toda56_core.core import (
    GENERAL_ROOT_NAME,
    checked_general_inputs,
)
from phase173_r4_r11_zero_public_connection.route import (
    prepare_zero_toda56_public_connection,
)
from phase173_r4_r11_zero_public_connection.source import (
    screened_zero_toda56_context,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    TodaLemma54TypedSource,
)
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


def _prepared():
    original = build_shared_typed_bridge()
    goal = exact_prior_database_result(4, 7)
    assert isinstance(goal, TodaPrimaryGroupZeroStatement)
    prepared = prepare_zero_toda56_public_connection(bridge=original, goal=goal)
    assert prepared is not None
    return original, goal, prepared


def test_source_screen_preserves_original_registry() -> None:
    original, goal, (screened, provider) = _prepared()
    assert callable(provider)
    assert ADOPTED_ASSERTION_ID not in original.registry._assertions
    assert ADOPTED_ASSERTION_ID in screened.registry._assertions
    assert not any(link.step is not None and link.step.conclusion == goal
                   for link in screened.proof_links)
    inputs = checked_general_inputs(goal)
    assert inputs is not None
    assert all(isinstance(item, TodaPrimaryGroupZeroStatement) for item in inputs)
    assert all(not (link.step is not None and link.step.conclusion in inputs)
               for link in screened.proof_links)
    assert sum(link.step is not None and link.step.conclusion == TodaLemma54TypedSource()
               for link in screened.proof_links) == 1


def test_screen_rejects_wrong_target_and_source_missing() -> None:
    bridge = build_shared_typed_bridge()
    goal = exact_prior_database_result(4, 8)
    assert prepare_zero_toda56_public_connection(bridge=bridge, goal=goal) is None
    text = (Path(__file__).resolve().parents[2] / "sources/toda/Toda_05_2.tex").read_text(
        encoding="utf-8-sig",
    )
    zero_goal = exact_prior_database_result(4, 7)
    # The validated original text is required (not a synthetically provided lemma).
    import pytest
    with pytest.raises(ValueError):
        screened_zero_toda56_context(bridge, goal=zero_goal, chapter="not a source")
    assert text


def test_zero_root_discharge_before_public_install() -> None:
    _, goal, (screened, provider) = _prepared()
    context_id = next(iter(screened.registry._assertions))
    result = search_registered_partial_proof(
        n=4, k=7, goal=goal, bridge=screened,
        citing_assertion_id=context_id, expansion_provider=provider,
        lookup_mode="typed_reference",
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    roots = tuple(step for step in result.proven_steps if step.conclusion == goal
                  and step.rule is ProofRule.INFERENCE
                  and step.inference_rule is not None
                  and step.inference_rule.name == GENERAL_ROOT_NAME)
    assert len(roots) == 1
    root = roots[0]
    assert len(root.premises) == 4
    assert root.inference_rule.match_guard(root.premises, {})
    assert verified_db_step(root.premises[1], proof_target=goal, bridge=screened)
    assert verified_db_step(root.premises[2], proof_target=goal, bridge=screened)


def test_zero_web_trust_boundary_before_install(monkeypatch) -> None:
    """Test the real Web trust boundary with an injected isolated route."""
    import phase165_r55_nk_only_goal as group_query
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    original_search = group_query.search_group_from_registered_goal

    def injected(*, n, k, bridge=None, proof_order_catalog=None, goal=None,
                 context_sink=None):
        if n != 4 or k != 7:
            return original_search(n=n, k=k, bridge=bridge,
                                   proof_order_catalog=proof_order_catalog,
                                   goal=goal, context_sink=context_sink)
        if bridge is None:
            bridge = build_shared_typed_bridge()
        candidate = exact_prior_database_result(4, 7)
        screened, provider = prepare_zero_toda56_public_connection(
            bridge=bridge, goal=candidate,
        )
        if context_sink is not None:
            context_sink(screened)
        return search_registered_partial_proof(
            n=n, k=k, goal=candidate, bridge=screened,
            citing_assertion_id=next(iter(bridge.registry._assertions)),
            expansion_provider=provider, lookup_mode="typed_reference",
        )

    monkeypatch.setattr(group_query, "search_group_from_registered_goal", injected)
    view = build_standard_web_group_proof_view(
        n=4, k=7, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert view.rendered_lines
