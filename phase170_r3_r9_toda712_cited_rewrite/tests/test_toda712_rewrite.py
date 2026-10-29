"""Focused source, typed equality, provenance, negative and Web tests."""
from dataclasses import replace
from types import SimpleNamespace

import pytest

from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase168_r2_toda52_transport import (
    _toda52_cited_generator_equality, _toda52_group_presentation_matches,
    expand_toda52_finite_cyclic_goal,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase170_r3_r9_toda712_cited_rewrite.source712 import (
    ASSERT_ID, REF_ID, verified_toda712_generator_equality,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def _goal_and_source():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=12)
    assert len(goals) == 1
    source = exact_prior_database_result(3, 11)
    assert source is not None
    return bridge, goals[0], source


def test_r3r9_cited_source_and_registered_typed_equality():
    relation, position = verified_toda712_generator_equality()
    bridge, goal, source = _goal_and_source()
    records = [a for a in bridge.registry._assertions.values() if a.assertion_id.endswith(ASSERT_ID)]
    assert len(records) == 1
    assertion = records[0]
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert assertion.content == relation
    ref = bridge.registry.reference(assertion.reference_id)
    assert ref.locator == "(7.12)" and ref.publication_position == position
    assert not _toda52_group_presentation_matches(source, goal)
    assert _toda52_group_presentation_matches(source, goal, equality=relation)


def test_r3r9_requires_citation_as_third_subgoal():
    equality, _ = verified_toda712_generator_equality()
    _, goal, source = _goal_and_source()
    theorem = Toda52UniversalStatement()
    assert expand_toda52_finite_cyclic_goal(goal, (theorem,)) == ()
    options = expand_toda52_finite_cyclic_goal(goal, (theorem, equality))
    assert len(options) == 1
    expansion = options[0]
    assert expansion.subgoals == (source, theorem, equality)
    assert expansion.rule.match_guard(tuple(SimpleNamespace(conclusion=x) for x in expansion.subgoals), {})
    assert not expansion.rule.match_guard((SimpleNamespace(conclusion=source), SimpleNamespace(conclusion=theorem)), {})
    reversed_relation = Relation(equality.rhs, equality.lhs, RelationType.EQUALITY)
    assert _toda52_cited_generator_equality(equality.lhs, equality.rhs, reversed_relation)


def test_r3r9_forgeries_and_wrong_relation_are_rejected():
    equality, _ = verified_toda712_generator_equality()
    _, goal, source = _goal_and_source()
    theorem = Toda52UniversalStatement()
    bad = Relation(equality.lhs, equality.lhs, RelationType.EQUALITY)
    assert not _toda52_group_presentation_matches(source, goal, equality=bad)
    assert expand_toda52_finite_cyclic_goal(goal, (theorem, bad)) == ()
    options = expand_toda52_finite_cyclic_goal(goal, (theorem, equality))
    guard = options[0].rule.match_guard
    assert not guard((SimpleNamespace(conclusion=source), SimpleNamespace(conclusion=theorem), SimpleNamespace(conclusion=bad)), {})
    assert not guard((SimpleNamespace(conclusion=goal), SimpleNamespace(conclusion=theorem), SimpleNamespace(conclusion=equality)), {})


def test_r3r9_prior_db_group_and_source_are_not_a_completed_proof():
    equality, _ = verified_toda712_generator_equality()
    _, goal, _ = _goal_and_source()
    # An equality by itself is insufficient: (5.2) must be in the screened context.
    assert expand_toda52_finite_cyclic_goal(goal, (equality,)) == ()


def test_r3r9_actual_pi14_search_and_web_trust_boundary():
    from phase165_r52_partial_proof import ProofSearchStatus
    from web_group_proof import build_standard_web_group_proof_view
    result = search_group_from_registered_goal(n=2, k=12)
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(result.proven_steps) >= 4
    assert any(step.rule is ProofRule.GIVEN and step.inference_rule is not None
               and step.inference_rule.literature_reference is not None
               and step.inference_rule.literature_reference.locator == "(7.12)"
               for step in result.proven_steps)
    view = build_standard_web_group_proof_view(
        n=2, k=12, max_depth=2, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof" and view.partial_result is False
    assert view.steps and view.rendered_lines
