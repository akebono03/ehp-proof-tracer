"""Fail-closed review contracts for read-only R18 source boundaries."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r18_delta_image_surjectivity.audit import (
    HANDOFF_TRACKED,
    PRE_R17_HEAD,
    REVIEWED_HEAD,
    PINS,
    checked_lineage,
    git_blob_sha,
    matches_git_blob,
)


def _reviewed_files() -> tuple[str, ...]:
    return HANDOFF_TRACKED + (
        "phase174_r3_r7_r17_typed_map_open_goal/patch.py",
        "phase174_r3_r7_r17r1_historical_test_contract/audit.py",
        "phase174_r3_r7_r17r2_windows_git_path_guard_fix/patch.py",
    )


def test_allow_only_exact_reviewed_clean_or_handoff_state() -> None:
    files = _reviewed_files()
    assert checked_lineage(REVIEWED_HEAD, REVIEWED_HEAD, (), files) == "R17_MERGED_CLEAN"
    assert checked_lineage(PRE_R17_HEAD, REVIEWED_HEAD, HANDOFF_TRACKED, files) == (
        "R17_PATCHES_UNCOMMITTED_MATCH_MERGED_REMOTE"
    )


@pytest.mark.parametrize("local,remote,changed", (
    ("a" * 40, REVIEWED_HEAD, ()),
    (REVIEWED_HEAD, "b" * 40, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, HANDOFF_TRACKED),
    (PRE_R17_HEAD, REVIEWED_HEAD, ()),
    (PRE_R17_HEAD, REVIEWED_HEAD, HANDOFF_TRACKED + ("other.py",)),
))
def test_unreviewed_state_refused(local, remote, changed) -> None:
    with pytest.raises(RuntimeError):
        checked_lineage(local, remote, changed, _reviewed_files())


def test_unreviewed_commit_path_is_rejected() -> None:
    with pytest.raises(RuntimeError, match="unexpected files"):
        checked_lineage(REVIEWED_HEAD, REVIEWED_HEAD, (), _reviewed_files() + ("proof.py",))


def test_uniform_crlf_checkout_still_source_guarded() -> None:
    lf = b"first\nsecond\n"
    sha = git_blob_sha(lf)
    assert matches_git_blob(lf, sha)
    assert matches_git_blob(b"first\r\nsecond\r\n", sha)
    assert not matches_git_blob(lf + b"unreviewed", sha)
    assert not matches_git_blob(b"first\r\nsecond\n", sha)


def test_source_pins_cover_math_and_database_and_proof_code() -> None:
    for path in (
        "phase165_r52_r9_shared_math.py",
        "phase165_r57_r19_delta_image_backward.py",
        "toda_delta_image_rules.py",
        "phase169_r10e4_ordered_db_prior/db_prior.py",
        "data/sphere.csv", "data/HyoujiGen.csv",
    ):
        assert path in PINS
        assert len(PINS[path]) == 40


def test_audit_has_no_production_install_or_file_mutation() -> None:
    path = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "inspect_live_frontier" in functions
    assert not functions.intersection({"install", "patch", "apply", "rewrite_source"})
    assert "git reset" not in path.read_text(encoding="utf-8")
