"""Focused R32R1 handoff and guarded replacement tests (no real writes)."""
from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import pytest

from phase174_r3_r7_r32r1_reviewed_head_handoff_fix import install


def _patched_audit():
    source = install.PACKAGE / "replacement" / "audit.py"
    spec = importlib.util.spec_from_file_location("r32r1_patched_audit_fixture", source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _mock_checkout(monkeypatch, tmp_path: Path, local: str, remote: str):
    audit = _patched_audit()
    for path in audit.PINS:
        file = tmp_path / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(b"reviewed")
    prior = tmp_path / audit.R31_AUDIT
    prior.parent.mkdir(parents=True, exist_ok=True)
    prior.write_bytes((install.ROOT / audit.R31_AUDIT).read_bytes())
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "matches_pin", lambda data, _sha: data == b"reviewed")

    def git_stub(*args):
        if args == ("rev-parse", "--show-toplevel"):
            return str(tmp_path)
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return local
        if args == ("ls-remote", "origin", "refs/heads/develop"):
            return remote + "\trefs/heads/develop"
        if args in (("diff", "--cached", "--name-only"),
                    ("diff", "--name-only")):
            return ""
        raise AssertionError(f"Unexpected git invocation: {args}")

    monkeypatch.setattr(audit, "git", git_stub)
    return audit


@pytest.mark.parametrize("local,mode", (
    (install.BASE_HEAD, "R31_LOCAL_UNMERGED_REVIEWED"),
    (install.REVIEWED_R31_MERGE_HEAD, "R31_MERGED_REVIEWED"),
))
def test_reviewed_local_handoff_modes(monkeypatch, tmp_path, local, mode):
    audit = _mock_checkout(monkeypatch, tmp_path, local, install.REVIEWED_R31_MERGE_HEAD)
    state = audit.verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["handoff_mode"] == mode
    assert state["r31_preserved"] is True
    assert state["tracked_changes"] == 0


@pytest.mark.parametrize("local,remote", (
    (install.BASE_HEAD, install.BASE_HEAD),
    ("f" * 40, install.REVIEWED_R31_MERGE_HEAD),
    (install.REVIEWED_R31_MERGE_HEAD, "f" * 40),
))
def test_unreviewed_heads_fail_closed(monkeypatch, tmp_path, local, remote):
    audit = _mock_checkout(monkeypatch, tmp_path, local, remote)
    with pytest.raises(RuntimeError, match="Unreviewed"):
        audit.verify_checkout()


def test_changed_r31_file_fail_closed(monkeypatch, tmp_path):
    audit = _mock_checkout(monkeypatch, tmp_path, install.BASE_HEAD,
                           install.REVIEWED_R31_MERGE_HEAD)
    (tmp_path / audit.R31_AUDIT).write_text("tampered", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R31 audit file changed"):
        audit.verify_checkout()


def test_pinned_source_mismatch_rejected(monkeypatch, tmp_path):
    audit = _mock_checkout(monkeypatch, tmp_path, install.BASE_HEAD,
                           install.REVIEWED_R31_MERGE_HEAD)
    bad = next(iter(audit.PINS))
    (tmp_path / bad).write_bytes(b"tampered")
    with pytest.raises(RuntimeError, match="reviewed file differs"):
        audit.verify_checkout()


def test_repaired_files_have_exact_reviewed_hashes():
    for rel, (_before, after, replacement) in install.TARGETS.items():
        assert replacement.is_file()
        assert install.sha256(install.normalized_bytes(replacement)) == after
        assert len(after) == 64
        if rel.endswith("audit.py"):
            ast.parse(replacement.read_text(encoding="utf-8"))
            assert "REVIEWED_R31_MERGE_HEAD" in replacement.read_text(encoding="utf-8")
        else:
            content = replacement.read_text(encoding="utf-8")
            assert "R31_REUSABLE_REGRESSION" in content
            assert "R31_REGRESSION'" not in content
            assert "R32_CONTRACT" in content
            assert "R18_SURJECTIVITY" in content
            assert "R5_HOPF_INJECTIVITY" in content


def test_old_r31_head_pinned_tests_not_selected_by_new_runner():
    content = (install.PACKAGE / "replacement" / "run.ps1").read_text(encoding="utf-8")
    assert "test_source_guard_preserves_reviewed_r30_handoff" not in content
    assert "test_r31_reports_no_unsupported_completion" not in content
    assert "test_typed_hopf_delta_bridge_has_distinct_independent_goals" in content
    assert "test_toda_proposition_source_dependency_order" in content


def _fixture_installer(monkeypatch, tmp_path: Path):
    for rel, (_, _, replacement) in install.TARGETS.items():
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(replacement.read_bytes())
    r31 = tmp_path / install.R31_FILE
    r31.parent.mkdir(parents=True, exist_ok=True)
    r31.write_bytes((install.ROOT / install.R31_FILE).read_bytes())
    monkeypatch.setattr(install, "ROOT", tmp_path)

    def fake_git(*args):
        if args == ("rev-parse", "--show-toplevel"):
            return str(tmp_path)
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return install.BASE_HEAD
        if args == ("ls-remote", "origin", "refs/heads/develop"):
            return install.REVIEWED_R31_MERGE_HEAD + "\trefs/heads/develop"
        if args in (("diff", "--cached", "--name-only"),
                    ("diff", "--name-only")):
            return ""
        raise AssertionError(f"Unexpected git invocation: {args}")

    monkeypatch.setattr(install, "git", fake_git)


def test_guarded_install_idempotent_and_read_only_for_r31(monkeypatch, tmp_path):
    _fixture_installer(monkeypatch, tmp_path)
    before = (tmp_path / install.R31_FILE).read_bytes()
    assert set(install.preflight()["target_states"].values()) == {"PATCHED"}
    assert set(install.install()["target_states"].values()) == {"PATCHED"}
    assert set(install.install()["target_states"].values()) == {"PATCHED"}
    assert (tmp_path / install.R31_FILE).read_bytes() == before


def test_installer_rejects_unknown_existing_file(monkeypatch, tmp_path):
    _fixture_installer(monkeypatch, tmp_path)
    victim = tmp_path / next(iter(install.TARGETS))
    victim.write_text("unreviewed modification", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Local R32 changes"):
        install.preflight()
