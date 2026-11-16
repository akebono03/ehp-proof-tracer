"""R3R6R2 regression: only explicit audit additions may extend R2 history."""
from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from phase175_r3r6_lemma57_general import audit


def git(repo: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True,
        text=True, encoding="utf-8", check=False,
    )
    assert process.returncode == 0, process.stderr
    return process.stdout.strip()


def commit(repo: Path, name: str) -> str:
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=EHP Audit Test", "-c", "user.email=test@example.invalid",
        "commit", "-q", "-m", name)
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def reviewed_history(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "audit-repo"
    repo.mkdir()
    git(repo, "init", "-q")
    (repo / "baseline.txt").write_text("unchanged production code\n", encoding="utf-8")
    old = commit(repo, "reviewed R2 checkpoint")
    return repo, old


def record(repo: Path, old: str) -> tuple[dict[str, object], dict[str, object]]:
    return ({"preflight": {"head": old}}, {"head": git(repo, "rev-parse", "HEAD")})


@pytest.mark.parametrize("added", [
    "phase175_r2_k4_frontier_audit/audit.py",
    "phase175_r3_pi73_hopf_lift/audit.py",
    "phase175_r3r5_pi73_lemma57_frontier/audit.py",
    "phase175_r3r6_lemma57_general/audit.py",
    "phase175_r3r6_lemma57_general/tests/test_lineage.py",
])
def test_only_reviewed_audit_additions_allowed(reviewed_history, added: str) -> None:
    repo, old = reviewed_history
    path = repo / added
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("isolated audit only\n", encoding="utf-8")
    commit(repo, "add reviewed audit file")
    previous, checked = record(repo, old)
    evidence = audit.verify_r3r6_lineage(repo, previous, checked)
    assert evidence["mode"] == "AUDIT_ONLY_DESCENDANT"
    assert evidence["audit_only_paths"] == [added]
    if added.startswith("phase175_r3r5_"):
        assert evidence["r3r5_added_paths"] == [added]
    if added.startswith("phase175_r3r6_"):
        assert evidence["r3r6_added_paths"] == [added]


@pytest.mark.parametrize("path", [
    "src/proof.py",
    "phase175_r3r5_pi73_lemma57_frontier/unreviewed.py",
    "phase175_r3r6_lemma57_general/unreviewed.py",
])
def test_unreviewed_additions_rejected(reviewed_history, path: str) -> None:
    repo, old = reviewed_history
    file = repo / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text("unexpected change\n", encoding="utf-8")
    commit(repo, "unexpected added file")
    previous, checked = record(repo, old)
    with pytest.raises(RuntimeError, match="R3R6_LINEAGE_NOT_AUDIT_ONLY"):
        audit.verify_r3r6_lineage(repo, previous, checked)


def test_modified_production_file_rejected(reviewed_history) -> None:
    repo, old = reviewed_history
    (repo / "baseline.txt").write_text("production modified\n", encoding="utf-8")
    commit(repo, "modify production")
    previous, checked = record(repo, old)
    with pytest.raises(RuntimeError, match="R3R6_LINEAGE_NOT_AUDIT_ONLY"):
        audit.verify_r3r6_lineage(repo, previous, checked)


def test_removed_file_rejected(reviewed_history) -> None:
    repo, old = reviewed_history
    (repo / "baseline.txt").unlink()
    commit(repo, "remove production")
    previous, checked = record(repo, old)
    with pytest.raises(RuntimeError, match="R3R6_LINEAGE_NOT_AUDIT_ONLY"):
        audit.verify_r3r6_lineage(repo, previous, checked)


def test_relocation_cannot_be_treated_as_addition(reviewed_history) -> None:
    repo, old = reviewed_history
    destination = repo / "phase175_r3r5_pi73_lemma57_frontier" / "audit.py"
    destination.parent.mkdir(parents=True)
    (repo / "baseline.txt").rename(destination)
    commit(repo, "relocate original file")
    previous, checked = record(repo, old)
    with pytest.raises(RuntimeError, match="R3R6_LINEAGE_NOT_AUDIT_ONLY"):
        audit.verify_r3r6_lineage(repo, previous, checked)


def test_unchanged_head_is_allowed(reviewed_history) -> None:
    repo, old = reviewed_history
    previous, checked = record(repo, old)
    assert audit.verify_r3r6_lineage(repo, previous, checked)["mode"] == "SAME_HEAD"


def test_fake_checked_head_rejected(reviewed_history) -> None:
    repo, old = reviewed_history
    previous, checked = record(repo, old)
    checked["head"] = "0" * 40
    with pytest.raises(RuntimeError, match="R3R6_UNVERIFIED_GIT_HEAD"):
        audit.verify_r3r6_lineage(repo, previous, checked)
