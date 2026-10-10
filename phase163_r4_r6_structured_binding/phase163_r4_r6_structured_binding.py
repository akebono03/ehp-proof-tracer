"""Phase 163 R4-R6: opt-in typed binding of existing verified citation steps.

No automatic theorem discovery, proof execution, or citation permission is added.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

from phase162_reference_boundary import validate_cited_fixed_statement
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from proof import ProofStep
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    ProofStepLink,
    UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class FixedStatementBinding:
    """Explicit association supplied after existing citation ancestry verification."""

    reference_locator: str
    component_key: str
    citation_step: ProofStep
    expected_conclusion: object

    def __post_init__(self) -> None:
        if not isinstance(self.reference_locator, str) or not self.reference_locator:
            raise ValueError("reference_locator is required")
        if not isinstance(self.component_key, str) or not self.component_key:
            raise ValueError("component_key is required")
        if not isinstance(self.citation_step, ProofStep):
            raise TypeError("citation_step must be a ProofStep")
        if self.expected_conclusion is None:
            raise ValueError("expected_conclusion is required")


def bind_verified_fixed_statements(
    base: RegistryBridgeResult,
    bindings: tuple[FixedStatementBinding, ...],
) -> RegistryBridgeResult:
    """Return a new registry snapshot with selected metadata entries typed.

    This checks an *existing* verified-citation boundary, not the external
    truth of a theorem. The original bridge snapshot is never mutated.
    """
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be a RegistryBridgeResult")
    if not isinstance(bindings, tuple):
        raise TypeError("bindings must be a tuple")

    selected: dict[str, FixedStatementBinding] = {}
    for binding in bindings:
        if not isinstance(binding, FixedStatementBinding):
            raise TypeError("bindings must contain FixedStatementBinding")
        identifier = f"boundary:{binding.reference_locator}:{binding.component_key}"
        if identifier in selected:
            raise ValueError(f"duplicate binding: {identifier}")
        # Existing validator checks the registered locator, component, identity,
        # citation shape and exact typed conclusion.
        validate_cited_fixed_statement(
            binding.citation_step,
            binding.reference_locator,
            binding.component_key,
            binding.expected_conclusion,
        )
        selected[identifier] = binding

    eligible = {
        record.assertion_id
        for record in base.records
        if record.source == "boundary"
        and record.status is MigrationStatus.METADATA_ONLY
    }
    if not set(selected).issubset(eligible):
        unknown = sorted(set(selected) - eligible)
        raise ValueError(f"binding is not a metadata-only boundary: {unknown}")

    result = UnifiedStatementRegistry()
    seen_refs: set[str] = set()
    for record in base.records:
        if record.assertion_id is None:
            continue
        assertion = base.registry.assertion(record.assertion_id)
        if assertion.reference_id not in seen_refs:
            result.add_reference(base.registry.reference(assertion.reference_id))
            seen_refs.add(assertion.reference_id)
        if record.assertion_id in selected:
            binding = selected[record.assertion_id]
            assertion = replace(
                assertion, content=binding.citation_step.conclusion,
                kind=AssertionKind.STATEMENT,
            )
        result.add_assertion(assertion)

    records: list[MigrationRecord] = []
    proof_links: list[ProofStepLink] = list(base.proof_links)
    for record in base.records:
        if record.assertion_id in selected:
            binding = selected[record.assertion_id]
            records.append(replace(
                record,
                status=MigrationStatus.STRUCTURED,
                detail="Typed conclusion from existing verified citation boundary; not independently literature-verified",
            ))
            proof_links.append(ProofStepLink(
                assertion_id=record.assertion_id,
                step=binding.citation_step,
            ))
        else:
            records.append(record)

    return RegistryBridgeResult(result, tuple(records), tuple(proof_links))
