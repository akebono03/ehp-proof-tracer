"""Focused pure contracts, plus production-backed execution from run.ps1."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from types import SimpleNamespace

import pytest

from phase175_r4r12r13r8r6_binding_contract import audit


class FakeRule(Enum):
    GIVEN = auto()
    INFERENCE = auto()


class FakeOrigin(Enum):
    FIXED_STATEMENT = auto()
    PROOF_INTERNAL = auto()


@dataclass(frozen=True)
class FakeCitation:
    number: int
    reference: object
    step_indices: tuple[int, ...]
    assertion_ids: tuple[str, ...]
    reference_ids: tuple[str, ...]
    statement_bodies: tuple[str, ...]


class FakeRegistry:
    def __init__(self, origin, content):
        self.value = SimpleNamespace(reference_id="source-1", origin=origin, content=content)

    def assertion(self, assertion_id: str):
        assert assertion_id == "assertion-1"
        return self.value


def example_model(*, body=("$x=y$.",), cited_child=False, multiple=False):
    source = SimpleNamespace(rule=FakeRule.GIVEN, conclusion="source", premises=())
    other = SimpleNamespace(rule=FakeRule.GIVEN, conclusion="other", premises=())
    child = SimpleNamespace(rule=FakeRule.INFERENCE, conclusion="derived",
                            premises=(source, other) if multiple else (source,))
    steps = (source, other, child) if multiple else (source, child)
    indices = (0, len(steps) - 1) if cited_child else (0,)
    citation = FakeCitation(1, SimpleNamespace(locator="(5.8)"), indices,
                            ("assertion-1",), ("source-1",), body)
    mapping = ((1,), (), (1,)) if multiple and cited_child else (
        ((1,), (), ()) if multiple else ((1,), (1,) if cited_child else ())
    )
    return SimpleNamespace(steps=steps, citations=(citation,), step_citation_numbers=mapping)


def test_registered_fixed_source_with_body_is_accepted():
    model = example_model()
    row = audit.inspect_binding(model, FakeRegistry(FakeOrigin.FIXED_STATEMENT, "source"))
    assert row["registered_fixed_body_gaps"] == []
    assert row["citations"][0]["direct_consumers"][0]["child_cited"] is False


def test_registered_fixed_source_without_body_is_a_gap():
    model = example_model(body=())
    row = audit.inspect_binding(model, FakeRegistry(FakeOrigin.FIXED_STATEMENT, "source"))
    assert row["registered_fixed_body_gaps"][0]["issue"] == "REGISTERED_FIXED_BODY_MISSING"


def test_multiple_premise_does_not_inherit_direct_given_citation():
    model = example_model(multiple=True)
    row = audit.inspect_binding(model, FakeRegistry(FakeOrigin.FIXED_STATEMENT, "source"))
    assert row["citations"][0]["direct_consumers"] == []


def test_bad_step_reverse_link_fails_closed():
    model = example_model()
    model.step_citation_numbers = ((), ())
    with pytest.raises(RuntimeError, match="CITATION_STEP_DISAGREEMENT"):
        audit.inspect_binding(model, FakeRegistry(FakeOrigin.FIXED_STATEMENT, "source"))


def test_public_prefix_guard_tests_heading_formula_and_yori_separately():
    good = ("[R3] (5.11).", r"$\Delta(\eta_9)$.", "[R3]より,",
            "[R7] (5.8).", r"$\Delta(\iota_9)$.", "[R7]より,")
    assert audit.check_public_lines(good, r3=3, r7=7)["pass"]
    assert not audit.check_public_lines(good[:-1], r3=3, r7=7)["pass"]
    assert not audit.check_public_lines(("[R3]より,", "[R7]より,"), r3=3, r7=7)["pass"]


def test_target_scope_and_source_contract_are_fixed():
    assert audit.TARGETS == ((5, 4), (6, 5), (7, 5))
    assert len(audit.REQUIRED_FILES) == 6
