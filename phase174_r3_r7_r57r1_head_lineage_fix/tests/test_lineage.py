"""R57R1 strict guard regression: only reviewed descendants, no pin bypass."""
from __future__ import annotations
import ast
import hashlib
from pathlib import Path
import subprocess
import pytest
from phase174_r3_r7_r57r1_head_lineage_fix import install


def audited_original() -> str:
    path = Path(install.__file__).parent / "R57_INSTALL_ORIGINAL_AUDITED.py.txt"
    return path.read_text(encoding="utf-8")


def test_exact_original_sha_and_patched_sha() -> None:
    original = audited_original()
    assert install.hash_data(original.encode("utf-8")) == install.EXPECTED_BEFORE_SHA256
    after = install.patch_candidate(original)
    assert install.hash_data(after.encode("utf-8")) == install.EXPECTED_AFTER_SHA256
    ast.parse(after)


def test_patch_changes_only_the_head_lineage_guard() -> None:
    original = audited_original()
    after = install.patch_candidate(original)
    assert after == original.replace(install.ORIGINAL, install.REPLACEMENT, 1)
    assert "if git('rev-parse','HEAD') != HEAD:" not in after
    assert "git', 'merge-base', '--is-ancestor', HEAD, 'HEAD'" in after
    assert "if git('branch','--show-current') != 'develop':" in after
    assert "if git('diff','--cached','--name-only'):" in after
    assert "if git('rev-parse','HEAD:'+name)!=PINS[name]:" in after
    assert "current_hash==LOCAL_SHA256[name]" in after


def test_wrong_or_ambiguous_anchor_refused() -> None:
    original = audited_original()
    with pytest.raises(ValueError):
        install.patch_candidate(original.replace(install.ORIGINAL, ''))
    with pytest.raises(ValueError):
        install.patch_candidate(original + install.ORIGINAL)


def git_run(where: Path, *args: str, ok: bool = True):
    p = subprocess.run(["git", *args], cwd=str(where), capture_output=True, text=True)
    if ok:
        assert p.returncode == 0, p.stderr
    return p


def test_git_ancestor_allowlisted_and_unrelated_rejected(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    git_run(repo, "init", "-q")
    git_run(repo, "config", "user.email", "audit@example.invalid")
    git_run(repo, "config", "user.name", "Test")
    (repo / "one.txt").write_text("first\n", encoding="utf-8")
    git_run(repo, "add", "one.txt")
    git_run(repo, "commit", "-qm", "reviewed base")
    reviewed = git_run(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / "two.txt").write_text("second\n", encoding="utf-8")
    git_run(repo, "add", "two.txt")
    git_run(repo, "commit", "-qm", "allowed descendant")
    assert git_run(repo, "merge-base", "--is-ancestor", reviewed, "HEAD").returncode == 0
    unrelated = git_run(repo, "hash-object", "-w", "two.txt").stdout.strip()
    assert git_run(repo, "merge-base", "--is-ancestor", unrelated, "HEAD", ok=False).returncode != 0


def test_develop_branch_and_git_blob_pins_are_not_removed() -> None:
    updated = install.patch_candidate(audited_original())
    assert 'PINS = {' in updated
    assert 'AFTER_SHA256 = {' in updated
    assert 'LOCAL_SHA256 = {' in updated
    assert 'if content not in (baseline,intended):' in updated
    assert 'if current_hash==AFTER_SHA256[name]:' in updated
    assert "unreviewed local edits:" in updated


def test_no_mathematical_rule_or_proof_tree_mutation() -> None:
    patcher = Path(install.__file__).read_text(encoding="utf-8")
    assert 'ProofStep(' not in patcher
    assert 'new_mathematical_rules' not in patcher
    assert 'register_fixed' not in patcher
    assert install.TARGET.name == "install.py"
    assert install.TARGET.parent.name == "phase174_r3_r7_r57_narrative_source_cleanup"
