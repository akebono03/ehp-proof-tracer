from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

from phase176_r3r18_root_child_frontier.audit import summarize


@dataclass(frozen=True)
class FakeOption:
    rule: object
    subgoals: tuple


def test_empty_candidates():
    assert summarize(()) == {"count": 0, "truncated": False, "items": []}


def test_candidate_children_are_visible():
    row = summarize((FakeOption(SimpleNamespace(name="rule1"), ("A", "B")),))
    assert row["count"] == 1
    assert row["items"][0]["subgoals"] == ["'A'", "'B'"]


def test_candidate_limit_is_explicit():
    row = summarize(tuple(FakeOption(SimpleNamespace(name="r"), ()) for _ in range(3)), 2)
    assert row["count"] == 3
    assert row["truncated"] is True
    assert len(row["items"]) == 2
