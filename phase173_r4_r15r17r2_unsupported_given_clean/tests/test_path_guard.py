"""R15R17-R2 R2R1: Windows canonical Git paths and HEAD safety contract."""
from __future__ import annotations

from pathlib import Path

from phase173_r4_r15r17r2_unsupported_given_clean import install


PACKAGE = Path(__file__).resolve().parents[1]


def test_windows_git_root_is_compared_as_canonical_paths() -> None:
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "[System.IO.Path]::GetFullPath($GitRoot.Trim())" in script
    assert "[System.IO.Path]::GetFullPath($Root)" in script
    assert "[System.StringComparison]::OrdinalIgnoreCase" in script
    assert "R15R17R2_REPOSITORY_ROOT=PASS" in script
    assert "((& git --no-pager rev-parse --show-toplevel).Trim() -ne $Root)" not in script


def test_head_guard_uses_reviewed_r1_commit_without_weakening_blob_guard() -> None:
    assert install.REVIEWED_REMOTE == "11fdf0f5c52ce2de786e36c3a3d0abe7a0d0fa26"
    assert install.REVIEWED_REMOTE in install.ALLOWED_HEADS
    assert "874c6f63ad85374cd19e00e92600c92c5c056cb3" in install.ALLOWED_HEADS
    assert install.REVIEWED_BLOB == "6dd75099bb2c71fb9873477cb36c11bdb7dad410"
    assert len(install.REVIEWED_BLOB) == 40


def test_run_script_preserves_dryrun_normal_restore_flows() -> None:
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in script
    assert "[switch]$Restore" in script
    assert "python -m phase173_r4_r15r17r2_unsupported_given_clean.install --dry-run" in script
    assert "python -m phase173_r4_r15r17r2_unsupported_given_clean.install --restore" in script
    assert "R15R17R2_FOCUSED_PYTEST=PASS" in script
    assert "git --no-pager fetch origin develop" in script
    assert "git reset" not in script
    assert "git clean" not in script
    assert "git commit" not in script
