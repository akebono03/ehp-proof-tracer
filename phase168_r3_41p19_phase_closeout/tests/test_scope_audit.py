"""No test is silently ignored by the R3-41P19 active-suite audit."""
from __future__ import annotations

from pathlib import Path

from phase168_r3_41p19_phase_closeout.scope_audit import (
    diagnostic_lines, generate_report, missing_test_dependencies,
)


def test_missing_helper_is_identified_without_importing_legacy_code(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_current.py").write_text(
        "from tests.test_retired import _legacy_helper\n", encoding="utf-8"
    )
    archived = tmp_path / "archive" / "phases" / "phase123" / "tests"
    archived.mkdir(parents=True)
    (archived / "test_retired.py").write_text("def _legacy_helper(): pass\n", encoding="utf-8")
    rows = missing_test_dependencies(tmp_path)
    assert len(rows) == 1
    assert rows[0]["module"] == "tests.test_retired"
    assert rows[0]["archived"] == ["archive/phases/phase123/tests/test_retired.py"]


def test_existing_helper_is_not_false_positive(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_present.py").write_text("def _helper(): pass\n", encoding="utf-8")
    (tests / "test_importer.py").write_text(
        "from tests.test_present import _helper\n", encoding="utf-8"
    )
    assert missing_test_dependencies(tmp_path) == []


def test_nonzero_pytest_never_reports_full_suite_pass(tmp_path):
    (tmp_path / "tests").mkdir()
    out = tmp_path / "audit" / "output"
    out.mkdir(parents=True)
    (out / "pytest_full_stdout.log").write_text(
        "ERROR collecting tests/test_old.py\n1 error in 1.00s\n", encoding="utf-8"
    )
    report = generate_report(tmp_path, out, 2)
    assert report["status"] == "ACTIVE_SUITE_INCOMPLETE"
    assert not report["full_suite_certified"]
    assert "ERROR collecting tests/test_old.py" in diagnostic_lines(
        (out / "pytest_full_stdout.log").read_text(encoding="utf-8")
    )
    assert (out / "active_suite_diagnostics.md").is_file()
