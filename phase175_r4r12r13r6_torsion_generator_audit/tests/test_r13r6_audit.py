"""Focused tests for read-only typed-generator diagnostics."""
from __future__ import annotations

from dataclasses import dataclass

from phase175_r4r12r13r6_torsion_generator_audit.audit import shape, inspect


@dataclass(frozen=True)
class Sample:
    item: int


def test_shape_exposes_dataclass_field_and_value() -> None:
    actual = shape(Sample(3))
    assert actual["type"] == "Sample"
    assert actual["fields"]["item"]["repr"] == "3"


def test_report_keeps_unproved_equivalence_false() -> None:
    result = inspect()
    assert result["equivalence_proved"] is False
    assert result["new_given"] == 0
    assert result["new_mathematical_rules"] == 0
    assert result["production_code_modified"] is False
    assert result["group_proof_complete"] is False


def test_report_records_both_torsion_representations() -> None:
    result = inspect()
    assert result["db_torsion_generator"]["repr"]
    assert result["toda58_torsion_expression"]["repr"]
    assert result["free_generator_exact_equality"] is True
    assert result["cited58_screened"] is True
