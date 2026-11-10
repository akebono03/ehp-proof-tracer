"""Verify the published source-first proof after bespoke narrative deletion."""
from __future__ import annotations

from phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.audit import inspect_shared_display


def test_real_public_proof_uses_shared_typed_and_reference_projection() -> None:
    observed = inspect_shared_display()
    assert observed['source_first_root_complete'] is True
    assert observed['root_ancestor_steps'] == 28
    assert observed['dedicated_r55r3_narrative_remaining'] is False
    assert observed['r7_typed_formula_visible'] is True
    assert observed['new_givens'] == 0
    assert observed['new_math_rules'] == 0
    assert observed['both_http_200'] is True
    assert observed['both_http_complete'] is True
