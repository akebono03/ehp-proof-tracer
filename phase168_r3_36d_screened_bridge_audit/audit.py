"""R3-36D audit-only: compare unscreened vs publication-screened proof links."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal, registered_group_goal_candidates
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from proof import ProofRule


def link_details(bridge, step):
    output = []
    for link in bridge.proof_links:
        if link.step is None:
            continue
        relation = ("exact" if link.step == step else
                    "same_conclusion" if link.step.conclusion == step.conclusion else None)
        if relation is None:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        output.append({
            "relation": relation,
            "assertion_id": assertion.assertion_id,
            "origin": assertion.origin.value,
            "reference_locator": reference.locator,
            "linked_step_rule": link.step.rule.value,
            "linked_step_repr": repr(link.step)[:5000],
            "actual_step_repr": repr(step)[:5000],
        })
    return output


def inspect():
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=4, k=1)
    if len(candidates) != 1:
        raise RuntimeError(f"Expected one pi5^4 typed goal, got {len(candidates)}")
    goal = candidates[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        raise RuntimeError("No citing assertion id; cannot reconstruct publication context")
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    )
    result = search_group_from_registered_goal(n=4, k=1, bridge=bridge)
    original_model = build_linked_proof_narrative_model(result, bridge)
    screened_model = build_linked_proof_narrative_model(result, screened)
    given_steps = []
    for i, step in enumerate(result.proven_steps):
        if step.rule is not ProofRule.GIVEN:
            continue
        given_steps.append({
            "step_index": i,
            "conclusion_type": type(step.conclusion).__name__,
            "original_citations": list(original_model.step_citation_numbers[i]),
            "screened_citations": list(screened_model.step_citation_numbers[i]),
            "original_links": link_details(bridge, step),
            "screened_links": link_details(screened, step),
        })
    def citations(model):
        return [{"number": c.number,
                 "locator": c.reference.locator or c.reference.label,
                 "assertion_ids": list(c.assertion_ids),
                 "step_indices": list(c.step_indices)}
                for c in model.citations]
    return {
        "mode": "AUDIT_ONLY",
        "goal": "pi_5^4",
        "status": result.status.value,
        "citing_assertion_id": citing_id,
        "original_bridge_link_count": len(bridge.proof_links),
        "screened_bridge_link_count": len(screened.proof_links),
        "original_citations": citations(original_model),
        "screened_citations": citations(screened_model),
        "given_steps": given_steps,
        "limitation": "Screened bridge is reconstructed from the same goal and citation ID; equivalence to search's internal screened bridge must still be checked if search applies additional transforms.",
    }


def main():
    report = inspect()
    path = Path(__file__).resolve().parent / "output" / "audit.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("AUDIT_ONLY: no repository files modified")
    print("SEARCH:", report["status"], "ORIGINAL LINKS:", report["original_bridge_link_count"],
          "SCREENED LINKS:", report["screened_bridge_link_count"])
    for entry in report["given_steps"]:
        print("STEP", entry["step_index"], entry["conclusion_type"],
              "original", [x["relation"] for x in entry["original_links"]],
              "screened", [x["relation"] for x in entry["screened_links"]])
    for c in report["screened_citations"]:
        print("SCREENED REF", c["number"], c["locator"], c["assertion_ids"])
    print("REPORT:", path)


if __name__ == "__main__":
    main()
