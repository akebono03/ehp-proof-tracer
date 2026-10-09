"""Focused read-only Phase 162 R9 audit contracts."""

from audit import analyze, report


def test_root_and_replay_use_same_step():
    audit = analyze()
    assert audit["presentation"].root_step is audit["root"]
    assert audit["root"].premises


def test_provenance_contains_root_and_direct_dependencies():
    audit = analyze()
    paths = {record["path"] for record in audit["records"]}
    assert "root" in paths
    assert {"root/1", "root/2", "root/3"}.issubset(paths)


def test_audit_does_not_claim_no_renderer_defects():
    audit = analyze()
    text = report(audit)
    assert "Stable transport" in text
    assert "意味の異なる完全列" in text
    assert "stable_tail" in audit["issues"]
