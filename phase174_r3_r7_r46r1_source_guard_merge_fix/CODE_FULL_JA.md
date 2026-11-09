# R46R1 全コード（省略なし）

変更したファイルの全文と新規ファイルを列挙する。数学的本番モジュールは変更しない。

## 既存変更後: phase174_r3_r7_r46_prop42_dfs_audit/source_guard.py

```python
"""R46 reviewed source guard after the R45/R45R1 audit-only GitHub merge.

Unlike R45's older guard, this checks the current reviewed remote commit,
then verifies all unchanged mathematical sources and both R45 handoff files.
The accepted previous local HEAD is the direct parent of the new remote HEAD.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import (
    ROOT,
    PINS as R45_PRODUCTION_PINS,
    git,
    matches_git_blob,
)

PREVIOUS_REVIEWED_HEAD = "4b06ef96628b39e591cfa0b423fa0e0dec366a3b"
REVIEWED_HEAD = "4d37adab06b40330832c8ec1f08a1b7924ff95af"
REVIEWED_SEARCH_BLOB = "06009bfcf57f99cac58c229d99c53f16324692d0"
R45_LOCAL_PINS = {
    "phase174_r3_r7_r45_ehp_open_obligation_audit/audit.py": "4339a6281208edb27896cb5aa0e27315c655324de9876862c28ea27d4d1aeef5",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/source_guard.py": "726c99fae70021670eeacaa71584dec0f2c34cc1c87e7a7395c40a6dfd6426de",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1": "47e13f0876f0ac97292a0b55acb681c8763b7552cdf15211e0083bfa9fa5db89",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py": "a22bd2634bc22976793a8d4e205f3374117317e79b5323e1566670b5471b17ac",
}


def normalized_sha256(data: bytes) -> str:
    """Accept CRLF/LF conversions only, not edits to statement content."""
    return sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Accept only the two reviewed checkout states with unchanged source bytes."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R46 ZIP must be extracted into repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R46 requires the develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_line or remote_line[0] != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed GitHub develop HEAD; re-audit R46 pins")
    local_head = git("rev-parse", "HEAD")
    if local_head not in (PREVIOUS_REVIEWED_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local HEAD differs from both reviewed R45 merge states")
    staged = git("diff", "--cached", "--name-only").splitlines()
    if staged:
        raise RuntimeError("Staged changes require separate review: " + repr(staged))
    tracked = git("diff", "--name-only").splitlines()
    if tracked:
        raise RuntimeError("Tracked changes require separate review: " + repr(tracked))
    for relative, expected_blob in R45_PRODUCTION_PINS.items():
        file_path = ROOT / relative
        if not file_path.is_file() or not matches_git_blob(
            file_path.read_bytes(), expected_blob
        ):
            raise RuntimeError("Reviewed mathematical source differs: " + relative)
    core_path = ROOT / "phase165_r3_recursive_search.py"
    if not core_path.is_file() or not matches_git_blob(
        core_path.read_bytes(), REVIEWED_SEARCH_BLOB
    ):
        raise RuntimeError("Canonical depth-first search source changed")
    for relative, expected_sha in R45_LOCAL_PINS.items():
        file_path = ROOT / relative
        if not file_path.is_file() or normalized_sha256(file_path.read_bytes()) != expected_sha:
            raise RuntimeError("R45R1 reviewed handoff changed: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": local_head,
        "remote_head": REVIEWED_HEAD,
        "mode": (
            "R45_R45R1_MERGED" if local_head == REVIEWED_HEAD
            else "R45_R45R1_PRE_MERGE_LOCAL"
        ),
        "r45_production_pins": len(R45_PRODUCTION_PINS),
        "r45r1_local_pins": len(R45_LOCAL_PINS),
        "search_core_pin": REVIEWED_SEARCH_BLOB,
        "tracked_changes": 0,
        "production_files_changed": 0,
        "full_pytest": False,
    }
```

## 新規: phase174_r3_r7_r46r1_source_guard_merge_fix/patch.py

```python
"""R46R1: guarded, idempotent repair for R46's outdated parent Source Guard."""
from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import (
    ROOT,
    PINS as R45_PRODUCTION_PINS,
    git,
    matches_git_blob,
)

PACKAGE = Path(__file__).resolve().parent
TARGET = "phase174_r3_r7_r46_prop42_dfs_audit/source_guard.py"
PREVIOUS_REVIEWED_HEAD = "4b06ef96628b39e591cfa0b423fa0e0dec366a3b"
REVIEWED_HEAD = "4d37adab06b40330832c8ec1f08a1b7924ff95af"
REVIEWED_SEARCH_BLOB = "06009bfcf57f99cac58c229d99c53f16324692d0"
R45_LOCAL_PINS = {
    "phase174_r3_r7_r45_ehp_open_obligation_audit/audit.py": "4339a6281208edb27896cb5aa0e27315c655324de9876862c28ea27d4d1aeef5",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/source_guard.py": "726c99fae70021670eeacaa71584dec0f2c34cc1c87e7a7395c40a6dfd6426de",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1": "47e13f0876f0ac97292a0b55acb681c8763b7552cdf15211e0083bfa9fa5db89",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py": "a22bd2634bc22976793a8d4e205f3374117317e79b5323e1566670b5471b17ac",
}


def normalized_sha256(data: bytes) -> str:
    return sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def reviewed_files() -> tuple[Path, Path, Path]:
    """The only permitted patch target and its two source-verified snapshots."""
    return (
        ROOT / TARGET,
        PACKAGE / "baseline" / "source_guard.py",
        PACKAGE / "replacement" / "source_guard.py",
    )


def verify_revised_merge() -> dict[str, object]:
    """Review remote/local lineage and all mathematics before modifying anything."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R46R1 must run from reviewed repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R46R1 requires develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_line or remote_line[0] != REVIEWED_HEAD:
        raise RuntimeError("GitHub develop changed since the reviewed R45 merge")
    local_head = git("rev-parse", "HEAD")
    if local_head not in (PREVIOUS_REVIEWED_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local checkout is not a reviewed R45 merge state")
    if git("diff", "--cached", "--name-only").splitlines():
        raise RuntimeError("R46R1 refuses staged changes")
    if git("diff", "--name-only").splitlines():
        raise RuntimeError("R46R1 refuses tracked modifications")
    for relative, blob in R45_PRODUCTION_PINS.items():
        candidate = ROOT / relative
        if not candidate.is_file() or not matches_git_blob(candidate.read_bytes(), blob):
            raise RuntimeError("Unreviewed mathematical source: " + relative)
    core = ROOT / "phase165_r3_recursive_search.py"
    if not core.is_file() or not matches_git_blob(core.read_bytes(), REVIEWED_SEARCH_BLOB):
        raise RuntimeError("Unreviewed shared search engine")
    for relative, digest in R45_LOCAL_PINS.items():
        candidate = ROOT / relative
        if not candidate.is_file() or normalized_sha256(candidate.read_bytes()) != digest:
            raise RuntimeError("Unreviewed R45/R45R1 audit file: " + relative)
    return {"local_head": local_head, "remote_head": REVIEWED_HEAD}


def pending_replacement() -> tuple[Path, Path, str]:
    destination, original, replacement = reviewed_files()
    if not all(path.is_file() for path in (destination, original, replacement)):
        raise RuntimeError("R46R1 reviewed replacement or target is missing")
    before = normalized_sha256(original.read_bytes())
    after = normalized_sha256(replacement.read_bytes())
    if before == after:
        raise RuntimeError("R46R1 replacement unexpectedly equals baseline")
    current = normalized_sha256(destination.read_bytes())
    if current not in (before, after):
        raise RuntimeError("Existing R46 guard differs from both reviewed snapshots")
    return destination, replacement, "ALREADY_REPAIRED" if current == after else "REPLACE"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    checkout = verify_revised_merge()
    destination, replacement, mode = pending_replacement()
    if not args.dry_run:
        if mode == "REPLACE":
            destination.write_bytes(replacement.read_bytes())
        if pending_replacement()[2] != "ALREADY_REPAIRED":
            raise RuntimeError("R46R1 replacement verification failed")
        from phase174_r3_r7_r46_prop42_dfs_audit.source_guard import verify_checkout
        if verify_checkout()["remote_head"] != REVIEWED_HEAD:
            raise RuntimeError("R46 source guard verification failed")
    prefix = "PHASE174_R3R7R46R1_"
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "LOCAL_HEAD=" + checkout["local_head"])
    print(prefix + "REMOTE_HEAD=" + checkout["remote_head"])
    print(prefix + "TARGET=" + destination.relative_to(ROOT).as_posix() + ":" + mode)
    print(prefix + "PRODUCTION_FILES_CHANGED=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "GATE=" + (
        "PASS_R46R1_MERGE_GUARD_DRYRUN" if args.dry_run
        else "PASS_R46R1_MERGE_GUARD_REPAIRED"
    ))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規: phase174_r3_r7_r46r1_source_guard_merge_fix/run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r46r1_source_guard_merge_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R46R1 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R46R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r46r1_source_guard_merge_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R46R1 guarded repair failed' }
    powershell -NoProfile -ExecutionPolicy Bypass `
      -File '.\phase174_r3_r7_r46_prop42_dfs_audit\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R46 cited Prop42 DFS audit failed' }
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
      'phase174_r3_r7_r46r1_source_guard_merge_fix/tests/test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R46R1 guard regression tests failed' }
    Write-Output 'PHASE174_R3R7R46R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R46R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```

## 新規: phase174_r3_r7_r46r1_source_guard_merge_fix/tests/test_patch.py

```python
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
```

## 新規: phase174_r3_r7_r46r1_source_guard_merge_fix/__init__.py

```python
"""R46R1 source guard lineage correction (audit-only)."""
```
