"""Focused tests: no alternative renderer or source guessing."""
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from web_group_proof import build_standard_web_group_proof_view


def test_pi54_actual_screened_context_has_all_registered_references():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=1, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status.value == "complete"
    assert len(contexts) == 1
    model = build_linked_proof_narrative_model(result, contexts[0])
    by_locator = {c.reference.locator: c for c in model.citations}
    assert by_locator["Proposition 5.1"].assertion_ids == (
        "shared:2:toda:adopted:prop5.1:pi4_3",
    )
    assert by_locator["(4.5)"].assertion_ids == (
        "shared:4:typed_literature:assertion:toda:tex:ch4:0006",
    )


def test_public_entry_remains_model_backed():
    view = build_standard_web_group_proof_view(n=4, k=1)
    assert view is not None
