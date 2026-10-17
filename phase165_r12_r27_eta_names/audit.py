"""Audit exact Web goal expansion, not just the normalized source definition."""
from __future__ import annotations
import json
from pathlib import Path
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r12_r2_quotient_rules import CyclicStructureStatement, QuotientIsomorphismStatement
from phase165_r12_r26_map_candidates import build_cited_eta_quotient_provider


def main() -> None:
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=3, k=1)
    if len(candidates) != 1:
        raise RuntimeError("expected exactly one pi4^3 goal")
    target_goal = candidates[0]
    cyclic = CyclicStructureStatement(target_goal.lhs, target_goal.rhs.generator, target_goal.rhs.order)
    direct = build_cited_eta_quotient_provider(bridge)(cyclic)
    shared = shared_expansion_provider(bridge, proof_target=target_goal)(cyclic)
    connected = [item for item in shared if any(item.subgoals == d.subgoals for d in direct)]
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    data = {
        "phase": "165 R12-R27",
        "web_generator_name": target_goal.rhs.generator.name,
        "exact_web_cyclic_candidate_count": len(direct),
        "common_candidate_count": len(connected),
        "candidate_subgoals": [[repr(g) for g in option.subgoals] for option in direct],
        "web_search_status": result.status.value,
        "web_search_complete": result.conclusion is not None and not result.open_goals,
        "open_goals": [repr(g) for g in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "full_pytest_run": False,
        "status": "WEB_COMPLETE" if result.conclusion is not None and not result.open_goals else "NORMALIZATION_CONNECTED_MORE_PROOFS_NEEDED",
    }
    destination = Path(__file__).resolve().parent / "audit_result.json"
    destination.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("Audit saved:", destination)


if __name__ == "__main__":
    main()
