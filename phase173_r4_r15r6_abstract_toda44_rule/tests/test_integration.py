"""Focused real-repository typed abstract inference contracts."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaPrimaryGroup
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
from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
    ABSTRACT_RULE_NAME,
    canonical_abstract_result,
    abstract_toda44_rule,
    expand_abstract_toda44,
)
from proof import (
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)


@pytest.mark.parametrize("k", (3, 4, 7, 8, 31))
def test_canonical_abstract_result_is_k_unbounded(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    statement = canonical_abstract_result(goal)
    assert statement is not None
    assert statement.group == TodaPrimaryGroup(4 + k, 4)
    assert statement.invariant_summands is not None
    proposals = expand_abstract_toda44(
        statement, (TodaProp44UniversalStatement(), TodaLemma54TypedSource()),
        proof_target=goal,
    )
    assert len(proposals) == 1
    assert proposals[0].rule.name == ABSTRACT_RULE_NAME


def test_k31_abstract_result_is_eight_order_two_factors_not_named() -> None:
    goal = exact_prior_database_result(4, 31)
    statement = canonical_abstract_result(goal)
    assert statement is not None
    assert statement.invariant_summands == (("finite", 2),) * 8
    assert checked_general_inputs(goal) is None
    assert not hasattr(statement, "generator")


def test_k31_source_screen_rejects_missing_duplicate_and_wrong_target() -> None:
    goal = exact_prior_database_result(4, 31)
    statement = canonical_abstract_result(goal)
    theorem = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    assert expand_abstract_toda44(statement, (), proof_target=goal) == ()
    assert expand_abstract_toda44(statement, (theorem,), proof_target=goal) == ()
    assert expand_abstract_toda44(statement, (theorem, lemma, lemma), proof_target=goal) == ()
    assert expand_abstract_toda44(
        statement, (theorem, lemma),
        proof_target=exact_prior_database_result(4, 8),
    ) == ()
    forged = replace(statement, invariant_summands=(("finite", 4),) * 4)
    assert expand_abstract_toda44(forged, (theorem, lemma), proof_target=goal) == ()


def test_k31_proof_engine_rule_replay_rejects_unadmitted_priors() -> None:
    goal = exact_prior_database_result(4, 31)
    statement = canonical_abstract_result(goal)
    source = (TodaProp44UniversalStatement(), TodaLemma54TypedSource())
    rule = expand_abstract_toda44(statement, source, proof_target=goal)[0].rule
    from phase173_r4_r10_general_toda56_core.core import checked_abstract_inputs
    first, second = checked_abstract_inputs(goal)
    lemma = ProofStep(TodaLemma54TypedSource(), (), ProofRule.GIVEN)
    hopf_goal = canonical_hopf_relation()
    hopf = ProofStep(
        hopf_goal, (lemma,), ProofRule.INFERENCE,
        inference_rule=lemma54_hopf_inference_rule(hopf_goal),
    )
    steps = (
        ProofStep(TodaProp44UniversalStatement(), (), ProofRule.GIVEN),
        admitted_db_step(first, proof_target=goal),
        admitted_db_step(second, proof_target=goal),
        hopf,
    )
    assert all(step is not None for step in steps)
    matches = find_inference_matches_for_rule(rule, steps)
    assert len(matches) == 1
    derived = apply_inference_match(matches[0])
    assert derived.conclusion == statement
    assert derived.rule is ProofRule.INFERENCE
    assert rule.match_guard((steps[0], steps[2], steps[1], steps[3]), ()) is False
    forged = ProofStep(first, (), ProofRule.GIVEN)
    assert rule.match_guard((steps[0], forged, steps[2], steps[3]), ()) is False
    wrong_hopf = ProofStep(hopf_goal, (), ProofRule.GIVEN)
    assert rule.match_guard((steps[0], steps[1], steps[2], wrong_hopf), ()) is False
    # These are isolated contract-test leaves, not an audited public source tree.


def test_existing_named_generator_root_is_unchanged() -> None:
    goal = exact_prior_database_result(4, 8)
    assert checked_general_inputs(goal) is None
    goal31 = exact_prior_database_result(4, 31)
    assert checked_general_inputs(goal31) is None
    assert canonical_abstract_result(goal31) is not None
