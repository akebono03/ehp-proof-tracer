"""Actual typed inference tests, executed in the full project checkout."""
from __future__ import annotations

import pytest

pytest.importorskip("phase165_r14_r6_generic_iso")

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r3r6_lemma57_general.rule import (
    TodaLemma57DoubleSuspensionMembership,
    expand_cited_lemma57_zero_generator,
    lemma57_criterion_inputs,
)
from phase175_r3r6_lemma57_general.source import TodaLemma57GeneralCriterion


def pi62_zero_generator_goal() -> GeneratorImage:
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    return GeneratorImage(e, prior.rhs.generator, Zero())


def test_actual_pi62_goal_has_one_general_lemma57_membership_obligation() -> None:
    goal = pi62_zero_generator_goal()
    subgoals = lemma57_criterion_inputs(goal)
    assert subgoals is not None
    assert subgoals[0] == TodaLemma57GeneralCriterion()
    assert isinstance(subgoals[1], TodaLemma57DoubleSuspensionMembership)
    assert subgoals[1].alpha == goal.source_generator.right
    proposals = expand_cited_lemma57_zero_generator(goal, (TodaLemma57GeneralCriterion(),))
    assert len(proposals) == 1
    assert proposals[0].subgoals == subgoals
    assert all(not hasattr(item, "premises") for item in proposals[0].subgoals)


def test_no_unscreened_source_cannot_generate_lemma57_proposal() -> None:
    goal = pi62_zero_generator_goal()
    assert expand_cited_lemma57_zero_generator(goal, ()) == ()
    assert expand_cited_lemma57_zero_generator(goal, (TodaLemma57GeneralCriterion(),) * 2) == ()


def test_invalid_map_or_wrong_eta_rejected() -> None:
    original = pi62_zero_generator_goal()
    different = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 4))
    assert lemma57_criterion_inputs(GeneratorImage(
        different, original.source_generator, Zero(),
    )) is None
    fake_eta = HomotopyElement(
        name="η₃", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3),
    )
    wrong = Composition(fake_eta, original.source_generator.right)
    assert lemma57_criterion_inputs(GeneratorImage(
        original.map, wrong, Zero(),
    )) is None


def test_nonzero_target_image_does_not_trigger_rule() -> None:
    goal = pi62_zero_generator_goal()
    assert lemma57_criterion_inputs(GeneratorImage(
        goal.map, goal.source_generator, goal.source_generator,
    )) is None


def test_isolated_source_registry_has_only_general_fixed_leaf() -> None:
    from pathlib import Path

    from phase175_r3r6_lemma57_general.source import (
        GENERAL_ASSERTION_ID, build_isolated_lemma57_source,
    )
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    root = Path(__file__).resolve().parents[2]
    bridge = build_isolated_lemma57_source(root)
    assert len(bridge.proof_links) == 1
    link = bridge.proof_links[0]
    assert link.assertion_id == GENERAL_ASSERTION_ID
    assert link.step is not None
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.conclusion == TodaLemma57GeneralCriterion()
    assert bridge.registry.assertion(GENERAL_ASSERTION_ID).origin is AssertionOrigin.FIXED_STATEMENT
    assert bridge.registry.reference(
        bridge.registry.assertion(GENERAL_ASSERTION_ID).reference_id,
    ).publication_position == 9100
