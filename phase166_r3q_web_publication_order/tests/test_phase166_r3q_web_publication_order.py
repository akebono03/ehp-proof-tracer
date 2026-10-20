"""Phase 166 R3-Q: ordinary Web search uses the unified publication order."""

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase166_r3c_publication_order import precedes_citing_assertion


def test_r3q_pi32_web_complete_is_preserved():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    view = build_group_proof_progress_view(n=2, k=1, max_depth=2)
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert view.steps
    assert view.rendered_lines


def test_r3q_pi43_ordinary_search_runs_under_registered_target_order():
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=3, k=1)
    assert len(candidates) == 1
    target_id = "shared:2:toda:adopted:prop5.1:pi4_3"
    target = bridge.registry.assertion(target_id)
    assert target.content == candidates[0]
    assert target.component_position == 500
    assert precedes_citing_assertion(
        bridge,
        "shared:2:toda:adopted:prop5.1:delta_iota5_relation",
        target_id,
    )
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    assert result.status in (ProofSearchStatus.COMPLETE, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None or result.conclusion.lhs == TodaPrimaryGroup(4, 3)


def test_r3q_pi54_uses_general_prop51_assertion_as_publication_boundary():
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=4, k=1)
    assert len(candidates) == 1
    target_id = "shared:2:toda:adopted:prop5.1:higher_eta_group_relation"
    target = bridge.registry.assertion(target_id)
    assert target.component_position == 600
    assert candidates[0].lhs == TodaPrimaryGroup(5, 4)
    assert precedes_citing_assertion(
        bridge,
        "shared:2:toda:adopted:prop5.1:pi4_3",
        target_id,
    )
    result = search_group_from_registered_goal(n=4, k=1, bridge=bridge)
    assert result.status in (ProofSearchStatus.COMPLETE, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None or result.conclusion.lhs == TodaPrimaryGroup(5, 4)
