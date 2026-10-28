"""Static contract checks; PowerShell execution remains Windows-only."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / "run.ps1").read_text(encoding="utf-8")


def test_requires_opt_in_repair():
    assert "[switch]$Repair" in SCRIPT
    assert "if (-not $Repair)" in SCRIPT
    assert "GIT_REF_RESCUE_DRY_RUN=PASS" in SCRIPT


def test_both_normal_refs_are_verified_and_preserved():
    assert "refs/heads/develop^{commit}" in SCRIPT
    assert "refs/remotes/origin/develop^{commit}" in SCRIPT
    assert "if ($postLocal -ne $localCommit -or $postRemote -ne $remoteCommit)" in SCRIPT


def test_only_conflicted_develop_filenames_are_eligible():
    assert "^develop \\([^)]*競合コピー[^)]*\\)$" in SCRIPT
    assert "refs\\heads" in SCRIPT
    assert "refs\\remotes\\origin" in SCRIPT
    assert "git check-ref-format" in SCRIPT


def test_files_are_moved_outside_git_and_not_deleted():
    assert "Join-Path $HOME" in SCRIPT
    assert "[System.IO.File]::Move" in SCRIPT
    assert "Get-FileHash" in SCRIPT
    assert "Remove-Item" not in SCRIPT
    assert "reset --hard" not in SCRIPT


def test_no_automatic_remote_operations():
    assert "Invoke-GitOrFail -Arguments @('fetch'" not in SCRIPT
    assert "Invoke-GitOrFail -Arguments @('pull'" not in SCRIPT
    assert "git gc" not in SCRIPT
