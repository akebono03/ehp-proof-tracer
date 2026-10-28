"""R10ET closeout R1 focused, non-repository-modifying contract tests."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

from phase169_r10et_closeout_r1_sync_guard.audit import (
    REVIEWED_GITHUB_HEAD, decision, git_blob_map, remote_sha,
)


def test_remote_parser_accepts_only_exact_develop_reference():
    line = REVIEWED_GITHUB_HEAD + "\trefs/heads/develop\n"
    assert remote_sha(line) == REVIEWED_GITHUB_HEAD
    assert remote_sha(REVIEWED_GITHUB_HEAD + "\trefs/heads/main") is None
    assert remote_sha("garbage") is None


def test_ready_requires_clean_synced_verified_tree():
    assert decision(head=REVIEWED_GITHUB_HEAD, remote=REVIEWED_GITHUB_HEAD,
                    status=[], source_matches=True, document_matches=True) == (
                        "READY_FOR_DOCUMENT_CLOSEOUT")


def test_old_head_with_changes_is_never_auto_updated():
    assert decision(head="2" * 40, remote=REVIEWED_GITHUB_HEAD,
                    status=[" M local.py"], source_matches=True,
                    document_matches=True) == "SYNC_REQUIRED_PRESERVE_LOCAL_CHANGES"


def test_unknown_remote_refuses_document_closeout():
    assert decision(head=REVIEWED_GITHUB_HEAD, remote=None, status=[],
                    source_matches=True, document_matches=True) == "REMOTE_UNVERIFIED_NO_CHANGES"


def test_source_drift_or_remote_change_requires_review():
    assert decision(head=REVIEWED_GITHUB_HEAD, remote=REVIEWED_GITHUB_HEAD,
                    status=[], source_matches=False, document_matches=True) == "WORKTREE_CONTENT_REVIEW_REQUIRED"
    assert decision(head=REVIEWED_GITHUB_HEAD, remote="1" * 40,
                    status=[], source_matches=True, document_matches=True) == "REMOTE_ADVANCED_REVIEW_NEW_HEAD"


def test_git_blob_map_reads_without_writing_objects(tmp_path: Path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    f = tmp_path / "hello.txt"
    f.write_bytes(b"test content\n")
    content = b"test content\n"
    expected = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
    assert git_blob_map(tmp_path, {"hello.txt": expected}) == {"hello.txt": expected}
    assert not (tmp_path / ".git" / "index").exists()
