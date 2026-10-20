"""R3-T: read-only diagnosis of Toda (4.5) backward matching."""
from __future__ import annotations
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from proof import ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension

def inspect():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=1)
    given = [
        (link.assertion_id, link.step.conclusion)
        for link in bridge.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    ]
    isos = [(i, item) for i, item in given if isinstance(item, Toda45IsomorphismStatement)]
    bases = [(i, item) for i, item in given if
             isinstance(item, Relation) and item.relation_type is RelationType.EQUALITY
             and isinstance(item.lhs, TodaPrimaryGroup)
             and isinstance(item.rhs, FiniteCyclicGroup)]
    suspensions = [(i, item) for i, item in given if isinstance(item, GeneratorSuspension)]
    cases = []
    for goal in goals:
        candidates = []
        for iso_id, iso in isos:
            m = iso.map
            target_matches = m.target_group == goal.lhs
            eligible_bases = [(i, b) for i, b in bases
                              if b.lhs == m.source_group and b.rhs.order == goal.rhs.order]
            for base_id, base in eligible_bases:
                expected = IteratedSuspension(expression=base.rhs.generator, exponent=m.exponent)
                candidates.append({
                    "iso_assertion_id": iso_id,
                    "base_assertion_id": base_id,
                    "target_group_matches": target_matches,
                    "source_group_matches": base.lhs == m.source_group,
                    "order_matches": base.rhs.order == goal.rhs.order,
                    "expected_generator": repr(expected),
                    "goal_generator": repr(goal.rhs.generator),
                    "generator_matches": expected == goal.rhs.generator,
                })
            if not eligible_bases:
                candidates.append({
                    "iso_assertion_id": iso_id,
                    "target_group_matches": target_matches,
                    "source_group": repr(m.source_group),
                    "target_group": repr(m.target_group),
                    "eligible_given_base_count": 0
                })
        provider = shared_expansion_provider(bridge, proof_target=goal)
        expansions = provider(goal)
        cases.append({
            "goal": repr(goal),
            "isomorphism_given_count": len(isos),
            "base_relation_given_count": len(bases),
            "generator_suspension_given_count": len(suspensions),
            "generator_suspensions": [{"assertion_id": i, "statement": repr(s)} for i,s in suspensions],
            "match_matrix": candidates,
            "direct_toda45_options": len(expand_registered_toda45_finite_cyclic_goal(goal, tuple(v for _,v in given))),
            "common_rule_names": [x.rule.name for x in expansions],
            "eta_specialization_exists": any("higher-eta specialization" in x.rule.name for x in expansions),
        })
    return {
        "phase": "166 R3-T gate audit",
        "mode": "read_only",
        "production_code_modified": False,
        "goal_count": len(goals),
        "cases": cases,
        "full_pytest_run": False,
    }

def main():
    report = inspect()
    output = Path(__file__).with_name("r3t_gate_report.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("REPORT:", output)

if __name__ == "__main__":
    main()
