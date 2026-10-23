"""Read-only audit of the actual search-adapter bridge for pi5^4."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import phase165_r52_r9_shared_math as shared
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from homotopy_groups import TodaPrimaryGroup
from proof import Relation


def capture():
    bridge = shared.build_shared_typed_bridge()
    actual_search_contexts = []
    original = shared.search_registered_partial_proof

    def intercept(*args, **kwargs):
        context = kwargs["bridge"]
        goal = kwargs.get("goal")
        if isinstance(goal, Relation) and goal.lhs == TodaPrimaryGroup(5, 4):
            actual_search_contexts.append(context)
        return original(*args, **kwargs)

    with patch.object(shared, "search_registered_partial_proof", side_effect=intercept):
        result = search_group_from_registered_goal(n=4, k=1, bridge=bridge)

    if len(actual_search_contexts) != 1:
        raise RuntimeError(
            "Expected exactly one pi5^4 search adapter context; got "
            + str(len(actual_search_contexts))
        )
    searched = actual_search_contexts[0]
    original_model = build_linked_proof_narrative_model(result, bridge)
    searched_model = build_linked_proof_narrative_model(result, searched)

    def summarize(model):
        return [{
            "number": c.number,
            "locator": c.reference.locator or c.reference.label,
            "step_indices": list(c.step_indices),
            "assertion_ids": list(c.assertion_ids),
            "reference_ids": list(c.reference_ids),
        } for c in model.citations]

    return {
        "mode": "AUDIT_ONLY",
        "status": result.status.value,
        "goal": "pi_5^4",
        "context_captured_count": len(actual_search_contexts),
        "original_link_count": len(bridge.proof_links),
        "search_context_link_count": len(searched.proof_links),
        "original_citations": summarize(original_model),
        "search_context_citations": summarize(searched_model),
        "given_step_links": [
            {
                "step_index": i,
                "step_type": type(s.conclusion).__name__,
                "original_exact_ids": [
                    l.assertion_id for l in bridge.proof_links
                    if l.step is not None and l.step == s
                ],
                "actual_search_exact_ids": [
                    l.assertion_id for l in searched.proof_links
                    if l.step is not None and l.step == s
                ],
            }
            for i, s in enumerate(result.proven_steps) if s.rule.value == "given"
        ],
    }


def main():
    report = capture()
    path = Path(__file__).resolve().parent / "output" / "audit.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("AUDIT_ONLY: no repository files modified")
    print("SEARCH:", report["status"])
    print("LINKS original=", report["original_link_count"],
          " actual_search=", report["search_context_link_count"])
    for item in report["search_context_citations"]:
        print("[R" + str(item["number"]) + "]", item["locator"],
              "ids=", item["assertion_ids"])
    print("REPORT:", path)


if __name__ == "__main__":
    main()
