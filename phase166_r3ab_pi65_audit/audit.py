"""Phase 166 R3-AB: read-only pi6^5 publication and transport diagnostic."""
from __future__ import annotations

import json
import traceback
from pathlib import Path

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider, search_shared_group_goal
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase166_r3c_publication_order import precedes_citing_assertion
from proof import ProofRule, Relation
from toda_rules import Toda45IsomorphismStatement


def _run(label, callback):
    try:
        result = callback()
        return {
            "label": label,
            "status": str(result.status),
            "complete": str(result.status).endswith(".COMPLETE"),
            "conclusion": repr(result.conclusion),
            "open_goals": [repr(x) for x in result.open_goals],
            "diagnostics": [str(x) for x in result.diagnostics],
        }
    except Exception as exc:
        return {"label": label, "exception": repr(exc),
                "traceback": traceback.format_exc(limit=8)}


def audit_pi65():
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=5, k=1)
    report = {"phase": "166 R3-AB", "production_code_modified": False,
              "full_pytest_run": False, "candidate_count": len(candidates)}
    if len(candidates) != 1:
        report["candidate_reprs"] = [repr(x) for x in candidates]
        return report
    goal = candidates[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    report["goal"] = repr(goal)
    report["citing_assertion_id"] = citing_id
    if citing_id is None:
        report["failure_point"] = "missing publication target"
        report["web_search"] = _run("web", lambda: search_group_from_registered_goal(n=5,k=1,bridge=bridge))
        return report
    context = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    )
    given = [(link.assertion_id, link.step.conclusion) for link in context.proof_links
             if link.step is not None and link.step.rule is ProofRule.GIVEN]
    pi43 = [(i, x) for i, x in given
            if isinstance(x, Relation) and x.lhs == TodaPrimaryGroup(4,3)
            and isinstance(x.rhs, FiniteCyclicGroup)]
    toda45 = [(i, x) for i, x in given if isinstance(x, Toda45IsomorphismStatement)]
    report["given_count"] = len(given)
    report["pi43"] = [{"id": i, "value": repr(x),
                       "precedes": precedes_citing_assertion(bridge,i,citing_id)} for i,x in pi43]
    report["toda45"] = [{"id": i, "value": repr(x),
                         "precedes": precedes_citing_assertion(bridge,i,citing_id)} for i,x in toda45]
    provider = shared_expansion_provider(context, proof_target=goal)
    options = provider(goal)
    report["root_options"] = [{"rule": x.rule.name,
                               "subgoals": [repr(y) for y in x.subgoals]} for x in options]
    children = []
    for item in options:
        for child in item.subgoals:
            if isinstance(child, Relation) and isinstance(child.rhs, FiniteCyclicGroup):
                candidates_child = provider(child)
                children.append({
                    "goal": repr(child),
                    "suspension_exponent": getattr(child.rhs.generator, "exponent", None)
                        if isinstance(child.rhs.generator, IteratedSuspension) else None,
                    "rules": [{"rule": o.rule.name, "subgoals": [repr(g) for g in o.subgoals]}
                              for o in candidates_child],
                })
    report["cyclic_children"] = children
    catalog, diagnostic = resolve_reviewed_order_catalog(bridge, n=5,k=1)
    report["legacy_catalog"] = {"present": catalog is not None, "diagnostic": diagnostic}
    report["direct_search"] = _run("direct", lambda: search_shared_group_goal(
        n=5,k=1,group_structure=goal.rhs,bridge=bridge,citing_assertion_id=citing_id,
    ))
    report["web_search"] = _run("web", lambda: search_group_from_registered_goal(
        n=5,k=1,bridge=bridge,
    ))
    return report


def main():
    report = audit_pi65()
    output = Path(__file__).with_name("report.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {k: report.get(k) for k in (
        "phase", "candidate_count", "citing_assertion_id", "given_count",
        "pi43", "toda45", "legacy_catalog", "direct_search", "web_search",
    )}
    summary["root_rule_names"] = [x["rule"] for x in report.get("root_options", [])]
    summary["cyclic_child_rule_names"] = [
        {"exponent": c["suspension_exponent"], "rules": [x["rule"] for x in c["rules"]]}
        for c in report.get("cyclic_children", [])
    ]
    summary["report"] = str(output)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
