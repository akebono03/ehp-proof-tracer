"""R3R1: audited HEAD guard and read-only safety of its PowerShell runner."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HEAD = "aa25a9930d36b61e7588d1ef8e5916a766b569e6"
OBSOLETE_HEAD = "11fdf0f5c52ce2de786e36c3a3d0abe7a0d0fa26"


def test_reviewed_head_is_r2_committed_head() -> None:
    source = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert source.count(EXPECTED_HEAD) == 1
    assert OBSOLETE_HEAD not in source
    assert "R15R17R3_REVIEWED_HEAD=" in source
    assert "current HEAD=" in source


def test_runner_keeps_read_only_git_guard() -> None:
    source = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "git --no-pager" in source
    assert "'write-tree'" in source
    assert "$IndexBefore -ne $IndexAfter" in source
    assert "git --no-pager @Arguments" in source
    assert "R15R17R3_PRODUCTION_WRITES=NONE" in source
    for forbidden in ("git reset", "git clean", "git add ", "git commit"):
        assert forbidden not in source


def test_r2_source_hash_check_is_still_mandatory() -> None:
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    runner = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "def check_r2_installation()" in source
    assert 'state.get("installed_sha256")' in source
    assert "check_r2_installation()" in source
    assert "R15R17-R3 audit program failed" in runner
