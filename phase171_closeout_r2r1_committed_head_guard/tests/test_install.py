"""Isolated guards for exact R2 script replacement, without project mathematics."""
from __future__ import annotations

from pathlib import Path
import shutil

import pytest

from phase171_closeout_r2r1_committed_head_guard import install


@pytest.fixture
def worktree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    root = tmp_path / "repo"
    r2 = root / "phase171_closeout_r2_documentation_full_output"
    r2.mkdir(parents=True)
    for relative in install.REPLACEMENTS:
        target = r2 / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        reviewed_name = Path(relative).name
        (target).write_bytes(
            (install.HERE / "reviewed_originals" / reviewed_name).read_bytes()
        )
    for name in install.SECTIONS:
        section = r2 / "sections" / name
        section.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(install.HERE.parent / "phase171_closeout_r2_documentation_full_output" / "sections" / name,
                     section)
    (r2 / "run.ps1").write_text("# reviewed launcher", encoding="utf-8")
    for relative in install.DOCUMENTS:
        document = root / relative
        document.parent.mkdir(parents=True, exist_ok=True)
        document.write_text("# existing document\n", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", root)
    monkeypatch.setattr(install, "R2", r2)
    monkeypatch.setattr(install, "git", lambda *args: {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "committed-r1r1",
        ("rev-parse", "origin/develop"): "committed-r1r1",
        ("diff", "--cached", "--name-only", "--"): "",
    }[args])
    return root, r2


@pytest.mark.parametrize("corrected", [False, True])
def test_only_whole_reviewed_old_or_corrected_states_pass(worktree, corrected):
    _, r2 = worktree
    if corrected:
        for relative, asset in install.REPLACEMENTS.items():
            (r2 / relative).write_bytes((install.HERE / asset).read_bytes())
    head, before, replacement, already = install.inspect()
    assert head == "committed-r1r1"
    assert len(before) == len(replacement) == 2
    assert already is corrected


def test_unknown_and_mixed_install_states_are_refused(worktree):
    _, r2 = worktree
    (r2 / "update_docs.py").write_bytes(b"unreviewed source")
    with pytest.raises(RuntimeError, match="unreviewed R2 source"):
        install.inspect()
    (r2 / "update_docs.py").write_bytes((install.HERE / install.REPLACEMENTS["update_docs.py"]).read_bytes())
    with pytest.raises(RuntimeError, match="mixed R2 correction states"):
        install.inspect()


def test_unreviewed_document_section_is_refused(worktree):
    _, r2 = worktree
    (r2 / "sections" / "readme.md").write_text("unreviewed", encoding="utf-8")
    with pytest.raises(RuntimeError, match="unreviewed Phase 171 document section"):
        install.inspect()
