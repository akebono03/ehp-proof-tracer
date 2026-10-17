"""Focused, pure audit checks. No repository-wide test execution."""
from __future__ import annotations
from types import SimpleNamespace

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r25_web_order_diagnostic.phase165_r12_r25_web_order_diagnostic import describe, inspect_order, summarize_result
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from proof import Relation


def test_describe_retains_concrete_generator_details():
    relation = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, "eta3"))
    data = describe(relation)
    assert data["lhs"]["fields"]["group_dimension"]["value"] == 4
    assert data["rhs"]["fields"]["generator"]["value"] == "eta3"


def test_summary_never_promotes_open_goals_to_proofs():
    result = make_partial_proof_result(n=3, k=1, status=ProofSearchStatus.SEARCH_FAILED,
                                       open_goals=("missing",), diagnostics=("no proof",))
    report = summarize_result(result)
    assert report["proven_step_count"] == 0
    assert report["open_goals"] == ["'missing'"]
    assert report["conclusion"] == "None"


def test_goal_shape_difference_remains_visible():
    left = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, "η_3"))
    right = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, "η₃"))
    assert left != right
    assert describe(left) != describe(right)
