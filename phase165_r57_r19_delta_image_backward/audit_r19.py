"""Read-only diagnosis of R57-R19 Delta image goal and its premises."""
from __future__ import annotations

import json
from pathlib import Path
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates


def main() -> None:
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=1)
    if len(roots) != 1:
        raise RuntimeError("pi4^3 must have exactly one registered goal")
    root = roots[0]
    expand = shared_expansion_provider(bridge, proof_target=root)
    visited = []
    pending = [(root, 0)]
    while pending and len(visited) < 100:
        goal, depth = pending.pop(0)
        if any(old[0] == goal for old in visited):
            continue
        options = expand(goal)
        visited.append((goal, depth, options))
        if depth < 6:
            for option in options:
                pending.extend((subgoal, depth + 1) for subgoal in option.subgoals)
    records = [{"goal": repr(goal), "depth": depth,
                "rules": [getattr(x.rule, "name", repr(x.rule)) for x in options],
                "subgoals": [[repr(g) for g in x.subgoals] for x in options]}
               for goal, depth, options in visited]
    path = Path(__file__).with_name("delta_image_goals.json")
    path.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
    for row in records:
        if "TodaDeltaImageFreeCyclicStatement" in row["goal"]:
            print("Delta image expansion count:", len(row["rules"]))
            print("Rules:", row["rules"])
            for group in row["subgoals"]:
                print("Delta image subgoals:", group)
    print("R57-R19 read-only goal audit:", path)


if __name__ == "__main__":
    main()
