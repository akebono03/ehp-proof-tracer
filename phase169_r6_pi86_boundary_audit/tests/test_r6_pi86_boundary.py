"""R6 read-only diagnostic checks for the existing pi_8^6 partial proof."""
from __future__ import annotations

import pytest

from phase169_r6_pi86_boundary_audit.audit import inspect, summary_markdown


@pytest.fixture(scope="module")
def observation():
    return inspect()


def test_r6_exposes_real_screened_source_boundary(observation):
    assert observation["candidate_count"] == 1
    assert observation["prior_pi64"]["relation_available_as_db_goal"]
    assert observation["screened_toda45"]
    assert observation["pi86_target_citation"]


def test_r6_contrasts_executing_and_goal_only_expansions(observation):
    for key in (
        "existing_r3o_options", "existing_r5b_options", "existing_r57_options",
        "goal_only_one_step_options", "goal_only_two_step_options",
    ):
        assert type(observation[key]) is int and observation[key] >= 0
    assert observation["goal_only_two_step_options"] == 0


def test_r6_web_does_not_promote_partial_proof(observation):
    assert observation["web_partial"] == (observation["pi86_status"] != "complete")
    assert observation["web_key"] in ("generic-complete-proof", "generic-partial-proof")
    if observation["pi86_status"] != "complete":
        assert not observation["proof_tree_verified"]
        assert observation["pi86_open_goals"] > 0


def test_r6_no_claim_of_finished_future_phase(observation):
    assert observation["production_modified"] is False
    assert observation["full_pytest_run"] is False
    narrative = summary_markdown(observation)
    assert "Goal-only" in narrative
    assert "GIVEN" in narrative
