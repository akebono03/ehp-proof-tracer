"""Read-only regression checks for the pi4^3 audit."""
from phase165_r52_r20_pi43_audit import audit_pi43, pi43_goal
from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge


def test_pi43_audit_goal_is_correct():
    goal = pi43_goal()
    assert goal.lhs == TodaPrimaryGroup(4, 3)
    assert goal.rhs.order == 2


def test_pi43_audit_reports_observed_search_without_inventing_steps():
    bridge = build_shared_typed_bridge()
    before = tuple(bridge.proof_links)
    report = audit_pi43(bridge)
    assert tuple(bridge.proof_links) == before
    assert report.status in ("complete", "partial", "search_failed")
    assert report.full_pytest_run is False
    assert report.proof_complete == (report.status == "complete")
    if report.root_expansion_count == 0 and not report.proof_complete:
        assert "no_backward_expansion_for_pi43_group_goal" in report.missing_obligations
