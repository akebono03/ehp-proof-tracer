"""Phase 163 R4: additive, read-only adapters; no proof search integration."""
from dataclasses import dataclass
from enum import Enum
from typing import Any

from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


class MigrationStatus(str, Enum):
    STRUCTURED = "structured"
    METADATA_ONLY = "metadata_only"
    UNRESOLVED_SOURCE = "unresolved_source"


@dataclass(frozen=True)
class MigrationRecord:
    source: str
    source_key: str
    assertion_id: str | None
    status: MigrationStatus
    detail: str


@dataclass(frozen=True)
class RegistryBridgeResult:
    registry: UnifiedStatementRegistry
    records: tuple[MigrationRecord, ...]
    proof_links: tuple[ProofStepLink, ...]

    def records_for(self, source: str) -> tuple[MigrationRecord, ...]:
        return tuple(record for record in self.records if record.source == source)

    @property
    def unresolved(self) -> tuple[MigrationRecord, ...]:
        return tuple(record for record in self.records
                     if record.status is MigrationStatus.UNRESOLVED_SOURCE)


def _reference_kind(locator: str) -> ReferenceKind:
    if locator.startswith("Proposition "):
        return ReferenceKind.PROPOSITION
    if locator.startswith("Lemma "):
        return ReferenceKind.LEMMA
    if locator.startswith("Theorem "):
        return ReferenceKind.THEOREM
    if locator.startswith("Definition "):
        return ReferenceKind.DEFINITION
    if locator.startswith("Corollary "):
        return ReferenceKind.COROLLARY
    if locator.startswith("Remark "):
        return ReferenceKind.REMARK
    return ReferenceKind.EQUATION


def build_registry_bridge(
    *,
    components_by_reference: dict[str, tuple[Any, ...]] | None = None,
    theorem_facts: Any = None,
    proof_repository: Any = None,
) -> RegistryBridgeResult:
    """Snapshot existing records without fabricating publication/availability order.

    The literature component catalog stores *metadata*, not a typed theorem.
    Its entries are deliberately marked METADATA_ONLY. Proof repository entries
    retain their exact typed conclusion and ProofStep but are not inferred to
    be literature-fixed facts merely from theorem text.
    """
    if components_by_reference is None:
        from toda_literature_statement_boundary import _FIXED_COMPONENTS_BY_REFERENCE
        components_by_reference = _FIXED_COMPONENTS_BY_REFERENCE
    if theorem_facts is None:
        from theorem_facts import THEOREM_FACT_REPOSITORY
        theorem_facts = THEOREM_FACT_REPOSITORY

    registry = UnifiedStatementRegistry()
    records: list[MigrationRecord] = []
    links: list[ProofStepLink] = []

    def ensure_reference(reference_id: str, kind: ReferenceKind,
                         locator: str, source_id: str | None) -> None:
        try:
            existing = registry.reference(reference_id)
        except KeyError:
            registry.add_reference(LiteratureEntry(
                reference_id=reference_id, kind=kind,
                locator=locator, source_id=source_id,
            ))
        else:
            if existing.locator != locator or existing.kind != kind:
                raise ValueError(f"conflicting reference identity: {reference_id}")

    for locator, components in sorted(components_by_reference.items()):
        reference_id = f"toda:{locator}"
        ensure_reference(reference_id, _reference_kind(locator), locator, "Toda")
        for component in components:
            if component.reference_locator != locator:
                raise ValueError(f"component locator mismatch: {locator}")
            key = component.component_key
            assertion_id = f"boundary:{locator}:{key}"
            # A component's order is not a proof completion position.
            registry.add_assertion(AssertionEntry(
                assertion_id=assertion_id, reference_id=reference_id,
                kind=AssertionKind.STATEMENT, content=component,
                origin=AssertionOrigin.FIXED_STATEMENT,
                component_position=component.order,
                scope=component.range_text,
            ))
            records.append(MigrationRecord(
                "boundary", f"{locator}/{key}", assertion_id,
                MigrationStatus.METADATA_ONLY,
                "Component metadata only; mathematical Statement not reconstructed",
            ))

    for index, fact in enumerate(theorem_facts.entries):
        reference = fact.reference
        locator = reference.locator
        if not locator:
            records.append(MigrationRecord(
                "theorem_fact", str(index), None,
                MigrationStatus.UNRESOLVED_SOURCE,
                "LiteratureReference.locator is missing; no attribution invented",
            ))
            continue
        reference_id = f"fact:{reference.label}:{locator}"
        ensure_reference(reference_id, _reference_kind(locator), locator,
                         reference.label)
        assertion_id = f"fact:{reference.label}:{locator}:{index}"
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id, reference_id=reference_id,
            kind=AssertionKind.STATEMENT,
            content=fact.statement,
            origin=AssertionOrigin.FIXED_STATEMENT,
        ))
        records.append(MigrationRecord(
            "theorem_fact", str(index), assertion_id,
            MigrationStatus.STRUCTURED,
            "Typed theorem fact preserved; source identity not conflated",
        ))

    if proof_repository is not None:
        for entry in proof_repository.entries():
            reference_id = f"repository:{entry.key}"
            ensure_reference(reference_id, ReferenceKind.REMARK,
                             entry.key, None)
            assertion_id = f"repository:{entry.key}:conclusion"
            registry.add_assertion(AssertionEntry(
                assertion_id=assertion_id, reference_id=reference_id,
                kind=AssertionKind.STATEMENT,
                content=entry.step.conclusion,
                origin=AssertionOrigin.PROOF_INTERNAL,
            ))
            links.append(ProofStepLink(
                assertion_id=assertion_id, repository_key=entry.key,
                step=entry.step,
            ))
            records.append(MigrationRecord(
                "proof_repository", entry.key, assertion_id,
                MigrationStatus.STRUCTURED,
                "Concrete ProofStep preserved; literature attribution unresolved",
            ))
    return RegistryBridgeResult(registry, tuple(records), tuple(links))
