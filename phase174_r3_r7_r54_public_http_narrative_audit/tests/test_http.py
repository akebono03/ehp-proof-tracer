"""R54 public Flask Group query; in-process HTTP, real source-backed search."""
from __future__ import annotations

from phase174_r3_r7_r54_public_http_narrative_audit.audit import (
    inspect_public_http_proof,
)


def test_group_and_group_proof_http_return_complete_cited_narrative() -> None:
    report = inspect_public_http_proof()
    assert report["inprocess_http_verified"] is True
    assert report["checked_form_kinds"] == ["group", "group_proof"]
    assert report["both_http_200"] is True
    assert report["both_complete_proof"] is True
    for observed in report["cases"]:
        assert observed["conclusion_latex"].replace(" ", "") == r"\pi_{12}^{7}=0"
        assert observed["public_proof_key"] == "generic-complete-proof"
        assert observed["citation_references_visible"] is True
        assert observed["proof_ends_with_box"] is True
        assert observed["proof_mode"] == "narrative"
    assert report["production_files_changed"] == 0
    assert report["live_server_checked"] is False
    assert report["browser_katex_checked"] is False
