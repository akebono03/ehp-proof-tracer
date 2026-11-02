"""Focused regression tests for general zero/cyclic/direct-sum candidate roots."""
from __future__ import annotations

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
    lemma54_hopf_inference_rule,
)
from phase173_r4_r10_general_toda56_core.core import (
    GENERAL_ROOT_NAME,
    checked_general_inputs,
    expand_general_toda56,
    general_toda56_rule,
)
from proof import ProofRule, ProofStep


@pytest.mark.parametrize("dimension", (8, 9, 10, 11))
def test_registered_general_inputs_are_type_checked(dimension: int) -> None:
    goal = exact_prior_database_result(4, dimension - 4)
    pair = checked_general_inputs(goal)
    assert pair is not None
    assert pair[0] == exact_prior_database_result(3, dimension - 4)
    assert pair[1] == exact_prior_database_result(7, dimension - 7)
    assert admitted_db_step(pair[0], proof_target=goal) is not None
    assert admitted_db_step(pair[1], proof_target=goal) is not None


def test_pi11_zero_target_has_two_zero_priors_and_no_generator_obligations() -> None:
    from phase173_r4_r4_typed_generator_audit.audit import _map_components
    goal = exact_prior_database_result(4, 7)
    assert isinstance(goal, TodaPrimaryGroupZeroStatement)
    pair = checked_general_inputs(goal)
    assert pair is not None
    assert all(isinstance(item, TodaPrimaryGroupZeroStatement) for item in pair)
    assert _map_components(*pair) == ()


def test_pi12_unproved_epsilon_image_fails_closed() -> None:
    goal = exact_prior_database_result(4, 8)
    assert goal is not None
    assert checked_general_inputs(goal) is None
    assert expand_general_toda56(
        goal, (TodaProp44UniversalStatement(), TodaLemma54TypedSource()),
        proof_target=goal,
    ) == ()


def test_pi7_existing_source_bound_path_is_not_replaced_by_shape_only() -> None:
    goal = exact_prior_database_result(4, 3)
    assert checked_general_inputs(goal) is None


def test_forged_target_or_other_sphere_is_rejected() -> None:
    bogus = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 4))
    assert checked_general_inputs(bogus) is None
    wrong_sphere = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(11, 5))
    assert checked_general_inputs(wrong_sphere) is None


def test_source_first_proposal_for_zero_requires_both_cited_sources() -> None:
    goal = exact_prior_database_result(4, 7)
    source = (TodaProp44UniversalStatement(), TodaLemma54TypedSource())
    assert expand_general_toda56(goal, (), proof_target=goal) == ()
    assert expand_general_toda56(goal, source[:1], proof_target=goal) == ()
    assert expand_general_toda56(goal, source, proof_target=goal,
                                 bridge=None)[0].rule.name == GENERAL_ROOT_NAME
    assert expand_general_toda56(goal, source + source[:1], proof_target=goal) == ()
    assert expand_general_toda56(
        goal, source, proof_target=exact_prior_database_result(4, 6)
    ) == ()


def test_zero_root_guard_requires_two_independently_admitted_priors() -> None:
    goal = exact_prior_database_result(4, 7)
    first, second = checked_general_inputs(goal)
    rule = general_toda56_rule(goal, first, second)
    lemma_step = ProofStep(TodaLemma54TypedSource(), (), ProofRule.GIVEN)
    hopf = ProofStep(
        canonical_hopf_relation(), (lemma_step,), ProofRule.INFERENCE,
        inference_rule=lemma54_hopf_inference_rule(canonical_hopf_relation()),
    )
    premises = (
        ProofStep(TodaProp44UniversalStatement(), (), ProofRule.GIVEN),
        admitted_db_step(first, proof_target=goal),
        admitted_db_step(second, proof_target=goal),
        hopf,
    )
    assert all(step is not None for step in premises)
    assert rule.match_guard(premises, {}) is True
    assert rule.match_guard((premises[0], premises[2], premises[1], premises[3]), {}) is False
    forged = ProofStep(first, (), ProofRule.GIVEN)
    assert rule.match_guard((premises[0], forged, premises[2], premises[3]), {}) is False
    wrong_hopf = ProofStep(canonical_hopf_relation(), (), ProofRule.GIVEN)
    assert rule.match_guard((premises[0], premises[1], premises[2], wrong_hopf), {}) is False


def test_wrong_prior_refused_by_general_rule() -> None:
    goal = exact_prior_database_result(4, 7)
    first, second = checked_general_inputs(goal)
    with pytest.raises(ValueError, match="two earlier"):
        general_toda56_rule(goal, second, first)
