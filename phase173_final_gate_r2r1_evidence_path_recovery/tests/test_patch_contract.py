"""Review source-safety and unchanged R2 mathematical proof boundaries."""
from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_final_gate_r2r1_evidence_path_recovery import patch


PACKAGE = Path(__file__).resolve().parents[1]
REPLACEMENT_GATE = PACKAGE / "replacement" / "gate.py"
REPLACEMENT_RUNNER = PACKAGE / "replacement" / "run.ps1"


def _load_replacement_gate():
    spec = importlib.util.spec_from_file_location("phase173_r2r1_gate_review", REPLACEMENT_GATE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _copy_originals(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    target = repo / patch.TARGET_DIR
    target.mkdir(parents=True)
    new_package = tmp_path / "package"
    (new_package / "replacement").mkdir(parents=True)
    for name, original in patch.ORIGINAL_SHA256.items():
        fixture = PACKAGE / "tests" / "fixtures" / name
        assert patch.digest(fixture.read_bytes()) == original
        shutil.copyfile(fixture, target / name)
        shutil.copyfile(PACKAGE / "replacement" / name,
                        new_package / "replacement" / name)
    return repo, new_package


def test_replacements_are_whole_valid_source_files() -> None:
    import ast

    source = REPLACEMENT_GATE.read_text(encoding="utf-8")
    ast.parse(source)
    assert "def validate_snapshot" in source
    assert "def verify_prior_failure" in source
    assert "def finalize" in source
    assert "-PreviousEvidencePath" not in source
    script = REPLACEMENT_RUNNER.read_text(encoding="utf-8")
    assert "[string]$PreviousEvidencePath" in script
    assert "C:\\Users\\oomae\\AppData\\Local" in script
    assert "Test-CompletePreviousEvidence" in script
    assert "PHASE173_FINAL_R2_PRIOR_EVIDENCE_DIR=" in script
    for name in (
        "phase173_full_test_report.json",
        "phase173_full_test_attempt.json",
        "active_suite_stdout.txt",
        "active_suite_stderr.txt",
    ):
        assert name in script


def test_original_hashes_are_pinned() -> None:
    assert set(patch.ORIGINAL_SHA256) == {"gate.py", "run.ps1"}
    assert all(len(value) == 64 for value in patch.ORIGINAL_SHA256.values())
    assert patch.digest(b"hello") != patch.digest(b"HELLO")


def test_actual_reviewed_patch_apply_idempotent_and_rollback(tmp_path: Path) -> None:
    repo, new_package = _copy_originals(tmp_path)
    source_dir = repo / patch.TARGET_DIR
    applied = patch.apply_reviewed_patch(repo, new_package)
    assert len(applied) == 2
    assert all(state == "ALREADY_PATCHED"
               for _, _, state in patch.reviewed_files(repo, new_package))
    for name in patch.ORIGINAL_SHA256:
        assert (new_package / "original_backups" / name).read_bytes() == (
            PACKAGE / "tests" / "fixtures" / name
        ).read_bytes()
        assert (source_dir / name).read_bytes() == (
            PACKAGE / "replacement" / name
        ).read_bytes()
    assert patch.apply_reviewed_patch(repo, new_package) == ()
    restored = patch.rollback_reviewed_patch(repo, new_package)
    assert len(restored) == 2
    for name in patch.ORIGINAL_SHA256:
        assert patch.digest((source_dir / name).read_bytes()) == patch.ORIGINAL_SHA256[name]


def test_unreviewed_source_is_refused(tmp_path: Path) -> None:
    repo = tmp_path
    target = repo / patch.TARGET_DIR
    target.mkdir()
    (target / "gate.py").write_text("unsafe modification", encoding="utf-8")
    (target / "run.ps1").write_bytes(REPLACEMENT_RUNNER.read_bytes())
    with pytest.raises(RuntimeError, match="unreviewed local edits"):
        patch.reviewed_files(repo, PACKAGE)


def test_missing_source_is_refused(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="missing"):
        patch.reviewed_files(tmp_path, PACKAGE)


def test_fully_patched_source_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / patch.TARGET_DIR
    target.mkdir()
    for name in patch.ORIGINAL_SHA256:
        shutil.copyfile(PACKAGE / "replacement" / name, target / name)
    states = patch.reviewed_files(tmp_path, PACKAGE)
    assert all(state == "ALREADY_PATCHED" for _, _, state in states)


def test_atomic_write_refuses_stale_temp_file(tmp_path: Path) -> None:
    target = tmp_path / "source.py"
    target.write_text("old", encoding="utf-8")
    temp = tmp_path / "source.py.phase173_r2r1_tmp"
    temp.write_text("unreviewed", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Stale temporary"):
        patch._atomic_write(target, b"new")
    assert target.read_text(encoding="utf-8") == "old"
    assert temp.read_text(encoding="utf-8") == "unreviewed"


def test_reviewed_gate_accepts_only_approved_remote_fast_forward(tmp_path: Path) -> None:
    gate = _load_replacement_gate()
    for path in gate.REPAIRED_TEST_SHA256:
        file = tmp_path / path
        file.parent.mkdir(parents=True, exist_ok=True)
        # Replace reviewed hashes with a synthetic but precisely hashed test.
        file.write_bytes(b"reviewed_r1_fix = True\r\n")
    gate.REPAIRED_TEST_SHA256 = {
        key: gate.normalized_digest(b"reviewed_r1_fix = True\n")
        for key in gate.REPAIRED_TEST_SHA256
    }
    remote = "25b1ee1f7c848356604061991db06265cfccb296"
    def fake_git(repo: Path, *args: str, allow_nonzero: bool = False):
        if args == ("rev-parse", "--show-toplevel"):
            answer = str(repo)
        elif args == ("branch", "--show-current"):
            answer = "develop"
        elif args == ("rev-parse", "HEAD"):
            answer = gate.REVIEWED_BASE
        elif args == ("rev-parse", "origin/develop"):
            answer = remote
        elif args[0] == "rev-parse" and args[1].startswith("origin/develop:"):
            path = args[1].removeprefix("origin/develop:")
            answer = gate.APPROVED_REMOTE_R1_BLOBS.get(path, gate.REVIEWED_BLOBS.get(path, ""))
        elif args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            answer = gate.REVIEWED_BLOBS.get(args[1][5:], "")
        elif args[:2] == ("diff", "--name-only"):
            answer = "\n".join(gate.REPAIRED_TEST_SHA256)
        elif args == ("write-tree",):
            answer = "immutable-index-tree"
        else:
            answer = ""
        return SimpleNamespace(stdout=answer, returncode=0, stderr="")
    gate.git = fake_git
    snapshot = gate.validate_snapshot(tmp_path)
    assert snapshot["head"] == gate.REVIEWED_BASE
    assert snapshot["remote_head"] == remote
    assert snapshot["repaired_test_count"] == 3


def test_reviewed_gate_refuses_diverging_remote(tmp_path: Path) -> None:
    gate = _load_replacement_gate()
    original = gate.git
    def fake_git(repo: Path, *args: str, allow_nonzero: bool = False):
        if args == ("rev-parse", "--show-toplevel"):
            return SimpleNamespace(stdout=str(repo), returncode=0, stderr="")
        if args == ("branch", "--show-current"):
            return SimpleNamespace(stdout="develop", returncode=0, stderr="")
        if args == ("rev-parse", "HEAD"):
            return SimpleNamespace(stdout=gate.REVIEWED_BASE, returncode=0, stderr="")
        if args == ("rev-parse", "origin/develop"):
            return SimpleNamespace(stdout="not-on-same-history", returncode=0, stderr="")
        if args[:2] == ("merge-base", "--is-ancestor"):
            # The remote does not descend from the reviewed base.
            return SimpleNamespace(stdout="", returncode=1, stderr="")
        return original(repo, *args, allow_nonzero=allow_nonzero)
    gate.git = fake_git
    with pytest.raises(RuntimeError, match="not descended"):
        gate.validate_snapshot(tmp_path)


def test_existing_failure_evidence_check_is_unchanged() -> None:
    gate = _load_replacement_gate()
    assert len(gate.EXPECTED_PREVIOUS_FAILURES) == 5
    assert gate.EXPECTED_ACTIVE_PASSED == 3546
    assert gate.ACTIVE_SUITE_COMMAND.endswith("tests")
    assert gate.verify_prior_failure.__doc__.startswith("Require the precise")


def test_no_restart_of_full_pytest_in_patch_runner() -> None:
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "phase173_final_gate_r2_recovery/tests/test_gate_contract.py" in script
    assert "PHASE173_FINAL_R2R1_FULL_PYTEST=False" in script
    assert "PHASE173_FINAL_R2R1_APPLY=PASS" in script
