from dataclasses import dataclass
from types import SimpleNamespace

import pytest

from phase163_r4_registry_bridge import (
    MigrationStatus,
    build_registry_bridge,
)
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class Component:
    reference_locator: str
    component_key: str
    order: int | None = None
    range_text: str | None = None


def fixture_catalog():
    return {
        "(5.3)": (
            Component("(5.3)", "nu_prime_bracket_definition"),
            Component("(5.3)", "nu_prime_hopf_relation"),
        ),
        "Proposition 5.3": (
            Component("Proposition 5.3", "pi4_2", 1),
            Component("Proposition 5.3", "pi5_3", 2),
        ),
    }


def test_distinct_components_and_unknown_availability():
    result = build_registry_bridge(
        components_by_reference=fixture_catalog(),
        theorem_facts=SimpleNamespace(entries=()),
    )
    entries = result.registry.assertions_for("toda:(5.3)")
    assert len(entries) == 2
    assert entries[0].assertion_id != entries[1].assertion_id
    assert all(entry.available_after_position is None for entry in entries)
    assert all(record.status is MigrationStatus.METADATA_ONLY
               for record in result.records)


def test_component_order_does_not_grant_citation_availability():
    result = build_registry_bridge(
        components_by_reference=fixture_catalog(),
        theorem_facts=SimpleNamespace(entries=()),
    )
    first, second = result.registry.assertions_for("toda:Proposition 5.3")
    assert (first.component_position, second.component_position) == (1, 2)
    assert first.available_after_position is None
    assert second.available_after_position is None


def test_definition_like_component_keeps_source_kind_equation():
    result = build_registry_bridge(
        components_by_reference=fixture_catalog(),
        theorem_facts=SimpleNamespace(entries=()),
    )
    assert result.registry.reference("toda:(5.3)").kind.value == "equation"
    assert result.registry.assertions_for("toda:(5.3)")[0].kind.value == "statement"


def test_missing_theorem_locator_is_explicitly_unresolved():
    facts = SimpleNamespace(entries=(SimpleNamespace(
        reference=SimpleNamespace(label="Toda", locator=None),
        statement=object(),
    ),))
    result = build_registry_bridge(components_by_reference={}, theorem_facts=facts)
    assert len(result.unresolved) == 1
    assert result.unresolved[0].assertion_id is None


def test_theorem_fact_preserves_concrete_statement():
    statement = object()
    fact = SimpleNamespace(
        reference=SimpleNamespace(label="Toda", locator="Lemma 5.2"),
        statement=statement,
    )
    result = build_registry_bridge(
        components_by_reference={},
        theorem_facts=SimpleNamespace(entries=(fact,)),
    )
    entry = result.registry.assertions_for("fact:Toda:Lemma 5.2")[0]
    assert entry.content is statement
    assert result.records[0].status is MigrationStatus.STRUCTURED


def test_component_locator_mismatch_rejected():
    with pytest.raises(ValueError, match="locator mismatch"):
        build_registry_bridge(
            components_by_reference={"(5.3)": (Component("(5.4)", "x"),)},
            theorem_facts=SimpleNamespace(entries=()),
        )


def test_duplicate_component_key_rejected():
    with pytest.raises(ValueError, match="duplicate assertion_id"):
        build_registry_bridge(
            components_by_reference={"(5.3)": (
                Component("(5.3)", "x"), Component("(5.3)", "x"),
            )},
            theorem_facts=SimpleNamespace(entries=()),
        )


def test_explicit_proof_repository_preserves_step(monkeypatch):
    # Isolate the step type check while exercising the unchanged R2 contract.
    import sys
    class ProofStep:
        def __init__(self, conclusion):
            self.conclusion = conclusion
    monkeypatch.setitem(sys.modules, "proof", SimpleNamespace(ProofStep=ProofStep))
    step = ProofStep("G")
    repository = SimpleNamespace(entries=lambda: (
        SimpleNamespace(key="standard.toda.prop56", step=step),
    ))
    result = build_registry_bridge(
        components_by_reference={},
        theorem_facts=SimpleNamespace(entries=()),
        proof_repository=repository,
    )
    assert result.proof_links[0].step is step
    assert result.proof_links[0].repository_key == "standard.toda.prop56"
    assert result.registry.assertions_for(
        "repository:standard.toda.prop56"
    )[0].origin is AssertionOrigin.PROOF_INTERNAL


def test_empty_sources_yield_empty_registry():
    result = build_registry_bridge(
        components_by_reference={},
        theorem_facts=SimpleNamespace(entries=()),
    )
    assert result.records == ()
    assert result.proof_links == ()
