"""Read-only runtime contracts for R3-AB."""
from phase166_r3ab_pi65_audit.audit import audit_pi65


def test_pi65_goal_and_publication_metadata():
    report = audit_pi65()
    assert report["candidate_count"] == 1
    assert report["citing_assertion_id"] is not None
    assert report["pi43"]
    assert report["toda45"]
    assert all(x["precedes"] for x in report["pi43"] + report["toda45"])


def test_pi65_direct_and_web_consistent():
    report = audit_pi65()
    assert "exception" not in report["direct_search"]
    assert "exception" not in report["web_search"]
    assert report["direct_search"]["complete"] == report["web_search"]["complete"]
