"""Focused source and guarded inference contracts for the second Toda (5.5) clause."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, Multiple, Zero
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition, canonical_member,
)
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement,
    build_cited_toda55_quadruple_source,
    canonical_quadruple_goal,
    cited_quadruple_rule,
    expand_cited_quadruple,
)
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def available_sources():
    return (
        Toda55UniversalQuadrupleStatement(),
        CitedStableFamilyDefinition(4, 4, 3),
        TodaEtaFamilyGeneralDefinition(),
    )


def test_source_adopts_only_second_clause() -> None:
    bridge = build_cited_toda55_quadruple_source()
    assert len(bridge.proof_links) == 1
    step = bridge.proof_links[0].step
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == Toda55UniversalQuadrupleStatement()
    assertion = bridge.registry.assertion(bridge.proof_links[0].assertion_id)
    assert assertion.content == step.conclusion
    assert bridge.registry.reference(assertion.reference_id).publication_position == 8600


@pytest.mark.parametrize("n", (5, 6, 12))
def test_canonical_nu_quadruple_goal_is_typed(n: int) -> None:
    goal = canonical_quadruple_goal(n)
    assert isinstance(goal, Relation)
    assert goal.relation_type is RelationType.EQUALITY
    assert goal.lhs.coefficient == 4
    assert goal.lhs.expression.dimension == n
    assert isinstance(goal.rhs, Composition)
    assert tuple(x.generator.index for x in
                 (goal.rhs.left, goal.rhs.right.left, goal.rhs.right.right)) == (n, n + 1, n + 2)
    assert len(expand_cited_quadruple(goal, available_sources())) == 1


def test_unsupported_indices_and_sources_fail_closed() -> None:
    assert canonical_quadruple_goal(4) is None
    assert canonical_quadruple_goal(True) is None
    goal = canonical_quadruple_goal(5)
    assert expand_cited_quadruple(goal, ()) == ()
    assert expand_cited_quadruple(goal, available_sources()[:-1]) == ()
    assert expand_cited_quadruple(goal, available_sources() + (available_sources()[0],)) == ()
    assert expand_cited_quadruple(replace(goal, rhs=Zero()), available_sources()) == ()
    assert expand_cited_quadruple(Relation(Multiple(2, goal.lhs.expression), goal.rhs,
                                           RelationType.EQUALITY), available_sources()) == ()


def test_only_independently_inferred_family_member_can_close() -> None:
    goal = canonical_quadruple_goal(5)
    rule = cited_quadruple_rule(goal)
    family = CitedStableFamilyDefinition(4, 4, 3)
    member = canonical_member(family, 5)
    premise = ProofStep(member, (), ProofRule.INFERENCE,
                        inference_rule=InferenceRule(name="test independent family member"))
    cited = ProofStep(Toda55UniversalQuadrupleStatement(), (), ProofRule.GIVEN)
    eta = ProofStep(TodaEtaFamilyGeneralDefinition(), (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(rule, (premise, cited, eta))
    assert len(matches) == 1
    assert find_inference_matches_for_rule(rule, (
        ProofStep(member, (), ProofRule.GIVEN), cited, eta)) == ()
    assert find_inference_matches_for_rule(rule, (premise, cited)) == ()
    reordered = find_inference_matches_for_rule(rule, (premise, eta, cited))
    assert len(reordered) == 1
    assert reordered[0].premises == (premise, cited, eta)
