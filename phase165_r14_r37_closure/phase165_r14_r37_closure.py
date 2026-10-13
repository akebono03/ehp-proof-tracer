"""R37: attempt strict registry closure without upgrading unverified assertions."""
from __future__ import annotations

from pathlib import Path

from phase165_r14_r34_backward_search import pi32_goal, phase165_r34_expansions
from phase165_r14_r35_leaf_binding import backward_leaf_goals, known_source_candidates
from phase165_r14_r36_adopted_backward import adopted_leaf_steps, reconstruct_adopted_tex_goal
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from unified_statement_registry import AssertionOrigin


def registry_leaf_audit(tex_path: Path) -> tuple[dict, ...]:
    """Join by typed goal, not repr; never infer certification from a locator."""
    leaves = backward_leaf_goals(pi32_goal())
    adopted = adopted_leaf_steps(tex_path)
    candidates = known_source_candidates(tex_path)
    bridge, _ = build_phase165_r5_manifest_bridge()
    rows = []
    for goal in leaves:
        steps = [step for step in adopted if step.conclusion == goal]
        if len(steps) != 1:
            raise ValueError("frontier must have one adopted step")
        source = [c for c in candidates if c.goal == goal]
        if len(source) > 1:
            raise ValueError("ambiguous source candidate")
        locator = source[0].locator if source else ("(5.1)" if "FreeCyclicGroup" in repr(goal) else "Foundational")
        source_id = source[0].source_id if source else None
        existing = bridge.registry._assertions.get(source_id) if source_id else None
        if existing is not None and existing.origin is not AssertionOrigin.SOURCE_ARCHIVE:
            raise ValueError("source candidate changed classification unexpectedly")
        rows.append({
            "goal": repr(goal), "locator": locator,
            "source_id": source_id,
            "source_archive_present": existing is not None,
            "adopted_step_available": True,
            "strict_eligible": False,
            "blocker": ("FOUNDATIONAL_REVIEW" if locator == "Foundational"
                        else "EXACT_SOURCE_ID_UNRESOLVED" if source_id == "UNRESOLVED_EXACT_REGISTRY_ID"
                        else "SOURCE_ARCHIVE_NOT_VERIFIED"),
        })
    return tuple(rows)


def strict_search_attempt() -> tuple[bool, str]:
    """Invoke the existing production search unchanged with no invented approval."""
    bridge, _ = build_phase165_r5_manifest_bridge()
    citing = next((a.assertion_id for a in bridge.registry._assertions.values()
                   if a.origin is AssertionOrigin.FIXED_STATEMENT), None)
    if citing is None:
        raise ValueError("no fixed citing assertion registered")
    try:
        result = reconstruct_registered_goal(
            pi32_goal(), bridge, citing, phase165_r34_expansions,
            verified_assertion_ids=(),
        )
    except RegisteredGoalUnresolved as exc:
        return False, str(exc)
    if result.conclusion != pi32_goal():
        raise ValueError("unexpected strict proof goal")
    return True, ""


def audit_r37(tex_path: Path) -> dict:
    rows = registry_leaf_audit(tex_path)
    adopted_proof = reconstruct_adopted_tex_goal(pi32_goal(), adopted_leaf_steps(tex_path))
    strict_ok, reason = strict_search_attempt()
    return {
        "phase": "165 R14-R37", "goal": repr(pi32_goal()),
        "frontier_leaf_count": len(rows),
        "adopted_backward_proof_created": adopted_proof.conclusion == pi32_goal(),
        "strict_registry_proof_created": strict_ok,
        "strict_unresolved_reason": reason,
        "uncertified_leaf_count": sum(not x["strict_eligible"] for x in rows),
        "exact_source_id_unresolved_count": sum(x["blocker"] == "EXACT_SOURCE_ID_UNRESOLVED" for x in rows),
        "registry_assertions_promoted": 0,
        "existing_completed_proof_replay_used": False,
        "phase165_closed": strict_ok,
        "full_pytest_run": False,
        "status": ("STRICT_REGISTRY_PROOF_CREATED" if strict_ok
                   else "PHASE165_CLOSURE_BLOCKED_ON_SOURCE_CERTIFICATION"),
        "leaves": list(rows),
    }
