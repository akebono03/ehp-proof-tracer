"""Real-source scoped canonical backward search; its result may remain incomplete."""
from __future__ import annotations

from phase171_r2j_r4_r9_r2_scoped_search_bridge.audit import replay_scoped_search


def test_scoped_audit_is_readonly_and_never_claims_public_completion():
    report = replay_scoped_search()
    assert report["r8_inferred"] is True
    assert report["r8_rule_catalog_size"] >= 2
    assert report["scoped_root_options"] == 1
    assert report["new_given_added"] == 0
    assert report["public_provider_modified"] is False
    assert report["public_web_verified"] is False
    assert report["scoped_search_status"] in (
        "complete", "partial", "search_failed",
    )
    if report["trust_boundary_accepted"]:
        assert report["scoped_search_complete"] is True
