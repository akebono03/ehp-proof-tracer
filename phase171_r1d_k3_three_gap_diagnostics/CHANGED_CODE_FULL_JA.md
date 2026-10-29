# Phase 171 R1D-R2 — 変更コード全文

## 変更対象・追加位置

- `phase171_r1d_k3_three_gap_diagnostics/triage.py`: `EXPECTED_HEAD` の直後に新しい定数 `REVIEWED_CURRENT_HEAD`, `ALLOWED_WORKTREE_HEADS` を追加し、`tracked_state()` 全体を置換。`validate_report()` や `run()` は**変更しない**。
- `phase171_r1d_k3_three_gap_diagnostics/tests/test_triage.py`: ファイル末尾に5個の新規テスト関数を追加。既存13テストは保持。
- `phase171_r1d_k3_three_gap_diagnostics/README.md`: 追加した説明の全文は ZIP 内のファイルを参照。
- `run.ps1`, `__init__.py`, 全ての production source, DB, 正式文書: **変更なし**。

`triage.py` と `tests/test_triage.py` の import は一切変更なし。以下は変更対象ファイルの変更後 import 全文と、置換する関数・追加するテスト関数の全文である。ZIP には修正済み各ファイル全体も収録する。コード省略はない。

## `triage.py` の import 全文

```python
"""Read-only Phase 171 R1C k=3 gap diagnostics from an existing audit.json.

The tool does not rerun proof search, alter database entries, or certify proofs.
It reports the three observed incomplete registered goals without changing Git.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
```

## 定数の変更後全文（import の直後に配置）

```python
EXPECTED_HEAD = "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
REVIEWED_CURRENT_HEAD = "30c6c5eec6c3a4bbea8ffe0fd5d84e1f600e6f33"
ALLOWED_WORKTREE_HEADS = frozenset({EXPECTED_HEAD, REVIEWED_CURRENT_HEAD})
EXPECTED_BRANCH = "develop"
EXPECTED_STEM = 3
EXPECTED_DOMAIN_SIZE = 32
EXPECTED_INCOMPLETE = (3, 4, 5)
ACCEPTED_RESULTS = frozenset({
    "COMPLETE_AND_WEB_VERIFIED",
    "PROOF_UNFINISHED",
    "TYPED_TARGET_UNAVAILABLE",
    "CONCLUSION_MISMATCH",
    "WEB_UNVERIFIED",
    "WORKER_FAILURE",
})
DIAGNOSTIC_FIELDS = (
    "target_typed", "target_type", "target_coordinates",
    "search_status", "proven_steps", "open_goals", "open_goal_samples",
    "diagnostics", "search_complete", "root_conclusion_matches_target",
    "web_key", "web_partial", "web_steps", "web_lines", "web_error",
    "exception", "traceback",
)
```

## `tracked_state()` 全文（同名の既存関数を置換）

```python
def tracked_state(root: Path) -> dict:
    """Reject a changed production tree; ignore untracked audit directories."""
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    origin = git(root, "rev-parse", "--verify", "refs/remotes/origin/develop")
    if branch != EXPECTED_BRANCH or head not in ALLOWED_WORKTREE_HEADS or origin != head:
        raise RuntimeError(f"unexpected Git state: {branch}, {head}, {origin}")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked files have uncommitted changes")
    diff = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if diff.returncode:
        raise RuntimeError("could not inspect tracked diff")
    return {"branch": branch, "head": head, "origin_develop": origin,
            "tracked_digest": sha256(diff.stdout).hexdigest(), "tracked_clean": True}
```

## `tests/test_triage.py` の import 全文

```python
"""Focused read-only R1D report extraction tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase171_r1d_k3_three_gap_diagnostics import triage
```

## 新規テスト関数全文（ファイル末尾へ追加）

```python
def test_tracked_state_accepts_both_reviewed_clean_heads(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A post-audit commit may add audit files without invalidating the old report."""
    import subprocess

    for head in (triage.EXPECTED_HEAD, triage.REVIEWED_CURRENT_HEAD):
        def git_result(root: Path, *args: str) -> str:
            commands = {
                ("branch", "--show-current"): "develop",
                ("rev-parse", "HEAD"): head,
                ("rev-parse", "--verify", "refs/remotes/origin/develop"): head,
                ("status", "--porcelain", "--untracked-files=no"): "",
            }
            return commands[args]

        monkeypatch.setattr(triage, "git", git_result)
        monkeypatch.setattr(
            subprocess, "run", lambda *a, **kw:
            subprocess.CompletedProcess(args=a, returncode=0, stdout=b"", stderr=b""),
        )
        state = triage.tracked_state(tmp_path)
        assert state["head"] == head
        assert state["origin_develop"] == head
        assert state["tracked_clean"] is True
```

```python
def test_tracked_state_rejects_unreviewed_head(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    unreviewed = "f" * 40
    def git_result(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        return unreviewed
    monkeypatch.setattr(triage, "git", git_result)
    with pytest.raises(RuntimeError, match="unexpected Git state"):
        triage.tracked_state(tmp_path)
```

```python
def test_tracked_state_rejects_origin_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    def git_result(root: Path, *args: str) -> str:
        commands = {
            ("branch", "--show-current"): "develop",
            ("rev-parse", "HEAD"): triage.REVIEWED_CURRENT_HEAD,
            ("rev-parse", "--verify", "refs/remotes/origin/develop"): triage.EXPECTED_HEAD,
        }
        return commands[args]
    monkeypatch.setattr(triage, "git", git_result)
    with pytest.raises(RuntimeError, match="unexpected Git state"):
        triage.tracked_state(tmp_path)
```

```python
def test_tracked_state_rejects_modified_tracked_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    def git_result(root: Path, *args: str) -> str:
        commands = {
            ("branch", "--show-current"): "develop",
            ("rev-parse", "HEAD"): triage.REVIEWED_CURRENT_HEAD,
            ("rev-parse", "--verify", "refs/remotes/origin/develop"): triage.REVIEWED_CURRENT_HEAD,
            ("status", "--porcelain", "--untracked-files=no"): " M web_group_proof.py",
        }
        return commands[args]
    monkeypatch.setattr(triage, "git", git_result)
    with pytest.raises(RuntimeError, match="tracked files"):
        triage.tracked_state(tmp_path)
```

```python
def test_old_r1c_report_head_remains_pinned_after_git_review_update() -> None:
    assert triage.EXPECTED_HEAD != triage.REVIEWED_CURRENT_HEAD
    assert triage.validate_report(sample_report())
    report = sample_report()
    report["preflight"]["head"] = triage.REVIEWED_CURRENT_HEAD
    with pytest.raises(ValueError, match="unexpected reviewed HEAD"):
        triage.validate_report(report)
```

## 動作検証

- R1C に記録された 715b00d6 の HEAD は監査証拠として固定したまま。
- 30c6c5ee を新たな現在の Git HEAD として厳密に許可。
- `origin/develop` の不一致、未知の HEAD、追跡済みファイルの変更を拒否。
- 既存の `audit.json` からだけ詳細を抽出し、推論規則と Proof Tree は不変更。
- `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider phase171_r1d_k3_three_gap_diagnostics/tests/test_triage.py` で限定テスト。全体 pytest は Phase 終了時のみ。
- R1D-R2 の次は未完成3群の監査結果から R2 の数学的修正候補を決める。R1D-R2 は修正しない。
