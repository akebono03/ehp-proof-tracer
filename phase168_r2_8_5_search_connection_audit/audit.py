"""Read-only Phase 168 R2-8(5) proof-search connection audit."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r2_8_1_citation_mismatch_audit.audit import CASES


def summarize_result(result):
    """Describe observed results; never infer completion from a citation."""
    return {
        "status": getattr(getattr(result, "status", None), "value", str(getattr(result, "status", None))),
        "structure_status": getattr(getattr(result, "structure_status", None), "value", str(getattr(result, "structure_status", None))),
        "proven_step_count": len(getattr(result, "proven_steps", ())),
        "open_goal_count": len(getattr(result, "open_goals", ())),
        "open_goals": [repr(item) for item in getattr(result, "open_goals", ())],
        "diagnostics": [str(item) for item in getattr(result, "diagnostics", ())],
        "references": [str(item) for item in getattr(result, "references", ())],
        "conclusion": repr(getattr(result, "conclusion", None)),
    }


def inspect_case(bridge, n, k, locator, *, attempt_search=True):
    """Check citation selection, screened evidence and actual search independently."""
    row = {"n": n, "k": k, "locator": locator, "group": f"pi_{n+k}^{n}"}
    try:
        goals = registered_group_goal_candidates(bridge, n=n, k=k)
        row["goal_count"] = len(goals)
        if len(goals) != 1:
            row["classification"] = "GOAL_NOT_UNIQUE"
            return row
        goal = goals[0]
        row["goal"] = repr(goal)
        citing_id = resolve_specialized_goal_citing_id(bridge, goal)
        row["citing_assertion_id"] = citing_id
        if citing_id is None:
            row["classification"] = "CITATION_UNRESOLVED"
            return row
        assertion = bridge.registry._assertions.get(citing_id)
        if assertion is None:
            row["classification"] = "CITATION_ASSERTION_MISSING"
            return row
        ref = bridge.registry.reference(assertion.reference_id)
        row["citing_locator"] = str(ref.locator)
        row["publication_position"] = ref.publication_position
        row["component_position"] = assertion.component_position
        row["locator_matches_expected"] = ref.locator == locator
        try:
            screened = screen_shared_proof_context(
                bridge, goal=goal, citing_assertion_id=citing_id,
                explicit_publication_target=True,
            )
            links = tuple(screened.proof_links)
            row["screened_link_count"] = len(links)
            row["screened_assertion_ids"] = [link.assertion_id for link in links]
            row["self_as_given"] = any(link.assertion_id == citing_id for link in links)
            row["screening_error"] = None
        except Exception as exc:
            row["screening_error"] = f"{type(exc).__name__}: {exc}"
            row["classification"] = "SCREENING_FAILED"
            return row
        if not attempt_search:
            row["classification"] = "SCREENED_NOT_SEARCHED"
            return row
        try:
            result = search_group_from_registered_goal(n=n, k=k, bridge=bridge, goal=goal)
            row["search"] = summarize_result(result)
            row["classification"] = "SEARCH_" + row["search"]["status"].upper()
        except Exception as exc:
            row["search_error"] = f"{type(exc).__name__}: {exc}"
            row["classification"] = "SEARCH_EXCEPTION"
    except Exception as exc:
        row["audit_error"] = f"{type(exc).__name__}: {exc}"
        row["classification"] = "AUDIT_EXCEPTION"
    return row


def main():
    bridge = build_shared_typed_bridge()
    rows = [inspect_case(bridge, n, k, locator) for n, k, locator in CASES]
    report = {
        "audit": "phase168-r2-8-5", "read_only": True,
        "proof_completion_inferred_from_citation": False,
        "production_code_modified": False, "cases": rows,
    }
    output = Path(__file__).resolve().parent / "output" / "search_connection.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(f"{row['group']}: {row['classification']} cite={row.get('citing_assertion_id')} self_given={row.get('self_as_given')}")
    print("REPORT:", output)


if __name__ == "__main__":
    main()
