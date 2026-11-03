"""Real project tests: symbolic obligations, never fabricated proof steps."""
from __future__ import annotations

import pytest

from phase173_r4_r15r2_generator_obligation_audit.audit import (
    _factors,
    _select_right_images,
    inspect_k,
)
from expression import Composition, GeneratorSymbol, HomotopyElement


@pytest.mark.parametrize("k", (4, 7, 8, 31))
def test_registered_frontiers_are_described_without_claiming_proof(k: int) -> None:
    row = inspect_k(k)
    assert row["k"] == k
    assert row["abstract_compatible"] is True
    assert row["proof_completed_by_this_audit"] is False
    assert row["new_proof_steps"] == 0
    assert row["new_given_assertions"] == 0


def test_k31_has_four_plus_four_source_components() -> None:
    row = inspect_k(31)
    assert row["left_component_count"] == 4
    assert row["right_component_count"] == 4
    assert row["target_component_count"] == 8
    assert len(row["left_obligations"]) == 4
    assert all(item["factorization"] for item in row["left_obligations"])
    assert row["all_named_generators_proved"] is False


def test_k31_right_images_are_not_assumed_matched() -> None:
    row = inspect_k(31)
    matched = set(row["right_matched_target_indices"])
    pending = set(row["right_pending_indices"])
    residual = set(row["residual_target_indices"])
    assert not (matched & residual)
    assert len(matched) + len(residual) == 8
    assert len(matched) + len(pending) == 4


def test_composition_factorization_preserves_factor_objects() -> None:
    first = HomotopyElement(
        name="a", dimension=3, source=5, target=3,
        generator=GeneratorSymbol(family="a"),
    )
    second = HomotopyElement(
        name="b", dimension=5, source=6, target=5,
        generator=GeneratorSymbol(family="b"),
    )
    third = HomotopyElement(
        name="c", dimension=6, source=7, target=6,
        generator=GeneratorSymbol(family="c"),
    )
    expression = Composition(first, Composition(second, third))
    assert _factors(expression) == (first, second, third)


def test_empty_right_images_leave_all_targets_residual() -> None:
    target = (object(), object())
    matched, pending, residual = _select_right_images((), target)
    assert matched == ()
    assert pending == ()
    assert residual == (0, 1)
