from dataclasses import replace

import pytest

from phase163_r4_r7_representative_bindings import (
    WitnessCandidate,
    bind_representative_witnesses,
)
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from proof import (
    FoundationalReferenceIdentity,
    InferenceRule,
    LiteratureReference,
    ProofRule,
    ProofStep,
    Relation,
)


LOCATOR = "(5.3)"
KEY = "nu_prime_hopf_relation"


def _derived():
    given = ProofStep(conclusion="input", premises=(), rule=ProofRule.GIVEN)
    conclusion = Relation(lhs="H(nu_prime)", rhs="eta_5")
    return ProofStep(conclusion=conclusion, premises=(given,), rule=ProofRule.INFERENCE)


def _citation(witness, locator, component, expected):
    identity = FoundationalReferenceIdentity(
        key=f"literature:{locator}:{component}", label=locator
    )
    leaf = ProofStep(
        conclusion=expected, premises=(), rule=ProofRule.GIVEN,
        foundational_reference=identity,
    )
    return ProofStep(
        conclusion=expected, premises=(leaf,), rule=ProofRule.INFERENCE,
        foundational_reference=identity,
        inference_rule=InferenceRule(
            name="phase162_verified_literature_citation",
            literature_reference=LiteratureReference(label="Toda " + locator, locator=locator),
        ),
    )


def _candidate():
    step = _derived()
    return WitnessCandidate(LOCATOR, KEY, step, step.conclusion, "test fixture")


def test_r4_r7_accepted_typed_citation_keeps_original_metadata():
    base = build_registry_bridge()
    result, attempts = bind_representative_witnesses(
        base, (_candidate(),), citation_builder=_citation
    )
    assert attempts[0].status == "STRUCTURED"
    assertion_id = f"boundary:{LOCATOR}:{KEY}"
    assert result.registry.assertion(assertion_id).content == _candidate().expected_conclusion
    assert next(r for r in result.records if r.assertion_id == assertion_id).status is MigrationStatus.STRUCTURED
    assert next(r for r in base.records if r.assertion_id == assertion_id).status is MigrationStatus.METADATA_ONLY


def test_r4_r7_given_is_not_promoted():
    base = build_registry_bridge()
    candidate = _candidate()
    given = ProofStep(conclusion=candidate.expected_conclusion, premises=(), rule=ProofRule.GIVEN)
    result, attempts = bind_representative_witnesses(
        base, (replace(candidate, witness=given),), citation_builder=_citation
    )
    assert attempts[0].status == "GIVEN_UNVERIFIED"
    assert result.records == base.records


def test_r4_r7_rejects_invalid_citation_without_promotion():
    base = build_registry_bridge()
    def invalid(witness, locator, component, expected):
        return witness
    result, attempts = bind_representative_witnesses(
        base, (_candidate(),), citation_builder=invalid
    )
    assert attempts[0].status == "VERIFICATION_FAILED"
    assert result.records == base.records


def test_r4_r7_unregistered_component_is_not_promoted():
    base = build_registry_bridge()
    candidate = replace(_candidate(), component_key="not_in_registry")
    result, attempts = bind_representative_witnesses(
        base, (candidate,), citation_builder=_citation
    )
    assert attempts[0].status == "NOT_REGISTERED"
    assert result.records == base.records


def test_r4_r7_duplicate_rejected():
    base = build_registry_bridge()
    candidate = _candidate()
    with pytest.raises(ValueError, match="duplicate"):
        bind_representative_witnesses(base, (candidate, candidate), citation_builder=_citation)


def test_r4_r7_conclusion_mismatch_rejected():
    with pytest.raises(ValueError, match="must match"):
        WitnessCandidate(LOCATOR, KEY, _derived(), "not a conclusion", "test")
