# Phase 173 R4-R15R2R1 — 変更コードとテスト全文

## 変更対象

- `phase173_r4_r15r2_generator_obligation_audit/preflight.py`（ファイル全文を置換。既存 import は変更なし）
- `phase173_r4_r15r2_generator_obligation_audit/run.ps1`（スクリプト全文を置換）
- `phase173_r4_r15r2_generator_obligation_audit/tests/test_head_lineage.py`（`tests/__init__.py` と同じフォルダに追加）
- `README.md`、`design.md`：各全文を ZIP に同梱。

変更する既存の本番クラス・関数はありません。Phase 173 の数学的推論と監査本体 `audit.py` は変更しません。

---

## `preflight.py`：全文

```python
"""Strict read-only preflight for R15R1, committed or still locally installed."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from phase173_r4_r15r1_unbounded_abstract_frontier.patch_source import (
    ORIGINAL_BLOB,
    TARGET,
    transform,
)

REVIEWED_HEAD = "7104222524b63c9c517eaf8e09b8f0825842b316"
REVIEWED_R15R1_COMMITTED_HEAD = "c44519a123fdbf2c5ec57fe9c89e2fb1027f41a5"
REVIEWED_COMMITTED_CORE_BLOB = "d35600804ecbbc5f8566d52e45a2f6ecf8816347"
REVIEWED_COMMITTED_PATCH_BLOB = "06fcdb3c36362225332a1f49cda788b23f9cfc37"
PATCH_SOURCE = "phase173_r4_r15r1_unbounded_abstract_frontier/patch_source.py"
DEPENDENCIES = {
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase173_r4_r6_alias_source_audit/audit.py": "9670dbd8c721e15e0c76b3e043accab6cb01daf3",
    "phase169_r10eq_r1_universal_stable_definition/definition.py": "0c74d121419b6755e947a367d7de465d81193174",
}
ALLOWED_TRACKED = {
    ".pytest_cache/v/cache/nodeids",
    "phase173_r4_r10_general_toda56_core/core.py",
    "phase168_r3_5_model_renderer.py",
    "phase165_r52_r3_web_adapter.py",
    "phase173_r4_r13_narrative_audit/audit.py",
    "phase173_r4_r13_narrative_audit/tests/test_audit.py",
}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if completed.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + completed.stderr[:700])
    return completed.stdout.strip()


def git_content(root: Path, revision: str) -> bytes:
    completed = subprocess.run(
        ("git", "show", revision), cwd=root, capture_output=True, check=False,
    )
    if completed.returncode:
        raise RuntimeError("Cannot read reviewed git content: " + revision)
    return completed.stdout


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def reviewed_installed_core(root: Path, head: str) -> str:
    """Accept only the two reviewed commit states and the exact R15R1 core.

    Old HEAD: R15R1 is a local tracked change. New HEAD: the same R15R1
    core is committed. Neither case accepts an unrelated successor commit.
    """
    if head not in (REVIEWED_HEAD, REVIEWED_R15R1_COMMITTED_HEAD):
        raise RuntimeError("Unreviewed R15R1 commit lineage: " + head)
    if git(root, "rev-parse", REVIEWED_HEAD + ":" + TARGET) != ORIGINAL_BLOB:
        raise RuntimeError("Reviewed pre-R15R1 source blob changed")
    baseline = git_content(root, REVIEWED_HEAD + ":" + TARGET)
    transformed = normalized(transform(baseline))
    actual = normalized((root / TARGET).read_bytes())
    if actual != transformed:
        raise RuntimeError("R15R1 core does not equal reviewed transformation")

    if head == REVIEWED_HEAD:
        if git(root, "rev-parse", "HEAD:" + TARGET) != ORIGINAL_BLOB:
            raise RuntimeError("Pre-R15R1 committed core blob changed")
        return "LOCAL_PATCH"

    if git(root, "rev-parse", "HEAD:" + TARGET) != REVIEWED_COMMITTED_CORE_BLOB:
        raise RuntimeError("Committed R15R1 core blob changed")
    if normalized(git_content(root, "HEAD:" + TARGET)) != transformed:
        raise RuntimeError("Committed R15R1 core differs from the reviewed patch")
    if git(root, "rev-parse", "HEAD:" + PATCH_SOURCE) != REVIEWED_COMMITTED_PATCH_BLOB:
        raise RuntimeError("R15R1 patch implementation changed in committed state")
    if (normalized((root / PATCH_SOURCE).read_bytes())
            != normalized(git_content(root, "HEAD:" + PATCH_SOURCE))):
        raise RuntimeError("Unreviewed local R15R1 patch implementation")
    return "COMMITTED_PATCH"


def preflight(root: Path) -> bool:
    """Verify fixed reviewed commits and pristine mathematical dependencies."""
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Expected repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("Local and remote HEAD differ: " + head + "/" + remote)
    if head not in (REVIEWED_HEAD, REVIEWED_R15R1_COMMITTED_HEAD):
        raise RuntimeError("Unreviewed local or remote HEAD: " + head + "/" + remote)
    staged = git(root, "diff", "--cached", "--name-only")
    if staged:
        raise RuntimeError("Staged changes require review")
    modified = set(filter(None, git(root, "diff", "--name-only").splitlines()))
    if modified - ALLOWED_TRACKED:
        raise RuntimeError("Unexpected tracked modifications: " + str(modified - ALLOWED_TRACKED))
    for name, blob in DEPENDENCIES.items():
        if git(root, "rev-parse", "HEAD:" + name) != blob:
            raise RuntimeError("Committed dependency mismatch: " + name)
        if normalized((root / name).read_bytes()) != normalized(git_content(root, "HEAD:" + name)):
            raise RuntimeError("Unreviewed local dependency change: " + name)
    state = reviewed_installed_core(root, head)
    print("PHASE173_R4_R15R2_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R2_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R2_CORE_STATE=" + state, flush=True)
    print("PHASE173_R4_R15R2_PREVIOUS_R15R1_INSTALLED=True", flush=True)
    print("PHASE173_R4_R15R2_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R2_PRODUCTION_EDIT=NONE", flush=True)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    preflight(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`：全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'Git fetch failed' }
    python -m phase173_r4_r15r2_generator_obligation_audit.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R2 Preflight failed' }
    python -m pytest -q `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_static.py `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_head_lineage.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R2 static tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R2_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R2_PRODUCTION_EDIT=NONE'
        exit 0
    }
    python -m pytest -q `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_audit.py `
        phase173_r4_r10_general_toda56_core/tests/test_core.py `
        phase173_r4_r15r1_unbounded_abstract_frontier/tests
    if ($LASTEXITCODE -ne 0) { throw 'R15R2 focused tests failed' }
    Write-Output 'PHASE173_R4_R15R2_FOCUSED_PYTEST=PASS'
    python -m phase173_r4_r15r2_generator_obligation_audit.audit `
        --root "$Root" `
        --output (Join-Path $PSScriptRoot 'factor_obligation_report.json')
    if ($LASTEXITCODE -ne 0) { throw 'R15R2 factor audit failed' }
    Write-Output 'PHASE173_R4_R15R2_PHASE_COMPLETED=False'
} finally {
    Pop-Location
}
```

## `tests/test_head_lineage.py`：全文

```python
"""Focused tests of R15R1 HEAD lineage and content guards."""
from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from phase173_r4_r15r2_generator_obligation_audit import preflight as guard


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True, check=True,
    )
    return completed.stdout.strip()


def _make_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, str, str]:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-b", "develop")
    _git(root, "config", "user.name", "Test User")
    _git(root, "config", "user.email", "tester@example.invalid")
    core_file = root / guard.TARGET
    core_file.parent.mkdir(parents=True)
    core_file.write_bytes(b"original\n")
    _git(root, "add", "--", guard.TARGET)
    _git(root, "commit", "-m", "reviewed original")
    old_head = _git(root, "rev-parse", "HEAD")
    original_blob = _git(root, "rev-parse", "HEAD:" + guard.TARGET)

    patch_file = root / guard.PATCH_SOURCE
    patch_file.parent.mkdir(parents=True)
    patch_file.write_bytes(b"reviewed patch implementation\n")
    core_file.write_bytes(b"installed R15R1\n")
    _git(root, "add", "--", guard.TARGET, guard.PATCH_SOURCE)
    _git(root, "commit", "-m", "reviewed R15R1")
    new_head = _git(root, "rev-parse", "HEAD")
    monkeypatch.setattr(guard, "REVIEWED_HEAD", old_head)
    monkeypatch.setattr(guard, "REVIEWED_R15R1_COMMITTED_HEAD", new_head)
    monkeypatch.setattr(guard, "ORIGINAL_BLOB", original_blob)
    monkeypatch.setattr(guard, "REVIEWED_COMMITTED_CORE_BLOB", _git(root, "rev-parse", "HEAD:" + guard.TARGET))
    monkeypatch.setattr(guard, "REVIEWED_COMMITTED_PATCH_BLOB", _git(root, "rev-parse", "HEAD:" + guard.PATCH_SOURCE))
    monkeypatch.setattr(guard, "transform", lambda source: b"installed R15R1\n" if source == b"original\n" else b"unexpected\n")
    return root, old_head, new_head


def test_accepts_reviewed_committed_r15r1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, new_head = _make_repo(tmp_path, monkeypatch)
    assert guard.reviewed_installed_core(root, new_head) == "COMMITTED_PATCH"


def test_accepts_reviewed_local_r15r1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, old_head, _ = _make_repo(tmp_path, monkeypatch)
    _git(root, "checkout", old_head)
    (root / guard.TARGET).write_bytes(b"installed R15R1\n")
    assert guard.reviewed_installed_core(root, old_head) == "LOCAL_PATCH"


def test_rejects_unreviewed_future_commit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, _ = _make_repo(tmp_path, monkeypatch)
    _git(root, "commit", "--allow-empty", "-m", "unreviewed successor")
    with pytest.raises(RuntimeError, match="Unreviewed R15R1 commit lineage"):
        guard.reviewed_installed_core(root, _git(root, "rev-parse", "HEAD"))


def test_rejects_modified_worktree_core(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, new_head = _make_repo(tmp_path, monkeypatch)
    (root / guard.TARGET).write_bytes(b"changed\n")
    with pytest.raises(RuntimeError, match="does not equal reviewed transformation"):
        guard.reviewed_installed_core(root, new_head)


def test_rejects_modified_worktree_patch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, new_head = _make_repo(tmp_path, monkeypatch)
    (root / guard.PATCH_SOURCE).write_bytes(b"unreviewed patch implementation\n")
    with pytest.raises(RuntimeError, match="Unreviewed local R15R1 patch implementation"):
        guard.reviewed_installed_core(root, new_head)


def test_rejects_committed_core_with_wrong_blob(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, new_head = _make_repo(tmp_path, monkeypatch)
    monkeypatch.setattr(guard, "REVIEWED_COMMITTED_CORE_BLOB", "0" * 40)
    with pytest.raises(RuntimeError, match="Committed R15R1 core blob changed"):
        guard.reviewed_installed_core(root, new_head)
```

## 既存のテスト・監査ファイル（変更なし、全文参照）

実行用 ZIP には監査ファイル `audit.py`、既存テスト `tests/test_static.py` と `tests/test_audit.py` の全文を収録しています。
