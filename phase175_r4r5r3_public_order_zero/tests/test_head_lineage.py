"""R4R5R3R1: only reviewed R4R5R2 lineage may advance the pinned HEAD."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

import pytest

from phase175_r4r5r3_public_order_zero import audit


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=True,
    ).stdout.strip()


def commit(root: Path, message: str) -> None:
    git(root, "add", ".")
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.com",
        "commit", "-qm", message)


def prepared_repository(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, str]:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    (root / "baseline.txt").write_text("reviewed baseline\n", encoding="utf-8")
    commit(root, "reviewed source")
    old_head = git(root, "rev-parse", "HEAD")
    monkeypatch.setattr(audit, "EXPECTED_HEAD", old_head)
    return root, old_head


def reviewed_rule(root: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = root / audit.PRIOR_PACKAGE / "rule.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = b"original reviewed general rule\n"
    path.write_bytes(payload)
    monkeypatch.setattr(audit, "PRIOR_RULE_SHA256", hashlib.sha256(payload).hexdigest())
    return path


def test_exact_reviewed_head_does_not_require_new_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, old_head = prepared_repository(tmp_path, monkeypatch)
    assert audit.reviewed_head_lineage(root) == {
        "current_head": old_head, "intervening_paths": [],
    }


def test_reviewed_r4r5r2_commit_is_accepted_and_recorded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, old_head = prepared_repository(tmp_path, monkeypatch)
    rule = reviewed_rule(root, monkeypatch)
    (rule.parent / "README.md").write_text("audit\n", encoding="utf-8")
    commit(root, "175-4-5")
    current = git(root, "rev-parse", "HEAD")
    assert current != old_head
    result = audit.source_guard(root)
    assert result["reviewed_head"] == current
    assert result["reviewed_base_head"] == old_head
    assert result["reviewed_intervening_paths"] == [
        audit.PRIOR_PACKAGE + "/README.md", audit.PRIOR_PACKAGE + "/rule.py",
    ]


@pytest.mark.parametrize("stray", [
    "phase165_r52_r9_shared_math.py",
    "phase175_r4r5_eta7_annihilator_isolated_fake/rule.py",
    "other/README.md",
])
def test_unrelated_committed_change_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, stray: str,
) -> None:
    root, _ = prepared_repository(tmp_path, monkeypatch)
    reviewed_rule(root, monkeypatch)
    path = root / stray
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("changed\n", encoding="utf-8")
    commit(root, "unauthorized unrelated edit")
    with pytest.raises(RuntimeError, match="R4R5R3_UNREVIEWED_HEAD_CHANGES"):
        audit.source_guard(root)


def test_unrelated_non_descendant_head_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, old_head = prepared_repository(tmp_path, monkeypatch)
    rule = reviewed_rule(root, monkeypatch)
    commit(root, "new reviewed package")
    monkeypatch.setattr(audit, "EXPECTED_HEAD", "0" * 40)
    with pytest.raises(RuntimeError, match="R4R5R3_UNREVIEWED_HEAD"):
        audit.source_guard(root)
    assert old_head != "0" * 40


def test_reviewed_package_rule_byte_drift_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _ = prepared_repository(tmp_path, monkeypatch)
    rule = reviewed_rule(root, monkeypatch)
    commit(root, "reviewed package")
    rule.write_bytes(b"tampered rule\n")
    with pytest.raises(RuntimeError, match="R4R5R3_R4R5R2_RULE_DRIFT"):
        audit.source_guard(root)


def test_inherited_reviewed_commit_does_not_waive_production_blob_pin() -> None:
    from phase175_r4r5r3_public_order_zero import installer
    assert installer.TARGET_RELATIVE.as_posix() == "phase165_r52_r9_shared_math.py"
    assert len(installer.PINNED_GIT_BLOB) == 40
    assert "R4R5R3_PRODUCTION_SOURCE_BLOB_CHANGED" in (
        installer.plan.__code__.co_consts
    )
