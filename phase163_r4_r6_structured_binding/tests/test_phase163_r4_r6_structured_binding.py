from dataclasses import replace

import pytest

from phase163_r4_r6_structured_binding import (
    FixedStatementBinding,
    bind_verified_fixed_statements,
)
from phase163_r4_registry_bridge import (
    MigrationStatus,
    build_registry_bridge,
)
from proof import (
    FoundationalReferenceIdentity,
    InferenceRule,
    LiteratureReference,
    ProofRule,
    ProofStep,
    Relation,
)
from toda_literature_statement_boundary import get_toda_fixed_statement_component


LOCATOR = "(5.3)"
COMPONENT = "nu_prime_hopf_relation"


def _citation(conclusion):
    identity = FoundationalReferenceIdentity(
        key=f"literature:{LOCATOR}:{COMPONENT}",
        label=LOCATOR,
    )
    leaf = ProofStep(
        conclusion=conclusion,
        premises=(),
        rule=ProofRule.GIVEN,
        foundational_reference=identity,
    )
    return ProofStep(
        conclusion=conclusion,
        premises=(leaf,),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(
            name="phase162_verified_literature_citation",
            literature_reference=LiteratureReference(label="Toda (5.3)", locator=LOCATOR),
        ),
        foundational_reference=identity,
    )


def _binding():
    statement = Relation(lhs="H(nu_prime)", rhs="eta_5")
    return FixedStatementBinding(
        reference_locator=LOCATOR,
        component_key=COMPONENT,
        citation_step=_citation(statement),
        expected_conclusion=statement,
    )


def test_r4_r6_upgrades_only_selected_component():
    base = build_registry_bridge()
    binding = _binding()
    result = bind_verified_fixed_statements(base, (binding,))
    key = f"boundary:{LOCATOR}:{COMPONENT}"
    assert result.registry.assertion(key).content is binding.citation_step.conclusion
    assert result.registry.assertion(key).reference_id == f"toda:{LOCATOR}"
    assert len(result.proof_links) == len(base.proof_links) + 1
    assert next(r for r in result.records if r.assertion_id == key).status is MigrationStatus.STRUCTURED
    assert next(r for r in base.records if r.assertion_id == key).status is MigrationStatus.METADATA_ONLY
    assert base.registry.assertion(key).content == get_toda_fixed_statement_component(LOCATOR, COMPONENT)


def test_r4_r6_keeps_other_components_metadata_only():
    base = build_registry_bridge()
    result = bind_verified_fixed_statements(base, (_binding(),))
    for record in base.records:
        if record.assertion_id != f"boundary:{LOCATOR}:{COMPONENT}":
            assert next(r for r in result.records if r.source == record.source and r.source_key == record.source_key) == record


def test_r4_r6_rejects_mismatch():
    base = build_registry_bridge()
    binding = _binding()
    with pytest.raises(ValueError, match="Invalid fixed-statement citation"):
        bind_verified_fixed_statements(base, (replace(binding, expected_conclusion="false"),))


def test_r4_r6_rejects_unverified_witness():
    base = build_registry_bridge()
    binding = _binding()
    bad = replace(binding.citation_step, inference_rule=InferenceRule(name="not_verified"))
    with pytest.raises(ValueError, match="Invalid fixed-statement citation"):
        bind_verified_fixed_statements(base, (replace(binding, citation_step=bad),))


def test_r4_r6_rejects_unregistered_component():
    base = build_registry_bridge()
    binding = _binding()
    with pytest.raises(KeyError):
        bind_verified_fixed_statements(base, (replace(binding, component_key="invented"),))


def test_r4_r6_rejects_duplicate_binding():
    base = build_registry_bridge()
    binding = _binding()
    with pytest.raises(ValueError, match="duplicate binding"):
        bind_verified_fixed_statements(base, (binding, binding))


def test_r4_r6_empty_is_unchanged():
    base = build_registry_bridge()
    result = bind_verified_fixed_statements(base, ())
    assert result.records == base.records
    assert result.proof_links == base.proof_links
