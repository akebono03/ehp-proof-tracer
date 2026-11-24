"""Tests of observational mechanics only; no mathematical proofs are fabricated."""
from types import SimpleNamespace

import pytest

from phase176_r3r42_root_backward_frontier_audit.audit import (
    call_records, classify, option_record, wrap_provider,
)


def test_observer_preserves_original_tuple_and_order():
    original = (SimpleNamespace(rule=SimpleNamespace(name="rule B"), subgoals=("b",)),
                SimpleNamespace(rule=SimpleNamespace(name="rule A"), subgoals=("a",)))
    invoked = []
    observed = []

    def provider(goal):
        invoked.append(goal)
        return original

    wrapper = wrap_provider(provider, observed)
    assert wrapper("root") is original
    assert invoked == ["root"]
    assert observed == [("root", original)]
    assert [x["rule"] for x in call_records(observed, "root")[0]["options"]] == ["rule B", "rule A"]
    assert call_records(observed, "other") == []


def test_empty_call_is_distinct_from_no_call():
    observed = []
    wrapper = wrap_provider(lambda goal: (), observed)
    assert wrapper("root") == ()
    assert call_records(observed, "root") == [{"count": 0, "options": []}]
    assert call_records(observed, "unvisited") == []


def test_observer_does_not_mask_exception():
    observed = []

    def provider(goal):
        raise ValueError("original failure")

    with pytest.raises(ValueError, match="original failure"):
        wrap_provider(provider, observed)("root")
    assert observed == []


@pytest.mark.parametrize("status,root,gates,cyclic,expected", [
    ("complete", [], [], [], "ROOT_COMPLETE"),
    ("partial", [], [], [], "ROOT_PROVIDER_NOT_REACHED"),
    ("partial", [{"count": 0}], [{"before": 2, "after": 0}], [], "ROOT_CANDIDATES_FILTERED"),
    ("partial", [{"count": 0}], [{"before": 0, "after": 0}], [], "ROOT_NO_CANDIDATES"),
    ("partial", [{"count": 3}], [{"before": 3, "after": 3}], [{"count": 0}], "CYCLIC_CHILD_NO_CANDIDATES"),
    ("partial", [{"count": 3}], [], [{"count": 2}], "ROOT_CANDIDATES_UNVERIFIED"),
])
def test_classification(status, root, gates, cyclic, expected):
    assert classify(status, root, gates, cyclic) == expected


def test_record_preserves_all_subgoals():
    item = SimpleNamespace(rule=SimpleNamespace(name="test"), subgoals=("one", "two"))
    assert option_record(item) == {"rule": "test", "subgoals": ["'one'", "'two'"]}
