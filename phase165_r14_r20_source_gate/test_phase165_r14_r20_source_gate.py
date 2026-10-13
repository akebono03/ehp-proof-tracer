from phase165_r14_r20_source_gate import (
    AdoptedTextReview, diagonal_text_matches, source_scoped_reviewed_bridge,
    prop42_candidate_report, audit_r20,
)
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge

SOURCE = r"""\pi^{1}_{i}=0\ (i>1),\qquad
\pi^{n}_{i}=0\ (i<n),\qquad
G_k=(G_k;2)=0\ (k<0).
\pi^{n}_{n}=\gen{\iota_n}\cong \mathbb Z,\qquad
G_0=\gen{\iota}\cong \mathbb Z. \quad
\iota=E^{\infty}\iota_n."""


def test_all_diagonal_scope_tokens_required():
    assert diagonal_text_matches(AdoptedTextReview(SOURCE))
    assert not diagonal_text_matches(AdoptedTextReview(SOURCE.replace(
        r"\iota=E^{\infty}\iota_n", "")))


def test_no_review_no_new_assertions():
    base, _ = build_phase165_r5_manifest_bridge()
    out, ids, status = source_scoped_reviewed_bridge(base, AdoptedTextReview(SOURCE))
    assert out is base and ids == () and status == "EXPLICIT_REVIEW_REQUIRED"


def test_explicit_adopted_scope_review_uses_existing_r19_bridge():
    base, _ = build_phase165_r5_manifest_bridge()
    before = len(base.registry._assertions)
    reviewed, ids, status = source_scoped_reviewed_bridge(
        base, AdoptedTextReview(SOURCE, reviewer_confirmed_scope=True))
    assert status == "REVIEWED_ADOPTED_TEX"
    assert len(ids) == 2
    assert len(reviewed.registry._assertions) == before + 2
    assert len(base.registry._assertions) == before


def test_missing_source_is_fail_closed():
    base, _ = build_phase165_r5_manifest_bridge()
    result, ids, status = source_scoped_reviewed_bridge(base, None)
    assert result is base and not ids and status == "SOURCE_SCOPE_MISSING"


def test_prop42_two_candidates_still_unapproved():
    base, _ = build_phase165_r5_manifest_bridge()
    rows = prop42_candidate_report(base)
    assert len(rows) == 2
    assert all(not x["scope_certified"] and not x["proof_eligible"] for x in rows)


def test_standard_audit_does_not_create_proof():
    report = audit_r20()
    assert report["reviewed_diagonal_entries_added"] == 0
    assert report["new_proof_steps"] == 0
    assert report["pi32_proved"] is False
