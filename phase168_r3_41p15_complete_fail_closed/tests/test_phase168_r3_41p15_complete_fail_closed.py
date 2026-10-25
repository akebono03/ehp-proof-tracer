"""Phase 168 R3-41P15: complete Model handoff must fail closed."""
from __future__ import annotations

from unittest.mock import patch

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from proof import ProofRule, ProofStep
from web_group_proof import build_standard_web_group_proof_view
from phase168_r3_41p14_trust_boundary_audit.audit import probe_web_route


@pytest.mark.parametrize("context,positioned", ((False, True), (True, False)))
def test_missing_required_complete_context_fails_before_model(context, positioned):
    row = probe_web_route(context=context, positioned=positioned)
    assert row["status"] == "complete"
    assert row["rejected"] is True
    assert row["verify"] == 0
    assert row["model"] == 0
    assert row["render"] == 0


def test_complete_invokes_validator_even_for_unsupported_step_rule():
    # The P14 probe replaces the validator with an accepting mock, therefore
    # this assertion checks mandatory invocation, not genuine mathematical trust.
    row = probe_web_route(context=True, positioned=True, unsupported_rule=True)
    assert row["verify"] == 1
    assert row["model"] == 1
    assert row["render"] == 1
    assert row["rejected"] is False


def test_real_validator_rejects_unsupported_origin_before_model():
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import (
        AssertionEntry, AssertionKind, LiteratureEntry,
        ReferenceKind, UnifiedStatementRegistry,
    )

    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="synthetic-target-ref", kind=ReferenceKind.PROPOSITION,
        locator="Synthetic target", publication_position=200,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="synthetic-target", reference_id="synthetic-target-ref",
        kind=AssertionKind.STATEMENT, content="synthetic conclusion",
    ))
    bridge = RegistryBridgeResult(registry, (), ())
    step = ProofStep(
        conclusion="synthetic conclusion", premises=(), rule=ProofRule.RELATION,
    )
    result = make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(step,), conclusion=step.conclusion,
    )
    with pytest.raises(UnverifiedProofTree, match="unsupported proof-step origin"):
        verify_proof_tree_for_narrative(
            result, bridge, citing_assertion_id="synthetic-target",
        )


def test_actual_boundary_rejection_prevents_any_model_projection():
    row = probe_web_route(context=True, positioned=True, reject=True)
    assert row["verify"] == 1
    assert row["rejected"] is True
    assert row["model"] == 0
    assert row["render"] == 0


def test_partial_keeps_model_route_without_validation_claim():
    row = probe_web_route(context=True, positioned=True, partial=True)
    assert row["status"] == "partial"
    assert row["verify"] == 0
    assert row["model"] == 1
    assert row["render"] == 1
    assert row["rejected"] is False


@pytest.mark.parametrize("route", (("trace", "model"), ("narrative", "legacy")))
def test_explicit_compatibility_web_paths_remain_unchanged(route):
    mode, citation_source = route
    searched = object()
    view = object()
    with (
        patch("phase165_r55_nk_only_goal.search_group_from_registered_goal", return_value=searched) as search,
        patch("phase165_r52_r3_web_adapter.build_partial_web_group_proof_view", return_value=view) as renderer,
        patch("phase165_r52_r9_shared_math.build_shared_typed_bridge") as bridge,
        patch("phase168_r3_4_link_bridge.build_linked_proof_narrative_model") as projector,
    ):
        actual = build_standard_web_group_proof_view(
            n=2, k=1, mode=mode, citation_source=citation_source,
        )
    assert actual is view
    search.assert_called_once()
    renderer.assert_called_once()
    bridge.assert_not_called()
    projector.assert_not_called()
