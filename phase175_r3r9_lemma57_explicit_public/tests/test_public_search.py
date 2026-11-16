"""Focused actual public search and trust/citation boundary regression."""
from __future__ import annotations

from phase175_r1_k4_audit.audit import inspect_one_group
from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result


def test_real_group_query_has_direct_lemma57_proof_and_no_lemma54_reference() -> None:
    observed = inspect_one_group(3, 4)
    certified = verify_public_result(observed)
    assert certified["search_status"] == "complete"
    assert certified["web"] == "generic-complete-proof"
    assert certified["lemma54_used"] is False
    assert certified["reference_count"] >= 2
