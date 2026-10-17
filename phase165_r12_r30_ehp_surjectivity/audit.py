from __future__ import annotations
import json
from pathlib import Path
from homotopy_groups import TodaSuspensionMap
from map_property_rules import ImageWholeStatement, SurjectiveMapStatement, whole_image_implies_surjective_inference_rule
from phase165_r12_r12_ehp_consequences import expand_ehp_exactness_consequences
from phase165_r12_r30_ehp_surjectivity import expand_ehp_whole_image
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r8_rule_provider import create_rule_expansion_provider


def main() -> None:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=1)
    if len(goals) != 1:
        raise ValueError("expected unique pi4^3 goal")
    goal = goals[0]
    e = TodaSuspensionMap(goal.lhs.__class__(3, 2), goal.lhs)
    whole = ImageWholeStatement(e)
    direct = expand_ehp_whole_image(whole)
    common = shared_expansion_provider(bridge, proof_target=goal)(whole)
    matched = [item for item in common if any(item.subgoals == d.subgoals for d in direct)]
    surj = create_rule_expansion_provider((whole_image_implies_surjective_inference_rule(),))(SurjectiveMapStatement(e))
    ehp = expand_ehp_exactness_consequences(direct[0].subgoals[0]) if direct else ()
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    data = {"phase":"165 R12-R30", "whole_image_candidates":len(direct),
        "common_whole_image_candidates":len(matched), "surjective_to_whole_image_candidates":len(surj),
        "ehp_exactness_candidates":len(ehp),
        "ehp_subgoals":[repr(g) for option in ehp for g in option.subgoals],
        "web_search_status":getattr(result.status,"value",str(result.status)),
        "web_search_complete":result.conclusion is not None and not result.open_goals,
        "open_goals":[repr(x) for x in result.open_goals],
        "diagnostics":list(result.diagnostics), "full_pytest_run":False}
    target = Path(__file__).with_name("audit_result.json")
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2),encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("Audit saved:",target)


if __name__ == "__main__":
    main()
