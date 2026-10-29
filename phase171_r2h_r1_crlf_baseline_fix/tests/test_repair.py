"""Focused guards for the non-destructive R2H R1 package repair."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from phase171_r2h_r1_crlf_baseline_fix import repair


def _test_installation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    fixture_files = {
        "install.py": "baseline_install.py.txt",
        "test_install.py": "baseline_test_install.py.txt",
    }
    for relative, _, original_hash, _ in repair.FILES:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        source = Path(__file__).resolve().parents[1] / fixture_files[target.name]
        payload = source.read_bytes()
        assert sha256(payload).hexdigest() == original_hash
        target.write_bytes(payload)



def test_read_only_check_keeps_original_bytes(tmp_path: Path, monkeypatch) -> None:
    _test_installation(tmp_path, monkeypatch)
    before = [(tmp_path / path).read_bytes() for path, _, _, _ in repair.FILES]
    assert repair.run("check") == 0
    assert before == [(tmp_path / path).read_bytes() for path, _, _, _ in repair.FILES]


def test_guarded_repair_creates_backup_and_is_idempotent(tmp_path: Path, monkeypatch) -> None:
    _test_installation(tmp_path, monkeypatch)
    recovery = tmp_path / "recovery"
    monkeypatch.setenv("LOCALAPPDATA", str(recovery))
    assert repair.run("apply") == 0
    for relative, _, _, patched_hash in repair.FILES:
        assert sha256((tmp_path / relative).read_bytes()).hexdigest() == patched_hash
    assert len(list((recovery / "EHPProofTracerRecovery").glob("phase171_r2h_r1_*"))) == 1
    assert repair.run("apply") == 0
    assert len(list((recovery / "EHPProofTracerRecovery").glob("phase171_r2h_r1_*"))) == 1


def test_rejects_modified_installer_without_writing(tmp_path: Path, monkeypatch) -> None:
    _test_installation(tmp_path, monkeypatch)
    path = tmp_path / repair.FILES[0][0]
    path.write_bytes(path.read_bytes() + b"\n# unreviewed\n")
    before = path.read_bytes()
    with pytest.raises(RuntimeError, match="unreviewed"):
        repair.inspect()
    assert path.read_bytes() == before


def test_rejects_unrecognized_payload_hash(tmp_path: Path, monkeypatch) -> None:
    _test_installation(tmp_path, monkeypatch)
    original = repair.FILES
    item = original[0]
    monkeypatch.setattr(repair, "FILES", ((item[0], item[1], item[2], "0" * 64),))
    with pytest.raises(RuntimeError, match="payload hash"):
        repair.inspect()
