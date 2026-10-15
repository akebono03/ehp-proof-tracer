"""Read-only verification of the root expansions after R57-R18 installation."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates


def run() -> dict:
    bridge = build_shared_typed_bridge()
    records = []
    for n, k in ((2, 1), (3, 1), (4, 1)):
        goals = registered_group_goal_candidates(bridge, n=n, k=k)
        item = {"n": n, "k": k, "candidate_count": len(goals)}
        if len(goals) == 1:
            goal = goals[0]
            provider = shared_expansion_provider(bridge, proof_target=goal)
            expansions = provider(goal)
            item["root_expansion_count"] = len(expansions)
            item["expansion_rules"] = [getattr(x.rule, "name", repr(x.rule)) for x in expansions]
            item["required_subgoals"] = [[repr(g) for g in x.subgoals] for x in expansions]
        records.append(item)
    return {"phase": "165 R57-R18", "mode": "READ_ONLY_ROOT_AUDIT", "targets": records,
            "no_proof_certification": True, "full_pytest_run": False}


def main() -> None:
    result = run()
    destination = Path(__file__).with_name("root_expansions.json")
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
    for item in result["targets"]:
        print(f"pi_{item['n'] + item['k']}^{item['n']}: root_expansions={item.get('root_expansion_count', 'unknown')}")
        for name in item.get("expansion_rules", ()):
            print("  rule:", name)
    print("R57-R18 root audit written:", destination)


if __name__ == "__main__":
    main()
