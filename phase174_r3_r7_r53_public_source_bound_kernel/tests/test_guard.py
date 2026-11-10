"""R53 source guard and idempotent whole-function patch contracts."""
from __future__ import annotations

import ast

from phase174_r3_r7_r53_public_source_bound_kernel.install import (
    NEW_ANCHOR, OLD_ANCHOR, function_source, patched_source, prepare,
)
from phase174_r3_r7_r53_public_source_bound_kernel.source_guard import (
    REVIEWED_BLOBS, REVIEWED_HEAD, TARGET, TARGET_BLOB,
    verify_checkout,
)


def test_current_checked_develop_matches_reviewed_production_contract() -> None:
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["local_head"] == REVIEWED_HEAD
    assert state["remote_head"] == REVIEWED_HEAD
    assert state["reviewed_blob_count"] == len(REVIEWED_BLOBS) + 1
    assert len(TARGET_BLOB) == 40
    assert TARGET == "phase165_r55_nk_only_goal.py"


def test_replacement_is_idempotent_and_complete() -> None:
    working, old, updated = prepare()
    assert OLD_ANCHOR in old and NEW_ANCHOR not in old
    assert NEW_ANCHOR in updated and OLD_ANCHOR not in updated
    assert patched_source(old) == updated
    assert patched_source(updated) == updated
    actual = function_source(updated, "search_group_from_registered_goal")
    ast.parse(actual, feature_version=(3, 10))
    assert actual.count("build_public_source_bound_kernel_provider(provider, screened)") == 1
