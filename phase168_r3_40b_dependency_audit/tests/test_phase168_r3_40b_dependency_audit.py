"""Tests of the read-only audit, not tests of future ordering policy."""
from dataclasses import dataclass

import pytest

from phase168_r3_40b_dependency_audit.audit_core import (
    dependency_inversions,
    find_existing_step_index,
    flattened_order,
    proof_dependency_edges,
    relative_order,
)


@dataclass(frozen=True)
class Step:
    conclusion: str
    premises: tuple = ()


@dataclass(frozen=True)
class Entry:
    step_index: int
    after_indices: tuple = ()


def test_flattened_order_keeps_every_non_suppressed_step_once():
    entries = (Entry(0, (2,)), Entry(3, ()), Entry(4, ()))
    assert flattened_order(entries, 5, {1}) == (0, 2, 3, 4)


def test_flattened_order_rejects_duplicates_and_omissions():
    with pytest.raises(ValueError, match="duplicates"):
        flattened_order((Entry(0, (1,)), Entry(1, ())), 2)
    with pytest.raises(ValueError, match="loses or adds"):
        flattened_order((Entry(0, ()),), 2)


def test_premise_mapping_uses_step_identity_or_unique_value():
    a = Step("axiom")
    b = Step("result", (a,))
    assert find_existing_step_index((a, b), a) == (0, "identity")
    edges, unresolved = proof_dependency_edges((a, b))
    assert edges == ((0, 1),)
    assert unresolved == ()
    assert find_existing_step_index((Step("axiom"), b), a) == (0, "value")


def test_ambiguous_or_missing_premise_is_not_guessed():
    a = Step("axiom")
    b = Step("result", (a,))
    edges, unresolved = proof_dependency_edges((Step("axiom"), Step("axiom"), b))
    assert edges == ()
    assert unresolved[0]["resolution"] == "ambiguous_value"
    assert find_existing_step_index((b,), a)[1] == "not_in_flattened_steps"


def test_inversions_are_separate_from_editorial_preferences():
    axiom = Step("source")
    independent = Step("generator identity")
    theorem = Step("transport", (axiom,))
    steps = (axiom, independent, theorem)
    edges, _ = proof_dependency_edges(steps)
    assert dependency_inversions(edges, (0, 1, 2)) == ()
    # Natural exposition may still prefer transport before the independent identity.
    assert relative_order(2, 1, (0, 1, 2)) == "FAIL"
    assert dependency_inversions(edges, (0, 2, 1)) == ()
    assert relative_order(2, 1, (0, 2, 1)) == "PASS"
