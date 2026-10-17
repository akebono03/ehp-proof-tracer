"""Focused trace-contract tests, no global pytest suite."""
from types import SimpleNamespace
from audit import describe_expansions


def test_describe_empty():
    assert describe_expansions(()) == []


def test_describe_rule_and_subgoals():
    item = SimpleNamespace(rule=SimpleNamespace(name="example rule"), subgoals=("A", "B"))
    assert describe_expansions((item,)) == [{"rule": "example rule", "premises": ["A", "B"]}]
