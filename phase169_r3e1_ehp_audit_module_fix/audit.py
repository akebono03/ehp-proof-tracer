"""Live citation-screened R3E audit; no synthetic GIVEN or proof replay."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
from phase161_r4_literature_premise_matching import expand_phase161_r4_literature_goal
from phase165_r14_r5_ehp_connection import expand_registered_ehp_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule
from toda_rules import TodaProp42ExactnessStatement

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output" / "ehp_provider_connection.json"


def main() -> int:
    bridge = build_shared_typed_bridge()
    lower = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    context = []
    upper = search_group_from_registered_goal(n=3, k=2, bridge=bridge, context_sink=context.append)
    if len(context) != 1 or lower.status is not ProofSearchStatus.COMPLETE:
        raise AssertionError("lower complete proof and upper screened context are required")
    screened = context[0]
    goals = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(goals) != 1:
        raise AssertionError("upper typed goal must be unique")
    root_goal = goals[0]
    provider = shared_expansion_provider(screened, proof_target=root_goal)
    iso = TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(4, 2), TodaPrimaryGroup(5, 3))
    )
    original = expand_registered_ehp_goal(iso)
    options = tuple(opt for opt in provider(iso)
                    if original and opt.rule.name == original[0].rule.name
                    and opt.subgoals == original[0].subgoals)
    if len(original) != 1 or len(options) != 1:
        raise AssertionError("historical EHP root was not connected exactly once")
    typed_nodes = [iso]
    exactness = []
    terminal = []
    def descend(goal, depth=0):
        if depth > 7:
            raise AssertionError("unexpected EHP tree cycle")
        prior = expand_registered_ehp_goal(goal)
        if prior:
            options = tuple(x for x in provider(goal)
                            if x.rule.name == prior[0].rule.name and x.subgoals == prior[0].subgoals)
            if len(options) != 1:
                raise AssertionError("existing typed EHP expansion not connected: " + type(goal).__name__)
            for item in prior[0].subgoals:
                typed_nodes.append(item)
                descend(item, depth + 1)
            return
        if isinstance(goal, TodaProp42ExactnessStatement):
            if not provider(goal):
                raise AssertionError("missing Prop 4.2 exactness specialization")
            exactness.append(goal)
            return
        if expand_phase161_r4_literature_goal(goal) is not None:
            terminal.append(goal)
    descend(iso)
    if len(exactness) != 4 or len(terminal) != 2:
        raise AssertionError("existing EHP dependencies unexpectedly changed")
    if upper.status is ProofSearchStatus.COMPLETE:
        raise AssertionError("R3E must not prematurely certify pi_5^3")
    if not any(type(goal).__name__ == "TodaSuspensionIsomorphismStatement" for goal in upper.open_goals):
        raise AssertionError("EHP isomorphism proof is not yet complete")
    citing_lower = resolve_specialized_goal_citing_id(bridge, lower.conclusion)
    citing_upper = resolve_specialized_goal_citing_id(bridge, root_goal)
    if citing_lower is None or citing_upper is None or not precedes_citing_assertion(bridge, citing_lower, citing_upper):
        raise AssertionError("pi_4^2 citation must precede pi_5^3")
    if any(link.step is not None and link.step.rule is not ProofRule.GIVEN for link in screened.proof_links):
        raise AssertionError("screened literature context unexpectedly contains derived steps")
    report = {
        "phase": "169-R3E",
        "lower_status": lower.status.value,
        "upper_status": upper.status.value,
        "upper_proven_steps": len(upper.proven_steps),
        "historical_iso_proposals": len(original),
        "connected_iso_proposals": len(options),
        "ehp_connected_nodes": len(typed_nodes),
        "exactness_proposals": len(exactness),
        "terminal_goals": [type(x).__name__ for x in terminal],
        "terminal_proposals": {type(x).__name__: [o.rule.name for o in provider(x)] for x in terminal},
        "screened_given_count": len(screened.proof_links),
        "pi4_publication_prior": True,
        "complete_claim": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in report.items():
        print(f"{k.upper()}={v}")
    print("REPORT=" + str(OUTPUT))
    print("R3E_ACCEPTED_FRONTIER=True; no complete proof claimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
