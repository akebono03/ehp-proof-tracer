"""R59 focused, read-only source and conditional-sign audit."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r59_toda510_signed_semantics_audit.audit import (
    checked_git_files, inspect_semantics, signed_generator_is_identical,
)
from pathlib import Path


@pytest.mark.parametrize("sign", (-1, 1))
def test_toda510_order_two_identifies_both_signs(sign: int) -> None:
    assert signed_generator_is_identical(2, sign)


@pytest.mark.parametrize("order", (3, 4, 5, 8))
def test_not_a_general_sign_elimination(order: int) -> None:
    assert not signed_generator_is_identical(order, -1)


@pytest.mark.parametrize("order,sign", ((0, 1), (-2, 1), (2, 0), (2, 2)))
def test_invalid_signed_generator_parameters_rejected(order: int, sign: int) -> None:
    with pytest.raises(ValueError):
        signed_generator_is_identical(order, sign)


def test_existing_source_and_test_blobs_still_pinned() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(checked_git_files(root)) == 4


def test_real_toda_source_and_r35_premises_remain_coherent() -> None:
    root = Path(__file__).resolve().parents[2]
    report = inspect_semantics(root)
    assert report["printed_equation_sign_free"]
    assert report["actual_codomain_generator_order"] == 2
    assert report["positive_equals_negative_in_actual_codomain"]
    assert report["typed_image_remains_up_to_sign"]
    assert report["existing_kernel_rule_premises"] == 3
    assert report["source_given_count"] == 2
    assert report["source_reference_locators"] == ["Proposition 5.8", "(5.10)"]
    assert report["production_changes"] == 0
    assert report["new_given"] == 0
    assert report["new_mathematical_rules"] == 0
