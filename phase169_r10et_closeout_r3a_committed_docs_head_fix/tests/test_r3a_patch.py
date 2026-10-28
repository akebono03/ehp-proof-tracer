"""Focused non-mutating tests of the R3A exact-source audit patch."""
from __future__ import annotations

import hashlib
from pathlib import Path
from types import ModuleType
import json

import pytest

from phase169_r10et_closeout_r2_documentation.update_docs import REVIEWED_SOURCE_BLOBS
from phase169_r10et_closeout_r3a_committed_docs_head_fix.patch import (
    CURRENT_HEAD, OLD_SHA256, PREVIOUS_HEAD, TARGET, patch_bytes, reviewed_patch,
)

PACKAGE = Path(__file__).resolve().parents[1]

def reviewed_original() -> bytes:
    return (PACKAGE / "reviewed_sources" / "r3_audit_BEFORE_FULL.py").read_bytes()

def loaded_module() -> ModuleType:
    module = ModuleType("reviewed_r3a_audit")
    compile_source = patch_bytes(reviewed_original()).decode("utf-8")
    exec(compile(compile_source, TARGET, "exec"), module.__dict__)
    return module

def test_reviewed_original_matches_exact_sha256():
    assert hashlib.sha256(reviewed_original()).hexdigest() == OLD_SHA256

def test_three_guard_changes_only_and_full_output_match():
    updated = patch_bytes(reviewed_original())
    assert updated == (PACKAGE / "reviewed_sources" / "r3_audit_AFTER_FULL.py").read_bytes()
    src = updated.decode("utf-8")
    assert f'REVIEWED_HEAD = "{CURRENT_HEAD}"' in src
    assert f'R2A_MANIFEST_HEAD = "{PREVIOUS_HEAD}"' in src
    assert 'manifest.get("head") != R2A_MANIFEST_HEAD' in src
    assert 'if baseline[1]:' in src
    assert 'if set(baseline[1].splitlines()) != set(DOCUMENT_BLOBS):' not in src

def test_unreviewed_modified_source_is_rejected():
    with pytest.raises(RuntimeError, match="Unreviewed"):
        patch_bytes(reviewed_original() + b"\n# extra\n")

def test_patched_source_is_not_repatched():
    with pytest.raises(RuntimeError, match="Unreviewed"):
        patch_bytes(patch_bytes(reviewed_original()))

def test_reviewed_patch_only_targets_r3_audit(tmp_path: Path):
    target = tmp_path / TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(reviewed_original())
    assert reviewed_patch(tmp_path, PACKAGE) == patch_bytes(reviewed_original())
    assert target.read_bytes() == reviewed_original()

def test_manifest_requires_original_r2a_head(tmp_path: Path, monkeypatch):
    module = loaded_module()
    root = tmp_path / "repo"
    root.mkdir()
    backup = tmp_path / "backup"
    backup.mkdir()
    (backup / "manifest.json").write_text(json.dumps({
        "head": CURRENT_HEAD, "phase_169_closed": False,
        "full_pytest_executed": False, "index_modified": False,
        "documents": [],
    }), encoding="utf-8")
    with pytest.raises(RuntimeError, match="Unexpected R2A backup manifest"):
        module.certify_documents(root, backup)

def test_committed_clean_head_allows_audit_before_evidence(tmp_path: Path, monkeypatch):
    module = loaded_module()
    root = tmp_path / "repo"
    (root / ".git").mkdir(parents=True)
    (root / module.R6_REPORT).parent.mkdir(parents=True)
    (root / module.R6_REPORT).write_text(json.dumps({"cases": []}), encoding="utf-8")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    monkeypatch.setattr(module, "snapshot", lambda path: (CURRENT_HEAD, "", ""))
    monkeypatch.setattr(module, "certify_documents", lambda path, backup: [{"path": "README.md"}])
    monkeypatch.setattr(module, "review_r6_report", lambda report: (16, 3))
    def fake_git(path, *args, **kwargs):
        if args == ("branch", "--show-current"):
            return "develop"
        if args in (("rev-parse", "HEAD"), ("rev-parse", "refs/remotes/origin/develop")):
            return CURRENT_HEAD
        if args == ("ls-remote", "origin", "refs/heads/develop"):
            return CURRENT_HEAD + "\trefs/heads/develop"
        if args[:1] == ("hash-object",):
            return REVIEWED_SOURCE_BLOBS[args[-1]]
        raise AssertionError(args)
    monkeypatch.setattr(module, "git", fake_git)
    assert module.execute(root) == 0
    assert list((tmp_path / "local" / "EHPProofTracerRecovery").glob("r10et_closeout_r3_*/audit.json"))

def test_uncommitted_document_changes_are_rejected(tmp_path: Path, monkeypatch):
    module = loaded_module()
    root = tmp_path / "repo"
    (root / ".git").mkdir(parents=True)
    monkeypatch.setattr(module, "snapshot", lambda path: (CURRENT_HEAD, "README.md", ""))
    def fake_git(path, *args, **kwargs):
        if args == ("branch", "--show-current"):
            return "develop"
        if args in (("rev-parse", "HEAD"), ("rev-parse", "refs/remotes/origin/develop")):
            return CURRENT_HEAD
        if args == ("ls-remote", "origin", "refs/heads/develop"):
            return CURRENT_HEAD + "\trefs/heads/develop"
        raise AssertionError(args)
    monkeypatch.setattr(module, "git", fake_git)
    with pytest.raises(RuntimeError, match="Tracked unstaged changes"):
        module.execute(root)
