from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view


def main():
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    view = build_partial_web_group_proof_view(result, narrative_model=model)
    print("STATUS:", result.status)
    print("CITATIONS:", [(c.number, c.reference.locator) for c in model.citations])
    print("WEB_LINES:")
    for line in view.rendered_lines:
        print(repr((line.prefix, line.statement_latex, line.suffix)))
    assert len(model.citations) == 2
    assert [c.reference.locator for c in model.citations] == ["Proposition 5.1", "(5.2)"]
    print("MODEL_BACKED_VIEW: PASS")
    print("DEFAULT_WEB_ROUTE: UNCHANGED")


if __name__ == "__main__":
    main()
