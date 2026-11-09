"""Focused real-adoption and fail-closed inference-contract tests for R40."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, exact_prior_database_result
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
    RULE_NAME, adopted_prior_zero_image_rule, expand_adopted_prior_zero_image,
    verified_prior_zero_image_inputs,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)
from homotopy_groups import FiniteCyclicGroup


def fixture():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    relation = exact_prior_database_result(5, 5)
    assert type(relation) is Relation
    assert relation.lhs == TodaPrimaryGroup(10, 5)
    delta = TodaSuspensionMap(relation.lhs, TodaPrimaryGroup(11, 6))
    goal = ImageZeroStatement(delta)
    db = admitted_db_step(relation, proof_target=root, bridge=bridge)
    assert isinstance(db, ProofStep)
    zero = GeneratorImage(delta, relation.rhs.generator, Zero())
    independent = ProofStep(
        conclusion=zero, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only independent generator-zero fixture"),
    )
    return root, bridge, relation, goal, db, independent


def test_adopted_earlier_db_and_inferred_zero_have_one_general_candidate():
    root, bridge, relation, goal, db, independent = fixture()
    assert verified_prior_zero_image_inputs(goal, relation, proof_target=root, bridge=bridge) == (
        relation, independent.conclusion,
    )
    result = expand_adopted_prior_zero_image(goal, relation, proof_target=root, bridge=bridge)
    assert len(result) == 1
    assert result[0].rule.name == RULE_NAME
    assert result[0].subgoals == (relation, independent.conclusion)
    assert all(not isinstance(item, ProofStep) for item in result[0].subgoals)
    matches = find_inference_matches_for_rule(result[0].rule, (db, independent))
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == (db, independent)
    assert db.rule is ProofRule.GIVEN
    assert db.note == "ADOPTED_DATABASE_PRIOR; independent reference not asserted"


def test_historical_r6_does_not_accept_db_given_and_remains_unchanged():
    root, bridge, relation, goal, db, independent = fixture()
    old = expand_zero_image_from_cyclic_generator(goal, relation)
    assert len(old) == 1
    assert find_inference_matches_for_rule(old[0].rule, (db, independent)) == ()


def test_forged_db_step_with_different_source_identity_is_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    forged = replace(db, inference_rule=InferenceRule(name="test-only forged DB citation"))
    assert find_inference_matches_for_rule(rule, (forged, independent)) == ()
    forged_note = replace(db, note="CITED_TODA_SOURCE")
    assert find_inference_matches_for_rule(rule, (forged_note, independent)) == ()


def test_direct_given_for_generator_zero_is_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    forged = replace(independent, rule=ProofRule.GIVEN)
    assert find_inference_matches_for_rule(rule, (db, forged)) == ()
    assert find_inference_matches_for_rule(rule, (forged, db)) == ()
    assert find_inference_matches_for_rule(rule, (db,)) == ()

    # The matcher is premise-pattern based: valid input order is immaterial.
    matches = find_inference_matches_for_rule(rule, (independent, db))
    assert len(matches) == 1
    assert matches[0].premises == (db, independent)


def test_self_citing_or_prior_root_fails_strict_order():
    root, bridge, relation, goal, db, independent = fixture()
    wrong_root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 5))
    assert verified_prior_zero_image_inputs(
        goal, relation, proof_target=wrong_root, bridge=bridge,
    ) is None
    assert expand_adopted_prior_zero_image(
        goal, relation, proof_target=wrong_root, bridge=bridge,
    ) == ()
    with pytest.raises(ValueError, match="earlier adopted"):
        adopted_prior_zero_image_rule(
            goal, relation, proof_target=wrong_root, bridge=bridge,
        )


def test_non_database_presentation_and_wrong_order_are_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    other = Relation(relation.lhs, FiniteCyclicGroup(4, relation.rhs.generator), RelationType.EQUALITY)
    assert expand_adopted_prior_zero_image(
        goal, other, proof_target=root, bridge=bridge,
    ) == ()
    assert expand_adopted_prior_zero_image(
        goal, relation, proof_target="untyped root", bridge=bridge,
    ) == ()
    assert expand_adopted_prior_zero_image(
        "not a zero image", relation, proof_target=root, bridge=bridge,
    ) == ()


def test_cross_map_and_wrong_target_zero_fail():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    wrong_map = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(12, 7))
    altered = replace(independent, conclusion=GeneratorImage(
        wrong_map, relation.rhs.generator, Zero(),
    ))
    assert find_inference_matches_for_rule(rule, (db, altered)) == ()
    altered_two = replace(independent, conclusion=GeneratorImage(
        goal.map, relation.rhs.generator, "zero",
    ))
    assert find_inference_matches_for_rule(rule, (db, altered_two)) == ()


def test_rule_is_not_registered_by_constructing_it():
    root, bridge, relation, goal, db, independent = fixture()
    before = tuple(bridge.proof_links)
    options = expand_adopted_prior_zero_image(
        goal, relation, proof_target=root, bridge=bridge,
    )
    assert len(options) == 1
    assert bridge.proof_links == before
    assert all(link.step is None or link.step.conclusion != goal for link in before)
