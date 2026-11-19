"""Focused structural contracts for the read-only live tracer."""
from __future__ import annotations

from dataclasses import dataclass

from phase175_r4r12r13r8r2_live_citation_trace.trace import compact, trace_model


@dataclass(frozen=True)
class FakeReference:
    label: str
    locator: str


@dataclass(frozen=True)
class FakeCitation:
    number: int
    reference: FakeReference
    step_indices: tuple[int, ...]
    assertion_ids: tuple[str, ...]
    reference_ids: tuple[str, ...]
    statement_bodies: tuple[str, ...]


@dataclass(frozen=True)
class FakeStep:
    rule: object
    inference_rule: object
    conclusion: object
    premises: tuple[object, ...]


@dataclass(frozen=True)
class FakeModel:
    status: object
    root_index: int
    steps: tuple[FakeStep, ...]
    step_citation_numbers: tuple[tuple[int, ...], ...]
    citations: tuple[FakeCitation, ...]


def test_citation_references_are_not_fabricated() -> None:
    step = FakeStep(None, None, "typed-statement", ())
    model = FakeModel(None, 0, (step,), ((7,),), (
        FakeCitation(7, FakeReference("(5.8)", "(5.8)"), (0,), (), (), ()),
    ))
    result = trace_model(model)
    assert result["target_citations"][0]["statement_bodies"] == []
    assert result["steps"][0]["citation_numbers"] == [7]
    assert result["target_citations"][0]["step_indices"] == [0]


def test_non_target_citation_is_not_misidentified() -> None:
    model = FakeModel(None, 0, (), (), (
        FakeCitation(3, FakeReference("(5.10)", "(5.10)"), (), (), (), ("source",)),
    ))
    assert trace_model(model)["target_citations"] == []


def test_compact_truncates_without_changing_short_values() -> None:
    assert compact(42) == "42"
    assert compact("abcd", 3).endswith(" [TRUNCATED]")
