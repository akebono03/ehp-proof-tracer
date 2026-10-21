"""Read-only Phase 166 R3-AE audit of real registered stable-stem searches."""
from __future__ import annotations

import json
import traceback
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, FiniteCyclicGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates, search_group_from_registered_goal,
)
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase166_r3c_publication_order import precedes_citing_assertion
from proof import Relation, ProofRule
from toda_rules import Toda45IsomorphismStatement


STEMS = (2, 3, 7)
OFFSETS = (0, 1, 2)


def inspect_target(bridge, k: int, offset: int) -> dict:
    n = k + 2 + offset
    target_group = TodaPrimaryGroup(n + k, n)
    record = {"stem": k, "base_n": k + 2, "offset": offset,
              "target_group": repr(target_group)}
    try:
        candidates = registered_group_goal_candidates(bridge, n=n, k=k)
        record["candidate_count"] = len(candidates)
        record["candidate_reprs"] = [repr(v) for v in candidates]
        if len(candidates) != 1:
            record["diagnostic"] = "No unique registered typed target; search not attempted"
            return record
        goal = candidates[0]
        citing_id = resolve_specialized_goal_citing_id(bridge, goal)
        record["citing_id"] = citing_id
        record["goal_generator"] = repr(getattr(goal.rhs, "generator", None))
        if citing_id is not None:
            context = screen_shared_proof_context(
                bridge, goal=goal, citing_assertion_id=citing_id,
                explicit_publication_target=True,
            )
            given = [(link.assertion_id, link.step.conclusion)
                     for link in context.proof_links
                     if link.step is not None and link.step.rule is ProofRule.GIVEN]
            base_group = TodaPrimaryGroup(2 * k + 2, k + 2)
            bases = [(i, x) for i, x in given
                     if isinstance(x, Relation) and x.lhs == base_group]
            toda = [(i, x) for i, x in given
                    if isinstance(x, Toda45IsomorphismStatement)]
            record["base_premises"] = [
                {"id": i, "content": repr(x),
                 "precedes": precedes_citing_assertion(bridge, i, citing_id)}
                for i, x in bases
            ]
            record["toda45_premises"] = [
                {"id": i, "content": repr(x),
                 "precedes": precedes_citing_assertion(bridge, i, citing_id)}
                for i, x in toda
            ]
            provider = shared_expansion_provider(context, proof_target=goal)
            root = provider(goal)
            record["root_rules"] = [item.rule.name for item in root]
            record["root_subgoals"] = [
                {"rule": item.rule.name, "subgoals": [repr(x) for x in item.subgoals]}
                for item in root
            ]
            transported = []
            for item in root:
                for child in item.subgoals:
                    if (isinstance(child, Relation)
                            and child.lhs == target_group
                            and isinstance(child.rhs, FiniteCyclicGroup)):
                        transported.append({
                            "subgoal": repr(child),
                            "candidate_rules": [v.rule.name for v in provider(child)],
                        })
            record["transport_subgoals"] = transported
        else:
            record["publication_diagnostic"] = (
                "No unique publication target; the ordinary entry may use a fallback path"
            )
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, goal=goal,
        )
        record["search"] = {
            "status": str(result.status),
            "complete": str(result.status).endswith(".COMPLETE"),
            "conclusion_matches_goal": result.conclusion == goal,
            "open_goals": [repr(x) for x in result.open_goals],
            "diagnostics": [str(x) for x in result.diagnostics],
        }
    except Exception as exc:
        record["exception"] = repr(exc)
        record["traceback"] = traceback.format_exc(limit=7)
    return record


def audit() -> dict:
    bridge = build_shared_typed_bridge()
    records = [inspect_target(bridge, k, r) for k in STEMS for r in OFFSETS]
    return {
        "phase": "166 R3-AE",
        "production_code_modified": False,
        "full_pytest_run": False,
        "stem_values": list(STEMS),
        "offset_values": list(OFFSETS),
        "records": records,
        "summary": {
            "targets": len(records),
            "unique_candidates": sum(x.get("candidate_count") == 1 for x in records),
            "publication_bound": sum(bool(x.get("citing_id")) for x in records),
            "complete": sum(x.get("search", {}).get("complete", False) for x in records),
            "exceptions": sum("exception" in x for x in records),
        },
    }


def main() -> None:
    result = audit()
    report = Path(__file__).with_name("report.json")
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    overview = [{
        "stem": x["stem"], "n": x["base_n"] + x["offset"],
        "candidate_count": x.get("candidate_count"),
        "publication_target": x.get("citing_id"),
        "base_premises": len(x.get("base_premises", [])),
        "toda45_premises": len(x.get("toda45_premises", [])),
        "root_rules": x.get("root_rules", []),
        "search_status": x.get("search", {}).get("status"),
        "complete": x.get("search", {}).get("complete"),
        "diagnostics": x.get("search", {}).get("diagnostics", []),
        "exception": x.get("exception"),
    } for x in result["records"]]
    print(json.dumps({"summary": result["summary"], "targets": overview,
                      "report": str(report)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
