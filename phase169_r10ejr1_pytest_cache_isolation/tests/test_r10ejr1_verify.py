"""Focused checks for a non-writing R10EJ pytest cache wrapper."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from phase169_r10ejr1_pytest_cache_isolation.verify import (
    ORIGINAL_RUNNER,
    REVIEWED_ORIGINAL_RUNNER_SHA256,
    compose_addopts,
    sha256_bytes,
    verify_reviewed_runner,
)


def test_r10ejr1_addopts_preserves_existing_options():
    assert compose_addopts(None) == "-p no:cacheprovider"
    assert compose_addopts("") == "-p no:cacheprovider"
    assert compose_addopts("-q --tb=short") == "-q --tb=short -p no:cacheprovider"


def test_r10ejr1_reviewed_runner_guard_rejects_unreviewed_bytes(tmp_path: Path):
    runner = tmp_path / ORIGINAL_RUNNER
    runner.parent.mkdir(parents=True)
    runner.write_text("unreviewed run", encoding="utf-8")
    with pytest.raises(RuntimeError, match="differs from the reviewed ZIP"):
        verify_reviewed_runner(tmp_path)


def test_r10ejr1_reviewed_runner_guard_rejects_missing_file(tmp_path: Path):
    with pytest.raises(RuntimeError, match="missing"):
        verify_reviewed_runner(tmp_path)


def test_r10ejr1_sha256_constant_is_complete():
    assert len(REVIEWED_ORIGINAL_RUNNER_SHA256) == 64
    assert sha256_bytes(b"hello") == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_r10ejr1_pytest_without_cacheprovider_writes_no_cache(tmp_path: Path):
    """Check actual pytest behavior, not only an environment variable string."""
    (tmp_path / "test_pass.py").write_text("def test_pass():\n    assert 1 + 1 == 2\n", encoding="utf-8")
    env = dict(os.environ)
    env["PYTEST_ADDOPTS"] = "-p no:cacheprovider"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "test_pass.py"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert not (tmp_path / ".pytest_cache").exists()
