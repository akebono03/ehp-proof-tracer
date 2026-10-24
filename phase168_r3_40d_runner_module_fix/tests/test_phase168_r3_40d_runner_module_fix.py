"""Regression tests for the R3-40D module launch fix."""
from pathlib import Path
import subprocess
import sys


def test_runner_launches_capture_as_repository_root_module():
    root = Path(__file__).resolve().parents[1]
    runner = (root / "run.ps1").read_text(encoding="utf-8")
    assert "python -m phase168_r3_40d_runner_module_fix.check_and_capture" in runner
    assert "python (Join-Path $package 'check_and_capture.py')" not in runner
    assert (root / "check_and_capture.py").is_file()
    assert (root / "apply.py").is_file()


def test_python_module_execution_can_import_project_root(tmp_path):
    package = tmp_path / "module_probe"
    package.mkdir()
    (tmp_path / "project_root_probe.py").write_text(
        "MARKER = 'resolved-from-project-root'\n", encoding="utf-8"
    )
    (package / "capture.py").write_text(
        "from project_root_probe import MARKER\nprint(MARKER)\n",
        encoding="utf-8",
    )
    completed = subprocess.run(
        [sys.executable, "-m", "module_probe.capture"],
        cwd=tmp_path,
        check=True,
        text=True,
        capture_output=True,
    )
    assert completed.stdout.strip() == "resolved-from-project-root"
