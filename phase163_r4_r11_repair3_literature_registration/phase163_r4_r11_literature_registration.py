"""Phase 163 R4-R11 repair3: register typed literature assertions as data.

Proof ancestry is deliberately not certified here. Every entry is marked
SOURCE_UNVERIFIED in a separate evidence ledger. No search eligibility granted.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase163_r4_r10_generator_integrity import verify_prop56_pi5_2_generator
from phase163_r4_r11_prop56_remaining import (
    COMPONENT_KEYS,
    verify_prop56_remaining_component,
)
from scalar_rules import ScalarGreaterEqualStatement
from unified_statement_registry import (
    AssertionKind,
    UnifiedStatementRegistry,
)


LOCATOR = "Proposition 5.6"
ALL_KEYS = ("pi5_2_group_relation",) + COMPONENT_KEYS


@dataclass(frozen=True)
class LiteratureAssertionInput:
    component_key: str
    statement: object
    source_description: str
    scope_statement: object | None = None

    def __post_init__(self) -> None:
        if self.component_key not in ALL_KEYS:
            raise ValueError("unknown Proposition 5.6 component")
        if self.statement is None:
            raise ValueError("statement is required")
        if not isinstance(self.source_description, str) or not self.source_description.strip():
            raise ValueError("source_description is required")


@dataclass(frozen=True)
class LiteratureAssertionEvidence:
    assertion_id: str
    source_description: str
    verification_status: str
    proof_status: str


@dataclass(frozen=True)
class LiteratureRegistrationResult:
    snapshot: RegistryBridgeResult
    evidence: tuple[LiteratureAssertionEvidence, ...]


def register_prop56_literature_statements(
    base: RegistryBridgeResult,
    inputs: tuple[LiteratureAssertionInput, ...],
) -> LiteratureRegistrationResult:
    """Register exactly five checked typed conclusions, without proof certification.

    The source_description is a candidate provenance label, not independent
    verification against the printed literature. Keep proof_links unchanged.
    """
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    if not isinstance(inputs, tuple):
        raise TypeError("inputs must be a tuple")
    if not all(isinstance(item, LiteratureAssertionInput) for item in inputs):
        raise TypeError("all items must be LiteratureAssertionInput")
    keys = tuple(item.component_key for item in inputs)
    if len(keys) != len(ALL_KEYS) or set(keys) != set(ALL_KEYS):
        raise ValueError("all five distinct Proposition 5.6 components required")

    ids = {f"boundary:{LOCATOR}:{key}" for key in ALL_KEYS}
    existing = {r.assertion_id: r for r in base.records if r.assertion_id in ids}
    if len(existing) != 5 or any(
        rec.source != "boundary" or rec.status is not MigrationStatus.METADATA_ONLY
        for rec in existing.values()
    ):
        raise ValueError("all five target entries must be metadata-only boundaries")

    # Validate on a temporary snapshot first. No mutation of base, even on errors.
    new_contents = {f"boundary:{LOCATOR}:{item.component_key}": item.statement for item in inputs}
    trial = _copy_snapshot(base, new_contents)
    verify_prop56_pi5_2_generator(trial)
    for item in inputs:
        if item.component_key in COMPONENT_KEYS:
            if item.component_key == "higher_nu_group_relation":
                if not isinstance(item.scope_statement, ScalarGreaterEqualStatement):
                    raise ValueError("typed scope n >= 6 required")
            elif item.scope_statement is not None:
                raise ValueError("unexpected scope statement for concrete component")
            verify_prop56_remaining_component(
                trial,
                item.component_key,
                higher_range=item.scope_statement,
            )
        elif item.scope_statement is not None:
            raise ValueError("unexpected scope for pi5_2 component")

    evidence = tuple(
        LiteratureAssertionEvidence(
            assertion_id=f"boundary:{LOCATOR}:{item.component_key}",
            source_description=item.source_description,
            verification_status="SOURCE_UNVERIFIED",
            proof_status="PROOF_ANCESTRY_NOT_CHECKED",
        )
        for item in inputs
    )
    return LiteratureRegistrationResult(snapshot=trial, evidence=evidence)


def _copy_snapshot(
    base: RegistryBridgeResult,
    new_contents: dict[str, object],
) -> RegistryBridgeResult:
    registry = UnifiedStatementRegistry()
    references: set[str] = set()
    for record in base.records:
        if record.assertion_id is None:
            continue
        current = base.registry.assertion(record.assertion_id)
        if current.reference_id not in references:
            registry.add_reference(base.registry.reference(current.reference_id))
            references.add(current.reference_id)
        if record.assertion_id in new_contents:
            current = replace(
                current,
                content=new_contents[record.assertion_id],
                kind=AssertionKind.STATEMENT,
            )
        registry.add_assertion(current)
    records: list[MigrationRecord] = []
    for record in base.records:
        if record.assertion_id in new_contents:
            records.append(replace(
                record,
                status=MigrationStatus.STRUCTURED,
                detail=(
                    "Typed literature candidate; source unverified; "
                    "no proof ancestry verification or proof eligibility"
                ),
            ))
        else:
            records.append(record)
    return RegistryBridgeResult(registry, tuple(records), base.proof_links)


def existing_prop56_candidates() -> tuple[LiteratureAssertionInput, ...]:
    """Read existing Phase 65 conclusions; do not treat their proofs as citations."""
    from probes.probe_phase65_capabilities import build_phase65_representative_result

    data = build_phase65_representative_result()
    sources = (
        ("pi5_2_group_relation", "pi5_2_step"),
        ("pi6_3_group_relation", "pi6_3_step"),
        ("pi7_4_group_relation", "pi7_4_step"),
        ("pi8_5_group_relation", "pi8_5_step"),
        ("higher_nu_group_relation", "higher_step"),
    )
    return tuple(
        LiteratureAssertionInput(
            component_key=key,
            statement=data[step_key].conclusion,
            source_description=f"Phase65 representative {step_key}; Toda {LOCATOR} candidate",
            scope_statement=(
                data["higher_range_step"].conclusion
                if key == "higher_nu_group_relation" else None
            ),
        )
        for key, step_key in sources
    )
