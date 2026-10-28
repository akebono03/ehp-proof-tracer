"""Focused non-mutating tests of the Phase 170 R1 audit utilities."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def load_audit():
    path = Path(__file__).resolve().parents[1] / "audit.py"
    spec = importlib.util.spec_from_file_location("phase170_r1_audit_contract", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_core_cases_are_exactly_low_two_stem():
    audit = load_audit()
    assert audit.CORE_CASES == ((2, 2), (3, 2), (4, 2))
    assert all(n >= 2 and k >= 1 for n, k in audit.OTHER_STEM_CASES)


def test_step_graph_uses_actual_premises_not_conclusion_string():
    audit = load_audit()
    leaf = SimpleNamespace(premises=(), conclusion="source", rule=SimpleNamespace(name="GIVEN"), inference_rule=None)
    root = SimpleNamespace(premises=(leaf,), conclusion="target", rule=SimpleNamespace(name="INFERENCE"),
                           inference_rule=SimpleNamespace(name="typed_rule", literature_reference=None))
    rows, problems = audit.step_graph((leaf, root), ((), (2,)))
    assert not problems
    assert rows[0]["premises"] == []
    assert rows[1]["premises"] == [0]
    assert rows[1]["citation_numbers"] == [2]


def test_missing_premise_fails_reporting_closed():
    audit = load_audit()
    unknown = SimpleNamespace(premises=(), conclusion="unknown", rule=None, inference_rule=None)
    root = SimpleNamespace(premises=(unknown,), conclusion="root", rule=None, inference_rule=None)
    rows, problems = audit.step_graph((root,), ())
    assert rows[0]["premises"] == [None]
    assert any("missing/ambiguous" in message for message in problems)


def test_incomplete_status_cannot_be_promoted_by_trust():
    audit = load_audit()
    assert audit.classify("partial", "PASS") == "PARTIAL"
    assert audit.classify("complete", "FAIL") == "COMPLETE_NOT_CERTIFIED"
    assert audit.classify("complete", "PASS") == "COMPLETE_TRUSTED"


def test_output_report_must_be_outside_repository():
    audit = load_audit()
    assert audit.REVIEWED_BLOBS["phase165_r55_nk_only_goal.py"]
    assert len(audit.CORE_CASES) == 3


def test_csv_dimensions_support_spreadsheet_decimal_notation():
    audit = load_audit()
    assert audit.same_integer_cell("3", 3)
    assert audit.same_integer_cell("3.0", 3)
    assert not audit.same_integer_cell("3.5", 3)
    assert not audit.same_integer_cell("", 3)
