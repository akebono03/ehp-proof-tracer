from __future__ import annotations

import csv
from pathlib import Path

import audit_phase155_r2b as r2b


def _finding(**overrides):
    data = dict(
        finding_id="R2-00001",
        test_id="tests/test_x.py::test_x",
        file="tests/test_x.py",
        function="test_x",
        line=10,
        phase="154",
        r1_category="current_contract",
        status="stale_candidate_high",
        contract="ascii_prose_punctuation",
        assertion_kind="positive_literal",
        expected_literal="まず、",
        reason="candidate",
    )
    data.update(overrides)
    return r2b.R2Finding(**data)


def test_load_r2_high_findings_filters_non_high(tmp_path: Path):
    path = tmp_path / "r2.csv"
    fieldnames = [
        "finding_id", "test_id", "file", "function", "line", "phase",
        "r1_category", "status", "contract", "assertion_kind",
        "expected_literal", "reason",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            "finding_id": "R2-1",
            "test_id": "tests/test_x.py::test_x",
            "file": "tests/test_x.py",
            "function": "test_x",
            "line": "1",
            "phase": "154",
            "r1_category": "current_contract",
            "status": "stale_candidate_high",
            "contract": "x",
            "assertion_kind": "positive_literal",
            "expected_literal": "x",
            "reason": "x",
        })
        writer.writerow({
            "finding_id": "R2-2",
            "test_id": "tests/test_y.py::test_y",
            "file": "tests/test_y.py",
            "function": "test_y",
            "line": "2",
            "phase": "150",
            "r1_category": "current_contract",
            "status": "contract_sensitive_review",
            "contract": "x",
            "assertion_kind": "count",
            "expected_literal": "2",
            "reason": "x",
        })
    rows = r2b.load_r2_high_findings(path)
    assert len(rows) == 1
    assert rows[0].test_id == "tests/test_x.py::test_x"


def test_unique_test_ids_deduplicates_findings():
    items = [
        _finding(finding_id="A"),
        _finding(finding_id="B"),
        _finding(finding_id="C", test_id="tests/test_y.py::test_y"),
    ]
    assert r2b.unique_test_ids(items) == (
        "tests/test_x.py::test_x",
        "tests/test_y.py::test_y",
    )


def test_assertion_failure_is_confirmed_stale():
    finding = _finding()
    execution = r2b.TestExecution(
        test_id=finding.test_id,
        outcome="failed",
        duration_seconds=0.1,
        longrepr="AssertionError: assert old in rendered",
    )
    cls, _ = r2b.classify(finding, execution)
    assert cls == r2b.CLASS_CONFIRMED_STALE


def test_passing_phase154_is_current_contract():
    finding = _finding()
    execution = r2b.TestExecution(
        test_id=finding.test_id,
        outcome="passed",
        duration_seconds=0.1,
        longrepr="",
    )
    cls, _ = r2b.classify(finding, execution)
    assert cls == r2b.CLASS_CURRENT_CONTRACT


def test_passing_historical_category_is_historical_compatibility():
    finding = _finding(
        phase="140",
        r1_category="historical_compatibility",
    )
    execution = r2b.TestExecution(
        test_id=finding.test_id,
        outcome="passed",
        duration_seconds=0.1,
        longrepr="",
    )
    cls, _ = r2b.classify(finding, execution)
    assert cls == r2b.CLASS_HISTORICAL_COMPATIBILITY


def test_passing_older_unclassified_candidate_is_false_positive():
    finding = _finding(
        phase="140",
        r1_category="audit_only",
    )
    execution = r2b.TestExecution(
        test_id=finding.test_id,
        outcome="passed",
        duration_seconds=0.1,
        longrepr="",
    )
    cls, _ = r2b.classify(finding, execution)
    assert cls == r2b.CLASS_FALSE_POSITIVE


def test_non_assertion_failure_is_inconclusive():
    finding = _finding()
    execution = r2b.TestExecution(
        test_id=finding.test_id,
        outcome="failed",
        duration_seconds=0.1,
        longrepr="RuntimeError: unrelated failure",
    )
    cls, _ = r2b.classify(finding, execution)
    assert cls == r2b.CLASS_INCONCLUSIVE
