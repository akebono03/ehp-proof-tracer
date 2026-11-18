"""Focused contracts for the read-only typed mismatch trace."""
from __future__ import annotations

from dataclasses import dataclass

from phase175_r4r12r10r1r3_orientation_type_diagnostic.audit import differences, describe_tree


@dataclass(frozen=True)
class Point:
    x: object
    y: object


def test_equal_objects_have_no_differences() -> None:
    assert differences(Point(1, (2, 3)), Point(1, (2, 3))) == []


def test_different_class_preserved_as_mismatch() -> None:
    detail = differences(Point(1, 2), (1, 2))
    assert len(detail) == 1
    assert detail[0]["left_type"] == "Point"
    assert detail[0]["right_type"] == "tuple"


def test_nested_difference_reports_exact_field_path() -> None:
    detail = differences(Point(1, Point(2, 3)), Point(1, Point(2, 4)))
    assert len(detail) == 1
    assert detail[0]["path"] == "root.y.y"


def test_description_preserves_nested_types_and_values() -> None:
    detail = describe_tree(Point("a", (3, 4)))
    assert detail["type"].endswith(".Point")
    assert detail["children"][0]["repr"] == "'a'"
    assert len(detail["children"][1]["children"]) == 2
