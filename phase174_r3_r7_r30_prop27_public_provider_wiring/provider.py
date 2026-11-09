"""Source-certified Proposition 2.7 proposals in the ordinary shared provider.

This module adds only the reviewed *general* literature fact. Each typed
instance remains a checked INFERENCE from that general fixed reference.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    ASSERTION_ID,
    EXPECTED_THEOREM_SHA256,
    Prop27UniversalLiteratureStatement,
    register_universal_prop27,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise,
    Prop27TypedHopfDeltaStatement,
)
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionOrigin, ReferenceKind, UnifiedStatementRegistry,
)

MANIFEST_REFERENCE_ID = "toda:Proposition 2.7"
MANIFEST_SOURCE_ID = "toda:tex:ch2:0018"


def _reviewed_position() -> int:
    """Use the exact existing source manifest identity, never a guessed rank."""
    positions, rows, _manifest = _load_manifest_reference_order(DEFAULT_MANIFEST)
    records = rows.get(MANIFEST_REFERENCE_ID, ())
    if (len(records) != 1
            or records[0]["statement_id"] != MANIFEST_SOURCE_ID
            or records[0]["locator"] != "Proposition 2.7"):
        raise ValueError("Proposition 2.7 manifest identity was not uniquely reviewed")
    position = positions.get(MANIFEST_REFERENCE_ID)
    if type(position) is not int or position <= 0:
        raise ValueError("Proposition 2.7 lacks reviewed publication position")
    return position


def register_positioned_prop27(root: Path) -> RegistryBridgeResult:
    """Add a general literature reference with its real source-order identity.

    R28 checks the primary theorem SHA before a GIVEN is constructed. The
    returned isolated bridge can be merged by the ordinary shared bridge.
    """
    if not isinstance(root, Path):
        raise TypeError("root must be Path")
    position = _reviewed_position()
    source = register_universal_prop27(root)
    original = source.registry.reference(next(iter(source.registry._references)))
    if (original.locator != "Proposition 2.7"
            or original.kind is not ReferenceKind.PROPOSITION
            or len(source.proof_links) != 1):
        raise ValueError("reviewed general source registry contract changed")
    registry = UnifiedStatementRegistry()
    registry.add_reference(replace(
        original, source_id=MANIFEST_SOURCE_ID,
        publication_position=position,
    ))
    for assertion in source.registry._assertions.values():
        registry.add_assertion(assertion)
    return RegistryBridgeResult(registry, source.records, source.proof_links)


def has_certified_prop27_leaf(bridge: RegistryBridgeResult) -> bool:
    """Require one exact screened, positioned, typed R28 GIVEN and proof link.

    This checks the reference-and-link contract, not an arbitrary citation label.
    Source-byte certification is performed by register_positioned_prop27().
    """
    if not isinstance(bridge, RegistryBridgeResult):
        return False
    matched = tuple(
        assertion for assertion in bridge.registry._assertions.values()
        if type(assertion.content) is Prop27UniversalLiteratureStatement
    )
    if len(matched) != 1:
        return False
    assertion = matched[0]
    claim = assertion.content
    if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or claim != Prop27UniversalLiteratureStatement()
            or claim.source_sha256 != EXPECTED_THEOREM_SHA256
            or assertion.kind.value != "statement"):
        return False
    try:
        reference = bridge.registry.reference(assertion.reference_id)
        position = _reviewed_position()
    except (KeyError, TypeError, ValueError):
        return False
    if (reference.kind is not ReferenceKind.PROPOSITION
            or reference.locator != "Proposition 2.7"
            or reference.source_id != MANIFEST_SOURCE_ID
            or reference.publication_position != position):
        return False
    matching_links = tuple(link for link in bridge.proof_links
                           if link.assertion_id == assertion.assertion_id)
    if len(matching_links) != 1:
        return False
    step = matching_links[0].step
    return (type(step) is ProofStep
            and step.rule is ProofRule.GIVEN
            and step.premises == ()
            and step.conclusion == claim)


def expand_public_cited_prop27_goal(goal: object, bridge: RegistryBridgeResult):
    """Supply only applicable inverse rules when a screened cited leaf exists.

    Do not construct any ProofStep, bypass the recursive proof checker, or
    assert Delta surjectivity or a zero group.
    """
    if type(goal) not in (Prop27GeneralTheoremPremise, Prop27TypedHopfDeltaStatement):
        return ()
    if not has_certified_prop27_leaf(bridge):
        return ()
    from phase174_r3_r7_r29_prop27_canonical_provider.provider import (
        expand_cited_prop27_goal,
    )
    return expand_cited_prop27_goal(goal)
