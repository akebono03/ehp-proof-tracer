"""Diagnostic only: perform production search using the same shared bridge."""
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model


def main():
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    print("GOAL: pi_4^2")
    print("STATUS:", result.status)
    print("PROVEN_STEPS:", len(result.proven_steps))
    print("CITATION_COUNT:", len(model.citations))
    for citation in model.citations:
        print("CITATION:", citation.number, repr(citation.reference.locator),
              "steps=", citation.step_indices, "assertions=", citation.assertion_ids)
    print("STEP_CITATION_NUMBERS:", model.step_citation_numbers)
    print("ROOT_INDEX:", model.root_index)
    print("NOTE: Diagnostic projection only; Web output has not changed.")


if __name__ == "__main__":
    main()
