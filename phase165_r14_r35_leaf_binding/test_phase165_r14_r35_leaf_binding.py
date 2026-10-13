from pathlib import Path

import pytest

from phase165_r14_r35_leaf_binding import (
    backward_leaf_goals, known_source_candidates, audit_r35,
)
from phase165_r14_r34_backward_search import pi32_goal, trace_goal_frontier

TEX = Path(__file__).with_name("toda_51_complete.tex")


def test_r34_leaf_goals_remain_identical():
    leaves = backward_leaf_goals(pi32_goal())
    assert len(leaves) == trace_goal_frontier(pi32_goal())["unresolved_leaf_count"]
    assert [repr(x) for x in leaves] == trace_goal_frontier(pi32_goal())["unresolved_leaves"]


def test_known_sources_have_distinct_grounded_proposals():
    candidates = known_source_candidates(TEX)
    assert len(candidates) == 6
    assert {c.locator for c in candidates} == {"(5.1)", "Proposition 4.2", "Proposition 5.1"}
    assert all(c.certification == "unverified_source_claim" for c in candidates)


def test_leaf_matching_never_certifies():
    report = audit_r35(TEX)
    assert len(report["leaf_bindings"]) == report["total_unresolved_leaves"]
    assert all(not row["strict_eligible"] for row in report["leaf_bindings"])
    assert not report["strict_registry_proof_created"]
    assert report["registry_assertions_promoted"] == 0


def test_source_mapping_counts_consistent():
    report = audit_r35(TEX)
    assert (report["source_candidate_match_count"] + report["remaining_review_count"]
            == report["total_unresolved_leaves"])


def test_no_goal_fabrication():
    report = audit_r35(TEX)
    r34 = trace_goal_frontier(pi32_goal())
    assert [x["goal"] for x in report["leaf_bindings"]] == r34["unresolved_leaves"]


def test_limit_is_fail_closed():
    with pytest.raises(ValueError):
        backward_leaf_goals(pi32_goal(), 1)
