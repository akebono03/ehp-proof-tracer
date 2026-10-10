"""Phase 163 R4-R12 repair2: separate minimal stable-stem records.

The pi_4^3 record is an existing derived concrete statement associated with
Proposition 5.1, not a newly asserted literal component of that publication.
The pi_6^4 record already exists in the Proposition 5.3 fixed catalog.
Neither record certifies ancestry or independent literature verification.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import HomotopyElement, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase163_r4_r12_literature_registration import (
    LiteratureComponentRegistrationResult,
    existing_prop51_prop53_candidates,
    register_prop51_prop53_literature_statements,
)
from proof import Relation, RelationType
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, UnifiedStatementRegistry,
)

BASE_ID_1 = "stable-base:1-stem:pi4_3_group_relation"
BASE_ID_2 = "boundary:Proposition 5.3:pi6_4_group_relation"
GENERAL_ID_1 = "boundary:Proposition 5.1:higher_eta_group_relation"
GENERAL_ID_2 = "boundary:Proposition 5.3:higher_eta_squared_group_relation"


@dataclass(frozen=True)
class StableBaseRegistration:
    snapshot: RegistryBridgeResult
    base_1_id: str
    base_2_id: str
    relation_1: str
    relation_2: str
    source_status: str = "SOURCE_UNVERIFIED"
    proof_status: str = "PROOF_ANCESTRY_NOT_CHECKED"


def _check_pi4_3(value: object) -> None:
    if not isinstance(value, Relation) or value.relation_type is not RelationType.EQUALITY:
        raise ValueError("pi_4^3 must be an equality Relation")
    if value.lhs != TodaPrimaryGroup(group_dimension=4, sphere_dimension=3):
        raise ValueError("expected pi_4^3")
    if not isinstance(value.rhs, FiniteCyclicGroup) or value.rhs.order != 2:
        raise ValueError("pi_4^3 must be cyclic of order two")
    eta = value.rhs.generator
    if not isinstance(eta, HomotopyElement):
        raise ValueError("generator must be HomotopyElement")
    if (eta.generator is None or eta.generator.family != "η"
            or eta.generator.index != 3 or eta.dimension != 3
            or eta.source != 4 or eta.target != 3):
        raise ValueError("pi_4^3 must preserve eta_3")


def register_stable_minimal_dimensions(
    previous: LiteratureComponentRegistrationResult,
    pi4_3_statement: object,
) -> StableBaseRegistration:
    """Add a separate pi_4^3 record; preserve the existing pi_6^4 record.

    The 1-stem boundary is a specialization within n>=3.  The 2-stem
    minimum n=4 lies outside the 5.3 higher-formula scope n>=5.
    """
    if not isinstance(previous, LiteratureComponentRegistrationResult):
        raise TypeError("previous must be LiteratureComponentRegistrationResult")
    base = previous.snapshot
    _check_pi4_3(pi4_3_statement)
    existing_ids = {record.assertion_id for record in base.records}
    if BASE_ID_1 in existing_ids:
        raise ValueError("pi_4^3 minimal dimension already registered")
    if not {BASE_ID_2, GENERAL_ID_1, GENERAL_ID_2}.issubset(existing_ids):
        raise ValueError("required Proposition 5.1/5.3 components missing")
    if not {e.assertion_id for e in previous.evidence}.issuperset({BASE_ID_2, GENERAL_ID_1, GENERAL_ID_2}):
        raise ValueError("required components are not part of the typed registration")
    pi6 = base.registry.assertion(BASE_ID_2)
    if not isinstance(pi6.content, Relation) or pi6.content.lhs != TodaPrimaryGroup(
        group_dimension=6, sphere_dimension=4
    ):
        raise ValueError("pi_6^4 must be stored independently")
    if (not isinstance(pi6.content.rhs, FiniteCyclicGroup)
            or pi6.content.rhs.order != 2):
        raise ValueError("pi_6^4 order mismatch")
    generic_1 = base.registry.assertion(GENERAL_ID_1)
    generic_2 = base.registry.assertion(GENERAL_ID_2)
    if generic_1.scope != "n >= 3" or generic_2.scope != "n >= 5":
        raise ValueError("unexpected stable higher-formula scope")
    # Copy the existing registry without changing any existing assertion.
    registry = UnifiedStatementRegistry()
    seen: set[str] = set()
    for record in base.records:
        if record.assertion_id is None:
            continue
        assertion = base.registry.assertion(record.assertion_id)
        if assertion.reference_id not in seen:
            registry.add_reference(base.registry.reference(assertion.reference_id))
            seen.add(assertion.reference_id)
        registry.add_assertion(assertion)
    # A separate derived concrete fact, associated with the existing literature
    # reference but NOT represented as an additional fixed-literature component.
    registry.add_assertion(AssertionEntry(
        assertion_id=BASE_ID_1,
        reference_id=generic_1.reference_id,
        kind=AssertionKind.STATEMENT,
        content=pi4_3_statement,
        origin=AssertionOrigin.PROOF_INTERNAL,
        dependencies=(GENERAL_ID_1,),
    ))
    new_record = MigrationRecord(
        source="stable_base_specialization",
        source_key="1-stem/pi4_3",
        assertion_id=BASE_ID_1,
        status=MigrationStatus.STRUCTURED,
        detail=("Typed pi_4^3 result from existing Phase 50; specialization of "
                "5.1 n>=3; neither literature independently checked nor ancestry certified"),
    )
    return StableBaseRegistration(
        snapshot=RegistryBridgeResult(registry, base.records + (new_record,), base.proof_links),
        base_1_id=BASE_ID_1,
        base_2_id=BASE_ID_2,
        relation_1="WITHIN_GENERAL_SCOPE_N_EQUALS_3",
        relation_2="INDEPENDENT_MINIMUM_N_EQUALS_4_OUTSIDE_GENERAL_N_GE_5",
    )


def existing_stable_minimal_registration() -> StableBaseRegistration:
    """Construct candidate values from existing builders, without traversing ancestry."""
    from phase163_r4_registry_bridge import build_registry_bridge
    from toda_upstream_bootstrap import _build_phase50_result

    previous = register_prop51_prop53_literature_statements(
        build_registry_bridge(), existing_prop51_prop53_candidates()
    )
    pi4_3 = _build_phase50_result()["final_group_step"].conclusion
    return register_stable_minimal_dimensions(previous, pi4_3)
