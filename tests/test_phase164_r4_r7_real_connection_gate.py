"""Phase 164 R4-R7 focused real typed citation gate tests."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r7_real_connection_gate import (
    _make_distinct_proof_context,
    audit_phase164_r4_r7_connection,
)
from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings
from phase164_r2_citation_eligibility import assess_phase164_r2_citation
from phase164_r3_registry_search_connection import RegisteredLiteraturePremise, reconstruct_phase164_r3_pi5_3
from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement


@pytest.fixture(scope="module")
def prepared():
    crosswalk = audit_current_repository(Path("phase163_r4_r94_output/manifest.json"))
    leaves = build_phase59_3_data()["premise_steps"]
    return crosswalk, leaves


def test_real_bindings_are_screened_and_not_auto_approved(prepared):
    result = audit_phase164_r4_r7_connection(*prepared, user_confirmed_original=True)
    assert result.r3_rejected is True
    assert len(result.cited_assertion_ids) == 2
    assert result.accepted_assertion_ids == ()
    assert result.citation_reasons == (
        "independent_verification_not_recorded",
        "independent_verification_not_recorded",
    )


def test_baseline_proof_remains_seven_steps_four_exactness(prepared):
    result = audit_phase164_r4_r7_connection(*prepared, user_confirmed_original=True)
    assert result.legacy_derived_step_count == 7
    assert result.exactness_leaf_count == 4
    assert result.verified_inferences >= 7
    assert result.external_citation_order_supported is False


def test_distinct_proof_reference_does_not_invent_toda_order(prepared):
    crosswalk, leaves = prepared
    literature = tuple(step for step in leaves if step.rule is ProofRule.INFERENCE)
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, literature, user_confirmed_original=True,
    )
    bridge = _make_distinct_proof_context(registration.bridge)
    citing = bridge.registry.assertion("ehp-proof-tracer:pi5_3:isomorphism:goal")
    destination = bridge.registry.reference(citing.reference_id)
    assert destination.publication_position is None
    assert destination.source_id != bridge.registry.reference(
        bridge.registry.assertion(registration.bindings[0].assertion_id).reference_id
    ).source_id
    for binding in registration.bindings:
        assert bridge.registry.assertion(binding.assertion_id).available_after_position is None
        decision = assess_phase164_r2_citation(
            bridge, binding.assertion_id, citing.assertion_id,
            verified_assertion_ids=(),
        )
        assert decision.usable is False


def test_missing_user_confirmation_rejected(prepared):
    with pytest.raises(ValueError, match="explicit user"):
        audit_phase164_r4_r7_connection(*prepared, user_confirmed_original=False)


def test_exactness_missing_is_rejected(prepared):
    crosswalk, leaves = prepared
    with pytest.raises(ValueError, match="six existing leaves"):
        audit_phase164_r4_r7_connection(crosswalk, leaves[:-1], user_confirmed_original=True)


def test_registry_search_never_returns_success_with_unapproved_ids(prepared):
    crosswalk, leaves = prepared
    literature = tuple(step for step in leaves if step.rule is ProofRule.INFERENCE)
    exactness = tuple(step for step in leaves if isinstance(step.conclusion, TodaProp42ExactnessStatement))
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, literature, user_confirmed_original=True,
    )
    bridge = _make_distinct_proof_context(registration.bridge)
    mapped = tuple(RegisteredLiteraturePremise(binding.assertion_id, binding.step)
                   for binding in registration.bindings)
    roots = {}
    seen = set()
    def walk(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        if step.rule is ProofRule.GIVEN:
            roots[id(step)] = step
        for parent in step.premises:
            walk(parent)
    for step in leaves:
        walk(step)
    with pytest.raises(ValueError, match="citation not eligible"):
        reconstruct_phase164_r3_pi5_3(
            bridge, "ehp-proof-tracer:pi5_3:isomorphism:goal",
            mapped, exactness, tuple(roots.values()), verified_assertion_ids=(),
        )


def test_tampered_source_identity_is_rejected(prepared):
    crosswalk, leaves = prepared
    bad = dict(crosswalk)
    bad["leaves"] = [dict(row) for row in crosswalk["leaves"]]
    bad["leaves"][1]["source_statement_id"] = "toda:tex:invalid"
    with pytest.raises(ValueError):
        audit_phase164_r4_r7_connection(bad, leaves, user_confirmed_original=True)
