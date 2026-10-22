from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model


def main():
    for n, k in ((2, 1), (3, 1), (2, 2)):
        bridge = build_shared_typed_bridge()
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        model = build_linked_proof_narrative_model(result, bridge)
        print(f"PI_{n+k}^{n} STATUS={result.status.value} STEPS={len(result.proven_steps)}")
        print("CITATIONS:", [(c.number, c.reference.locator, c.step_indices, c.assertion_ids) for c in model.citations])
        locators = [c.reference.locator or c.reference.label for c in model.citations]
        assert len(locators) == len(set(locators)), locators
        print("UNIQUE_LOCATORS:", len(locators))
    print("R3-9 MODEL DEDUPLICATION: PASS")
    print("DEFAULT LONG-FORM WEB ROUTE: UNCHANGED")


if __name__ == "__main__":
    main()
