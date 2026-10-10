from dataclasses import replace

import pytest

from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from unified_statement_registry import LiteratureEntry, ReferenceKind
from phase163_r4_r8_choice_registration import build_nu_prime_choice
from phase163_r4_r9_declaration_catalog import (
    DeclarationKind,
    DeclarationProvenance,
    LiteratureDeclaration,
    adapt_r8_snapshot,
    register_declarations,
)
from proof import ProofRule, ProofStep
from toda_rules import toda_eta_family_definition_statement


def _definition():
    content = toda_eta_family_definition_statement(3)
    return LiteratureDeclaration(
        declaration_id="definition:eta3:test",
        reference_id="test:Definition 1",
        kind=DeclarationKind.DEFINITION,
        defined_symbol="eta_3",
        content=content,
        source_step=ProofStep(conclusion=content, premises=(), rule=ProofRule.GIVEN),
    )


def _base_with_test_reference():
    base = build_registry_bridge()
    base.registry.add_reference(LiteratureEntry(
        reference_id="test:Definition 1", kind=ReferenceKind.DEFINITION,
        locator="Definition 1", source_id="test_fixture_only",
    ))
    return base


def test_r4_r9_new_definition_can_be_registered_without_promoting_bridge():
    base = _base_with_test_reference()
    original_count = len(base.registry.assertions_for("test:Definition 1"))
    catalog = register_declarations(base, (_definition(),))
    assert catalog.find("definition:eta3:test").kind is DeclarationKind.DEFINITION
    assert len(base.registry.assertions_for("test:Definition 1")) == original_count
    assert catalog.find("definition:eta3:test").provenance is DeclarationProvenance.SOURCE_UNVERIFIED


def test_r4_r9_rejects_duplicate_declarations():
    d = _definition()
    with pytest.raises(ValueError, match="duplicate declaration_id"):
        register_declarations(_base_with_test_reference(), (d, d))


def test_r4_r9_rejects_unknown_reference():
    with pytest.raises(ValueError, match="unknown reference_id"):
        register_declarations(_base_with_test_reference(), (replace(_definition(), reference_id="toda:missing"),))


def test_r4_r9_rejects_unverified_external_source_promotion():
    with pytest.raises(ValueError, match="verification cannot be inferred"):
        replace(_definition(), provenance="verified")


def test_r4_r9_rejects_derived_source_step():
    step = _definition().source_step
    with pytest.raises(ValueError, match="leaf GIVEN"):
        replace(_definition(), source_step=replace(step, rule=ProofRule.INFERENCE))


def test_r4_r9_definition_cannot_be_plain_text():
    with pytest.raises(TypeError, match="typed mathematical object"):
        replace(_definition(), content="eta_3")


def test_r4_r9_mismatched_assertion_is_rejected():
    with pytest.raises(ValueError, match="assertion/reference mismatch"):
        register_declarations(_base_with_test_reference(), (
            replace(_definition(), assertion_id="boundary:Proposition 5.6:pi5_2_group_relation"),
        ))


def test_r4_r9_r8_choice_adapter_preserves_typed_bracket_and_metadata_only():
    from probes.probe_phase58_capabilities import build_phase58_representative_result
    base = build_registry_bridge()
    snapshot = build_nu_prime_choice(base, build_phase58_representative_result()["bracket_membership_step"])
    catalog = adapt_r8_snapshot(snapshot)
    entry = catalog.declarations[0]
    assert entry.kind is DeclarationKind.CHOICE
    assert entry.content.bracket.index == 1
    assert entry.content.bracket.second.coefficient == 2
    assert entry.assertion_id == "boundary:(5.3):nu_prime_bracket_definition"
    assert next(x.status for x in base.records if x.assertion_id == entry.assertion_id) is MigrationStatus.METADATA_ONLY
