"""Focused regression checks: proposed lower group is a Goal, never a GIVEN."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase165_r52_r27_r5_literature import _toda45_universal_statement
from phase169_r3o_stable_composite_rule import expand_cited_toda45_composite_transport
from phase169_r5a_pi75_premise_diagnostic.audit import summarize


def test_r5a_lower_and_upper_remain_db_goals_only():
    lower = database_structured_group_goal_candidates(n=4, k=2)
    upper = database_structured_group_goal_candidates(n=5, k=2)
    assert len(lower) == len(upper) == 1
    assert lower[0].lhs == TodaPrimaryGroup(6, 4)
    assert upper[0].lhs == TodaPrimaryGroup(7, 5)


def test_r5a_source_goal_can_form_a_candidate_but_not_proof():
    lower = database_structured_group_goal_candidates(n=4, k=2)[0]
    upper = database_structured_group_goal_candidates(n=5, k=2)[0]
    no_source = expand_cited_toda45_composite_transport(
        upper, (_toda45_universal_statement(),),
    )
    with_goal = expand_cited_toda45_composite_transport(
        upper, (lower, _toda45_universal_statement()),
    )
    assert not no_source
    assert len(with_goal) == 1
    assert with_goal[0].subgoals[0] == lower
    assert len(with_goal[0].subgoals) == 3


def test_r5a_stable_range_not_bypassed_for_pi64():
    lower = database_structured_group_goal_candidates(n=3, k=2)[0]
    upper = database_structured_group_goal_candidates(n=4, k=2)[0]
    assert expand_cited_toda45_composite_transport(
        upper, (lower, _toda45_universal_statement()),
    ) == ()


def test_r5a_summary_cannot_claim_proof_completion_for_failed_subgoals():
    blank = {"proved": False, "proof_rule": None, "steps_in_subtree": 0,
             "error": "unresolved", "unresolved": ["MapIsomorphism"]}
    report = {
        "head": "fixture", "target_citation": "a:1", "prior_eligibility": False,
        "prior_reason": "not_prior", "prior_source_citation": None,
        "screened_lower_given": False, "screened_toda45": True,
        "actual_cited_options": 0, "goal_only_options": 1,
        "attempts": {"lower_group_pi6_4": blank},
    }
    text = summarize(report)
    assert "unresolved" in text
    assert "Goal-only" in text
    assert "complete" not in text
