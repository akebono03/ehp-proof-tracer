"""R50 pins real source bytes and only the R49 audit merge is allowed."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r50_root_exactness_terminal_zero_frontier.source_guard import (
    PERMITTED_MERGE_PREFIX,
    R49_HANDOFF_SHA256,
    REVIEWED_BASE_HEAD,
    ROOT,
    ROOT_PROOF_SOURCE_BLOBS,
    normalized_sha256,
    verify_checkout,
)


def test_r50_source_guard_is_pinned_to_mathematical_sources() -> None:
    assert len(REVIEWED_BASE_HEAD) == 40
    assert PERMITTED_MERGE_PREFIX.endswith("r49_prop27_upper_delta_tree_frontier/")
    assert len(ROOT_PROOF_SOURCE_BLOBS) >= 5
    assert len(R49_HANDOFF_SHA256) == 6
    assert all(len(sha) == 40 for sha in ROOT_PROOF_SOURCE_BLOBS.values())
    assert all(len(digest) == 64 for digest in R49_HANDOFF_SHA256.values())


def test_r50_source_guard_accepts_reviewed_current_checkout() -> None:
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["production_files_changed"] == 0
    assert state["new_givens"] == 0
    assert state["full_pytest"] is False
    for relative, digest in R49_HANDOFF_SHA256.items():
        assert normalized_sha256((ROOT / relative).read_bytes()) == digest
