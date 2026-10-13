"""R14-R23: upgrade the TWO diagonal instances already held by Toda (5.1).

The upgrade is limited to explicitly checked adopted TeX.  It never promotes
archive assertions wholesale or alters the original bridge.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase165_r14_r18_diagonal_integration import derive_diagonal_iso_from_certified_groups
from phase165_r14_r21_toda51_completion import complete_toda51_source
from phase165_r14_r22_same_reference import integrate_toda51_into_existing_reference
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, ProofStepLink,
    UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class AdoptedTextReview:
    """Explicit source review: this is not a claim of original-edition verification."""
    complete_source_sha256: str
    diagonal_clause_checked: bool
    reviewer_note: str


def promote_diagonal_from_existing_reference(
    bridge: RegistryBridgeResult, review: AdoptedTextReview | None,
) -> tuple[RegistryBridgeResult, tuple[str, ...]]:
    """Create two typed FIXED_STATEMENT instances under the SAME (5.1) reference.

    Caller must compare source text with the adopted TeX and attest that fact.
    The existing six SOURCE_ARCHIVE components remain untouched.
    """
    if review is None or not review.diagonal_clause_checked or not review.reviewer_note.strip():
        raise ValueError("explicit adopted-TeX review required")
    diagonal_id = "phase165:r14r22:toda51:diagonal_cyclic"
    diagonal = bridge.registry.assertion(diagonal_id)
    if diagonal.origin is not AssertionOrigin.SOURCE_ARCHIVE:
        raise ValueError("diagonal source component is not an archive")
    if diagonal.content.get("complete_source_sha256") != review.complete_source_sha256:
        raise ValueError("adopted source checksum mismatch")
    if diagonal.content.get("clause_key") != "diagonal_cyclic":
        raise ValueError("wrong source clause")
    goals = diagonal.content.get("typed_specializations")
    if not isinstance(goals, tuple) or len(goals) != 2:
        raise ValueError("exactly two existing typed instances required")
    if (goals[0].lhs != TodaPrimaryGroup(1, 1)
            or goals[1].lhs != TodaPrimaryGroup(2, 2)):
        raise ValueError("invalid specialized dimensions")
    registry = UnifiedStatementRegistry()
    for entry in bridge.registry._references.values():
        registry.add_reference(entry)
    for entry in bridge.registry._assertions.values():
        registry.add_assertion(entry)
    ids = (
        "phase165:r14r23:toda51:diagonal:n1",
        "phase165:r14r23:toda51:diagonal:n2",
    )
    records = list(bridge.records)
    links = list(bridge.proof_links)
    for aid, goal in zip(ids, goals):
        registry.add_assertion(AssertionEntry(
            assertion_id=aid,
            reference_id=diagonal.reference_id,
            kind=AssertionKind.STATEMENT,
            content=goal,
            origin=AssertionOrigin.FIXED_STATEMENT,
            # Do not invent an original-edition verified availability position.
            available_after_position=None,
        ))
        records.append(MigrationRecord(
            source="phase165_r14_r23_adopted_tex_review",
            source_key=diagonal_id,
            assertion_id=aid,
            status=MigrationStatus.STRUCTURED,
            detail=review.reviewer_note,
        ))
        links.append(ProofStepLink(
            assertion_id=aid,
            step=ProofStep(
                conclusion=goal,
                premises=(),
                rule=ProofRule.GIVEN,
                note="Toda (5.1) adopted TeX diagonal cyclic clause: " + review.reviewer_note,
            ),
        ))
    return RegistryBridgeResult(registry, tuple(records), tuple(links)), ids


def derive_reviewed_diagonal_iso(
    bridge: RegistryBridgeResult, ids: tuple[str, ...],
) -> ProofStep:
    """Use the existing R18 inference rule; no legacy replay."""
    if len(ids) != 2 or len(set(ids)) != 2:
        raise ValueError("two distinct reviewed assertion IDs required")
    steps = []
    for aid in ids:
        assertion = bridge.registry.assertion(aid)
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            raise ValueError("reviewed source must be fixed statement")
        matches = tuple(link for link in bridge.proof_links if link.assertion_id == aid)
        if len(matches) != 1 or matches[0].step is None:
            raise ValueError("exactly one reviewed proof link required")
        step = matches[0].step
        if step.conclusion != assertion.content:
            raise ValueError("citation ProofStep conclusion mismatch")
        steps.append(step)
    suspension = TodaSuspensionMap(TodaPrimaryGroup(1, 1), TodaPrimaryGroup(2, 2))
    return derive_diagonal_iso_from_certified_groups(suspension, steps[0], steps[1])


def audit_r23(tex_path: Path) -> dict:
    tex = tex_path.read_text(encoding="utf-8")
    completed = complete_toda51_source(tex)
    base, summary = build_phase165_r5_manifest_bridge()
    r22 = integrate_toda51_into_existing_reference(base, tex)
    review = AdoptedTextReview(
        complete_source_sha256=completed.source_sha256,
        diagonal_clause_checked=True,
        reviewer_note="Adopted TeX (5.1) six clauses supplied and confirmed in project conversation; original edition not checked",
    )
    updated, ids = promote_diagonal_from_existing_reference(r22.bridge, review)
    proof = derive_reviewed_diagonal_iso(updated, ids)
    from phase165_r2_registry_lookup import find_eligible_goal_candidates
    # Separate review-based proof assembly from strict production citation eligibility.
    strict = find_eligible_goal_candidates(
        updated, updated.registry.assertion(ids[0]).content, ids[1],
        verified_assertion_ids=ids,
    )
    if len(base.registry._assertions) + 8 != len(updated.registry._assertions):
        raise RuntimeError("unexpected archive modification")
    return {
        "phase": "165 R14-R23",
        "reference_id": r22.reference_id,
        "original_manifest_assertions": summary.source_assertion_count,
        "six_source_components_preserved": all(
            updated.registry.assertion(aid).origin is AssertionOrigin.SOURCE_ARCHIVE
            for aid in r22.component_ids
        ),
        "typed_fixed_diagonal_claims": len(ids),
        "reviewed_toda_leaf_proofsteps": len(ids),
        "derived_suspension_iso_steps": 1,
        "derived_iso": repr(proof.conclusion),
        "derived_rule": proof.rule.value,
        "strict_citation_eligible_count": len(strict),
        "original_edition_verified": False,
        "production_pi32_proved": False,
        "status": "ADOPTED_TEX_DIAGONAL_ISO_DERIVED_STRICT_CITATION_PENDING",
        "full_pytest_run": False,
    }
