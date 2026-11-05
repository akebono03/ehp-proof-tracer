"""Focused regression tests for the reviewed post-R3-R4 HEAD transition."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r5_finite_cyclic_extension import patch


REVIEWED_CHANGED_PATHS = (
    "phase174_r3_r5_preflight/README.md",
    "phase174_r3_r5_preflight/__init__.py",
    "phase174_r3_r5_preflight/audit.py",
    "phase174_r3_r5_preflight/run.ps1",
    "phase174_r3_r5_preflight/tests/__init__.py",
    "phase174_r3_r5_preflight/tests/test_audit.py",
    "phase174_r3_r5_preflight/実装前監査.md",
)


def reviewed_git_output(*, remote: str | None = None, changed: tuple[str, ...] = REVIEWED_CHANGED_PATHS):
    """Return a controlled git responder; do not alter the real repository."""
    shared = b"reviewed synthetic shared provider"
    preflight = b"reviewed synthetic committed preflight"
    test = b"reviewed synthetic test"
    remote_head = patch.REVIEWED_HEAD if remote is None else remote
    responses = {
        ("rev-parse", "HEAD"): patch.REVIEWED_HEAD.encode(),
        ("branch", "--show-current"): b"develop\n",
        ("ls-remote", "origin", "refs/heads/develop"):
            (remote_head + "\trefs/heads/develop\n").encode(),
        ("merge-base", "--is-ancestor", patch.BASE_COMMIT, patch.REVIEWED_HEAD): b"",
        ("-c", "core.quotePath=false", "diff", "--name-only",
         patch.BASE_COMMIT + ".." + patch.REVIEWED_HEAD):
            ("\n".join(changed) + "\n").encode("utf-8"),
        ("show", "HEAD:" + patch.SHARED): shared,
        ("show", "HEAD:" + patch.TEST): test,
        ("show", "HEAD:" + patch.PREFLIGHT): preflight,
        ("diff", "--cached", "--name-only"): b"",
    }

    def fake_git(*args: str) -> bytes:
        return responses[args]

    return fake_git, shared, preflight, test


def test_reviewed_head_accepts_only_preflight_commit(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_git, shared, preflight, test = reviewed_git_output()
    monkeypatch.setattr(patch, "git", fake_git)
    monkeypatch.setattr(patch, "SHARED_BLOB", patch.blob_sha(shared))
    monkeypatch.setattr(patch, "PREFLIGHT_COMMITTED_BLOB", patch.blob_sha(preflight))
    assert patch.verify_originals() == (shared, test)


def test_changed_remote_head_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_git, shared, preflight, test = reviewed_git_output(remote="0" * 40)
    monkeypatch.setattr(patch, "git", fake_git)
    with pytest.raises(ValueError, match="Reviewed develop HEAD mismatch"):
        patch.verify_originals()


def test_unreviewed_commit_path_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_git, shared, preflight, test = reviewed_git_output(
        changed=REVIEWED_CHANGED_PATHS + ("unrelated.py",)
    )
    monkeypatch.setattr(patch, "git", fake_git)
    with pytest.raises(ValueError, match="Unexpected files changed"):
        patch.verify_originals()


def test_preflight_replacement_is_exact_idempotent_and_rejects_edits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base = Path(__file__).resolve().parents[2] / patch.PREFLIGHT
    # The committed original is loaded from git instead of trusting the current
    # working tree, which may already contain the narrowly reviewed update.
    from subprocess import run
    committed = run(
        ("git", "show", "HEAD:" + patch.PREFLIGHT),
        check=True, capture_output=True,
    ).stdout
    if patch.blob_sha(committed) != patch.PREFLIGHT_COMMITTED_BLOB:
        pytest.fail("Reviewed preflight original changed at HEAD")
    updated = patch.replace_preflight_provider_guard(committed)
    assert updated != committed
    assert patch.replace_preflight_provider_guard(updated) == updated
    with pytest.raises(ValueError, match="Refusing unrelated edit"):
        patch.replace_preflight_provider_guard(committed + b"# unrelated edit\n")


def test_unicode_path_from_real_git_is_not_octal_quoted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Guard compares literal UTF-8 paths, never Git's C-quoted names.

    Exercise a real temporary Git repository, not just a mocked Git reply.
    No files in the user's EHP repository are written by this test.
    """
    import subprocess

    def run(*args: str) -> bytes:
        return subprocess.run(
            ("git",) + args,
            check=True, cwd=tmp_path, capture_output=True,
        ).stdout

    run("init", "-q")
    run("-c", "user.name=EHP Test", "-c", "user.email=ehp@example.invalid",
        "commit", "-q", "--allow-empty", "-m", "initial")
    base = run("rev-parse", "HEAD").decode("ascii").strip()
    path = "phase174_r3_r5_preflight/実装前監査.md"
    file = tmp_path / path
    file.parent.mkdir(parents=True)
    file.write_text("source verified\n", encoding="utf-8")
    run("add", "--", path)
    run("-c", "user.name=EHP Test", "-c", "user.email=ehp@example.invalid",
        "commit", "-q", "-m", "add Japanese audit file")

    monkeypatch.chdir(tmp_path)
    reviewed_paths = patch.git(
        "-c", "core.quotePath=false", "diff", "--name-only",
        base + "..HEAD",
    ).decode("utf-8").splitlines()
    assert reviewed_paths == [path]
