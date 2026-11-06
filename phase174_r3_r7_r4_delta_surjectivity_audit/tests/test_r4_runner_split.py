"""Focused regression guards for duplicate pytest module names."""
from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import sys


RUNNER = Path(__file__).resolve().parents[1] / "run.ps1"


def _test_group(source: str, variable_name: str) -> tuple[str, ...]:
    match = re.search(
        r"\$" + re.escape(variable_name) + r"\s*=\s*@\((.*?)\)",
        source,
        flags=re.DOTALL,
    )
    assert match is not None
    return tuple(re.findall(r"'([^']+\.py)'", match.group(1)))


def test_r4_and_r3_duplicate_audit_names_use_independent_processes() -> None:
    source = RUNNER.read_text(encoding="utf-8-sig")
    local = _test_group(source, "R4Tests")
    regression = _test_group(source, "RegressionTests")
    assert any("phase174_r3_r7_r4_delta_surjectivity_audit" in path
               and path.endswith("test_audit.py") for path in local)
    assert any("phase174_r3_r7_r3_ehp_zero_rule" in path
               and path.endswith("test_audit.py") for path in regression)
    assert len(local) == 2
    assert len(regression) == 4
    assert {Path(path).name for path in local}.isdisjoint(
        {Path(path).name for path in regression} - {"test_audit.py"}
    )
    invocations = re.findall(
        r"& python -B -m pytest -q --import-mode=prepend -p no:cacheprovider\s+@(\w+)",
        source,
    )
    assert invocations == ["R4Tests", "RegressionTests"]
    assert "--import-mode=importlib" not in source


def test_runner_preserves_preflight_and_fail_closed_guards() -> None:
    source = RUNNER.read_text(encoding="utf-8-sig")
    assert "foreach ($TestPath in $FocusedTests)" in source
    assert source.count("if ($LASTEXITCODE -ne 0)") == 3
    assert "PHASE174_R3R7R4_FOCUSED_PYTEST=PASS" in source
    assert "audit.py' --dry-run" in source
    assert "audit.py'" in source
    assert "$env:PYTHONPATH = $PreviousPythonPath" in source
    assert "$env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode" in source
    assert "Pop-Location" in source
    assert "pytest -q --import-mode=prepend -p no:cacheprovider" in source
    assert "--all" not in source


def test_duplicate_test_module_basename_fails_together_and_passes_split(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first" / "tests" / "test_audit.py"
    second = tmp_path / "second" / "tests" / "test_audit.py"
    for test_file in (first, second):
        test_file.parent.mkdir(parents=True)
        test_file.write_text(
            "def test_collection_contract():\n    assert 1 + 1 == 2\n",
            encoding="utf-8",
        )
    base = [
        sys.executable, "-B", "-m", "pytest", "-q",
        "--import-mode=prepend", "-p", "no:cacheprovider",
    ]
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    combined = subprocess.run(
        base + [str(first), str(second)],
        cwd=tmp_path, env=environment, text=True,
        capture_output=True, check=False,
    )
    assert combined.returncode != 0
    assert "import file mismatch" in combined.stdout.lower()
    for test_file in (first, second):
        separate = subprocess.run(
            base + [str(test_file)],
            cwd=tmp_path, env=environment, text=True,
            capture_output=True, check=False,
        )
        assert separate.returncode == 0, separate.stdout + separate.stderr
