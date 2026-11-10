"""Focused algebraic EHP bridge tests; hypothetical steps never count as evidence."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapSurjective
from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization
from phase174_r3_r7_r56_cyclic_generator_bridge.rule import (
    CYCLIC_RULE_NAME,
    SURJECTIVE_RULE_NAME,
    canonical_typed_delta_generator,
    cyclic_generator_inputs,
    cyclic_generator_rule,
    delta_surjectivity_generator_inputs,
    delta_surjectivity_from_generator_rule,
    expand_cyclic_generator_from_hopf,
    expand_delta_surjectivity_from_generator,
)
from proof import (
    InferenceRule,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)


def _goal(n: int) -> Relation:
    theorem = typed_specialization(n)
    return Relation(
        theorem.delta.target_group,
        FreeCyclicGroup(canonical_typed_delta_generator(theorem)),
        RelationType.EQUALITY,
    )


def _test_step(statement: object, rule: ProofRule = ProofRule.INFERENCE) -> ProofStep:
    return ProofStep(
        statement, (), rule,
        inference_rule=InferenceRule(name="hypothetical-test-only"),
    )


@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_four_certified_inputs_propose_generator_relation(n: int) -> None:
    goal = _goal(n)
    required = cyclic_generator_inputs(goal)
    assert required is not None and len(required) == 4
    assert required == tuple(
        expand_cyclic_generator_from_hopf(goal)[0].subgoals
    )
    options = expand_cyclic_generator_from_hopf(goal)
    assert len(options) == 1
    assert options[0].rule.name == CYCLIC_RULE_NAME
    facts = tuple(_test_step(item) for item in required)
    matches = find_inference_matches_for_rule(cyclic_generator_rule(goal), facts)
    assert len(matches) == 1
    proof = apply_inference_match(matches[0])
    assert proof.rule is ProofRule.INFERENCE
    assert proof.conclusion == goal
    assert proof.premises == facts


def test_real_db_goal_generator_representation_is_canonical() -> None:
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result

    assert exact_prior_database_result(6, 5) == _goal(6)
    assert _goal(6).lhs == TodaPrimaryGroup(11, 6)
    element = _goal(6).rhs.generator
    assert element == HomotopyElement(
        name="Δ(ι13)", dimension=6, source=11, target=6,
        generator=GeneratorSymbol(family=r"\Delta(\iota_{13})"),
    )


@pytest.mark.parametrize("missing", range(4))
def test_missing_a_proved_hopf_premise_blocks_group_rule(missing: int) -> None:
    goal = _goal(6)
    facts = tuple(
        _test_step(item)
        for i, item in enumerate(cyclic_generator_inputs(goal))
        if i != missing
    )
    assert not find_inference_matches_for_rule(cyclic_generator_rule(goal), facts)


def test_proposed_group_cannot_be_discharged_by_direct_given_premises() -> None:
    goal = _goal(6)
    required = cyclic_generator_inputs(goal)
    for index in range(4):
        facts = tuple(
            _test_step(item, ProofRule.GIVEN if i == index else ProofRule.INFERENCE)
            for i, item in enumerate(required)
        )
        assert not find_inference_matches_for_rule(cyclic_generator_rule(goal), facts)


def test_mismatched_generator_or_dimension_is_rejected() -> None:
    goal = _goal(6)
    current = goal.rhs.generator
    bad = replace(current, name="Δ(ι15)")
    assert cyclic_generator_inputs(Relation(goal.lhs, FreeCyclicGroup(bad))) is None
    assert cyclic_generator_inputs(Relation(
        TodaPrimaryGroup(11, 7), goal.rhs
    )) is None
    assert cyclic_generator_inputs("pi11-6") is None
    assert canonical_typed_delta_generator(replace(
        typed_specialization(6), sign_undetermined=False
    )) is None


@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_generator_relation_alone_proves_delta_surjectivity(n: int) -> None:
    theorem = typed_specialization(n)
    goal = MapSurjective(theorem.delta)
    required = delta_surjectivity_generator_inputs(goal)
    assert required == (_goal(n),)
    proposals = expand_delta_surjectivity_from_generator(goal)
    assert len(proposals) == 1
    assert proposals[0].rule.name == SURJECTIVE_RULE_NAME
    assert proposals[0].subgoals == required
    for proof_kind in (ProofRule.GIVEN, ProofRule.INFERENCE):
        facts = (_test_step(required[0], proof_kind),)
        matches = find_inference_matches_for_rule(
            delta_surjectivity_from_generator_rule(goal), facts
        )
        assert len(matches) == 1
        assert apply_inference_match(matches[0]).conclusion == goal

def test_prior_relation_needs_no_prop27_reproof() -> None:
    goal = MapSurjective(typed_specialization(6).delta)
    relation, = delta_surjectivity_generator_inputs(goal)
    facts = (_test_step(relation, ProofRule.GIVEN),)
    assert len(find_inference_matches_for_rule(
        delta_surjectivity_from_generator_rule(goal), facts
    )) == 1
    assert all(type(x) is Relation for x in delta_surjectivity_generator_inputs(goal))

def test_missing_or_wrong_group_generator_blocks_surjectivity() -> None:
    theorem = typed_specialization(6)
    goal = MapSurjective(theorem.delta)
    relation, = delta_surjectivity_generator_inputs(goal)
    wrong = Relation(relation.lhs, FreeCyclicGroup(
        replace(relation.rhs.generator, name="Delta of wrong identity")
    ))
    rule = delta_surjectivity_from_generator_rule(goal)
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(rule, (_test_step(wrong),)) == ()
    assert find_inference_matches_for_rule(rule, (_test_step(theorem),)) == ()
    valid_relation = _test_step(relation)
    unrelated_theorem = _test_step(theorem)
    matches = find_inference_matches_for_rule(
        rule, (valid_relation, unrelated_theorem)
    )
    assert len(matches) == 1
    assert matches[0].premises == (valid_relation,)
    derived = apply_inference_match(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == (valid_relation,)

def test_unrelated_goals_and_odd_instances_have_no_proposals() -> None:
    assert expand_cyclic_generator_from_hopf(object()) == ()
    assert expand_delta_surjectivity_from_generator(object()) == ()
    theorem = typed_specialization(6)
    assert expand_delta_surjectivity_from_generator(
        MapSurjective(theorem.hopf)
    ) == ()


def test_providers_only_propose_subgoals_not_proofs_or_givens() -> None:
    candidates = (
        expand_cyclic_generator_from_hopf(_goal(6))
        + expand_delta_surjectivity_from_generator(
            MapSurjective(typed_specialization(6).delta)
        )
    )
    assert len(candidates) == 2
    for option in candidates:
        assert not any(isinstance(p, ProofStep) for p in option.subgoals)
        assert option.rule.conclusion_pattern is not None
