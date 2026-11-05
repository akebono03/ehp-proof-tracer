"""Regression tests for duplicate basenames during focused pytest collection."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from phase174_r3_r6_r3r2_pytest_importmode_fix import verify


def test_runner_uses_importlib_without_reapplying_production_patch() -> None:
    script = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(
        encoding="utf-8"
    )
    assert "--import-mode=importlib" in script
    assert "--collect-only" in script
    assert "phase172_r5_prior_reference_display/tests/test_projection.py" in script
    assert "phase174_r3_r6_r3_common_narrative/tests/test_projection.py" in script
    assert "phase174_r3_r6_source_extension/tests/test_source.py" in script
    assert "phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py" in script
    assert "scoped_guard_fix.patch --apply" not in script
    assert "common_narrative.patch --apply" not in script


def test_importlib_collects_duplicate_test_projection_modules(tmp_path: Path) -> None:
    left = tmp_path / "left" / "test_projection.py"
    right = tmp_path / "right" / "test_projection.py"
    left.parent.mkdir(parents=True)
    right.parent.mkdir(parents=True)
    left.write_text("def test_left():\n    assert 1 + 1 == 2\n", encoding="utf-8")
    right.write_text("def test_right():\n    assert 2 + 2 == 4\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--import-mode=importlib",
         "-p", "no:cacheprovider", str(left), str(right)],
        cwd=tmp_path, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "2 passed" in result.stdout


def test_inspection_is_read_only_and_has_two_reviewed_targets() -> None:
    assert len(verify.SOURCE_SHA256) == 2
    code = (Path(verify.__file__)).read_text(encoding="utf-8")
    assert "write_bytes(" not in code
    assert "write_text(" not in code
    assert "os.replace(" not in code
    assert "scoped_patch.TARGETS" in code
