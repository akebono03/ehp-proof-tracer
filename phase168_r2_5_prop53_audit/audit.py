"""Read-only audit of the pi_4^2 literature citation boundary and search."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id


def main() -> None:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=2)
    result = {
        "goal_count": len(goals),
        "goals": [repr(goal) for goal in goals],
        "proposition53_assertions": [],
        "toda52_assertions": [],
    }
    for item in bridge.registry._assertions.values():
        reference = bridge.registry.reference(item.reference_id)
        loc = str(reference.locator)
        if "Proposition 5.3" not in loc and "(5.2)" not in loc:
            continue
        record = {
            "assertion_id": item.assertion_id,
            "locator": loc,
            "publication_position": reference.publication_position,
            "component_position": item.component_position,
            "origin": str(item.origin),
            "content_type": type(item.content).__name__,
            "content": repr(item.content)[:600],
        }
        if "Proposition 5.3" in loc:
            result["proposition53_assertions"].append(record)
        else:
            result["toda52_assertions"].append(record)
    if len(goals) == 1:
        goal = goals[0]
        citing = resolve_specialized_goal_citing_id(bridge, goal)
        result["citing_assertion_id"] = citing
        if citing is not None:
            screened = screen_shared_proof_context(
                bridge, goal=goal, citing_assertion_id=citing,
                explicit_publication_target=True,
            )
            result["screened_given_count"] = len(screened.proof_links)
            result["screened_toda52_ids"] = [
                link.assertion_id for link in screened.proof_links
                if "toda:tex:ch5:0003" in link.assertion_id
            ]
            result["self_given"] = any(link.assertion_id == citing for link in screened.proof_links)
            result["toda52_precedes"] = [
                precedes_citing_assertion(bridge, entry["assertion_id"], citing)
                for entry in result["toda52_assertions"]
            ]
        result["search_attempted"] = True
        try:
            search = search_group_from_registered_goal(n=2, k=2, bridge=bridge, goal=goal)
            result["search_status"] = str(search.status)
            result["proven_count"] = len(getattr(search, "proven_steps", ()))
            result["open_goals"] = [repr(item) for item in getattr(search, "open_goals", ())]
            result["diagnostics"] = [str(item) for item in getattr(search, "diagnostics", ())]
        except Exception as exc:
            result["search_exception"] = f"{type(exc).__name__}: {exc}"
    output = Path(__file__).resolve().parent / "results.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for key in ("goal_count", "citing_assertion_id", "screened_toda52_ids", "self_given", "search_status", "open_goals", "diagnostics", "search_exception"):
        if key in result:
            value = result[key]
            if key == "open_goals":
                value = len(value)
            print(f"{key.upper()}: {value}")
    print(f"REPORT: {output}")


if __name__ == "__main__":
    main()
