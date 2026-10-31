"""Focused tests for read-only branch diagnostics and exception classification."""
from __future__ import annotations

import sys

import pytest

from phase165_r3_recursive_search import GoalExpansion, RegisteredGoalUnresolved
from phase171_r2j_r4_r9_r14_root_branch_diagnostic.audit import (
    CanonicalResolveTrace,
    ExactProviderObserver,
    classify_error,
    git_read,
    preflight,
    role,
    same,
    summarize,
)
from proof import Relation, RelationType
from relation_rules import equality_symmetry_inference_rule


def _targets():
    root = Relation("G", "C4", RelationType.EQUALITY)
    forward = Relation("a", "b", RelationType.EQUALITY)
    reverse = Relation("b", "a", RelationType.EQUALITY)
    return root, forward, reverse


def test_error_classification_preserves_failure_distinction():
    assert classify_error("cyclic proof dependency") == "cycle"
    assert classify_error("expected one registered derivation for X, found 0") == "no_derivation"
    assert classify_error("expected one registered derivation for X, found 3") == "ambiguous_derivations"
    assert classify_error("unknown failure") == "other_unresolved"


def test_temporary_trace_restores_original_hook_and_records_true_origin():
    root, forward, reverse = _targets()
    namespace = {"__name__": "phase165_r3_recursive_search", "RegisteredGoalUnresolved": RegisteredGoalUnresolved}
    exec(
        "def resolve(target, active):\n"
        "    if target in active:\n"
        "        raise RegisteredGoalUnresolved('cyclic proof dependency')\n"
        "    return target\n",
        namespace,
    )
    previous = sys.gettrace()
    assert previous is None
    with CanonicalResolveTrace(root, forward, reverse) as trace:
        with pytest.raises(RegisteredGoalUnresolved, match="cyclic proof dependency"):
            namespace["resolve"](forward, [root, forward])
    assert sys.gettrace() is previous
    assert trace.calls == 1
    assert trace.origin_totals["cycle"] == 1
    assert trace.exceptions[0]["origin"] is True
    assert trace.exceptions[0]["target_role"] == "forward"


def test_trace_distinguishes_origin_from_propagation():
    root, forward, reverse = _targets()
    namespace = {"__name__": "phase165_r3_recursive_search", "RegisteredGoalUnresolved": RegisteredGoalUnresolved}
    exec(
        "def resolve(target, active):\n"
        "    if target == 'outer':\n"
        "        return resolve('inner', active)\n"
        "    raise RegisteredGoalUnresolved('expected one registered derivation for inner, found 0')\n",
        namespace,
    )
    with CanonicalResolveTrace(root, forward, reverse) as trace:
        with pytest.raises(RegisteredGoalUnresolved):
            namespace["resolve"]("outer", ["outer"])
    assert trace.calls == 2
    assert trace.origin_totals["no_derivation"] == 1
    assert trace.exception_totals["no_derivation"] >= 2
    assert any(not item["origin"] for item in trace.exceptions)


def test_provider_observer_preserves_candidate_identity_and_order():
    root, forward, reverse = _targets()
    first = GoalExpansion(equality_symmetry_inference_rule(), (forward,))
    second = GoalExpansion(equality_symmetry_inference_rule(), (reverse,))
    original = (first, second)

    def factory(*args, **kwargs):
        def provider(goal):
            return original
        return provider

    watcher = ExactProviderObserver(factory, root, forward, reverse)
    result = watcher(proof_target=root)(reverse)
    assert result is original
    assert result[0] is first
    assert result[1] is second
    assert watcher.providers == 1
    assert watcher.events[0]["count"] == 2
    assert watcher.events[0]["role"] == "reverse"
    assert watcher(proof_target=forward)(reverse) is original
    assert watcher.providers == 1


def test_goal_identity_and_report_classification_do_not_claim_completion():
    root, forward, reverse = _targets()
    assert same(root, root)
    assert not same(root, "G")
    assert role(root, root, forward, reverse) == "root"
    assert role(reverse, root, forward, reverse) == "reverse"
    assert summarize({"public_status": "partial", "origin_counts": {"cycle": 1}}) == "ROOT_PARTIAL_WITH_CYCLE_ONLY_OBSERVED"
    assert summarize({"public_status": "partial", "origin_counts": {"cycle": 2, "no_derivation": 1}}) == "ROOT_PARTIAL_WITH_ZERO_DERIVATION_SUBGOALS"
    assert summarize({"public_status": "partial", "origin_counts": {"ambiguous_derivations": 1}}) == "ROOT_PARTIAL_AMBIGUITY_OBSERVED"


def test_preflight_is_read_only_and_matches_r11_provider():
    assert preflight()["provider_blob"] == "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"
    with pytest.raises(ValueError, match="read-only"):
        git_read("reset", "--hard")
