"""Phase 169 R3D: inspect live EHP-isomorphism dependencies without changing sources.

No unproved theorem, artificial GIVEN, or completed ProofStep is added.
"""
from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path

from homotopy_groups import (
    TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap,
)
from phase161_r4_literature_premise_matching import expand_phase161_r4_literature_goal
from phase165_r14_r5_ehp_connection import expand_registered_ehp_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates, search_group_from_registered_goal,
)
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule
from toda_rules import TodaProp42ExactnessStatement

PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parent
OUTPUT = PACKAGE / "output"


def _git(*args: str) -> str:
    completed = subprocess.run(
        ("git",) + args, cwd=REPOSITORY, capture_output=True,
        text=True, check=True, encoding="utf-8", errors="replace",
    )
    return completed.stdout.strip()


def _visible_assertions(bridge, context, goal: object) -> dict:
    """Report exact typed assertions; distinguish registered from eligible GIVEN."""
    registered = []
    for assertion in bridge.registry._assertions.values():
        if type(assertion.content) is not type(goal) or assertion.content != goal:
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        registered.append({
            "assertion_id": assertion.assertion_id,
            "locator": reference.locator,
            "publication_position": reference.publication_position,
            "component_position": assertion.component_position,
            "origin": assertion.origin.value,
        })
    screened = [
        link.assertion_id for link in context.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and type(link.step.conclusion) is type(goal)
        and link.step.conclusion == goal
    ]
    return {"registered": registered, "screened_given_assertion_ids": screened}


def _typed_requirement_types(bridge, context, requirement_type: type) -> dict:
    registered = []
    for a in bridge.registry._assertions.values():
        if isinstance(a.content, requirement_type):
            r = bridge.registry.reference(a.reference_id)
            registered.append({"id": a.assertion_id, "locator": r.locator,
                               "content_type": type(a.content).__name__})
    eligible = [
        link.assertion_id for link in context.proof_links
        if link.step is not None and isinstance(link.step.conclusion, requirement_type)
    ]
    return {"registered": registered[:15], "registered_count": len(registered),
            "screened_given_ids": eligible[:15], "screened_given_count": len(eligible)}


def _inspect_legacy_tree(goal: object, live, bridge, screened, depth: int = 0) -> dict:
    """Trace rule *proposals* only; never execute a rule or manufacture a step."""
    record = {
        "goal_type": type(goal).__name__, "goal_repr": repr(goal),
        "depth": depth, "live_provider_rule_names": [
            opt.rule.name for opt in live(goal)
        ],
        "exact_registered_provenance": _visible_assertions(bridge, screened, goal),
    }
    if depth > 8:
        record["depth_guard"] = True
        return record
    plans = expand_registered_ehp_goal(goal)
    if plans:
        record["historical_rule_names"] = [option.rule.name for option in plans]
        record["historical_subgoals"] = [
            _inspect_legacy_tree(child, live, bridge, screened, depth + 1)
            for child in plans[0].subgoals
        ]
        return record
    literature = expand_phase161_r4_literature_goal(goal)
    if literature is not None:
        record["literature_plan_rule"] = literature.inference_rule.name
        record["literature_requirements"] = [
            {"statement_type": requirement.statement_type.__name__,
             "required_proof_rule": (
                 requirement.proof_rule.value if requirement.proof_rule is not None else None
             ),
             "matching_registered_types": _typed_requirement_types(
                 bridge, screened, requirement.statement_type
             )}
            for requirement in literature.requirements
        ]
        return record
    if isinstance(goal, TodaProp42ExactnessStatement):
        record["prop42_specialization_candidates"] = len(live(goal))
    return record


def _flatten(tree: dict) -> list[dict]:
    return [tree] + [node for child in tree.get("historical_subgoals", ())
                     for node in _flatten(child)]


def run_audit() -> dict:
    """Read real published-position context for pi5^3 and inspect EHP frontier."""
    bridge = build_shared_typed_bridge()
    contexts = []
    lower = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    upper = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if not contexts:
        raise RuntimeError("Live pi5^3 search produced no screened citation context")
    screened = contexts[-1]
    upper_candidates = registered_group_goal_candidates(bridge, n=3, k=2)
    if lower.conclusion is None or len(upper_candidates) != 1:
        raise RuntimeError("Unique live typed group goal unavailable; no synthetic replacement")
    upper_goal = upper_candidates[0]
    lower_citing = resolve_specialized_goal_citing_id(bridge, lower.conclusion)
    upper_citing = resolve_specialized_goal_citing_id(bridge, upper_goal)
    publication = None
    if lower_citing is not None and upper_citing is not None:
        publication = precedes_citing_assertion(bridge, lower_citing, upper_citing)

    iso_goal = TodaSuspensionIsomorphismStatement(TodaSuspensionMap(
        TodaPrimaryGroup(4, 2), TodaPrimaryGroup(5, 3),
    ))
    live = shared_expansion_provider(screened, proof_target=upper_goal)
    historical = expand_registered_ehp_goal(iso_goal)
    tree = _inspect_legacy_tree(iso_goal, live, bridge, screened)
    nodes = _flatten(tree)
    exactness = [node for node in nodes if node["goal_type"] == "TodaProp42ExactnessStatement"]
    terminal = [node for node in nodes if node.get("literature_plan_rule")]
    unresolved_zero_options = [
        {"goal_type": node["goal_type"], "goal_repr": node["goal_repr"]}
        for node in nodes if not node["live_provider_rule_names"]
    ]
    record = {
        "phase": "169-R3D", "audit_only": True, "git_head": _git("rev-parse", "HEAD"),
        "lower_status": lower.status.value, "upper_status": upper.status.value,
        "upper_step_count": len(upper.proven_steps),
        "lower_citing_assertion": lower_citing,
        "upper_citing_assertion": upper_citing,
        "lower_claim_precedes_upper_claim": publication,
        "pi4_claim_screened_as_given": any(
            link.step is not None and link.step.conclusion == lower.conclusion
            for link in screened.proof_links
        ),
        "note": ("A screened pi4 claim is a registered fixed statement, not an "
                 "on-demand replay of its completed inference proof."),
        "iso_live_proposals": len(live(iso_goal)),
        "iso_historical_proposals": len(historical),
        "historical_tree": tree,
        "goal_type_counts": dict(Counter(node["goal_type"] for node in nodes)),
        "exactness_window_count": len(exactness),
        "exactness_windows_with_live_proposals": sum(
            bool(node["live_provider_rule_names"]) for node in exactness
        ),
        "literature_terminal_count": len(terminal),
        "literature_terminal_requirements": [
            {"goal_type": node["goal_type"], "rule": node["literature_plan_rule"],
             "required_types": node["literature_requirements"]}
            for node in terminal
        ],
        "live_missing_candidate_nodes": unresolved_zero_options,
        "completion_claim": False,
    }
    return record


def main() -> int:
    result = run_audit()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    dest = OUTPUT / "ehp_iso_dependency.json"
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("R3D_AUDIT_ONLY: no source, tests or documentation modified")
    for k in ("git_head", "lower_status", "upper_status", "upper_step_count",
              "lower_citing_assertion", "upper_citing_assertion",
              "lower_claim_precedes_upper_claim", "pi4_claim_screened_as_given",
              "iso_live_proposals", "iso_historical_proposals",
              "exactness_window_count", "exactness_windows_with_live_proposals",
              "literature_terminal_count"):
        print(f"{k.upper()}={result[k]}")
    for term in result["literature_terminal_requirements"]:
        print(f"TERMINAL {term['goal_type']} RULE={term['rule']}")
        for req in term["required_types"]:
            print("  REQUIRED", req["statement_type"], req["required_proof_rule"],
                  "REGISTERED", req["matching_registered_types"]["registered_count"],
                  "SCREENED", req["matching_registered_types"]["screened_given_count"])
    print("REPORT=" + str(dest))
    print("R3D_AUDIT_COMPLETE: no proof claim; full pytest not run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
