"""Focused checks for the one-token PowerShell runner correction."""
from __future__ import annotations

from pathlib import Path
import pytest

from phase171_closeout_r2r2_runner_splat_fix import repair


def test_reviewed_runner_has_only_the_one_splat_correction() -> None:
    old = repair.TARGET.read_bytes()
    new = repair.REPLACEMENT.read_bytes()
    assert repair.sha(new) == repair.CORRECTED_SHA
    assert old in (
        new,
        new.replace(b"& python @PythonArguments", b"& python @Args"),
    )
    assert b"& python @PythonArguments" in new
    assert b"& python @Args\n" not in new


def test_refuses_unreviewed_runner(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    forged = tmp_path / "run.ps1"
    forged.write_bytes(b"& python -B attacker.py\n")
    monkeypatch.setattr(repair, "TARGET", forged)
    monkeypatch.setattr(repair, "git", lambda *args: "develop" if args[0] == "branch" else ("" if args[0] == "diff" else "stable"))
    with pytest.raises(RuntimeError, match="unreviewed existing PowerShell runner"):
        repair.preflight()


def test_refuses_modified_installer(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    forged = tmp_path / "install.py"
    forged.write_text("print('unreviewed')\n", encoding="utf-8")
    monkeypatch.setattr(repair, "INSTALLER", forged)
    monkeypatch.setattr(repair, "git", lambda *args: "develop" if args[0] == "branch" else ("" if args[0] == "diff" else "stable"))
    with pytest.raises(RuntimeError, match="installer differs"):
        repair.preflight()


def test_dry_run_never_changes_the_runner(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import sys

    forged = tmp_path / "run.ps1"
    forged.write_bytes(repair.REPLACEMENT.read_bytes().replace(
        b"& python @PythonArguments", b"& python @Args"))
    monkeypatch.setattr(repair, "TARGET", forged)
    monkeypatch.setattr(repair, "git", lambda *args: "develop" if args[0] == "branch" else ("" if args[0] == "diff" else "stable"))
    monkeypatch.setattr(sys, "argv", ["repair.py", "--dry-run"])
    before = forged.read_bytes()
    assert repair.main() == 0
    assert forged.read_bytes() == before


def test_atomic_write_preserves_exact_bytes(tmp_path: Path) -> None:
    target = tmp_path / "run.ps1"
    repair.atomic_write(target, repair.REPLACEMENT.read_bytes())
    assert target.read_bytes() == repair.REPLACEMENT.read_bytes()


def test_apply_changes_only_runner_and_keeps_backup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    import sys

    target = tmp_path / "run.ps1"
    old = repair.REPLACEMENT.read_bytes().replace(
        b"& python @PythonArguments", b"& python @Args")
    target.write_bytes(old)
    monkeypatch.setattr(repair, "TARGET", target)
    monkeypatch.setattr(repair, "git", lambda *args: "develop" if args[0] == "branch" else ("" if args[0] == "diff" else "stable"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "localappdata"))
    monkeypatch.setattr(sys, "argv", ["repair.py"])
    assert repair.main() == 0
    assert target.read_bytes() == repair.REPLACEMENT.read_bytes()
    reports = list((tmp_path / "localappdata" / "EHPProofTracerRecovery").glob("*/audit.json"))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text(encoding="utf-8"))
    assert report["result"] == "PASS_RUNNER_CORRECTED"
    assert report["full_pytest"] is False
    assert (reports[0].parent / "run_before.ps1").read_bytes() == old
