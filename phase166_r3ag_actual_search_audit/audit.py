"""Read-only R3-AG audit: registry and DB-goal search are distinct."""
from __future__ import annotations

import json
import traceback
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3af_goal_adapter import database_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from homotopy_groups import TodaPrimaryGroup, FiniteCyclicGroup
from proof import Relation, ProofRule

CASES = tuple((k, k + 2 + r) for k in (2, 3, 7) for r in (0, 1, 2))


def analyze_case(bridge, k: int, n: int) -> dict:
    report = {"n": n, "k": k, "group": repr(TodaPrimaryGroup(n + k, n))}
    try:
        registered = registered_group_goal_candidates(bridge, n=n, k=k)
        database = database_group_goal_candidates(n=n, k=k)
        report["registered_count"] = len(registered)
        report["database_count"] = len(database)
        report["registered_goals"] = [repr(x) for x in registered]
        report["database_goals"] = [repr(x) for x in database]
        selected = registered if registered else database
        report["selected_source"] = "registered" if registered else "database"
        if len(selected) != 1:
            report["outcome"] = "NO_UNIQUE_TYPED_GOAL"
            return report
        goal = selected[0]
        assert isinstance(goal, Relation)
        citing_id = resolve_specialized_goal_citing_id(bridge, goal)
        report["citing_assertion_id"] = citing_id
        if citing_id is None:
            report["publication_boundary"] = "NO_REGISTERED_PUBLICATION_TARGET"
            # Do not silently promote the DB to a fixed reference or substitute
            # a fictitious citing assertion. The ordinary search path remains
            # separately observable, but has no publication-scoped attestation.
        else:
            screened = screen_shared_proof_context(
                bridge, goal=goal, citing_assertion_id=citing_id,
                explicit_publication_target=True,
            )
            given = [link for link in screened.proof_links
                     if link.step is not None and link.step.rule is ProofRule.GIVEN]
            base = TodaPrimaryGroup(2 * k + 2, k + 2)
            report["screened_given_count"] = len(given)
            report["base_group_given"] = [
                {"assertion_id": link.assertion_id, "statement": repr(link.step.conclusion)}
                for link in given if isinstance(link.step.conclusion, Relation)
                and link.step.conclusion.lhs == base
            ]
            report["toda45_given"] = [
                {"assertion_id": link.assertion_id, "statement": repr(link.step.conclusion)}
                for link in given if "Toda45IsomorphismStatement" in type(link.step.conclusion).__name__
            ]
        result = search_shared_group_goal(
            n=n, k=k, group_structure=goal.rhs, bridge=bridge,
            **({"citing_assertion_id": citing_id} if citing_id is not None else {}),
        )
        report["search_status"] = str(result.status)
        report["complete"] = str(result.status).endswith(".COMPLETE")
        report["conclusion_matches_goal"] = result.conclusion == goal
        report["open_goals"] = [repr(x) for x in result.open_goals]
        report["diagnostics"] = [str(x) for x in result.diagnostics]
        report["outcome"] = "SEARCH_EXECUTED"
    except Exception as exc:
        report["outcome"] = "EXCEPTION"
        report["exception"] = repr(exc)
        report["traceback"] = traceback.format_exc(limit=6)
    return report


def audit() -> dict:
    bridge = build_shared_typed_bridge()
    records = [analyze_case(bridge, k, n) for k, n in CASES]
    return {"phase": "166 R3-AG", "read_only": True, "records": records,
            "summary": {"targets": len(records),
                        "unique_goals": sum(x.get("registered_count", 0) + x.get("database_count", 0) > 0 for x in records),
                        "search_executed": sum(x.get("outcome") == "SEARCH_EXECUTED" for x in records),
                        "complete": sum(x.get("complete", False) for x in records),
                        "exceptions": sum(x.get("outcome") == "EXCEPTION" for x in records)}}


def main() -> None:
    result = audit()
    path = Path(__file__).with_name("report.json")
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"summary": result["summary"], "targets": [{
        "n": x["n"], "k": x["k"], "registered_count": x.get("registered_count"),
        "database_count": x.get("database_count"), "selected_source": x.get("selected_source"),
        "citing_assertion_id": x.get("citing_assertion_id"),
        "base_count": len(x.get("base_group_given", [])),
        "toda45_count": len(x.get("toda45_given", [])),
        "outcome": x["outcome"], "status": x.get("search_status"),
        "complete": x.get("complete"), "open_goals": len(x.get("open_goals", [])),
        "exception": x.get("exception"),
    } for x in result["records"]], "report": str(path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
