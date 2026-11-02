"""Focused real-type tests; no proof target is ever introduced as a GIVEN."""
from __future__ import annotations

from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    TodaLemma54TypedSource,
    canonical_hopf_relation,
    lemma54_hopf_inference_rule,
)
from phase173_r4_r7_source_first_rule.rule import (
    checked_inputs,
    expand_source_first_toda56,
    source_first_toda56_rule,
)
from phase173_r4_r7_source_first_rule.source import screened_source_first_context
from proof import ProofRule, ProofStep, Relation, RelationType


def _goal(i: int) -> Relation:
    goal = exact_prior_database_result(4, i - 4)
    assert isinstance(goal, Relation)
    assert goal.lhs == TodaPrimaryGroup(i, 4)
    return goal


def _context(goal: Relation):
    bridge = build_shared_typed_bridge()
    path = Path(__file__).resolve().parents[2] / "sources/toda/Toda_05_2.tex"
    chapter = path.read_text(encoding="utf-8-sig")
    return bridge, screened_source_first_context(bridge, goal=goal, chapter=chapter)


@pytest.mark.parametrize("i", [8, 9, 10])
def test_source_first_bounded_registered_generator_inputs(i: int) -> None:
    goal = _goal(i)
    inputs = checked_inputs(goal)
    assert inputs is not None
    first, second = inputs
    assert first == exact_prior_database_result(3, i - 4)
    assert second == exact_prior_database_result(7, i - 7)
    assert admitted_db_step(first, proof_target=goal) is not None
    assert admitted_db_step(second, proof_target=goal) is not None


def test_existing_pi74_is_never_selected() -> None:
    goal = _goal(7)
    assert checked_inputs(goal) is None
    assert expand_source_first_toda56(goal, (), proof_target=goal) == ()


def test_unregistered_target_and_wrong_generator_are_rejected() -> None:
    goal = _goal(8)
    wrong = Relation(goal.lhs, _goal(9).rhs, RelationType.EQUALITY)
    assert checked_inputs(wrong) is None
    assert checked_inputs(Relation(TodaPrimaryGroup(8, 5), goal.rhs, RelationType.EQUALITY)) is None


def test_no_unverified_reference_grants_root() -> None:
    goal = _goal(8)
    theorem = TodaProp44UniversalStatement()
    source = TodaLemma54TypedSource()
    assert expand_source_first_toda56(goal, (), proof_target=goal) == ()
    assert expand_source_first_toda56(goal, (theorem,), proof_target=goal) == ()
    assert expand_source_first_toda56(goal, (source,), proof_target=goal) == ()
    assert expand_source_first_toda56(goal, (theorem, theorem, source), proof_target=goal) == ()
    assert expand_source_first_toda56(goal, (theorem, source, source), proof_target=goal) == ()
    assert expand_source_first_toda56(goal, (theorem, source), proof_target=_goal(9)) == ()


def test_source_first_context_is_immutable_and_source_certified() -> None:
    goal = _goal(8)
    original, context = _context(goal)
    assert context is not None
    assert ADOPTED_ASSERTION_ID not in original.registry._assertions
    assert ADOPTED_ASSERTION_ID in context.registry._assertions
    assert not any(link.step is not None and link.step.conclusion == goal
                   for link in context.proof_links)
    leaves = tuple(link.step.conclusion for link in context.proof_links if link.step is not None)
    assert leaves.count(TodaLemma54TypedSource()) == 1
    assert leaves.count(TodaProp44UniversalStatement()) == 1


@pytest.mark.parametrize("i", [8, 9, 10])
def test_proposal_has_four_independently_provable_typed_subgoals(i: int) -> None:
    goal = _goal(i)
    _, context = _context(goal)
    assert context is not None
    available = tuple(link.step.conclusion for link in context.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    proposals = expand_source_first_toda56(goal, available, proof_target=goal,
                                           bridge=context)
    assert len(proposals) == 1
    theorem, first, second, hopf = proposals[0].subgoals
    assert theorem == TodaProp44UniversalStatement()
    assert (first, second) == checked_inputs(goal)
    assert hopf == canonical_hopf_relation()
    assert proposals[0].rule.conclusion_pattern == goal


def test_rule_requires_genuinely_admitted_prior_db_steps() -> None:
    goal = _goal(8)
    _, context = _context(goal)
    assert context is not None
    first, second = checked_inputs(goal)
    rule = source_first_toda56_rule(goal, first, second, bridge=context)
    steps = (
        ProofStep(TodaProp44UniversalStatement(), (), ProofRule.GIVEN),
        admitted_db_step(first, proof_target=goal, bridge=context),
        admitted_db_step(second, proof_target=goal, bridge=context),
        ProofStep(
            canonical_hopf_relation(),
            (ProofStep(TodaLemma54TypedSource(), (), ProofRule.GIVEN),),
            ProofRule.INFERENCE,
            inference_rule=lemma54_hopf_inference_rule(canonical_hopf_relation()),
        ),
    )
    assert all(step is not None for step in steps)
    assert rule.match_guard(steps, {}) is True
    swapped = (steps[0], steps[2], steps[1], steps[3])
    assert rule.match_guard(swapped, {}) is False
    untrusted = (steps[0], ProofStep(first, (), ProofRule.GIVEN), steps[2], steps[3])
    assert rule.match_guard(untrusted, {}) is False
    hopf_as_given = (steps[0], steps[1], steps[2],
                     ProofStep(canonical_hopf_relation(), (), ProofRule.GIVEN))
    assert rule.match_guard(hopf_as_given, {}) is False
    unsupported_hopf = (steps[0], steps[1], steps[2],
                        ProofStep(canonical_hopf_relation(), (), ProofRule.INFERENCE))
    assert rule.match_guard(unsupported_hopf, {}) is False


def test_wrong_target_cannot_reuse_another_group_inputs() -> None:
    goal = _goal(9)
    first, second = checked_inputs(_goal(8))
    with pytest.raises(ValueError, match="independently registered"):
        source_first_toda56_rule(goal, first, second)
