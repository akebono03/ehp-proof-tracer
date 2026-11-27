"""Isolated rule contract and genuine prior DB replay (not a public root proof)."""
from dataclasses import replace

import pytest

from homotopy_groups import (
    TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement, TodaSuspensionMap,
)
from map_property_rules import ImageZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step, exact_prior_database_result, verified_db_step,
)
from phase179_r5_zero_domain_image_isolated.rule import (
    RULE_NAME, expand_zero_domain_image, verified_zero_domain_inputs,
    zero_domain_image_rule, zero_domain_inputs,
)
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def image(q, n):
    return ImageZeroStatement(TodaSuspensionMap(TodaPrimaryGroup(q, n), TodaPrimaryGroup(q + 1, n + 1)))


@pytest.mark.parametrize('q,n', [(2,2), (7,3), (9,2), (9,3), (15,8), (40,20)])
def test_obligation_is_dimension_generic(q, n):
    assert zero_domain_inputs(image(q,n)) == (TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(q,n)),)


@pytest.mark.parametrize('goal', [None, 'zero', ImageZeroStatement(object()), image(1,1), image(2,3),
    image(True,2), image(9.0,2), image(9,2.0),
    ImageZeroStatement(TodaSuspensionMap(TodaPrimaryGroup(9,2),TodaPrimaryGroup(11,3))),
    ImageZeroStatement(TodaSuspensionMap(TodaPrimaryGroup(9,2),TodaPrimaryGroup(10,4))),
    ImageZeroStatement(TodaSuspensionMap(TodaPrimaryGroup(9,2),TodaPrimaryGroup(10.0,3))),
    ImageZeroStatement(TodaSuspensionMap('a','b')),
    ImageZeroStatement(TodaHopfInvariantMap(TodaPrimaryGroup(10,3),TodaPrimaryGroup(10,5))),
    ImageZeroStatement(TodaDeltaMap(TodaPrimaryGroup(10,5),TodaPrimaryGroup(8,2)))])
def test_malformed_or_unsupported_maps_rejected(goal):
    assert zero_domain_inputs(goal) is None
    assert expand_zero_domain_image(goal,proof_target=None,bridge=None) == ()


@pytest.fixture(scope='module')
def context():
    root = exact_prior_database_result(3,7)
    assert root == TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10,3))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root)
    return root, bridge


def test_real_adopted_zero_domain_replay(context):
    root, bridge = context
    goal = image(9,2)
    zero, = zero_domain_inputs(goal)
    before = tuple(bridge.proof_links), tuple(bridge.registry._assertions.items())
    witness = admitted_db_step(zero,proof_target=root,bridge=bridge)
    assert witness is not None and verified_db_step(witness,proof_target=root,bridge=bridge)
    option, = expand_zero_domain_image(goal,proof_target=root,bridge=bridge)
    assert option.rule.name == RULE_NAME and option.subgoals == (zero,)
    assert all(not isinstance(g,ProofStep) for g in option.subgoals)
    match, = find_inference_matches_for_rule(option.rule,(witness,))
    result = apply_inference_match(match)
    assert result.rule is ProofRule.INFERENCE and result.conclusion == goal
    assert result.premises == (witness,) and witness.rule is ProofRule.GIVEN
    assert before == (tuple(bridge.proof_links),tuple(bridge.registry._assertions.items()))
    print('PHASE179_R5_REAL_PRIOR_ZERO_IMAGE=VERIFIED')


def test_other_admitted_zero_domain_replay(context):
    root, bridge = context
    goal = image(9,3)
    zero, = zero_domain_inputs(goal)
    witness = admitted_db_step(zero,proof_target=root,bridge=bridge)
    assert witness is not None and verified_db_step(witness,proof_target=root,bridge=bridge)
    option, = expand_zero_domain_image(goal,proof_target=root,bridge=bridge)
    match, = find_inference_matches_for_rule(option.rule,(witness,))
    assert apply_inference_match(match).conclusion == goal


def test_unverified_nonzero_self_and_later_sources_rejected(context):
    root, bridge = context
    for goal in (image(8,2),image(10,3),image(11,3)):
        assert verified_zero_domain_inputs(goal,proof_target=root,bridge=bridge) is None
        assert expand_zero_domain_image(goal,proof_target=root,bridge=bridge) == ()
        with pytest.raises(ValueError):
            zero_domain_image_rule(goal,proof_target=root,bridge=bridge)
    assert not expand_zero_domain_image(image(9,2),proof_target=None,bridge=bridge)
    assert not expand_zero_domain_image(image(9,2),proof_target=root,bridge=None)


def test_forged_and_mismatched_premises_rejected(context):
    root, bridge = context
    goal = image(9,2)
    zero, = zero_domain_inputs(goal)
    witness = admitted_db_step(zero,proof_target=root,bridge=bridge)
    assert witness is not None
    rule = zero_domain_image_rule(goal,proof_target=root,bridge=bridge)
    for bad in (ProofStep(zero,(),ProofRule.GIVEN),
                replace(witness,note='forged'),
                replace(witness,rule=ProofRule.INFERENCE),
                replace(witness,premises=(witness,)),
                replace(witness,conclusion=TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9,3)))):
        assert not find_inference_matches_for_rule(rule,(bad,))
    assert not find_inference_matches_for_rule(rule,())
    print('PHASE179_R5_UNVERIFIED_PRIORS_REJECTED=VERIFIED')
