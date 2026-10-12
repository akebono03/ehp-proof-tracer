from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r6_binding_candidates import inventory_typed_source_bindings
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin,
    LiteratureEntry, ReferenceKind, UnifiedStatementRegistry,
)


def make_bridge(*, duplicate=False, matching=True):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "archive-ref", ReferenceKind.PROPOSITION, "Proposition 5.1",
        source_id="archive", publication_position=10,
    ))
    registry.add_reference(LiteratureEntry(
        "typed-ref", ReferenceKind.PROPOSITION,
        "Proposition 5.1" if matching else "Proposition 5.2",
        source_id="typed",
    ))
    registry.add_assertion(AssertionEntry(
        "phase163:archive:one", "archive-ref", AssertionKind.STATEMENT,
        {"source_text": "original"}, origin=AssertionOrigin.SOURCE_ARCHIVE,
    ))
    registry.add_assertion(AssertionEntry(
        "typed:one", "typed-ref", AssertionKind.STATEMENT,
        "typed expression", origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    if duplicate:
        registry.add_assertion(AssertionEntry(
            "typed:two", "typed-ref", AssertionKind.STATEMENT,
            "second typed expression", origin=AssertionOrigin.FIXED_STATEMENT,
        ))
    return RegistryBridgeResult(registry, (), ())


def test_unique_locator_is_only_a_review_candidate():
    bridge = make_bridge()
    report = inventory_typed_source_bindings(bridge)
    assert len(report.candidates) == 1
    assert report.candidates[0].source_position == 10
    assert report.candidates[0].status == "REVIEW_REQUIRED_NOT_PROOF_ELIGIBLE"
    assert report.proof_eligible_count == 0
    assert bridge.registry.assertion("typed:one").available_after_position is None
    assert bridge.proof_links == ()


def test_ambiguous_locator_is_not_bound():
    report = inventory_typed_source_bindings(make_bridge(duplicate=True))
    assert not report.candidates
    assert report.ambiguous_source_ids == ("phase163:archive:one",)


def test_unmatched_source_is_reported():
    report = inventory_typed_source_bindings(make_bridge(matching=False))
    assert report.unmatched_source_ids == ("phase163:archive:one",)
    assert not report.candidates


def test_invalid_bridge_rejected():
    import pytest
    with pytest.raises(TypeError):
        inventory_typed_source_bindings(object())
