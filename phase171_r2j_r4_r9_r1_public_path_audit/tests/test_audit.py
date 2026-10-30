"""Focused boundary checks: never equate the R4-R8 root with public completion."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r9_r1_public_path_audit.audit import (
    _git,
    has_exact_root_route,
    public_completion_observed,
)
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType


def _sample():
    goal = Relation("group", "cyclic", RelationType.EQUALITY)
    rule = InferenceRule(name="typed proof from prior obligations")
    left = ProofStep("cardinality", (), ProofRule.INFERENCE)
    right = ProofStep("element order", (), ProofRule.INFERENCE)
    root = ProofStep(goal, (left, right), ProofRule.INFERENCE, inference_rule=rule)
    return goal, root


def test_exact_r8_root_route_requires_same_rule_and_obligations():
    _, root = _sample()
    correct = GoalExpansion(root.inference_rule, tuple(p.conclusion for p in root.premises))
    assert has_exact_root_route((correct,), root)
    assert not has_exact_root_route((GoalExpansion(
        InferenceRule(name="unrelated"), correct.subgoals,
    ),), root)
    assert not has_exact_root_route((GoalExpansion(
        root.inference_rule, ("unrelated", "element order"),
    ),), root)


def test_public_completion_requires_real_completed_search_and_nonpartial_web():
    goal, _ = _sample()
    assert public_completion_observed(ProofSearchStatus.COMPLETE, goal, goal, False)
    assert not public_completion_observed(ProofSearchStatus.PARTIAL, goal, goal, False)
    assert not public_completion_observed(ProofSearchStatus.SEARCH_FAILED, goal, goal, False)
    assert not public_completion_observed(ProofSearchStatus.COMPLETE, goal, goal, True)
    assert not public_completion_observed(ProofSearchStatus.COMPLETE, goal, goal, None)
    assert not public_completion_observed(ProofSearchStatus.COMPLETE, object(), goal, False)


def test_audit_does_not_promote_a_non_group_or_wrong_relation():
    goal, _ = _sample()
    zero = Relation("group", "cyclic", RelationType.ZERO)
    assert not public_completion_observed(ProofSearchStatus.COMPLETE, zero, zero, False)
    assert not public_completion_observed(ProofSearchStatus.COMPLETE, goal, object(), False)


def test_no_supported_git_mutation():
    with pytest.raises(ValueError):
        _git("reset", "--hard")
    with pytest.raises(ValueError):
        _git("add", ".")


def test_missing_public_root_options_do_not_count_as_wiring():
    _, root = _sample()
    assert not has_exact_root_route((), root)
    unrelated = SimpleNamespace(rule=InferenceRule(name="typed proof from prior obligations"), subgoals=())
    assert not has_exact_root_route((unrelated,), root)
