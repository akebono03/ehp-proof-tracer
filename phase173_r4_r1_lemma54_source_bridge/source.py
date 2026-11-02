"""Derive the typed Hopf clause of Toda Lemma 5.4 from its verified source.

This module does not reclassify an archive row or DB goal as a proof. It
introduces one explicit fixed literature assertion only after source-hash,
exact-clause and existing publication-order verification. Its Hopf equality
is concluded by INFERENCE, not adopted directly as a GIVEN.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement, MapApplication
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)
from map_facts import EHP_H_MAP

SOURCE_ID = "toda:tex:ch5:0007"
ADOPTED_ASSERTION_ID = "phase173:r4r1:lemma54:typed_hopf_source"
HOPF_TEXT = r"H(\nu_{4})=\iota_7"
MEMBERSHIP_TEXT = r"\nu_{4}\in \pi^{4}_{7}"
DOUBLE_TEXT = r"2E \nu_{4}=E^{2}\nu'"


@dataclass(frozen=True)
class TodaLemma54TypedSource:
    """One exact source-verified, cited clause, never a DB group result."""
    source_id: str = SOURCE_ID
    hopf_formula: str = HOPF_TEXT
    membership_formula: str = MEMBERSHIP_TEXT
    double_formula: str = DOUBLE_TEXT


def canonical_hopf_relation() -> Relation:
    """Build the concrete Hopf relation independently of the requested goal."""
    nu4 = HomotopyElement(
        name="ν₄", dimension=4, source=7, target=4,
        generator=GeneratorSymbol(family="ν", index=4),
    )
    iota = HomotopyElement(
        name="ι_7", dimension=7, source=7, target=7,
        generator=GeneratorSymbol(family="ι", index=7),
    )
    return Relation(
        MapApplication(map=EHP_H_MAP, expression=nu4),
        iota,
        RelationType.EQUALITY,
    )


def validate_lemma54_text(text: str) -> None:
    """Require a unique original lemma environment with all three clauses."""
    if not isinstance(text, str):
        raise TypeError("Lemma 5.4 archived text must be a string")
    if text.count(r"\label{lem:5.4}") != 1:
        raise ValueError("Lemma 5.4 archive must contain one lemma label")
    start = text.find(r"\label{lem:5.4}")
    end = text.find(r"\end{lemma}", start)
    if end < 0:
        raise ValueError("Lemma 5.4 environment is incomplete")
    opening = text.rfind(r"\begin{lemma}", 0, start)
    if opening < 0:
        raise ValueError("Lemma 5.4 environment opening is absent")
    passage = text[opening:end]
    if any(token not in passage for token in (HOPF_TEXT, MEMBERSHIP_TEXT, DOUBLE_TEXT)):
        raise ValueError("Lemma 5.4 verified claims differ")


def _validated_archive(bridge: RegistryBridgeResult, chapter: str):
    """Match the archived row and the frozen full TeX text, not a DB goal."""
    validate_lemma54_text(chapter)
    candidates = tuple(
        assertion for assertion in bridge.registry._assertions.values()
        if assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
        and isinstance(assertion.content, dict)
        and assertion.content.get("source_statement_id") == SOURCE_ID
    )
    if len(candidates) != 1:
        raise ValueError("Expected a unique original Lemma 5.4 archive row")
    archive = candidates[0]
    content = archive.content
    source = content.get("source_text")
    if not isinstance(source, str) or not source:
        raise ValueError("Lemma 5.4 archive lacks source text")
    if content.get("source_sha256") != sha256(source.encode("utf-8")).hexdigest():
        raise ValueError("Lemma 5.4 archived SHA-256 does not match text")
    # Archive format may hold a shorter extracted block. It must belong to the
    # exactly checked chapter; never accept merely matching generic tokens.
    normalized = chapter.replace("\r\n", "\n")
    extracted = source.replace("\r\n", "\n")
    if extracted not in normalized:
        raise ValueError("Lemma 5.4 archive is not a literal source passage")
    if not all(token in extracted for token in (HOPF_TEXT, MEMBERSHIP_TEXT, DOUBLE_TEXT)):
        raise ValueError("Lemma 5.4 archive does not contain the complete lemma")
    reference = bridge.registry.reference(archive.reference_id)
    if reference.locator != "Lemma 5.4" or reference.kind is not ReferenceKind.LEMMA:
        raise ValueError("Lemma 5.4 archive has an incorrect reference")
    return archive


def add_verified_lemma54_source(
    bridge: RegistryBridgeResult, *, citing_assertion_id: str, chapter: str,
) -> RegistryBridgeResult:
    """Add one explicitly cited typed literature statement to an isolated bridge.

    Reuse the original referenced publication position, not a fabricated rank.
    No source-archive row itself becomes a GIVEN; the new source statement is
    checked before registration and must precede the actual citing assertion.
    """
    from phase166_r3c_publication_order import precedes_citing_assertion

    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("An existing typed reference bridge is required")
    archive = _validated_archive(bridge, chapter)
    if ADOPTED_ASSERTION_ID in bridge.registry._assertions:
        raise ValueError("Lemma 5.4 typed source already registered")
    registry = UnifiedStatementRegistry()
    for entry in bridge.registry._references.values():
        registry.add_reference(entry)
    for entry in bridge.registry._assertions.values():
        registry.add_assertion(entry)
    registry.add_assertion(AssertionEntry(
        assertion_id=ADOPTED_ASSERTION_ID,
        reference_id=archive.reference_id,
        kind=AssertionKind.STATEMENT,
        content=TodaLemma54TypedSource(),
        origin=AssertionOrigin.FIXED_STATEMENT,
        component_position=archive.component_position,
        scope=("adopted source-verified Lemma 5.4 exact clause",),
    ))
    result = RegistryBridgeResult(registry, bridge.records, bridge.proof_links)
    if not precedes_citing_assertion(result, ADOPTED_ASSERTION_ID, citing_assertion_id):
        raise ValueError("Lemma 5.4 has no proven earlier publication position")
    return result


def lemma54_hopf_inference_rule(goal: Relation) -> InferenceRule:
    """Extract only the uniquely typed Hopf clause as a derived ProofStep."""
    if goal != canonical_hopf_relation():
        raise ValueError("Only the concrete verified Lemma 5.4 Hopf fact is supported")
    claim = TodaLemma54TypedSource()

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.GIVEN
                and type(premises[0].conclusion) is TodaLemma54TypedSource
                and premises[0].conclusion == claim)

    return InferenceRule(
        name="Toda Lemma 5.4 cited Hopf identity consequence",
        description=(
            "Extract H(nu_4)=iota_7 from the fully source-verified and "
            "publication-screened Toda Lemma 5.4 typed literature statement."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaLemma54TypedSource,
            statement_pattern=claim,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Lemma 5.4", locator="Lemma 5.4",
        ),
    )


def expand_cited_lemma54_hopf(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """No source-verified screened claim means no proposal whatsoever."""
    if not isinstance(available, tuple):
        raise TypeError("available must be the screened source tuple")
    if goal != canonical_hopf_relation():
        return ()
    claim = TodaLemma54TypedSource()
    if sum(type(source) is TodaLemma54TypedSource and source == claim
           for source in available) != 1:
        return ()
    return (GoalExpansion(lemma54_hopf_inference_rule(goal), (claim,)),)
