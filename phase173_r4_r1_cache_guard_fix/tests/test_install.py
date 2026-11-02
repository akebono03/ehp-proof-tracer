"""Focused tests for preserving local files during the R4-R1 cache-guard correction."""
from __future__ import annotations

from pathlib import Path
from hashlib import sha256

import pytest

from phase173_r4_r1_cache_guard_fix.install import (
    FILES, PACKAGE, install, replacement_plan,
)
from phase173_r4_r1_cache_guard_fix.manifest import ORIGINAL_SHA256


def prepare_originals(tmp_path: Path, payload: Path) -> None:
    """Reuse the shipped original only when the original checksum can be reproduced."""
    # This is an offline negative test helper; each fixture uses realistic paths.
    for relative in FILES:
        target = tmp_path / PACKAGE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((payload / relative).read_bytes())


def test_correction_payload_files_exist() -> None:
    payload = Path(__file__).resolve().parents[1] / "payload" / PACKAGE
    assert all((payload / relative).is_file() for relative in FILES)
    assert set(ORIGINAL_SHA256) == set(FILES)


def test_already_corrected_is_idempotent(tmp_path: Path) -> None:
    payload = Path(__file__).resolve().parents[1] / "payload" / PACKAGE
    prepare_originals(tmp_path, payload)
    assert replacement_plan(tmp_path, payload) == ("CORRECTED",) * len(FILES)
    assert install(tmp_path, payload, dry_run=True) == "ALREADY_INSTALLED"


def test_unrecognized_local_edit_is_preserved(tmp_path: Path) -> None:
    payload = Path(__file__).resolve().parents[1] / "payload" / PACKAGE
    prepare_originals(tmp_path, payload)
    target = tmp_path / PACKAGE / "audit.py"
    target.write_text("custom local version", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Unrecognized local modifications"):
        install(tmp_path, payload, dry_run=False)
    assert target.read_text(encoding="utf-8") == "custom local version"


def test_partially_corrected_package_is_rejected(tmp_path: Path, monkeypatch) -> None:
    payload = Path(__file__).resolve().parents[1] / "payload" / PACKAGE
    prepare_originals(tmp_path, payload)
    target = tmp_path / PACKAGE / "audit.py"
    old = b"old audit mock"
    target.write_bytes(old)
    monkeypatch.setitem(ORIGINAL_SHA256, "audit.py", sha256(old).hexdigest())
    with pytest.raises(RuntimeError, match="Partially updated"):
        install(tmp_path, payload, dry_run=True)
    assert target.read_bytes() == old


def test_original_version_dry_run_does_not_write(tmp_path: Path, monkeypatch) -> None:
    payload = Path(__file__).resolve().parents[1] / "payload" / PACKAGE
    prepare_originals(tmp_path, payload)
    previous = {}
    for relative in FILES:
        old_bytes = ("before " + relative).encode("utf-8")
        target = tmp_path / PACKAGE / relative
        target.write_bytes(old_bytes)
        previous[relative] = old_bytes
        monkeypatch.setitem(ORIGINAL_SHA256, relative, sha256(old_bytes).hexdigest())
    assert replacement_plan(tmp_path, payload) == ("ORIGINAL",) * len(FILES)
    assert install(tmp_path, payload, dry_run=True) == "DRY_RUN_VALIDATED_NO_FILES_CHANGED"
    assert all((tmp_path / PACKAGE / rel).read_bytes() == old for rel, old in previous.items())


def test_original_version_install_backups_and_only_replaces_package(tmp_path: Path, monkeypatch) -> None:
    payload = Path(__file__).resolve().parents[1] / "payload" / PACKAGE
    prepare_originals(tmp_path, payload)
    previous = {}
    for relative in FILES:
        old_bytes = ("before " + relative).encode("utf-8")
        (tmp_path / PACKAGE / relative).write_bytes(old_bytes)
        previous[relative] = old_bytes
        monkeypatch.setitem(ORIGINAL_SHA256, relative, sha256(old_bytes).hexdigest())
    outside = tmp_path / "actual_production_file.py"
    outside.write_text("must remain unchanged", encoding="utf-8")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "localappdata"))
    assert install(tmp_path, payload, dry_run=False) == "INSTALLED_UNTRACKED_AUDIT_PACKAGE_ONLY"
    assert replacement_plan(tmp_path, payload) == ("CORRECTED",) * len(FILES)
    for relative, old_bytes in previous.items():
        backups = list((tmp_path / "localappdata" / "EHPProofTracerRecovery" /
                        "phase173_r4_r1_cache_guard_fix" / "backups").glob("*/" + relative))
        assert len(backups) == 1
        assert backups[0].read_bytes() == old_bytes
    assert outside.read_text(encoding="utf-8") == "must remain unchanged"
