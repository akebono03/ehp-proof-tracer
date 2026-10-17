"""Phase 165 reference-stop R2: read-only actual pi43 search audit."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
from phase165_r52_partial_proof import ProofSearchStatus
from proof import ProofRule

PI32_ID = "shared:2:toda:adopted:prop5.1:finite_dimensional:component:pi3_2_group_relation"
PI43_ID = "shared:2:toda:adopted:prop5.1:pi4_3"


def matches_step(step, statement):
    return type(step.conclusion) is type(statement) and step.conclusion == statement


def graph_report(result, pi32):
    steps = result.proven_steps
    pi32_steps = [s for s in steps if matches_step(s, pi32)]
    suspension_steps = [s for s in steps if type(s.conclusion).__name__ == "GeneratorSuspension"]
    ancestor_ids = set()
    seen = set()
    def walk(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        if matches_step(step, pi32):
            ancestor_ids.add(id(step))
        for premise in step.premises:
            if hasattr(premise, "conclusion") and hasattr(premise, "premises"):
                walk(premise)
    roots = [s for s in steps if matches_step(s, result.conclusion)] if result.conclusion is not None else []
    for root in roots:
        walk(root)
    return {
        "pi32_steps_in_result": len(pi32_steps),
        "pi32_given_steps_in_result": sum(s.rule is ProofRule.GIVEN for s in pi32_steps),
        "generator_suspension_steps_in_result": len(suspension_steps),
        "generator_suspension_details": [
            {"statement": repr(s.conclusion), "reference": getattr(getattr(s,"foundational_reference",None),"key",None),
             "premise_count": len(s.premises)} for s in suspension_steps
        ],
        "pi32_root_reached_by_step_object_edges": bool(ancestor_ids),
        "note": "Object-edge ancestry is indicative only: some proof formats store premises as statements.",
    }


def run():
    bridge = build_shared_typed_bridge()
    pi32_candidates = registered_group_goal_candidates(bridge, n=2, k=1)
    pi43_candidates = registered_group_goal_candidates(bridge, n=3, k=1)
    assert len(pi32_candidates) == 1, "pi32 candidate must be unique"
    assert len(pi43_candidates) == 1, "pi43 candidate must be unique"
    pi32, pi43 = pi32_candidates[0], pi43_candidates[0]
    # Do not assume a historical publication rank; this is the current adopted source convention.
    screened = screen_shared_proof_context(bridge, goal=pi43, citing_assertion_id=PI43_ID)
    admitted = [link for link in screened.proof_links if link.assertion_id == PI32_ID]
    assert len(admitted) <= 1, "unexpected ambiguous pi32 source links"
    catalog, diagnostic = resolve_reviewed_order_catalog(bridge, n=3, k=1)
    assert diagnostic is None, diagnostic
    # Exercise the actual production search rather than simulating leaf resolution.
    result = search_shared_group_goal(n=3, k=1, group_structure=pi43.rhs,
                                      bridge=bridge, proof_order_catalog=catalog)
    graph = graph_report(result, pi32)
    report = {
        "phase": "165 reference-stop R2",
        "status": "ACTUAL_PI43_SEARCH_AUDITED",
        "pi32_adopted_fixed_given_admitted": len(admitted) == 1,
        "pi32_source_step_is_given": bool(admitted and admitted[0].step and admitted[0].step.rule is ProofRule.GIVEN),
        "pi32_reference_claim": repr(pi32),
        "pi43_goal": repr(pi43),
        "reviewed_proof_development_order_available": catalog is not None,
        "publication_order_independently_verified": False,
        "search_status": result.status.value,
        "search_complete": result.status is ProofSearchStatus.COMPLETE,
        "open_goals": [repr(x) for x in result.open_goals],
        "proven_step_count": len(result.proven_steps),
        "proof_tree": graph,
        "fixed_given_stop_observed": graph["pi32_given_steps_in_result"] > 0,
        "source_files_modified": False,
        "full_pytest_run": False,
    }
    dest=Path(__file__).parent/'audit_result.json'
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", dest)
    return report


if __name__ == "__main__":
    run()
