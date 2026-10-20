"""Inspect real Toda (4.5) generic-to-concrete inference opportunities."""
from __future__ import annotations
import json
from pathlib import Path

from expression import IteratedSuspension
from homotopy_groups import TodaPrimaryGroup, FiniteCyclicGroup, TodaIteratedSuspensionMap
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r57_r20_general_specialization import (
    specialize_typed_statement, expand_cited_general_specialization,
)
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from proof import Relation, ProofRule
from toda_rules import Toda45IsomorphismStatement
from phase165_r55_nk_only_goal import registered_group_goal_candidates


def inspect():
    bridge = build_shared_typed_bridge()
    sources = tuple(link.step.conclusion for link in bridge.proof_links
                    if link.step is not None and link.step.rule is ProofRule.GIVEN)
    symbolic = tuple(s for s in sources
                     if isinstance(s, Toda45IsomorphismStatement))
    target = TodaPrimaryGroup(5, 4)
    base = TodaPrimaryGroup(4, 3)
    goal_iso = Toda45IsomorphismStatement(
        map=TodaIteratedSuspensionMap(exponent=1,
            source_group=base, target_group=target))
    matching = [(s, specialize_typed_statement(s, goal_iso)) for s in symbolic]
    options = expand_cited_general_specialization(goal_iso, sources)
    targets = registered_group_goal_candidates(bridge, n=4, k=1)
    return {
       "phase": "166 R3-T specialization connection",
       "production_code_modified": False,
       "symbolic_toda45_given_count": len(symbolic),
       "concrete_iso_is_given": goal_iso in sources,
       "concrete_iso_specialization_candidates": len(options),
       "source_binding_results": [
           {"source": repr(s), "bindings": bindings}
           for s,bindings in matching],
       "specialization_subgoals": [
           [repr(x) for x in option.subgoals] for option in options],
       "pi54_registered_goal_count": len(targets),
       "pi54_direct_transport_count": sum(
           len(expand_registered_toda45_finite_cyclic_goal(goal, sources))
           for goal in targets),
       "pi43_is_direct_given": any(
           isinstance(s, Relation) and s.lhs == base and
           isinstance(s.rhs, FiniteCyclicGroup) for s in sources),
       "named_eta_transport_requires_separate_generator_proof": True,
       "full_pytest_run": False
    }


def main():
    output=Path(__file__).with_name("r3t_specialization_report.json")
    report=inspect()
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2,default=str))
    print("REPORT:",output)


if __name__=="__main__":
    main()
