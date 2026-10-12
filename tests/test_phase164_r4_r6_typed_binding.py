"""Phase 164 R4-R6 focused typed-binding tests."""
from dataclasses import replace

import pytest

from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings
from phase163_r3_registry_validation import audit_dependencies
from phase163_r4_registry_bridge import MigrationStatus
from proof import ProofRule
from toda_rules import TodaProp42ExactnessStatement
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from unified_statement_registry import AssertionOrigin


@pytest.fixture(scope="module")
def inputs():
    from pathlib import Path
    crosswalk = audit_current_repository(Path("phase163_r4_r94_output/manifest.json"))
    leaves = tuple(
        step for step in build_phase59_3_data()["premise_steps"]
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    return crosswalk, leaves


def test_registers_exact_two_typed_assertions(inputs):
    crosswalk, leaves = inputs
    result = register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=True)
    assert len(result.bindings) == 2
    assert len(result.bridge.records) == 2
    assert all(row.status is MigrationStatus.STRUCTURED for row in result.bridge.records)
    assert all(result.bridge.registry.assertion(b.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT for b in result.bindings)


def test_uses_original_leaf_identity_and_conclusion(inputs):
    crosswalk, leaves = inputs
    result = register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=True)
    for binding, leaf, link in zip(result.bindings, leaves, result.bridge.proof_links):
        assert binding.step is leaf
        assert link.step is leaf
        assert result.bridge.registry.assertion(binding.assertion_id).content is leaf.conclusion
        assert leaf.rule is ProofRule.INFERENCE


def test_explicit_source_confirmation_required(inputs):
    crosswalk, leaves = inputs
    with pytest.raises(ValueError, match="explicit user"):
        register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=False)


def test_tampered_manifest_pairing_rejected(inputs):
    crosswalk, leaves = inputs
    changed = dict(crosswalk)
    changed["leaves"] = [dict(row) for row in crosswalk["leaves"]]
    changed["leaves"][0]["source_statement_id"] = "toda:tex:ch5:incorrect"
    with pytest.raises(ValueError):
        register_phase164_r4_r6_typed_bindings(changed, leaves, user_confirmed_original=True)


def test_corrupted_math_rejected(inputs):
    crosswalk, leaves = inputs
    original = leaves[0].conclusion
    changed_delta = replace(original.delta_iota5_relation, positive_value=replace(original.delta_iota5_relation.positive_value, coefficient=3))
    changed_step = replace(leaves[0], conclusion=replace(original, delta_iota5_relation=changed_delta))
    with pytest.raises(ValueError, match="typed mathematical clause mismatch"):
        register_phase164_r4_r6_typed_bindings(crosswalk, (changed_step, leaves[1]), user_confirmed_original=True)


def test_no_availability_or_proof_search_promotion(inputs):
    crosswalk, leaves = inputs
    result = register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=True)
    assert result.citation_eligible is False
    assert result.proof_search_connected is False
    for binding in result.bindings:
        entry = result.bridge.registry.assertion(binding.assertion_id)
        ref = result.bridge.registry.reference(entry.reference_id)
        assert entry.available_after_position is None
        assert ref.publication_position is None
    assert audit_dependencies(result.bridge.registry).valid


def test_partial_statement_coverage_preserved(inputs):
    crosswalk, leaves = inputs
    result = register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=True)
    assert "excludes stable" in result.bindings[0].coverage
    assert "excludes membership" in result.bindings[1].coverage


def test_no_global_registry_mutation(inputs):
    from phase163_r4_registry_bridge import build_registry_bridge
    before = build_registry_bridge()
    before_count = len(before.records)
    crosswalk, leaves = inputs
    register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=True)
    after = build_registry_bridge()
    assert len(after.records) == before_count
