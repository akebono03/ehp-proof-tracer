"""Phase 166 R3-G: read-only inspection of stable transport connection."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
from proof import Relation
from toda_rules import Toda45IsomorphismStatement
from homotopy_groups import TodaPrimaryGroup


def inspect() -> dict:
    bridge = build_shared_typed_bridge()
    goal_candidates = registered_group_goal_candidates(bridge, n=4, k=1)
    base_candidates = registered_group_goal_candidates(bridge, n=3, k=1)
    catalog, order_diagnostic = resolve_reviewed_order_catalog(bridge, n=4, k=1)
    statements = [link.step.conclusion for link in bridge.proof_links if link.step is not None]
    iso = [statement for statement in statements if isinstance(statement, Toda45IsomorphismStatement)]
    symbolic = [statement for statement in statements if _is_generic_eta_group_relation(statement)]
    report = {
        "phase": "166 R3-G route check",
        "production_changes": False,
        "pi54_goal_candidate_count": len(goal_candidates),
        "pi43_goal_candidate_count": len(base_candidates),
        "reviewed_order_available": catalog is not None,
        "reviewed_order_diagnostic": order_diagnostic,
        "toda45_given_count": len(iso),
        "toda45_target_matches_pi54": sum(getattr(statement.map, 'target_group', None) == TodaPrimaryGroup(5, 4) for statement in iso),
        "higher_eta_symbolic_given_count": len(symbolic),
        "candidate_analysis": [],
    }
    for goal in goal_candidates:
        transport = expand_registered_toda45_finite_cyclic_goal(goal, tuple(statements + base_candidates))
        report["candidate_analysis"].append({
            "goal": repr(goal),
            "toda45_direct_backward_options": len(transport),
            "rule_names": [x.rule.name for x in transport],
            "base_candidate_exactly_matched": any(
                getattr(base, 'lhs', None) == TodaPrimaryGroup(4, 3)
                for base in base_candidates
            ),
        })
    if len(goal_candidates) == 1:
        goal = goal_candidates[0]
        outcome = search_shared_group_goal(n=4, k=1, group_structure=goal.rhs, bridge=bridge, proof_order_catalog=catalog)
        roots = [s for s in outcome.proven_steps if s.conclusion == goal]
        report["public_result"] = {
            "status": outcome.status.value if hasattr(outcome.status, 'value') else str(outcome.status),
            "open_goal_count": len(outcome.open_goals),
            "open_goal_types": [type(x).__name__ for x in outcome.open_goals],
            "root_rules": [getattr(getattr(s, 'inference_rule', None), 'name', None) for s in roots],
            "diagnostics": list(outcome.diagnostics),
        }
    return report


if __name__ == '__main__':
    result = inspect()
    target = Path(__file__).resolve().parent / 'audit_result.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    print('Saved:', target)
