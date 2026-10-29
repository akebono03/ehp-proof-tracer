# Phase 170 R3-R8 HEAD 同期修正 — 変更コード全文

## 変更ファイル・関数

- `phase170_r3_r8_n2_exhaustive_audit/audit.py`: `phase170_r3r8_preflight()`（関数全文と関連定数）
- `phase170_r3_r8_n2_exhaustive_audit/tests/test_head_sync.py`: 新規テストファイル（全文）。既存テストは変更しない。
- `phase170_r3_r8_n2_exhaustive_audit/README.md`: 現在の HEAD の説明（英語）。
- `phase170_r3_r8_n2_exhaustive_audit/DESIGN_JA.md`: R3-R7 コミット済み状態への対応記録（日本語）。

本体の production コード、関数、クラス、import、既存テスト、DB は**変更しない**。`audit.py` の import も**変更なし**。新規クラスもない。新規テスト関数は `test_head_sync.py` に置く。

## 更新した関連定数

```python
REVIEWED_HEAD_UNCOMMITTED = "84a9d8ad6110ed82b80bdeb7e9a0c5a361214de0"
REVIEWED_HEAD_COMMITTED = "f479e0aabdfeefa69ad986e20c0f69ce0efd7bbd"
REVIEWED_GIT_BLOB_BEFORE_R3R7 = "b3e104857e3a8129fb01df65ce3a38ff188ecd1f"
REVIEWED_GIT_BLOB_AFTER_R3R7 = "3bf9dfa2080e330e7030f0f0a7762f3fb1fa8fff"
REVIEWED_R3R7_FILE_SHA256 = "d2dcaab3dd6555c0b998f73835ed792ff405479c73a8687ae2accb04de638f73"
TARGET = "phase168_r2_toda52_transport.py"
```

## `phase170_r3r8_preflight()` の全文

```python
def phase170_r3r8_preflight(root: Path) -> dict:
    """Accept only byte-verified R3-R7, whether committed or uncommitted."""
    branch, head = git(root, "branch", "--show-current"), git(root, "rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError(f"unreviewed branch: {branch}")
    if head == REVIEWED_HEAD_UNCOMMITTED:
        expected_blob = REVIEWED_GIT_BLOB_BEFORE_R3R7
        expected_changes = [TARGET]
        installation = "R3R7_UNCOMMITTED"
    elif head == REVIEWED_HEAD_COMMITTED:
        expected_blob = REVIEWED_GIT_BLOB_AFTER_R3R7
        expected_changes = []
        installation = "R3R7_COMMITTED"
    else:
        raise RuntimeError(f"unreviewed branch or HEAD: {branch} {head}")
    if git(root, "rev-parse", f"HEAD:{TARGET}") != expected_blob:
        raise RuntimeError("committed source blob differs from reviewed version")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("staged tracked changes present")
    changes = git(root, "diff", "--name-only").splitlines()
    if changes != expected_changes:
        raise RuntimeError(f"unexpected tracked changes: {changes!r}")
    actual_sha = sha256((root / TARGET).read_bytes()).hexdigest()
    if actual_sha != REVIEWED_R3R7_FILE_SHA256:
        raise RuntimeError(f"R3-R7 source bytes differ: {actual_sha}")
    for relative in (
        "phase170_r3_r6_prop58_source.py",
        "phase169_r10e4_ordered_db_prior/db_prior.py",
        "phase168_r3_41p13_trust_boundary/verification.py",
        "web_group_proof.py",
        "data/sphere.csv",
        "data/HyoujiGen.csv",
    ):
        if not (root / relative).is_file():
            raise RuntimeError(f"required reviewed source missing: {relative}")
    return {
        "branch": branch,
        "head": head,
        "installation": installation,
        "r3r7_source_sha256": actual_sha,
        "tracked_changed_paths": changes,
    }
```

## 新規テストファイルの全文（import を含む）

```python
"""R3-R8 preflight: reviewed committed and uncommitted R3-R7 states."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase170_r3_r8_n2_exhaustive_audit import audit


@pytest.fixture
def reviewed_root(tmp_path: Path) -> Path:
    source = (Path(__file__).resolve().parents[2]
              / "phase170_r3_r7_toda52_ordered_db_transport"
              / "replacement" / "phase168_r2_toda52_transport.py")
    target = tmp_path / audit.TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    for name in (
        "phase170_r3_r6_prop58_source.py",
        "phase169_r10e4_ordered_db_prior/db_prior.py",
        "phase168_r3_41p13_trust_boundary/verification.py",
        "web_group_proof.py",
        "data/sphere.csv",
        "data/HyoujiGen.csv",
    ):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"reviewed fixture")
    return tmp_path


def stub_git(monkeypatch: pytest.MonkeyPatch, *, head: str,
             changed: str, blob: str, staged: str = "", branch: str = "develop") -> None:
    responses = {
        ("branch", "--show-current"): branch,
        ("rev-parse", "HEAD"): head,
        ("rev-parse", f"HEAD:{audit.TARGET}"): blob,
        ("diff", "--cached", "--name-only"): staged,
        ("diff", "--name-only"): changed,
    }

    def replacement(_root: Path, *args: str) -> str:
        return responses[args]

    monkeypatch.setattr(audit, "git", replacement)


def test_committed_r3r7_clean_worktree_is_accepted(
    reviewed_root: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub_git(monkeypatch, head=audit.REVIEWED_HEAD_COMMITTED, changed="",
             blob=audit.REVIEWED_GIT_BLOB_AFTER_R3R7)
    result = audit.phase170_r3r8_preflight(reviewed_root)
    assert result["installation"] == "R3R7_COMMITTED"
    assert result["tracked_changed_paths"] == []
    assert result["r3r7_source_sha256"] == audit.REVIEWED_R3R7_FILE_SHA256


def test_original_r3r7_uncommitted_worktree_is_accepted(
    reviewed_root: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub_git(monkeypatch, head=audit.REVIEWED_HEAD_UNCOMMITTED,
             changed=audit.TARGET, blob=audit.REVIEWED_GIT_BLOB_BEFORE_R3R7)
    result = audit.phase170_r3r8_preflight(reviewed_root)
    assert result["installation"] == "R3R7_UNCOMMITTED"
    assert result["tracked_changed_paths"] == [audit.TARGET]


def test_unreviewed_head_still_rejected(
    reviewed_root: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub_git(monkeypatch, head="0" * 40, changed="",
             blob=audit.REVIEWED_GIT_BLOB_AFTER_R3R7)
    with pytest.raises(RuntimeError, match="unreviewed branch or HEAD"):
        audit.phase170_r3r8_preflight(reviewed_root)


def test_unreviewed_branch_still_rejected(
    reviewed_root: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub_git(monkeypatch, head=audit.REVIEWED_HEAD_COMMITTED,
             changed="", branch="main", blob=audit.REVIEWED_GIT_BLOB_AFTER_R3R7)
    with pytest.raises(RuntimeError, match="unreviewed branch"):
        audit.phase170_r3r8_preflight(reviewed_root)


def test_wrong_git_blob_still_rejected(
    reviewed_root: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub_git(monkeypatch, head=audit.REVIEWED_HEAD_COMMITTED,
             changed="", blob="0" * 40)
    with pytest.raises(RuntimeError, match="committed source blob differs"):
        audit.phase170_r3r8_preflight(reviewed_root)


def test_committed_r3r7_with_tracked_change_still_rejected(
    reviewed_root: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub_git(monkeypatch, head=audit.REVIEWED_HEAD_COMMITTED,
             changed=audit.TARGET, blob=audit.REVIEWED_GIT_BLOB_AFTER_R3R7)
    with pytest.raises(RuntimeError, match="unexpected tracked changes"):
        audit.phase170_r3r8_preflight(reviewed_root)


def test_staged_changes_still_rejected(
    reviewed_root: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub_git(monkeypatch, head=audit.REVIEWED_HEAD_COMMITTED,
             changed="", staged=audit.TARGET, blob=audit.REVIEWED_GIT_BLOB_AFTER_R3R7)
    with pytest.raises(RuntimeError, match="staged tracked changes"):
        audit.phase170_r3r8_preflight(reviewed_root)


def test_changed_r3r7_bytes_still_rejected(
    reviewed_root: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub_git(monkeypatch, head=audit.REVIEWED_HEAD_COMMITTED,
             changed="", blob=audit.REVIEWED_GIT_BLOB_AFTER_R3R7)
    (reviewed_root / audit.TARGET).write_bytes(b"not the reviewed source")
    with pytest.raises(RuntimeError, match="source bytes differ"):
        audit.phase170_r3r8_preflight(reviewed_root)
```

## 検証

独立限定テスト：`16 passed`（既存8＋新規8）。GitHub `develop` HEAD `f479e0aabdfeefa69ad986e20c0f69ce0efd7bbd` を実際に照合し、R3-R7 のコミット済み source blob `3bf9dfa2080e330e7030f0f0a7762f3fb1fa8fff` と旧 source ファイルの SHA-256 `d2dcaab3dd6555c0b998f73835ed792ff405479c73a8687ae2accb04de638f73` が対応することを確認した。

### 実際に実行する限定 pytest

`python -m pytest -q phase170_r3_r8_n2_exhaustive_audit/tests/test_audit_contract.py phase170_r3_r8_n2_exhaustive_audit/tests/test_head_sync.py`

監査は `python -B phase170_r3_r8_n2_exhaustive_audit/audit.py` を使用し、`run.ps1` から全登録ステムを検索する。全体 pytest は行わない。

## Phase 境界

R3-R8 は監査限定。R3-R7 の証明生成、Toda (5.2)、先行 DB 利用、Trust Boundary の実装には手を加えない。全件監査結果を確認するまでは、$n=2$ 全登録範囲の完成を主張しない。
