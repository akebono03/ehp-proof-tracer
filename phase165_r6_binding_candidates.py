"""Phase 165 R6: source-to-typed-statement candidate matching, not approval.

An identical source locator is insufficient to establish mathematical equivalence.
All result records are NON_ELIGIBLE until separately reviewed and authorized.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class BindingCandidate:
    source_assertion_id: str
    typed_assertion_id: str
    locator: str
    source_position: int
    status: str = "REVIEW_REQUIRED_NOT_PROOF_ELIGIBLE"


@dataclass(frozen=True)
class BindingInventory:
    candidates: tuple[BindingCandidate, ...]
    unmatched_source_ids: tuple[str, ...]
    ambiguous_source_ids: tuple[str, ...]
    typed_without_source_ids: tuple[str, ...]
    proof_eligible_count: int = 0


def inventory_typed_source_bindings(bridge: RegistryBridgeResult) -> BindingInventory:
    """Match only by normalized locator; never alter Registry or ProofStep links.

    A unique locator match is a review candidate only, not a semantic binding.
    Original-edition ordering, availability, and verification remain untouched.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    registry = bridge.registry
    sources = tuple(sorted(
        (item for item in registry._assertions.values()
         if item.origin is AssertionOrigin.SOURCE_ARCHIVE
         and item.assertion_id.startswith("phase163:archive:")),
        key=lambda x: x.assertion_id,
    ))
    typed = tuple(sorted(
        (item for item in registry._assertions.values()
         if item.origin is AssertionOrigin.FIXED_STATEMENT
         and not item.assertion_id.startswith("phase163:archive:")),
        key=lambda x: x.assertion_id,
    ))
    candidates = []
    unmatched = []
    ambiguous = []
    matched_typed = set()
    for source in sources:
        reference = registry.reference(source.reference_id)
        position = reference.publication_position
        if not isinstance(position, int) or isinstance(position, bool) or position < 1:
            raise ValueError("source position missing")
        matches = tuple(
            entry for entry in typed
            if registry.reference(entry.reference_id).locator == reference.locator
        )
        if not matches:
            unmatched.append(source.assertion_id)
        elif len(matches) != 1:
            ambiguous.append(source.assertion_id)
        else:
            item = matches[0]
            candidates.append(BindingCandidate(
                source_assertion_id=source.assertion_id,
                typed_assertion_id=item.assertion_id,
                locator=reference.locator,
                source_position=position,
            ))
            matched_typed.add(item.assertion_id)
    return BindingInventory(
        candidates=tuple(candidates),
        unmatched_source_ids=tuple(unmatched),
        ambiguous_source_ids=tuple(ambiguous),
        typed_without_source_ids=tuple(
            item.assertion_id for item in typed
            if item.assertion_id not in matched_typed
        ),
    )
