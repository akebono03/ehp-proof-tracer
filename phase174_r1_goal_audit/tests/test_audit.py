"""Pure tests for the Phase 174 R1 audit serializers."""
from types import SimpleNamespace

from phase174_r1_goal_audit.audit import (
    PRIOR_OPEN_GOALS,
    TARGETS,
    result_record,
    statement_record,
    proposal_record,
    step_record,
)


def test_target_set_and_prior_counts_are_explicit():
    assert TARGETS == ((5, 3), (4, 8), (4, 9))
    assert [PRIOR_OPEN_GOALS[target] for target in TARGETS] == [3, 3, 2]


def test_statement_record_preserves_type_and_full_representation():
    statement = SimpleNamespace(lhs="source", rhs="target")
    record = statement_record(statement)
    assert record["type"] == "SimpleNamespace"
    assert record["lhs"]["repr"] == "'source'"
    assert record["rhs"]["repr"] == "'target'"
    assert record["repr"] == repr(statement)


def test_result_record_preserves_duplicate_internal_goals():
    result = SimpleNamespace(
        status=SimpleNamespace(value="search_failed"),
        structure_status=SimpleNamespace(value="unknown"),
        conclusion=None,
        open_goals=("same", "same", "another"),
        proven_steps=(),
        diagnostics=("unresolved",),
        references=(),
        abstract_structure=None,
    )
    record = result_record(result)
    assert record["open_goal_count"] == 3
    assert [item["repr"] for item in record["open_goals"]] == [
        "'same'", "'same'", "'another'",
    ]
    assert record["abstract_certificate"] is None


def test_step_record_preserves_premises():
    premise = SimpleNamespace(
        rule=SimpleNamespace(value="given"),
        conclusion="source",
    )
    step = SimpleNamespace(
        rule=SimpleNamespace(value="inference"),
        conclusion="target",
        premises=(premise,),
        inference_rule=SimpleNamespace(name="checked_rule"),
    )
    record = step_record(step)
    assert record["premise_count"] == 1
    assert record["premises"][0]["conclusion"]["repr"] == "'source'"
    assert record["inference_rule_name"] == "checked_rule"


def test_proposal_record_never_confuses_subgoals_with_proofs():
    proposal = SimpleNamespace(
        rule=SimpleNamespace(name="typed_rule"),
        subgoals=("open_one", "open_two"),
    )
    record = proposal_record(proposal)
    assert record["rule"] == "typed_rule"
    assert record["subgoal_count"] == 2
    assert record["subgoals"][0]["repr"] == "'open_one'"
