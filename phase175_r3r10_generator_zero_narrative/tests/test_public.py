"""Actual public Group query must show the cited generator image before zero map."""
from __future__ import annotations

from phase175_r3r10_generator_zero_narrative.audit import _audit_public_result


def test_pi73_public_narrative_explicit_lemma57_generator_zero() -> None:
    observed = _audit_public_result()
    assert observed["search_status"] == "complete"
    assert observed["web"] == "generic-complete-proof"
    assert observed["trust"] is True
    assert observed["lemma54_used"] is False
    assert "=0" in observed["display_line"]
