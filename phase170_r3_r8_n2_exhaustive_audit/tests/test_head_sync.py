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
