"""Phase 169 R3A: read-only diagnosis of pi_4^2 -> pi_5^3 EHP dependencies.

No rule or ProofStep is created as an axiom. The optional prior-proof probe is
labeled experimental and never writes it to the application's proof catalog.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys
import traceback

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from homotopy_groups import TodaSuspensionIsomorphismStatement
from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase165_r14_r5_ehp_connection import expand_registered_ehp_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge,
    search_shared_group_goal,
    shared_expansion_provider,
)
from phase165_r52_r17_internal_dependency import CompletedInternalProof
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase165_r57_r12_ordered_proofs import OrderedCompletedProof
from phase165_r57_r16_web_proof_order import REVIEWED_PROOF_TARGET_ORDER
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule


def inspect_expansions(goal, provider):
    """List typed proposals only; no proposal is considered a derivation."""
    try:
        options = provider(goal)
        if not isinstance(options, tuple):
            raise TypeError("expansion provider returned a non-tuple")
    except Exception as exc:
        return {"type": type(goal).__name__, "goal": repr(goal),
                "error": type(exc).__name__ + ": " + str(exc)}
    return {
        "type": type(goal).__name__,
        "goal": repr(goal),
        "candidate_count": len(options),
        "rule_counts": dict(Counter(getattr(e.rule, "name", "<unnamed>") for e in options)),
        "expansions": [{
            "rule": getattr(e.rule, "name", "<unnamed>"),
            "premise_types": [type(x).__name__ for x in e.subgoals],
            "premises": [repr(x) for x in e.subgoals],
        } for e in options],
    }


def inspect_screened_given(bridge, goal):
    """Look for a linked, screened, exact GIVEN; never adopt mere registry text."""
    matches = []
    for link in bridge.proof_links:
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        if type(step.conclusion) is not type(goal) or step.conclusion != goal:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.content != goal:
            continue
        ref = bridge.registry.reference(assertion.reference_id)
        matches.append({"assertion_id": assertion.assertion_id, "locator": ref.locator})
    return matches


def inspect_prior_proof_experiment(bridge, proof4, goal4, goal5, citing5):
    """Test a caller-local ordered prior proof, not a published order decision.

    The current Web route is never patched and the result is NOT production
    availability, even if a trial succeeds. Refuse missing citation boundaries.
    """
    if citing5 is None:
        return {"stage": "SKIPPED_UNRESOLVED_CITATION_BOUNDARY"}
    if proof4.status is not ProofSearchStatus.COMPLETE:
        return {"stage": "SKIPPED_PI4_NOT_PROVED"}
    roots = [step for step in proof4.proven_steps
             if step.rule is ProofRule.INFERENCE
             and type(step.conclusion) is type(goal4)
             and step.conclusion == goal4]
    if len(roots) != 1:
        return {"stage": "SKIPPED_NONUNIQUE_PI4_PROOF_ROOT", "root_count": len(roots)}
    try:
        prior = OrderedCompletedProof(CompletedInternalProof(roots[0]), 0)
        experiment = search_shared_group_goal(
            n=3, k=2, group_structure=goal5.rhs,
            bridge=bridge, citing_assertion_id=citing5,
            ordered_completed_proofs=(prior,), target_order=1,
        )
        return {
            "stage": "LOCAL_ORDER_EXPERIMENT_ONLY_NOT_WEB_PROOF",
            "status": experiment.status.value,
            "proven_steps": len(experiment.proven_steps),
            "open_goals": [repr(x) for x in experiment.open_goals],
            "diagnostics": list(experiment.diagnostics),
        }
    except Exception as exc:
        return {"stage": "LOCAL_ORDER_EXPERIMENT_ERROR",
                "error": type(exc).__name__ + ": " + str(exc)}


def audit():
    bridge = build_shared_typed_bridge()
    goals4 = registered_group_goal_candidates(bridge, n=2, k=2)
    goals5 = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(goals4) != 1 or len(goals5) != 1:
        return {"audit_status": "STOP_NONUNIQUE_GOALS",
                "pi4_goal_count": len(goals4), "pi5_goal_count": len(goals5)}
    goal4, goal5 = goals4[0], goals5[0]
    contexts = []
    proof5 = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    proof4 = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    if len(contexts) != 1:
        return {"audit_status": "STOP_SCREENED_CONTEXT_MISSING",
                "context_count": len(contexts), "pi5_status": proof5.status.value}
    screened = contexts[0]
    citing5 = resolve_specialized_goal_citing_id(bridge, goal5)
    provider = shared_expansion_provider(screened, proof_target=goal5)
    iso_goal = phase161_r5_target_goal()
    if not isinstance(iso_goal, TodaSuspensionIsomorphismStatement):
        raise TypeError("historical EHP goal has unexpected type")
    if iso_goal.map.source_group != goal4.lhs or iso_goal.map.target_group != goal5.lhs:
        raise ValueError("historical EHP map endpoints do not match current group goals")
    legacy = expand_registered_ehp_goal(iso_goal)
    legacy_subgoals = []
    for expansion in legacy:
        for goal in expansion.subgoals:
            if not any(type(old) is type(goal) and old == goal for old in legacy_subgoals):
                legacy_subgoals.append(goal)
    inspections = [inspect_expansions(iso_goal, provider)]
    for child in legacy_subgoals:
        report = inspect_expansions(child, provider)
        report["screened_given"] = inspect_screened_given(screened, child)
        inspections.append(report)
    # A second level is useful when diagnosing exactness and Hopf properties;
    # inspect only the first three proposals per child to bound output.
    grandchildren = []
    for child in legacy_subgoals:
        for expansion in provider(child)[:3]:
            for subgoal in expansion.subgoals:
                if not any(type(old) is type(subgoal) and old == subgoal for old in grandchildren):
                    grandchildren.append(subgoal)
    for child in grandchildren[:20]:
        report = inspect_expansions(child, provider)
        report["screened_given"] = inspect_screened_given(screened, child)
        inspections.append(report)
    return {
        "audit_status": "OBSERVED",
        "pi4_status": proof4.status.value,
        "pi4_steps": len(proof4.proven_steps),
        "pi5_status": proof5.status.value,
        "pi5_steps": len(proof5.proven_steps),
        "pi5_open_goals": [repr(x) for x in proof5.open_goals],
        "pi5_citation_boundary": citing5,
        "pi4_registered_as_prior": (2, 2) in REVIEWED_PROOF_TARGET_ORDER,
        "pi5_registered_in_proof_order": (3, 2) in REVIEWED_PROOF_TARGET_ORDER,
        "pi4_group_goal": repr(goal4),
        "pi5_group_goal": repr(goal5),
        "ehp_iso_goal": repr(iso_goal),
        "historical_ehp_root_proposals": len(legacy),
        "historical_ehp_root_rules": [getattr(x.rule, "name", "<unnamed>") for x in legacy],
        "historical_ehp_root_premises": [[repr(x) for x in e.subgoals] for e in legacy],
        "common_provider_inspections": inspections,
        "experimental_pi4_reuse": inspect_prior_proof_experiment(
            bridge, proof4, goal4, goal5, citing5,
        ),
        "production_patched": False,
    }


def render_report(data):
    lines = ["Phase 169 R3A — pi_5^3 EHP and prior-proof frontier",
             "AUDIT_ONLY: no application, test or documentation edits",
             "AUDIT_STATUS=" + str(data.get("audit_status"))]
    for key in ("pi4_status", "pi4_steps", "pi5_status", "pi5_steps",
                "pi5_citation_boundary", "pi4_registered_as_prior",
                "pi5_registered_in_proof_order", "ehp_iso_goal",
                "historical_ehp_root_proposals", "historical_ehp_root_rules"):
        lines.append(key.upper() + "=" + str(data.get(key)))
    lines.append("\nCURRENT COMMON BACKWARD PROVIDER:")
    for part in data.get("common_provider_inspections", []):
        lines.append("GOAL=" + part["type"] + " " + part["goal"])
        lines.append("  CANDIDATES=" + str(part.get("candidate_count")))
        lines.append("  RULES=" + str(part.get("rule_counts")))
        if "error" in part:
            lines.append("  ERROR=" + str(part["error"]))
        for candidate in part.get("expansions", []):
            lines.append("  RULE=" + candidate["rule"])
            for premise in candidate["premises"]:
                lines.append("    PREMISE=" + premise)
        if "screened_given" in part:
            lines.append("  DIRECT_SCREENED_GIVEN=" + str(part["screened_given"]))
    lines.append("\nEXPERIMENTAL ORDERED PI4 REUSE (NEVER PRODUCTION):")
    lines.append(json.dumps(data.get("experimental_pi4_reuse", {}),
                            ensure_ascii=False, indent=2))
    return "\n".join(lines) + "\n"


def main():
    out = PACKAGE / "output"
    out.mkdir(exist_ok=True)
    try:
        data = audit()
    except Exception:
        error = traceback.format_exc()
        (out / "audit_error.txt").write_text(error, encoding="utf-8")
        print(error)
        return 1
    (out / "ehp_reuse_frontier.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8",
    )
    (out / "ehp_reuse_frontier.txt").write_text(render_report(data), encoding="utf-8")
    print("AUDIT_STATUS", data.get("audit_status"))
    for k in ("pi4_status", "pi5_status", "pi4_registered_as_prior",
              "historical_ehp_root_proposals"):
        print(k.upper(), data.get(k))
    for x in data.get("common_provider_inspections", []):
        print("GOAL", x["type"], "CANDIDATES", x.get("candidate_count"),
              "RULES", x.get("rule_counts"))
    trial = data.get("experimental_pi4_reuse", {})
    print("PI4_REUSE_EXPERIMENT", trial.get("stage"), trial.get("status"))
    print("REPORT", out / "ehp_reuse_frontier.txt")
    print("JSON", out / "ehp_reuse_frontier.json")
    return 0 if data.get("audit_status") == "OBSERVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
