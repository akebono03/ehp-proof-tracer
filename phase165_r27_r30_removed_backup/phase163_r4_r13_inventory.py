"""Phase 163 R4-R13: read-only inventory of typed and metadata-only records.

No new mathematical assertions, provenance claims, or proof-search eligibility.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from proof import Relation
from toda_literature_statement_boundary import TodaFixedStatementComponent


class InventoryClassification(str, Enum):
    TYPED_SOURCE_UNVERIFIED = "TYPED_SOURCE_UNVERIFIED"
    METADATA_ONLY = "METADATA_ONLY"
    OTHER_TYPED_NOT_AUDITED = "OTHER_TYPED_NOT_AUDITED"
    UNRESOLVED_SOURCE = "UNRESOLVED_SOURCE"


@dataclass(frozen=True)
class InventoryItem:
    assertion_id: str | None
    locator: str | None
    component_key: str | None
    classification: InventoryClassification
    statement_type: str | None
    scope_text: str | None
    scope_assessment: str
    generator_assessment: str
    detail: str


@dataclass(frozen=True)
class InventoryReport:
    items: tuple[InventoryItem, ...]
    proof_links_count: int

    def count(self, classification: InventoryClassification) -> int:
        return sum(item.classification is classification for item in self.items)


def _generator_assessment(content: object) -> str:
    if not isinstance(content, Relation):
        return "NOT_A_GROUP_RELATION"
    group = content.rhs
    if isinstance(group, (FiniteCyclicGroup, FreeCyclicGroup)):
        return "PRESENT" if group.generator is not None else "MISSING"
    if isinstance(group, DirectSumGroup):
        summands = group.summands
        return "PRESENT" if summands and all(
            isinstance(term, (FiniteCyclicGroup, FreeCyclicGroup))
            and term.generator is not None for term in summands
        ) else "INCOMPLETE_OR_UNSUPPORTED"
    return "NOT_A_CYCLIC_PRESENTATION"


def inventory_registry_snapshot(
    snapshot: RegistryBridgeResult,
    source_unverified_ids: frozenset[str],
    typed_scope_ids: frozenset[str],
) -> InventoryReport:
    """Classify every migration record without modifying registry or links.

    A text scope alone is not proof of a separately checked typed range.
    An assertion not explicitly in source_unverified_ids is NOT marked verified.
    """
    if not isinstance(snapshot, RegistryBridgeResult):
        raise TypeError("snapshot must be RegistryBridgeResult")
    if not isinstance(source_unverified_ids, frozenset) or not isinstance(typed_scope_ids, frozenset):
        raise TypeError("ID collections must be frozensets")
    if not typed_scope_ids.issubset(source_unverified_ids):
        raise ValueError("typed scope ids must be among audited typed registrations")
    items: list[InventoryItem] = []
    observed_ids: set[str] = set()
    for record in snapshot.records:
        if record.assertion_id is None:
            items.append(InventoryItem(
                assertion_id=None, locator=None, component_key=None,
                classification=InventoryClassification.UNRESOLVED_SOURCE,
                statement_type=None, scope_text=None,
                scope_assessment="NOT_APPLICABLE", generator_assessment="NOT_ASSESSED",
                detail=record.detail,
            ))
            continue
        assertion_id = record.assertion_id
        observed_ids.add(assertion_id)
        assertion = snapshot.registry.assertion(assertion_id)
        reference = snapshot.registry.reference(assertion.reference_id)
        original_component = isinstance(assertion.content, TodaFixedStatementComponent)
        if record.status is MigrationStatus.METADATA_ONLY:
            if not original_component:
                raise ValueError("metadata_only assertion unexpectedly contains typed content")
            classification = InventoryClassification.METADATA_ONLY
        elif record.status is MigrationStatus.STRUCTURED:
            if original_component:
                raise ValueError("structured assertion still contains component metadata")
            classification = (
                InventoryClassification.TYPED_SOURCE_UNVERIFIED
                if assertion_id in source_unverified_ids else
                InventoryClassification.OTHER_TYPED_NOT_AUDITED
            )
        else:
            classification = InventoryClassification.UNRESOLVED_SOURCE
        scope = assertion.scope
        scope_assessment = (
            "TYPED_SCOPE_CHECKED_SOURCE_UNVERIFIED" if assertion_id in typed_scope_ids
            else "TEXT_SCOPE_ONLY_NOT_CHECKED" if scope is not None
            else "NO_SCOPE_METADATA"
        )
        component_key = (
            assertion_id.rsplit(":", 1)[-1]
            if record.source == "boundary" else None
        )
        items.append(InventoryItem(
            assertion_id=assertion_id,
            locator=reference.locator,
            component_key=component_key,
            classification=classification,
            statement_type=type(assertion.content).__name__,
            scope_text=scope,
            scope_assessment=scope_assessment,
            generator_assessment=(
                "NOT_ASSESSED_METADATA_ONLY" if original_component
                else _generator_assessment(assertion.content)
            ),
            detail=record.detail,
        ))
    unknown_ids = source_unverified_ids - observed_ids
    if unknown_ids:
        raise ValueError("typed evidence refers to absent assertion ids: " + ", ".join(sorted(unknown_ids)))
    return InventoryReport(tuple(items), len(snapshot.proof_links))


def existing_phase163_r4_r13_inventory() -> InventoryReport:
    """Read R4-R11, R4-R12 and stable minimum snapshots; do not traverse proofs."""
    from phase163_r4_registry_bridge import build_registry_bridge
    from phase163_r4_r11_literature_registration import (
        existing_prop56_candidates,
        register_prop56_literature_statements,
    )
    from phase163_r4_r12_literature_registration import (
        existing_prop51_prop53_candidates,
        register_prop51_prop53_literature_statements,
    )
    from phase163_r4_r12_stable_bases import register_stable_minimal_dimensions, BASE_ID_1
    from toda_upstream_bootstrap import _build_phase50_result

    prop56_inputs = existing_prop56_candidates()
    prop56 = register_prop56_literature_statements(build_registry_bridge(), prop56_inputs)
    prop53_inputs = existing_prop51_prop53_candidates()
    prop53 = register_prop51_prop53_literature_statements(prop56.snapshot, prop53_inputs)
    minimal = register_stable_minimal_dimensions(
        prop53, _build_phase50_result()["final_group_step"].conclusion
    )
    typed_ids = frozenset(
        [e.assertion_id for e in prop56.evidence]
        + [e.assertion_id for e in prop53.evidence]
    )
    scope_ids = frozenset(
        ["boundary:Proposition 5.6:higher_nu_group_relation"]
        + ["boundary:Proposition 5.1:higher_eta_group_relation"]
        + ["boundary:Proposition 5.3:higher_eta_squared_group_relation"]
    )
    report = inventory_registry_snapshot(minimal.snapshot, typed_ids, scope_ids)
    stable = minimal.snapshot.registry.assertion(BASE_ID_1)
    if stable.origin.value != "proof_internal":
        raise ValueError("stable pi4_3 minimum must remain proof_internal")
    return report
