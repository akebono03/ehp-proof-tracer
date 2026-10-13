"""R35: inventory and safely associate strict-search leaves with known source claims.

This is a locator map, not verification or a registry certification.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from phase165_r14_r34_backward_search import pi32_goal, phase165_r34_expansions
from phase165_r14_r33_final_group import pi33_cyclic_step, hopf_eta2_image_step
from phase165_r14_r31_hopf_injective import (
    toda51_pi21_zero_step, prop42_e_h_exactness_step,
)
from phase165_r14_r30_hopf_surjective import prop42_h_delta_exactness_step
from phase165_r14_r29_delta_derived import Prop42ApplicationPolicy
from phase165_r14_r26_prop42_typed import (
    bind_proposition42, adopted_tex_proofstep,
)
from phase165_r14_r24_delta_connection import reviewed_r23_isomorphism
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class LeafBindingCandidate:
    goal: object
    locator: str
    source_id: str
    evidence: str
    certification: str = "unverified_source_claim"


def backward_leaf_goals(root: object, limit: int = 80) -> tuple[object, ...]:
    """Enumerate original typed leaf objects, never parse their repr strings."""
    if type(limit) is not int or limit <= 0:
        raise ValueError("limit must be positive")
    queue = [root]
    visited = []
    leaves = []
    while queue:
        current = queue.pop(0)
        if any(current == existing for existing in visited):
            continue
        if len(visited) >= limit:
            raise ValueError("goal graph limit exceeded")
        visited.append(current)
        expansions = phase165_r34_expansions(current)
        if len(expansions) > 1:
            raise ValueError("ambiguous goal expansion")
        if expansions:
            queue.extend(expansions[0].subgoals)
        else:
            leaves.append(current)
    return tuple(leaves)


def known_source_candidates(tex_path: Path) -> tuple[LeafBindingCandidate, ...]:
    """Use the already implemented source-specific R23/R26/R30/R31/R33 factories.

    The factories produce provisional GIVEN claims, NOT registry eligible leaves.
    """
    policy = Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)
    bridge, _ = build_phase165_r5_manifest_bridge()
    r23_iso, _ = reviewed_r23_isomorphism(Path(tex_path))
    prop42_delta_e = adopted_tex_proofstep(
        bind_proposition42(bridge, n=1, i=2, index_scope_confirmed=True)
    )
    candidates = (
        (pi33_cyclic_step(tex_path), "(5.1)", "phase163:archive:toda:(5.1)", "diagonal group"),
        (hopf_eta2_image_step(), "Proposition 5.1", "UNRESOLVED_EXACT_REGISTRY_ID", "Hopf generator image"),
        (toda51_pi21_zero_step(tex_path), "(5.1)", "phase163:archive:toda:(5.1)", "pi_2(S^1)=0"),
        (prop42_e_h_exactness_step(policy), "Proposition 4.2", "phase163:archive:toda:tex:ch4:0005", "E to H exactness"),
        (prop42_h_delta_exactness_step(policy), "Proposition 4.2", "phase163:archive:toda:tex:ch4:0005", "H to Delta exactness"),
        (prop42_delta_e, "Proposition 4.2", "phase163:archive:toda:tex:ch4:0005", "Delta to E exactness"),
    )
    result = []
    for step, locator, source_id, evidence in candidates:
        if not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN:
            raise ValueError("expected source-specific provisional leaf")
        result.append(LeafBindingCandidate(step.conclusion, locator, source_id, evidence))
    # The R23 suspension is a derived premise and must NOT be mapped as a source leaf.
    if r23_iso.rule is not ProofRule.INFERENCE:
        raise ValueError("R23 derived suspension premise changed")
    return tuple(result)


def audit_r35(tex_path: Path) -> dict:
    """Provide a per-leaf mismatch report; never silently fill gaps."""
    leaves = backward_leaf_goals(pi32_goal())
    candidates = known_source_candidates(tex_path)
    rows = []
    for index, goal in enumerate(leaves, start=1):
        matches = [row for row in candidates if row.goal == goal]
        if len(matches) > 1:
            status = "AMBIGUOUS_SOURCE_CANDIDATES"
        elif len(matches) == 1:
            status = "SOURCE_CANDIDATE_FOUND_NOT_CERTIFIED"
        else:
            status = "NEEDS_RULE_OR_SOURCE_REVIEW"
        matched = matches[0] if len(matches) == 1 else None
        rows.append({
            "number": index,
            "goal": repr(goal),
            "type": type(goal).__name__,
            "status": status,
            "candidate_locator": matched.locator if matched else None,
            "candidate_source_id": matched.source_id if matched else None,
            "evidence": matched.evidence if matched else None,
            "strict_eligible": False,
        })
    mapped = sum(r["status"] == "SOURCE_CANDIDATE_FOUND_NOT_CERTIFIED" for r in rows)
    return {
        "phase": "165 R14-R35",
        "total_unresolved_leaves": len(rows),
        "source_candidate_match_count": mapped,
        "remaining_review_count": len(rows) - mapped,
        "leaf_bindings": rows,
        "registry_assertions_promoted": 0,
        "existing_proof_replay_used": False,
        "strict_registry_proof_created": False,
        "status": "SOURCE_LEAVES_MAPPED_CERTIFICATION_PENDING",
        "full_pytest_run": False,
    }
