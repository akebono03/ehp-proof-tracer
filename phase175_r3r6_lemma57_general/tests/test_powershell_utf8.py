"""R3R6R1 focused regression for Windows Python UTF-8 default decoding."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parents[1]


def test_run_script_sets_utf8_before_pytest_and_audit() -> None:
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    utf8_setting = "$env:PYTHONUTF8 = '1'"
    io_setting = "$env:PYTHONIOENCODING = 'utf-8'"
    assert script.count(utf8_setting) == 1
    assert script.count(io_setting) == 1
    assert script.index(utf8_setting) < script.index("& python -B -m pytest")
    assert script.index(io_setting) < script.index("& python -B -m pytest")
    assert script.index(utf8_setting) < script.index("& python @argsPy")
    assert script.index("phase175_r3r5_pi73_lemma57_frontier\\tests") != -1


def test_utf8_child_python_reads_existing_utf8_markdown_without_encoding(tmp_path: Path) -> None:
    report_path = tmp_path / "report.md"
    report_path.write_text("# 日本語の監査報告 — Toda Lemma 5.7\n", encoding="utf-8")
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    command = (
        "from pathlib import Path; import sys; "
        "assert sys.flags.utf8_mode == 1; "
        "assert 'Lemma 5.7' in Path(sys.argv[1]).read_text()"
    )
    result = subprocess.run(
        [sys.executable, "-B", "-c", command, str(report_path)],
        env=environment, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
