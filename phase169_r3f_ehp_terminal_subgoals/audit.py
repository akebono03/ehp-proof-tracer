"""R3F actual citation-screened terminal frontier; never assert completion."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r14_r5_ehp_connection import expand_registered_ehp_terminal_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase161_r3_backward_goal_schema import expand_phase161_r3_goal
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement
from proof import ProofRule
from toda_rules import TodaProp51FiniteDimensionalStatement

HERE = Path(__file__).resolve().parent


def run() -> int:
    bridge = build_shared_typed_bridge()
    contexts = []
    lower = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    upper = search_group_from_registered_goal(n=3, k=2, bridge=bridge, context_sink=contexts.append)
    if lower.status is not ProofSearchStatus.COMPLETE or len(contexts) != 1:
        raise AssertionError("required lower proof or actual screened context unavailable")
    if upper.status is ProofSearchStatus.COMPLETE:
        raise AssertionError("R3F must not claim a completed pi_5^3 proof")
    screened = contexts[0]
    upper_goals = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(upper_goals) != 1:
        raise AssertionError("unique typed pi_5^3 Goal required")
    provider = shared_expansion_provider(screened, proof_target=upper_goals[0])
    iso = TodaSuspensionIsomorphismStatement(TodaSuspensionMap(
        TodaPrimaryGroup(4, 2), TodaPrimaryGroup(5, 3)
    ))
    terminal_goals = []
    def descend(g, depth=0):
        if depth > 7:
            raise AssertionError("unexpected historical EHP dependency cycle")
        proposal = expand_phase161_r3_goal(g)
        if proposal is not None:
            for sg in proposal.subgoals:
                descend(sg, depth+1)
            return
        from phase161_r4_literature_premise_matching import expand_phase161_r4_literature_goal
        if expand_phase161_r4_literature_goal(g) is not None:
            terminal_goals.append(g)
    descend(iso)
    if len(terminal_goals) != 2:
        raise AssertionError("expected two existing n=3 EHP terminal Goals")
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    result = {}
    for g in terminal_goals:
        options = expand_registered_ehp_terminal_goal(g, available)
        live = provider(g)
        matching = tuple(x for x in live if any(x.rule.name == p.rule.name and x.subgoals == p.subgoals for p in options))
        if len(options) != 1 or len(matching) != 1:
            raise AssertionError("terminal proposal not connected exactly once: " + type(g).__name__)
        if not all(pattern.proof_rule is ProofRule.INFERENCE for pattern in matching[0].rule.premise_patterns):
            raise AssertionError("historical inference-only guard weakened")
        result[type(g).__name__] = {
            "provider_count": len(matching),
            "rule": matching[0].rule.name,
            "subgoals": [type(s).__name__ for s in matching[0].subgoals],
            "subgoal_reprs": [repr(s) for s in matching[0].subgoals],
        }
    report = {
        "phase": "169-R3F", "audit_only": False,
        "lower_status": lower.status.value,
        "upper_status": upper.status.value,
        "proven_steps": len(upper.proven_steps),
        "screened_prop51_composite_count": sum(isinstance(a,TodaProp51FiniteDimensionalStatement) for a in available),
        "terminal_proposals": result,
        "new_givens": 0, "complete_claim": False,
    }
    path = HERE / "output" / "ehp_terminal_frontier.json"
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    for key,value in report.items():
        print(f"{key.upper()}={value}")
    print("REPORT=" + str(path))
    print("R3F_TERMINAL_CANDIDATES_CONNECTED=True; completion not claimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
