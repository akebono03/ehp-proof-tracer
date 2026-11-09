"""Verify R46R1's exact reviewed merge and one-file guard repair."""
from __future__ import annotations

from hashlib import sha1
from pathlib import Path

import pytest

from phase174_r3_r7_r46r1_source_guard_merge_fix import patch
from phase174_r3_r7_r46_prop42_dfs_audit import source_guard


def test_only_r46_source_guard_is_replaced_and_contents_are_pinned():
    destination, baseline, replacement = patch.reviewed_files()
    assert patch.TARGET == "phase174_r3_r7_r46_prop42_dfs_audit/source_guard.py"
    assert all(path.is_file() for path in (destination, baseline, replacement))
    assert patch.pending_replacement()[2] == "ALREADY_REPAIRED"
    assert patch.normalized_sha256(destination.read_bytes()) == patch.normalized_sha256(
        replacement.read_bytes()
    )
    original = baseline.read_text(encoding="utf-8")
    revised = replacement.read_text(encoding="utf-8")
    assert "verify_r45_checkout()" in original
    assert "verify_r45_checkout()" not in revised
    assert "for relative, expected_blob in R45_PRODUCTION_PINS.items()" in revised
    assert "for relative, expected_sha in R45_LOCAL_PINS.items()" in revised
    assert 'git("ls-remote", "origin", "refs/heads/develop")' in revised


def test_reviewed_head_is_exact_new_commit_and_prior_is_direct_parent():
    assert source_guard.PREVIOUS_REVIEWED_HEAD == "4b06ef96628b39e591cfa0b423fa0e0dec366a3b"
    assert source_guard.REVIEWED_HEAD == "4d37adab06b40330832c8ec1f08a1b7924ff95af"
    assert len(source_guard.R45_PRODUCTION_PINS) == 12
    assert len(source_guard.R45_LOCAL_PINS) == 4
    assert len(source_guard.REVIEWED_SEARCH_BLOB) == 40


def test_source_guard_checks_real_blob_hashes_and_rejects_tampering(tmp_path, monkeypatch):
    def blob_sha(value: bytes) -> str:
        return sha1(b"blob " + str(len(value)).encode("ascii") + b"\0" + value).hexdigest()

    math_path = tmp_path / "math.py"
    search_path = tmp_path / "phase165_r3_recursive_search.py"
    handoff_path = tmp_path / "handoff.py"
    math_path.write_bytes(b"math\n")
    search_path.write_bytes(b"search\n")
    handoff_path.write_bytes(b"handoff\n")
    monkeypatch.setattr(source_guard, "ROOT", tmp_path)
    monkeypatch.setattr(source_guard, "R45_PRODUCTION_PINS", {"math.py": blob_sha(b"math\n")})
    monkeypatch.setattr(source_guard, "REVIEWED_SEARCH_BLOB", blob_sha(b"search\n"))
    monkeypatch.setattr(source_guard, "R45_LOCAL_PINS", {"handoff.py": source_guard.normalized_sha256(b"handoff\n")})

    state = {"local": source_guard.PREVIOUS_REVIEWED_HEAD, "remote": source_guard.REVIEWED_HEAD,
             "staged": "", "tracked": ""}

    def fake_git(*args):
        key = " ".join(args)
        if key == "rev-parse --show-toplevel":
            return str(tmp_path)
        if key == "branch --show-current":
            return "develop"
        if key == "ls-remote origin refs/heads/develop":
            return state["remote"] + " refs/heads/develop"
        if key == "rev-parse HEAD":
            return state["local"]
        if key == "diff --cached --name-only":
            return state["staged"]
        if key == "diff --name-only":
            return state["tracked"]
        raise AssertionError(key)

    monkeypatch.setattr(source_guard, "git", fake_git)
    assert source_guard.verify_checkout()["mode"] == "R45_R45R1_PRE_MERGE_LOCAL"
    state["local"] = source_guard.REVIEWED_HEAD
    assert source_guard.verify_checkout()["mode"] == "R45_R45R1_MERGED"
    state["remote"] = source_guard.PREVIOUS_REVIEWED_HEAD
    with pytest.raises(RuntimeError, match="Unreviewed GitHub"):
        source_guard.verify_checkout()
    state["remote"] = source_guard.REVIEWED_HEAD
    state["staged"] = "unreviewed.py"
    with pytest.raises(RuntimeError, match="Staged changes"):
        source_guard.verify_checkout()
    state["staged"] = ""
    state["tracked"] = "math.py"
    with pytest.raises(RuntimeError, match="Tracked changes"):
        source_guard.verify_checkout()
    state["tracked"] = ""
    math_path.write_bytes(b"not math\n")
    with pytest.raises(RuntimeError, match="mathematical source"):
        source_guard.verify_checkout()
    math_path.write_bytes(b"math\n")
    handoff_path.write_bytes(b"not handoff\n")
    with pytest.raises(RuntimeError, match="R45R1 reviewed handoff"):
        source_guard.verify_checkout()


def test_r46r1_runner_remains_audit_only():
    runner = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in runner
    assert "patch --dry-run" in runner
    assert "phase174_r3_r7_r46_prop42_dfs_audit\\run.ps1" in runner
    assert "--import-mode=importlib" in runner
    assert "git reset" not in runner
    assert "git clean" not in runner
    assert "FULL_PYTEST=False" in runner
