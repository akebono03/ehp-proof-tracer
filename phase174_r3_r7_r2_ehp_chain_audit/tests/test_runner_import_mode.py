"""Regression: pytest must not shadow same-name production Python modules."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _create_collision_fixture(root: Path) -> Path:
    module = root / "phase165_r12_r11_prop42_unified.py"
    module.write_text("GENERAL_ASSERTION_ID = 'present'\n", encoding="utf-8")
    sibling = root / "phase165_r12_r11_prop42_unified" / "tests"
    sibling.mkdir(parents=True)
    test = sibling / "test_source_module.py"
    test.write_text(
        "from phase165_r12_r11_prop42_unified import GENERAL_ASSERTION_ID\n"
        "def test_import():\n"
        "    assert GENERAL_ASSERTION_ID == 'present'\n",
        encoding="utf-8",
    )
    return test


def _run_fixture(root: Path, test: Path, import_mode: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        (
            sys.executable, "-B", "-m", "pytest", "-q",
            "--import-mode=" + import_mode, "-p", "no:cacheprovider",
            str(test),
        ),
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def test_same_named_directory_causes_importlib_collection_error(tmp_path: Path) -> None:
    test = _create_collision_fixture(tmp_path)
    result = _run_fixture(tmp_path, test, "importlib")
    assert result.returncode != 0
    assert "cannot import name" in result.stdout or "cannot import name" in result.stderr


def test_prepend_recovers_source_module_import(tmp_path: Path) -> None:
    test = _create_collision_fixture(tmp_path)
    result = _run_fixture(tmp_path, test, "prepend")
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "1 passed" in result.stdout


def test_powershell_runner_selects_safe_import_mode() -> None:
    runner = Path(__file__).resolve().parents[1] / "run.ps1"
    contents = runner.read_text(encoding="utf-8")
    assert "--import-mode=prepend" in contents
    assert "--import-mode=importlib" not in contents
    assert "-p no:cacheprovider" in contents
    assert "'phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py'" in contents
    assert "'phase165_r12_r12_ehp_consequences/tests/test_phase165_r12_r12_ehp_consequences.py'" in contents
    assert "'phase165_r14_r6_generic_iso/test_phase165_r14_r6_generic_iso.py'" in contents
