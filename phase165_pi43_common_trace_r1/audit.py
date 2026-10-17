"""Read-only production-context trace for a generic pi_4^3 backward search."""
from __future__ import annotations

import json
from pathlib import Path
from collections import Counter

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from proof import Relation, ProofRule
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider, search_shared_group_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def describe_expansions(expansions):
    return [
        {"rule": str(getattr(item.rule, "name", type(item.rule).__name__)),
         "premises": [str(x) for x in item.subgoals]}
        for item in expansions
    ]


def trace(max_child_goals: int = 12):
    # Guard the already-confirmed removal. Do not recreate the retired adapter.
    adapter = REPO / "phase165_r52_r23_existing_rule_adapter.py"
    assert not adapter.exists(), "retired pi43 adapter unexpectedly exists"
    shared = (REPO / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8")
    assert "expand_existing_pi43_rules" not in shared, "group-specific provider still active"
    eta3 = HomotopyElement(name="η_3", dimension=3, source=4, target=3,
                           generator=GeneratorSymbol(family="η", index=3))
    goal = Relation(TodaPrimaryGroup(group_dimension=4, sphere_dimension=3),
                    FiniteCyclicGroup(order=2, generator=eta3))
    bridge = build_shared_typed_bridge()
    assertions = tuple(bridge.registry._assertions.values())
    assert assertions, "empty typed registry"
    screened = screen_shared_proof_context(bridge, goal=goal,
                                           citing_assertion_id=assertions[0].assertion_id)
    provider = shared_expansion_provider(screened, proof_target=goal)
    root = provider(goal)
    cited = {str(link.step.conclusion) for link in screened.proof_links
             if link.step is not None and link.step.rule is ProofRule.GIVEN}
    children = []
    seen = set()
    for expansion in root:
        for child in expansion.subgoals:
            key = str(child)
            if key in seen:
                continue
            seen.add(key)
            if len(children) >= max_child_goals:
                break
            proposals = provider(child)
            children.append({"goal": key, "cited_given_exact": key in cited,
                             "proposals": len(proposals),
                             "rule_names": [str(getattr(x.rule,"name",type(x.rule).__name__)) for x in proposals[:12]],
                             "sample": describe_expansions(proposals[:3])})
        if len(children) >= max_child_goals:
            break
    report = {"phase": "165 common pi43 R1", "mode": "READ_ONLY_DYNAMIC",
              "group_adapter_absent": True,
              "typed_reference_leaves": len(screened.proof_links),
              "goal": str(goal), "root_proposals": len(root),
              "root_rules": dict(Counter(str(getattr(x.rule, "name", type(x.rule).__name__)) for x in root)),
              "root_expansions": describe_expansions(root[:24]),
              "first_level_subgoals": children,
              "truncated_root_expansions": len(root)>24,
              "max_child_goals": max_child_goals,
              "full_pytest_run": False}
    out = HERE / "audit_result.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("phase", "mode", "group_adapter_absent", "typed_reference_leaves", "root_proposals", "root_rules", "full_pytest_run")}, ensure_ascii=False, indent=2))
    print("Audit saved:", out)
    return report


if __name__ == "__main__":
    trace()
