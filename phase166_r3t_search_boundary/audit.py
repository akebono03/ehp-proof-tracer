"""R3-T read-only inspection of recursive proof and transport boundaries."""
from __future__ import annotations

import json
from pathlib import Path
from expression import IteratedSuspension
from homotopy_groups import TodaPrimaryGroup, TodaIteratedSuspensionMap, FiniteCyclicGroup
from proof import Relation, ProofRule
from toda_rules import Toda45IsomorphismStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase165_r57_r20_general_specialization import expand_cited_general_specialization

def inspect():
    bridge = build_shared_typed_bridge()
    given = tuple(link.step.conclusion for link in bridge.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN)
    goals = registered_group_goal_candidates(bridge, n=4, k=1)
    pi43 = registered_group_goal_candidates(bridge, n=3, k=1)
    base = TodaPrimaryGroup(4, 3)
    target = TodaPrimaryGroup(5, 4)
    iso = Toda45IsomorphismStatement(
        map=TodaIteratedSuspensionMap(
            exponent=1, source_group=base, target_group=target))
    specialization = expand_cited_general_specialization(iso, given)
    pi43_results = []
    for candidate in pi43:
        result = search_shared_group_goal(n=3, k=1, group_structure=candidate.rhs, bridge=bridge)
        pi43_results.append({
            "goal": repr(candidate),
            "status": result.status.name,
            "proven_steps": len(result.proven_steps),
        })
    targets = []
    for goal in goals:
        derived_base_candidates = []
        for source in pi43:
            if not isinstance(source.rhs, FiniteCyclicGroup):
                continue
            symbolic_suspension_goal = Relation(
                target,
                FiniteCyclicGroup(order=source.rhs.order,
                    generator=IteratedSuspension(
                        expression=source.rhs.generator, exponent=1)))
            expanded = expand_registered_toda45_finite_cyclic_goal(
                symbolic_suspension_goal, (source, iso))
            derived_base_candidates.append({
                "base": repr(source),
                "symbolic_transport_goal": repr(symbolic_suspension_goal),
                "hypothetical_expansion_count": len(expanded),
                "hypothetical_subgoals": [
                    [repr(subgoal) for subgoal in item.subgoals]
                    for item in expanded
                ],
            })
        targets.append({
            "goal": repr(goal),
            "direct_expansion_count": len(
                expand_registered_toda45_finite_cyclic_goal(goal, given)),
            "transport_with_derived_candidate": derived_base_candidates
        })
    return {
        "phase": "166 R3-T search boundary",
        "mode": "read_only",
        "production_code_modified": False,
        "pi43_candidate_count": len(pi43),
        "pi43_search": pi43_results,
        "concrete_toda45_specialization_count": len(specialization),
        "pi54": targets,
        "hypothetical_premises_are_not_proven_by_this_audit": True,
        "full_pytest_run": False
    }

def main():
    output = Path(__file__).with_name("report.json")
    report = inspect()
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2),
                      encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("REPORT:", output)

if __name__ == "__main__":
    main()
