"""R5C exercises the reviewed-R4 precondition with a synthetic Git state."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase169_r10et_r5c_preserve_staged_r5 import run
from phase169_r10et_r5c_preserve_staged_r5.patch import git_blob


def test_r5b_only_two_explicitly_reviewed_heads():
    assert run.REVIEWED_HEADS == (
        "5a8ad4a56c5407c0fbe15ba14516a1c1a99f0562",
        "3a8014efb91ddf76060c4d07d73153e55ea52c75",
    )
    assert run.BASE_HEAD != run.R4_COMMITTED_HEAD


def test_r5b_preserves_exact_reviewed_r4_target_set():
    assert set(run.R4_TARGETS) == {
        "phase169_r10a_verified_stable_chain_projection/projection.py",
        "phase168_r3_5_model_renderer.py",
    }


@pytest.mark.parametrize("committed", (False, True))
def test_r5b_accepts_only_verified_r4_bytes_in_both_git_states(
    tmp_path, monkeypatch, committed,
):
    from phase169_r10et_r4_cyclic_definition_projection import patch as r4_patch

    file_name = "reviewed_r4_source.py"
    provider = "reviewed_r5_target.py"
    r4_before = b"def f():\n    return 1\n"
    r4_after = b"def f():\n    return 2\n"
    r5_input = b"def provider():\n    return 1\n"
    (tmp_path / file_name).write_bytes(r4_after)
    (tmp_path / provider).write_bytes(r5_input)

    head = run.R4_COMMITTED_HEAD if committed else run.BASE_HEAD
    expected_dirty = set() if committed else {file_name}
    monkeypatch.setattr(run, "R4_TARGETS", (file_name,))
    monkeypatch.setattr(run, "EXPECTED_BLOBS", {provider: git_blob(r5_input)})
    monkeypatch.setattr(
        r4_patch, "EXPECTED_GIT_BLOBS", {file_name: git_blob(r4_before)},
    )
    monkeypatch.setattr(
        r4_patch, "transformed", lambda before, name: (r4_after, "def f():\n    return 2\n"),
    )

    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return head
        if args == ("diff", "--name-only"):
            return file_name if not committed else ""
        if args == ("diff", "--cached", "--name-status"):
            return ""
        if args == ("diff", "--cached", "--raw"):
            return ""
        raise AssertionError(args)

    def fake_git_bytes(root, path):
        return r4_after if path == file_name else r5_input

    def fake_run(args, **kwargs):
        assert args[-1] == f"{run.BASE_HEAD}:{file_name}"
        return SimpleNamespace(stdout=r4_before)

    monkeypatch.setattr(run, "git", fake_git)
    monkeypatch.setattr(run, "git_bytes", fake_git_bytes)
    monkeypatch.setattr(run.subprocess, "run", fake_run)
    assert run.verify_preconditions(tmp_path) == (head, expected_dirty)


@pytest.mark.parametrize("failure", ("unknown_head", "wrong_r4", "unexpected_diff"))
def test_r5b_fails_closed_on_unreviewed_inputs(tmp_path, monkeypatch, failure):
    from phase169_r10et_r4_cyclic_definition_projection import patch as r4_patch

    file_name = "reviewed_r4_source.py"
    provider = "reviewed_r5_target.py"
    r4_before = b"def f():\n    return 1\n"
    r4_after = b"def f():\n    return 2\n"
    r5_input = b"def provider():\n    return 1\n"
    (tmp_path / file_name).write_bytes(
        r4_after if failure != "wrong_r4" else b"unreviewed source"
    )
    (tmp_path / provider).write_bytes(r5_input)
    monkeypatch.setattr(run, "R4_TARGETS", (file_name,))
    monkeypatch.setattr(run, "EXPECTED_BLOBS", {provider: git_blob(r5_input)})
    monkeypatch.setattr(
        r4_patch, "EXPECTED_GIT_BLOBS", {file_name: git_blob(r4_before)},
    )
    monkeypatch.setattr(
        r4_patch, "transformed", lambda before, name: (r4_after, "complete function"),
    )

    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "other" if failure == "unknown_head" else run.R4_COMMITTED_HEAD
        if args == ("diff", "--name-only"):
            return "another_file.py" if failure == "unexpected_diff" else ""
        if args == ("diff", "--cached", "--name-status"):
            return ""
        if args == ("diff", "--cached", "--raw"):
            return ""
        raise AssertionError(args)

    monkeypatch.setattr(run, "git", fake_git)
    monkeypatch.setattr(run, "git_bytes", lambda root, path: r4_after if path == file_name else r5_input)
    monkeypatch.setattr(
        run.subprocess, "run", lambda args, **kwargs: SimpleNamespace(stdout=r4_before),
    )
    with pytest.raises(RuntimeError, match="unreviewed HEAD|R4 implementation differs|unexpected tracked changes"):
        run.verify_preconditions(tmp_path)


def test_r5c_allows_exact_reviewed_staged_r5_additions(monkeypatch, tmp_path):
    names = sorted(run.REVIEWED_STAGED_R5)
    calls = []

    def fake_git(root, *args):
        calls.append(args)
        if args == ("diff", "--cached", "--name-status"):
            return "\n".join("A\t" + name for name in names)
        if args == ("diff", "--cached", "--raw"):
            return "reviewed immutable raw staged fingerprint"
        raise AssertionError(args)

    monkeypatch.setattr(run, "git", fake_git)
    assert run.reviewed_index_snapshot(tmp_path) == (
        "reviewed immutable raw staged fingerprint"
    )
    assert len(calls) == 2


@pytest.mark.parametrize("change", (
    "M\tphase169_r10et_r5_common_definition_provider/audit.py",
    "A\tphase165_r52_r9_shared_math.py",
    "A\tunrelated/package.txt",
))
def test_r5c_rejects_other_staged_paths_or_modifications(monkeypatch, tmp_path, change):
    monkeypatch.setattr(run, "git", lambda root, *args: change)
    with pytest.raises(RuntimeError, match="unreviewed staged"):
        run.reviewed_index_snapshot(tmp_path)


def test_r5c_rejects_partial_staged_package(monkeypatch, tmp_path):
    one = sorted(run.REVIEWED_STAGED_R5)[0]
    monkeypatch.setattr(run, "git", lambda root, *args: "A\t" + one)
    with pytest.raises(RuntimeError, match="unreviewed staged paths"):
        run.reviewed_index_snapshot(tmp_path)


def test_r5c_accepts_no_staging(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args in (("diff", "--cached", "--name-status"), ("diff", "--cached", "--raw")):
            return ""
        raise AssertionError(args)

    monkeypatch.setattr(run, "git", fake_git)
    assert run.reviewed_index_snapshot(tmp_path) == ""
