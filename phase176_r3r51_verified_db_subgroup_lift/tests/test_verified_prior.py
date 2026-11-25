"""Contextual DB admission and rejection; synthetic non-DB premises are fixtures."""
from dataclasses import replace

import pytest

from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, exact_prior_database_result, verified_db_step
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import (
    RULE_NAME, finite_cyclic_subgroup_lift_rule,
)
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.tests.test_finite_cyclic_subgroup_lift import inferred
from phase176_r3r51_verified_db_subgroup_lift.apply import ROOT, PINS, updated_source
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


@pytest.fixture(scope='module')
def actual():
    root = exact_prior_database_result(3,5)
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, root.rhs.order)
    options = shared_expansion_provider(bridge, proof_target=root)(goal)
    for option in options:
        if option.rule.name != RULE_NAME:
            continue
        prior = admitted_prior_group_step(option.subgoals[2].lhs, proof_target=root, bridge=bridge)
        if prior is None or prior.conclusion != option.subgoals[2]:
            continue
        assert verified_db_step(prior, proof_target=root, bridge=bridge)
        facts = tuple(prior if j == 2 else inferred(s) for j,s in enumerate(option.subgoals))
        return root, bridge, goal, option, facts
    pytest.fail('no public lift candidate with an eligible exact DB prior')


def test_public_candidate_accepts_verified_db_only_in_codomain(actual):
    root, bridge, goal, option, facts = actual
    match, = find_inference_matches_for_rule(option.rule, facts)
    derived = apply_inference_match(match)
    assert derived.conclusion == goal and derived.rule is ProofRule.INFERENCE
    assert derived.premises == facts
    assert facts[2].rule is ProofRule.GIVEN
    assert all(not isinstance(s, ProofStep) for s in option.subgoals)
    assert all(s.rule is ProofRule.INFERENCE for j,s in enumerate(facts) if j != 2)
    args = goal, *option.subgoals[1:]
    assert not find_inference_matches_for_rule(finite_cyclic_subgroup_lift_rule(*args), facts)
    assert not find_inference_matches_for_rule(finite_cyclic_subgroup_lift_rule(*args, bridge=bridge), facts)
    assert not find_inference_matches_for_rule(finite_cyclic_subgroup_lift_rule(*args, proof_target=root), facts)


def test_forged_given_cannot_pass_even_with_same_conclusion(actual):
    root, bridge, goal, option, facts = actual
    prior = facts[2]
    for forged in (ProofStep(prior.conclusion, (), ProofRule.GIVEN),
                   replace(prior, note='forged'), replace(prior, inference_rule=None),
                   replace(prior, premises=(facts[0],))):
        changed = facts[:2] + (forged,) + facts[3:]
        assert not find_inference_matches_for_rule(option.rule, changed)
    args = goal, *option.subgoals[1:]
    wrong_context = finite_cyclic_subgroup_lift_rule(*args, bridge=bridge, proof_target=prior.conclusion)
    assert not find_inference_matches_for_rule(wrong_context, facts)


@pytest.mark.parametrize('index',(0,1,3,4))
def test_non_codomain_given_remains_forbidden(actual,index):
    _, _, _, option, facts = actual
    changed = tuple(replace(s, rule=ProofRule.GIVEN) if j == index else s for j,s in enumerate(facts))
    assert not find_inference_matches_for_rule(option.rule, changed)


@pytest.mark.parametrize('index',range(5))
def test_missing_independent_premise_rejected(actual,index):
    _, _, _, option, facts = actual
    assert not find_inference_matches_for_rule(option.rule, tuple(s for j,s in enumerate(facts) if j != index))


def test_inferred_codomain_remains_supported(actual):
    _, _, _, option, facts = actual
    inferred_facts = facts[:2] + (inferred(facts[2].conclusion),) + facts[3:]
    assert find_inference_matches_for_rule(option.rule, inferred_facts)


def test_patch_idempotent_and_unknown_bytes_rejected():
    for path in PINS:
        raw = (ROOT/path).read_bytes()
        assert updated_source(path,raw) == raw
        with pytest.raises(ValueError):
            updated_source(path,raw+b'\n# unknown edit\n')
