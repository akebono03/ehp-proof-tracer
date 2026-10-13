"""R14-R19: optional reviewed Toda (5.1) diagonal facts in an isolated registry.

An explicit review record is required. No archival source is automatically a leaf.
"""
from __future__ import annotations
from dataclasses import dataclass
from phase163_r4_registry_bridge import (
    RegistryBridgeResult, MigrationRecord, MigrationStatus,
)
from phase165_r14_r15_typed_diagonal import match_diagonal_toda51_claims
from phase165_r14_r18_diagonal_integration import derive_diagonal_iso_from_certified_groups
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from proof import ProofStep, ProofRule
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ReferenceKind, ProofStepLink, UnifiedStatementRegistry,
)

@dataclass(frozen=True)
class DiagonalSourceReview:
    """Manual review, not an automatic claim about Toda's original edition."""
    assertion_ids: tuple[str, str]
    adopted_tex_clause_confirmed: bool = False
    original_edition_confirmed: bool = False

def _diagonal_goals():
    suspension = TodaSuspensionMap(TodaPrimaryGroup(1,1), TodaPrimaryGroup(2,2))
    rows = match_diagonal_toda51_claims(suspension)
    if len(rows) != 3 or any(r.verified for r in rows[:2]):
        raise ValueError("unexpected R15 diagonal claim contract")
    return suspension, (rows[0].goal, rows[1].goal)

def reviewed_diagonal_bridge(base: RegistryBridgeResult,
                             review: DiagonalSourceReview | None = None):
    """Add typed reviewed entries to a fresh registry, never mutate base."""
    suspension, goals = _diagonal_goals()
    if review is None or not review.adopted_tex_clause_confirmed:
        return base, (), "REVIEW_REQUIRED"
    if review.assertion_ids != (
        "phase165:r14r19:toda51:diagonal:n1",
        "phase165:r14r19:toda51:diagonal:n2",
    ):
        raise ValueError("review assertion identifiers mismatch")
    ref_id = "phase165:r14r19:reviewed:toda51"
    registry = UnifiedStatementRegistry()
    for entry in base.registry._references.values():
        registry.add_reference(entry)
    for entry in base.registry._assertions.values():
        registry.add_assertion(entry)
    registry.add_reference(LiteratureEntry(
        reference_id=ref_id, kind=ReferenceKind.EQUATION, locator="(5.1)",
        source_id="Toda adopted TeX; original edition verified" if review.original_edition_confirmed
                  else "Toda adopted TeX; original edition unverified",
        publication_position=1,
    ))
    records = list(base.records)
    links = list(base.proof_links)
    added = []
    for aid, goal in zip(review.assertion_ids, goals):
        registry.add_assertion(AssertionEntry(
            assertion_id=aid, reference_id=ref_id,
            kind=AssertionKind.STATEMENT, content=goal,
            origin=AssertionOrigin.FIXED_STATEMENT,
            available_after_position=1,
        ))
        records.append(MigrationRecord(
            "reviewed_adopted_tex", aid, aid, MigrationStatus.STRUCTURED,
            "explicit reviewer attestation of (5.1) diagonal clause",
        ))
        links.append(ProofStepLink(aid, step=ProofStep(
            conclusion=goal, premises=(), rule=ProofRule.GIVEN,
            note="Explicitly reviewed Toda (5.1) adopted TeX clause",
        )))
        added.append(aid)
    return RegistryBridgeResult(registry, tuple(records), tuple(links)), tuple(added), "REVIEWED_ADOPTED_TEX"

def audit_r19():
    base, _ = build_phase165_r5_manifest_bridge()
    bridge, ids, status = reviewed_diagonal_bridge(base)
    _, goals = _diagonal_goals()
    try:
        derive_diagonal_iso_from_certified_groups(
            TodaSuspensionMap(TodaPrimaryGroup(1,1),TodaPrimaryGroup(2,2)),
            None, None,
        )
    except ValueError:
        fail_closed = True
    else:
        fail_closed = False
    return {
        "phase": "165 R14-R19",
        "source_locator": "(5.1)",
        "typed_diagonal_claims": len(goals),
        "review_status": status,
        "reviewed_assertions_added": len(ids),
        "new_proof_steps": 0,
        "base_registry_unchanged": bridge is base,
        "fail_closed_unreviewed": fail_closed,
        "pi32_proved": False,
        "status": "REVIEW_GATE_READY_PRODUCTION_LEAVES_NOT_ADMITTED",
        "full_pytest_run": False,
    }
