"""R43 checked Git patch and fail-closed source constraints."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
    ANCHOR, BASE_BLOB, INSERT, expected_replacement, verify_checkout,
)


def test_r43_uses_only_reviewed_r42_handoff():
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["r42_reviewed_files"] == 11
    assert state["shared_math_mode"] == "INSTALLED"


def test_patch_rejects_unreviewed_or_unpinned_text():
    with pytest.raises(RuntimeError, match="Unexpected shared provider"):
        expected_replacement(b"invalid\n" + ANCHOR.encode("utf-8"))


def test_patch_preserves_exact_single_anchor_and_no_direct_givens():
    from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
        ROOT, TARGET, git_bytes, normalize,
    )
    original = git_bytes("show", "HEAD:" + TARGET)
    new = expected_replacement(original)
    assert new.count(INSERT.encode("utf-8")) == 1
    assert new.replace(INSERT.encode("utf-8"), b"", 1) == normalize(original)
    assert b"ProofStep(" not in INSERT.encode("utf-8")
    assert (ROOT / TARGET).is_file()
