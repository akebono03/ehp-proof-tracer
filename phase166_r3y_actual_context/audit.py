"""Read-only comparison of the actual web search context and the R3-X context."""
from __future__ import annotations

import json
from pathlib import Path

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r7_proof_order_guard import restrict_registered_ordered_claims
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from proof import ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement

TARGET = "shared:2:toda:adopted:prop5.1:higher_eta_group_relation"


def main():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=1)
    if len(goals) != 1:
        raise RuntimeError("expected one typed pi5^4 target")
    goal = goals[0]
    stages = [
        ("publication", screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=TARGET,
            explicit_publication_target=True,
        )),
    ]
    stages.append(("proof_order", restrict_registered_ordered_claims(stages[-1][1], goal)))
    stages.append(("prop42", prefer_universal_prop42_derivation(stages[-1][1])))
    reports = []
    for name, context in stages:
        given = [(link.assertion_id, link.step.conclusion) for link in context.proof_links
                 if link.step is not None and link.step.rule is ProofRule.GIVEN]
        bases = [(identifier, value) for identifier, value in given
                 if isinstance(value, Relation)
                 and value.relation_type is RelationType.EQUALITY
                 and value.lhs == TodaPrimaryGroup(4, 3)
                 and isinstance(value.rhs, FiniteCyclicGroup)
                 and value.rhs.order == 2]
        source = [(identifier, value) for identifier, value in given
                  if isinstance(value, Toda45IsomorphismStatement)]
        provider = shared_expansion_provider(context, proof_target=goal)
        root_options = provider(goal)
        normalized = [option for option in root_options
                      if option.rule.name == "proved generator suspension normalizes transported cyclic group"]
        transport = []
        for option in normalized:
            for child in option.subgoals:
                if not (isinstance(child, Relation) and isinstance(child.rhs, FiniteCyclicGroup)
                        and isinstance(child.rhs.generator, IteratedSuspension)):
                    continue
                transport.append({
                    "child": repr(child),
                    "rules": [{"rule": x.rule.name, "subgoals": [repr(y) for y in x.subgoals]}
                              for x in provider(child)],
                })
        reports.append({
            "stage": name,
            "given_count": len(given),
            "pi43": [{"id": i, "value": repr(v)} for i, v in bases],
            "toda45": [{"id": i, "value": repr(v)} for i, v in source],
            "root_rules": [option.rule.name for option in root_options],
            "normalization_count": len(normalized),
            "transport": transport,
        })
    actual = stages[-1][1]
    provider = shared_expansion_provider(actual, proof_target=goal)
    observed = []
    def observer(kind, current, step):
        relevant = (current == goal
                    or isinstance(current, Toda45IsomorphismStatement)
                    or isinstance(current, Relation) and (
                        current.lhs == TodaPrimaryGroup(4, 3)
                        or current.lhs == TodaPrimaryGroup(5, 4)
                    ))
        if relevant and len(observed) < 80:
            observed.append({"kind": kind, "goal": repr(current),
                             "rule": getattr(getattr(step, "inference_rule", None), "name", None)})
    try:
        root = reconstruct_registered_goal(
            goal, actual, TARGET, provider,
            lookup_mode="typed_reference_publication", progress_observer=observer,
        )
        outcome = {"complete": True, "root": repr(root.conclusion)}
    except RegisteredGoalUnresolved as exc:
        outcome = {"complete": False, "error": str(exc)}
    report = {"phase": "166 R3-Y", "read_only": True,
              "full_pytest_run": False, "stages": reports,
              "actual_search": outcome, "observed": observed}
    path = Path(__file__).with_name("report.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {"stages": [{"stage": x["stage"], "given": x["given_count"],
                            "pi43": len(x["pi43"]), "toda45": len(x["toda45"]),
                            "normalization": x["normalization_count"],
                            "transport_rules": [[o["rule"] for o in t["rules"]] for t in x["transport"]]}
                           for x in reports], "actual_search": outcome,
               "observed_tail": observed[-18:], "report": str(path)}
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
