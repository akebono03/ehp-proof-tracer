"""Phase 163 R3: conservative identity and citation audits, not proof search."""
from dataclasses import dataclass
from enum import Enum
from typing import Any

from unified_statement_registry import (
    AssertionEntry,
    AssertionOrigin,
    UnifiedStatementRegistry,
)


class CitationDecision(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    UNKNOWN = "unknown"


class IdentityDecision(str, Enum):
    SAME = "same"
    DIFFERENT = "different"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class CitationAssessment:
    decision: CitationDecision
    reason: str


@dataclass(frozen=True)
class DependencyAudit:
    cycles: tuple[tuple[str, ...], ...]
    missing: tuple[tuple[str, str], ...]

    @property
    def valid(self) -> bool:
        return not self.cycles and not self.missing


def compare_assertion_identity(left: AssertionEntry, right: AssertionEntry) -> IdentityDecision:
    """Structural identity only: no symbolic/algebraic equivalence inferred."""
    if not isinstance(left, AssertionEntry) or not isinstance(right, AssertionEntry):
        raise TypeError("left and right must be AssertionEntry")
    if left.assertion_id == right.assertion_id:
        return IdentityDecision.SAME
    if left.kind != right.kind or left.origin != right.origin:
        return IdentityDecision.DIFFERENT
    try:
        equal = left.content == right.content
        if type(equal) is bool and not equal:
            return IdentityDecision.DIFFERENT
    except (TypeError, ValueError):
        pass
    return IdentityDecision.UNKNOWN


def audit_dependencies(registry: UnifiedStatementRegistry) -> DependencyAudit:
    """Read-only audit over registered assertions; never infer missing entries."""
    if not isinstance(registry, UnifiedStatementRegistry):
        raise TypeError("registry must be UnifiedStatementRegistry")
    entries = {entry.assertion_id: entry for ref in registry._references.values()
               for entry in registry.assertions_for(ref.reference_id)}
    missing = sorted((identifier, dep) for identifier, entry in entries.items()
                     for dep in entry.dependencies if dep not in entries)
    visited: set[str] = set()
    active: dict[str, int] = {}
    path: list[str] = []
    cycles: set[tuple[str, ...]] = set()

    def visit(identifier: str) -> None:
        if identifier in active:
            cycle = path[active[identifier]:]
            smallest = min(range(len(cycle)), key=lambda i: cycle[i])
            cycles.add(tuple(cycle[smallest:] + cycle[:smallest]))
            return
        if identifier in visited:
            return
        active[identifier] = len(path)
        path.append(identifier)
        for dep in sorted(entries[identifier].dependencies):
            if dep in entries:
                visit(dep)
        path.pop()
        del active[identifier]
        visited.add(identifier)

    for identifier in sorted(entries):
        visit(identifier)
    return DependencyAudit(tuple(sorted(cycles)), tuple(missing))


def assess_citation(
    registry: UnifiedStatementRegistry,
    cited_assertion_id: str,
    citing_assertion_id: str,
) -> CitationAssessment:
    """Citation within a known document; unknown positions never grant access."""
    if not isinstance(registry, UnifiedStatementRegistry):
        raise TypeError("registry must be UnifiedStatementRegistry")
    cited = registry.assertion(cited_assertion_id)
    citing = registry.assertion(citing_assertion_id)
    if cited_assertion_id == citing_assertion_id:
        return CitationAssessment(CitationDecision.DENIED, "self_citation")
    if cited.origin is AssertionOrigin.PROOF_INTERNAL:
        return CitationAssessment(CitationDecision.DENIED, "proof_internal_not_external_reference")
    audit = audit_dependencies(registry)
    if not audit.valid:
        return CitationAssessment(CitationDecision.UNKNOWN, "dependency_graph_unverified")
    source = registry.reference(cited.reference_id)
    destination = registry.reference(citing.reference_id)
    if not source.source_id or not destination.source_id or source.source_id != destination.source_id:
        return CitationAssessment(CitationDecision.UNKNOWN, "document_order_unverified")
    if cited.available_after_position is None or destination.publication_position is None:
        return CitationAssessment(CitationDecision.UNKNOWN, "availability_position_unverified")
    if cited.available_after_position < destination.publication_position:
        return CitationAssessment(CitationDecision.ALLOWED, "available_before_citing_entry")
    return CitationAssessment(CitationDecision.DENIED, "not_available_before_citing_entry")
