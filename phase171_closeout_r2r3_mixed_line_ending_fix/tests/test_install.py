"""Isolated review of the guarded R2R3 historical line-ending patch."""
from __future__ import annotations

import hashlib
from pathlib import Path
import shutil

import pytest

from phase171_closeout_r2r3_mixed_line_ending_fix import install as r


def test_replacement_hashes_and_reviewed_old_sources():
    for relative, asset in r.REPLACEMENTS.items():
        patched = (r.HERE / asset).read_bytes()
        historical = (r.HERE / "reviewed_originals" / relative).read_bytes()
        assert hashlib.sha256(patched).hexdigest() == r.EXPECTED_NEW_SHA256[relative]
        assert hashlib.sha256(historical).hexdigest() == r.REVIEWED_OLD_SHA256[relative]
        assert historical != patched


def test_runner_calls_install_with_real_arguments():
    content = (r.HERE / "run.ps1").read_text(encoding="utf-8")
    assert "& python @Arguments" in content
    assert '"--dry-run"' in content
    assert "@Args\n" not in content


def _fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    root = tmp_path / "repo"
    r2 = root / "phase171_closeout_r2_documentation_full_output"
    for rel in r.REPLACEMENTS:
        path = r2 / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((r.HERE / "reviewed_originals" / rel).read_bytes())
    for name in r.SECTIONS:
        path = r2 / "sections" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((r.HERE / "reviewed_sections" / name).read_bytes())
    (r2 / "run.ps1").write_text("# audit-only mock runner\n", encoding="utf-8")
    old = root / "phase171_closeout_r2r1_committed_head_guard" / "run.ps1"
    old.parent.mkdir(parents=True, exist_ok=True)
    old.write_text("# existing Phase 171 runner\n", encoding="utf-8")
    monkeypatch.setattr(r, "ROOT", root)
    monkeypatch.setattr(r, "R2", r2)

    def fake_git(*args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD") or args == ("rev-parse", "origin/develop"):
            return r.BASE
        if args[:2] == ("rev-parse", "HEAD:" + r.R1R1_TEST):
            return r.TEST_BLOB
        if args[:1] == ("rev-parse",) and args[1].startswith("HEAD:"):
            return r.DOCUMENT_BLOBS[args[1][5:]]
        if args in (("diff", "--cached", "--name-only", "--"),
                    ("diff", "--name-only", "HEAD", "--")):
            return ""
        if args == ("merge-base", "--is-ancestor", r.BASE, "HEAD"):
            return ""
        raise AssertionError(args)

    monkeypatch.setattr(r, "git", fake_git)
    return r2


def test_preflight_accepts_only_reviewed_pair(tmp_path, monkeypatch):
    r2 = _fixture(tmp_path, monkeypatch)
    before, after, already = r.preflight()
    assert not already
    assert len(before) == len(after) == 2
    assert all(before[p] != after[p] for p in before)
    for path, data in after.items():
        path.write_bytes(data)
    _, _, already = r.preflight()
    assert already


def test_preflight_rejects_mixed_patch_state(tmp_path, monkeypatch):
    r2 = _fixture(tmp_path, monkeypatch)
    (r2 / "update_docs.py").write_bytes((r.HERE / r.REPLACEMENTS["update_docs.py"]).read_bytes())
    with pytest.raises(RuntimeError, match="mixed state"):
        r.preflight()


def test_preflight_rejects_unreviewed_document_section(tmp_path, monkeypatch):
    r2 = _fixture(tmp_path, monkeypatch)
    (r2 / "sections" / "design.md").write_text("Changed!\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="reviewed document section"):
        r.preflight()


def test_preflight_rejects_unreviewed_tracked_change(tmp_path, monkeypatch):
    _fixture(tmp_path, monkeypatch)
    original = r.git

    def modified_git(*args):
        if args == ("diff", "--name-only", "HEAD", "--"):
            return "phase165_r52_r9_shared_math.py"
        return original(*args)

    monkeypatch.setattr(r, "git", modified_git)
    with pytest.raises(RuntimeError, match="unexpected tracked"):
        r.preflight()
