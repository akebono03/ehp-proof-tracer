"""Unit tests for guarded and repeatable R2F root-collision repair."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from phase171_r2f_r1_root_shadow_fix import install


def fixture_paths(monkeypatch, tmp_path: Path):
    repo = tmp_path / "repo"
    package = tmp_path / "package"
    repo.mkdir()
    package.mkdir()
    target = repo / "audit.py"
    source = package / "audit_FULL.py"
    original = b"old verified audit\n"
    updated = b"new verified audit\n"
    target.write_bytes(original)
    source.write_bytes(updated)
    monkeypatch.setattr(install, "PATCHES", (
        install.PatchSpec(
            "audit.py", "audit_FULL.py",
            sha256(original).hexdigest(), sha256(updated).hexdigest(),
        ),
    ))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "recovery"))
    return repo, package, target, original, updated


def test_check_never_modifies_existing_files(monkeypatch, tmp_path: Path) -> None:
    repo, package, target, original, updated = fixture_paths(monkeypatch, tmp_path)
    result = install.preflight(repo, package)
    assert len(result) == 1
    assert result[0]["state"] == "NEEDS_REPAIR"
    assert target.read_bytes() == original


def test_apply_is_idempotent_and_backs_up_original(monkeypatch, tmp_path: Path) -> None:
    repo, package, target, original, updated = fixture_paths(monkeypatch, tmp_path)
    install.apply(repo, package)
    assert target.read_bytes() == updated
    backups = list((tmp_path / "recovery" / "EHPProofTracerRecovery").glob(
        "phase171_r2f_r1_fix_*/audit.py.before"
    ))
    assert len(backups) == 1
    assert backups[0].read_bytes() == original
    install.apply(repo, package)
    assert target.read_bytes() == updated
    assert len(list((tmp_path / "recovery" / "EHPProofTracerRecovery").glob(
        "phase171_r2f_r1_fix_*/audit.py.before"
    ))) == 1


def test_unrecognized_edit_is_rejected_without_overwrite(monkeypatch, tmp_path: Path) -> None:
    repo, package, target, original, updated = fixture_paths(monkeypatch, tmp_path)
    target.write_bytes(b"user-customized audit\n")
    with pytest.raises(RuntimeError, match="refusing to overwrite"):
        install.apply(repo, package)
    assert target.read_bytes() == b"user-customized audit\n"
    assert not (tmp_path / "recovery").exists()


def test_bundle_corruption_is_rejected_without_overwrite(monkeypatch, tmp_path: Path) -> None:
    repo, package, target, original, updated = fixture_paths(monkeypatch, tmp_path)
    (package / "audit_FULL.py").write_bytes(b"corrupted bundle\n")
    with pytest.raises(RuntimeError, match="checksum mismatch"):
        install.apply(repo, package)
    assert target.read_bytes() == original
