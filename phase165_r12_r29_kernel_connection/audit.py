from __future__ import annotations
import json
from pathlib import Path
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r12_r29_kernel_connection import expand_kernel_multiple_from_suspension
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r12_r26_map_candidates import build_cited_eta_quotient_provider
from phase165_r12_r28_presentation_connection import expand_eta_presentation


def main() -> None:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=1)
    if len(goals) != 1:
        raise ValueError("expected unique pi4^3 goal")
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    goal = goals[0]
    cyclic = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    expansions = build_cited_eta_quotient_provider(bridge)(cyclic)
    if len(expansions) != 1:
        raise ValueError("expected one quotient expansion")
    quotient = expansions[0].subgoals[0]
    from phase165_r12_r2_quotient_rules import first_isomorphism_quotient_inference_rule
    from phase165_r8_rule_provider import create_rule_expansion_provider
    iso_steps = create_rule_expansion_provider((first_isomorphism_quotient_inference_rule(),))(quotient)
    kernel = next(x for x in iso_steps[0].subgoals if isinstance(x, KernelMultipleStatement))
    direct = expand_kernel_multiple_from_suspension(kernel)
    shared = shared_expansion_provider(bridge, proof_target=goal)(kernel)
    matches = [x for x in shared if any(x.subgoals == d.subgoals for d in direct)]
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    status = getattr(result.status, "value", str(result.status))
    data = {
        "phase": "165 R12-R29",
        "kernel_backward_candidate_count": len(direct),
        "common_kernel_candidate_count": len(matches),
        "kernel_subgoals": [repr(x) for d in direct for x in d.subgoals],
        "web_search_status": status,
        "web_search_complete": result.conclusion is not None and not result.open_goals,
        "open_goals": [repr(x) for x in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "full_pytest_run": False,
    }
    filename = Path(__file__).with_name("audit_result.json")
    filename.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("Audit saved:", filename)


if __name__ == "__main__":
    main()
