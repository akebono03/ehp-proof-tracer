"""Targeted tests for read-only component lookup and citation boundaries."""
from dataclasses import dataclass

from phase165_typed_component_lookup import index_typed_components, search_typed_components
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class CompositeFact:
    pi3_2_group_relation: str
    eta2_hopf_relation: str
    delta_iota5_relation: str
    higher_eta_group_relation: str



def make_registry():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "test:prop51", ReferenceKind.PROPOSITION, "Proposition 5.1",
    ))
    registry.add_assertion(AssertionEntry(
        "test:prop51:all", "test:prop51", AssertionKind.STATEMENT,
        CompositeFact("group", "hopf", "delta", "higher"),
        origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    registry.add_assertion(AssertionEntry(
        "test:internal", "test:prop51", AssertionKind.STATEMENT,
        CompositeFact("internal", "internal", "internal", "internal"),
        origin=AssertionOrigin.PROOF_INTERNAL,
    ))
    return registry



def test_prop51_four_fields_are_separately_searchable():
    registry = make_registry()
    matches = search_typed_components(registry, reference_locator="Proposition 5.1")
    assert {item.component_name for item in matches} == {
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    }
    assert {item.assertion_id for item in matches} == {"test:prop51:all"}



def test_lookup_selects_delta_by_field_and_typed_predicate():
    registry = make_registry()
    matches = search_typed_components(
        registry,
        reference_locator="Proposition 5.1",
        component_name="delta_iota5_relation",
        predicate=lambda item: item == "delta",
    )
    assert len(matches) == 1
    assert matches[0].content == "delta"



def test_lookup_does_not_promote_internal_assertions_or_modify_registry():
    registry = make_registry()
    before = tuple(registry._assertions)
    matches = index_typed_components(registry)
    assert len(matches) == 4
    assert all(item.origin is AssertionOrigin.FIXED_STATEMENT for item in matches)
    assert tuple(registry._assertions) == before



def test_invalid_registry_is_rejected():
    import pytest
    with pytest.raises(TypeError):
        index_typed_components(object())
