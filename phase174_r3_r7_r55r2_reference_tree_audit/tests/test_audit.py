"""Focused, read-only regression checks for the R55R2 diagnostic logic."""
from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r55r2_reference_tree_audit.audit import (
    ancestor_contains,
    lines_containing,
    reference_snapshot,
)


@dataclass(frozen=True)
class FakeStep:
    premises: tuple[object, ...] = ()


def test_reference_snapshot_preserves_original_ids_and_bodies() -> None:
    ref = SimpleNamespace(locator="Proposition 2.7", label="Toda Proposition 2.7")
    citation = SimpleNamespace(
        number=7, reference=ref, assertion_ids=("shared:19:prop27",),
        reference_ids=("shared:19:reference",), step_indices=(12,),
        statement_bodies=(),
    )
    model = SimpleNamespace(citations=(citation,))
    observed = reference_snapshot(model, "Proposition 2.7")
    assert observed["number"] == 7
    assert observed["assertion_ids"] == ["shared:19:prop27"]
    assert observed["reference_body_present"] is False


def test_reference_snapshot_rejects_missing_or_ambiguous_locator() -> None:
    ref = SimpleNamespace(locator="(5.9)", label="Toda")
    citation = SimpleNamespace(
        number=2, reference=ref, assertion_ids=(), reference_ids=(),
        step_indices=(), statement_bodies=(),
    )
    with pytest.raises(RuntimeError, match="Expected one cited"):
        reference_snapshot(SimpleNamespace(citations=()), "(5.9)")
    with pytest.raises(RuntimeError, match="Expected one cited"):
        reference_snapshot(SimpleNamespace(citations=(citation, citation)), "(5.9)")


def test_ancestor_contains_distinguishes_unrelated_delta_proofs() -> None:
    lower = FakeStep()
    prop = FakeStep()
    upper = FakeStep((lower, prop))
    unrelated = FakeStep()
    assert ancestor_contains(upper, lower) is True
    assert ancestor_contains(upper, prop) is True
    assert ancestor_contains(upper, unrelated) is False


def test_lines_containing_does_not_add_unprinted_formulas() -> None:
    prose = "完全性より, H は単射.\n次に全射性を得る.\n□\n"
    assert lines_containing(prose, ("完全性", "\\Delta")) == [
        "完全性より, H は単射."
    ]
