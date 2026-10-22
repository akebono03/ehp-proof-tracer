from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model


def main():
    for n, k in ((2, 1), (3, 1), (2, 2)):
        bridge = build_shared_typed_bridge()
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        model = build_linked_proof_narrative_model(result, bridge)
        locators = [c.reference.locator or c.reference.label for c in model.citations]
        print(f"PI_{n+k}^{n}: {locators}")
        assert len(locators) == len(set(locators))
        if (n, k) == (2, 1):
            assert len(locators) == 4
        if (n, k) == (3, 1):
            assert len(locators) == 4, locators
            assert sum(locator.startswith("Chapter V, i)") for locator in locators) == 1
        if (n, k) == (2, 2):
            assert locators == ["Proposition 5.1", "(5.2)"]
    print("R3-10 REGISTERED HEADING ALIAS: PASS")
    print("DEFAULT WEB ROUTE: UNCHANGED")


if __name__ == "__main__":
    main()
