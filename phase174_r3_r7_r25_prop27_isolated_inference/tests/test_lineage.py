"""Focused regression tests for the R25 reviewed-ancestor Git guard."""

import pytest

from phase174_r3_r7_r25_prop27_isolated_inference.audit import (
    REVIEWED_HEAD, classify_lineage,
)


def test_r25_lineage_accepts_original_reviewed_head():
    assert classify_lineage(REVIEWED_HEAD, REVIEWED_HEAD, True, ()) == "REVIEWED_HEAD"


def test_r25_lineage_accepts_reviewed_r24_commit():
    result = classify_lineage(
        "a" * 40, REVIEWED_HEAD, True,
        ("phase174_r3_r7_r24_prop27_general_typed_design/audit.py",),
    )
    assert result == "R24_R25_ONLY_DESCENDANT"


def test_r25_lineage_accepts_matching_updated_remote():
    head = "b" * 40
    assert classify_lineage(
        head, head, True,
        ("phase174_r3_r7_r24_prop27_general_typed_design/tests/test_audit.py",),
    ) == "R24_R25_ONLY_DESCENDANT"


@pytest.mark.parametrize("paths", [
    ("proof.py",),
    ("phase174_r3_r7_r24_prop27_general_typed_design/audit.py", "toda_rules.py"),
    ("tests/test_phase50_prop27_theorem_semantics.py",),
])
def test_r25_lineage_rejects_unrelated_commits(paths):
    with pytest.raises(RuntimeError, match="Unreviewed committed paths"):
        classify_lineage("a" * 40, REVIEWED_HEAD, True, paths)


def test_r25_lineage_rejects_unreviewed_parent():
    with pytest.raises(RuntimeError, match="does not descend"):
        classify_lineage("a" * 40, REVIEWED_HEAD, False, ())


def test_r25_lineage_rejects_diverging_remote():
    with pytest.raises(RuntimeError, match="Remote develop"):
        classify_lineage("a" * 40, "b" * 40, True, ())


def test_r25_lineage_accepts_reviewed_r24_with_committed_pytest_cache():
    head = "bfaf93f712651b8c6fca5e4ef174dfac3d937515"
    changed = (
        ".pytest_cache/v/cache/nodeids",
        "phase174_r3_r7_r24_prop27_general_typed_design/audit.py",
    )
    assert classify_lineage(head, head, True, changed) == "R24_R25_ONLY_DESCENDANT"


@pytest.mark.parametrize("cache_path", [
    ".pytest_cache/v/cache/lastfailed",
    ".pytest_cache/README.md",
    ".pytest_cache/v/cache/nodeids.bak",
    "tests/.pytest_cache/v/cache/nodeids",
])
def test_r25_lineage_rejects_other_committed_cache_paths(cache_path):
    with pytest.raises(RuntimeError, match="Unreviewed committed paths"):
        classify_lineage("a" * 40, REVIEWED_HEAD, True, (cache_path,))
