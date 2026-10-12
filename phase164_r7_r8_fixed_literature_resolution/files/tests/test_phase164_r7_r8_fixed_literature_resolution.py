"""Phase 164 R7-R8: special fixed-literature resolution stays separate from R2 citation."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings
from phase164_r4_r8_registry_reconstruction import (
    _known_trusted_roots,
    reconstruct_phase164_r4_r8_pi5_3,
)
from phase164_r7_statement_resolution import resolve_registered_statement
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from unified_statement_registry import AssertionOrigin


@pytest.fixture(scope="module")
def source_case():
    leaves = build_phase59_3_data()["premise_steps"]
    literature = tuple(step for step in leaves if step.rule is ProofRule.INFERENCE)
    crosswalk = audit_current_repository(Path("phase163_r4_r94_output/manifest.json"))
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, literature, user_confirmed_original=True,
    )
    return crosswalk, leaves, literature, registration


def _resolve(registration, index=0, **kwargs):
    binding = registration.bindings[index]
    arguments = dict(
        expected_conclusion=binding.step.conclusion,
        confirmed_fixed_step=binding.step,
        confirmed_source_locator=binding.locator,
        source_confirmation_recorded=True,
    )
    arguments.update(kwargs)
    return resolve_registered_statement(registration.bridge, binding.assertion_id, **arguments)


def test_r78_both_confirmed_references_preserve_exact_proof_steps(source_case):
    _, _, _, reg = source_case
    for index in range(2):
        resolved = _resolve(reg, index)
        assert resolved.assertion.origin is AssertionOrigin.FIXED_STATEMENT
        assert resolved.proof_link is reg.bridge.proof_links[index]
        assert resolved.proof_link.step is reg.bindings[index].step
        assert resolved.reference.publication_position is None
        assert resolved.assertion.available_after_position is None


def test_r78_requires_original_source_confirmation(source_case):
    _, _, _, reg = source_case
    with pytest.raises(ValueError, match="source confirmation"):
        _resolve(reg, source_confirmation_recorded=False)


def test_r78_rejects_wrong_locator(source_case):
    _, _, _, reg = source_case
    with pytest.raises(ValueError, match="locator mismatch"):
        _resolve(reg, confirmed_source_locator="(5.4)")


def test_r78_rejects_cloned_step(source_case):
    _, _, _, reg = source_case
    altered = replace(reg.bindings[0].step)
    with pytest.raises(ValueError, match="conclusion identity mismatch|ProofStep identity mismatch"):
        _resolve(reg, confirmed_fixed_step=altered)


def test_r78_does_not_grant_r2_citation(source_case):
    _, _, _, reg = source_case
    with pytest.raises(ValueError, match="not R2 citation approval"):
        _resolve(reg, citing_assertion_id=reg.bindings[1].assertion_id)


def test_r78_ordinary_resolver_still_rejects_fixed_proof_link(source_case):
    _, _, _, reg = source_case
    with pytest.raises(ValueError, match="fixed literature cannot inherit internal proof link"):
        resolve_registered_statement(reg.bridge, reg.bindings[0].assertion_id)


def test_r78_rejects_changed_availability_position(source_case):
    _, _, _, reg = source_case
    assertion = reg.bridge.registry.assertion(reg.bindings[0].assertion_id)
    # mutate the local isolated registry only; never change production data
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import UnifiedStatementRegistry
    new_registry = UnifiedStatementRegistry()
    for b in reg.bindings:
        ref = reg.bridge.registry.reference("toda:" + b.locator)
        new_registry.add_reference(ref)
        old = reg.bridge.registry.assertion(b.assertion_id)
        new_registry.add_assertion(replace(old, available_after_position=1) if b.assertion_id == assertion.assertion_id else old)
    mutated = RegistryBridgeResult(new_registry, reg.bridge.records, reg.bridge.proof_links)
    with pytest.raises(ValueError, match="publication boundary changed"):
        resolve_registered_statement(
            mutated, assertion.assertion_id,
            expected_conclusion=reg.bindings[0].step.conclusion,
            confirmed_fixed_step=reg.bindings[0].step,
            confirmed_source_locator=reg.bindings[0].locator,
            source_confirmation_recorded=True,
        )


def test_r78_existing_pi53_proof_reconstructs(source_case):
    crosswalk, leaves, _, _ = source_case
    result = reconstruct_phase164_r4_r8_pi5_3(
        crosswalk, leaves, _known_trusted_roots(leaves),
        user_confirmed_original=True,
    )
    assert len(result.validated.reconstruction.derived_steps) == 7
    assert result.citation_mode == "confirmed_fixed_literature"
