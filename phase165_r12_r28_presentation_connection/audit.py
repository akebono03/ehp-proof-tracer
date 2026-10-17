from __future__ import annotations
import json
from pathlib import Path
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r12_r2_quotient_rules import CyclicStructureStatement, HomomorphismPresentationStatement
from phase165_r12_r26_map_candidates import build_cited_eta_quotient_provider
from phase165_r12_r28_presentation_connection import expand_eta_presentation


def main() -> None:
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=3, k=1)
    if len(candidates) != 1:
        raise ValueError("Web goal is not unique")
    goal = candidates[0]
    cyclic = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    quotient_options = build_cited_eta_quotient_provider(bridge)(cyclic)
    presentations = []
    common_count = 0
    for option in quotient_options:
        for subgoal in option.subgoals:
            from phase165_r12_r2_quotient_rules import QuotientIsomorphismStatement
            if isinstance(subgoal, QuotientIsomorphismStatement):
                item = HomomorphismPresentationStatement(subgoal.map, subgoal.domain, subgoal.codomain,
                                                         subgoal.source_generator, subgoal.target_generator)
                presentations.append(item)
                common_count += len([o for o in shared_expansion_provider(bridge, proof_target=goal)(item)
                                     if any(o.subgoals == x.subgoals for x in expand_eta_presentation(item))])
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    report = {
        "phase": "165 R12-R28", "web_presentation_goal_count": len(presentations),
        "presentation_backward_candidate_count": sum(len(expand_eta_presentation(x)) for x in presentations),
        "common_presentation_candidate_count": common_count,
        "web_search_status": result.status.value,
        "web_search_complete": result.conclusion is not None and not result.open_goals,
        "open_goals": [repr(x) for x in result.open_goals],
        "diagnostics": list(result.diagnostics), "full_pytest_run": False,
    }
    dest = Path(__file__).resolve().parent / "audit_result.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", dest)


if __name__ == "__main__":
    main()
