"""R48 verifies a reviewed HEAD and the R47 handoff without production changes."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.source_guard import (
    REVIEWED_HEAD, REVIEWED_RULE_BLOBS, R47_HANDOFF_FILES,
    ROOT, normalized_sha256, verify_checkout,
)


def test_guard_pins_math_rules_and_the_prior_audit() -> None:
    assert len(REVIEWED_HEAD) == 40
    assert all(len(blob) == 40 for blob in REVIEWED_RULE_BLOBS.values())
    assert len(R47_HANDOFF_FILES) == 2
    assert all(len(digest) == 64 for digest in R47_HANDOFF_FILES.values())
    assert Path(ROOT).is_absolute()


def test_guard_accepts_the_exact_referenced_checkout() -> None:
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["remote_head"] == REVIEWED_HEAD
    assert state["production_files_changed"] == 0
    assert state["full_pytest"] is False
    for relative, digest in R47_HANDOFF_FILES.items():
        assert normalized_sha256((ROOT / relative).read_bytes()) == digest
