"""Pure tests for the two reviewed replacements, without a repository checkout."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r6_r2r1_regression_fix.patch import (
    normalize,
    patch_cumulative_test,
    patch_delta_audit,
)


def test_cumulative_lineage_replay_accepts_crlf_and_preserves_git_blob_guard() -> None:
    original = (
        "from pathlib import Path\n\n"
        "def test_r3r4_real_production_file_has_only_reviewed_wiring():\n"
        "    from phase174_r3_r6_r2_prop44_lemma54.patch import patch_shared\n"
        "    old = b'old'\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    r3r4 = old\n"
        "    r3r5 = old\n"
        "    r3r6 = old\n"
        "    new_source = patch_shared(r3r6.decode('utf-8')).encode('utf-8')\n"
        "    assert current in (r3r4, r3r5, r3r6, new_source)\n"
        "    assert git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'\n"
    )
    updated = patch_cumulative_test(original)
    assert "patch_shared(normalize(r3r6.decode('utf-8')))" in updated
    assert "normalize(current.decode('utf-8'))" in updated
    assert "git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'" in updated
    ast.parse(updated)
    assert normalize(updated.replace("\n", "\r\n")) == updated


def test_delta_audit_screen_reuses_verified_lemma_and_checks_both_ancestors() -> None:
    source = (
        "def inspect_public_provider():\n"
        "    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement\n"
        "    citation = 8800\n"
        "    bridge = original_bridge\n"
        "    if citation is None:\n"
        "        raise ValueError(\"No actual pi_8^5 publication position\")\n"
        "    screened = screen_shared_proof_context(\n"
        "        bridge, goal=target, citing_assertion_id=citation,\n"
        "    )\n"
        "    if (\n"
        "        step.rule is not ProofRule.INFERENCE\n"
        "        or not proof_has_cited_leaf(step.premises[0], TodaProp44UniversalStatement())\n"
        "        or not proof_has_cited_leaf(step.premises[1], TodaProp42GeneralExactnessStatement())\n"
        "    ):\n"
        "        raise ValueError('missing')\n"
    )
    updated = patch_delta_audit(source)
    assert "attach_earlier_verified_lemma54(bridge, citation)" in updated
    assert "proof_has_cited_leaf(step.premises[0], TodaLemma54TypedSource())" in updated
    assert "if amended is bridge:" in updated
    ast.parse(updated)


def test_changed_ancestry_guard_rejects_missing_expected_line() -> None:
    source = (
        "def inspect_public_provider():\n"
        "    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement\n"
    )
    with pytest.raises(ValueError, match="public context"):
        patch_delta_audit(source)


def test_lineage_test_rejects_unreviewed_prior_replay() -> None:
    source = (
        "def test_r3r4_real_production_file_has_only_reviewed_wiring():\n"
        "    from phase174_r3_r6_r2_prop44_lemma54.patch import patch_shared\n"
        "    return None\n"
    )
    with pytest.raises(ValueError, match="replay"):
        patch_cumulative_test(source)
