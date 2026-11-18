"""Only the quoted sources and typed η definition may close the Prop 2.5 chain."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase175_r4r10_cited_58_prop25_public import provider, source
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType


def eta_goal():
    signed = source.canonical_toda58()
    beta = HomotopyElement('η₇', 7, 8, 7, GeneratorSymbol('η', index=7))
    gamma = HomotopyElement('η₉', 9, 10, 9, GeneratorSymbol('η', index=9))
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from toda_rules import TodaDeltaImageUpToSignStatement
    return TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4)),
        gamma, Composition(signed.positive_value, beta),
    )


def three_sources():
    return (
        source.CitedToda58SignedDelta(source.canonical_toda58()),
        source.CitedTodaProp25(),
        TodaEtaFamilyGeneralDefinition(),
    )


def test_toda58_formula_is_signed_and_typed() -> None:
    from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
    signed = source.canonical_toda58()
    assert typed_endpoints(signed.element) == (9, 9)
    assert typed_endpoints(signed.positive_value) == (7, 4)
    assert signed.positive_value.right.coefficient == -1
    assert source.CitedToda58SignedDelta(signed).locator == '(5.8)'


def test_cited_source58_requires_independent_given() -> None:
    signed = source.canonical_toda58()
    options = provider.expand_cited_toda58(signed, three_sources())
    assert len(options) == 1
    assert options[0].subgoals == (three_sources()[0],)
    assert not provider.expand_cited_toda58(signed, ())
    assert not provider.expand_cited_toda58(signed, (source.CitedTodaProp25(),))


def test_identity_requires_cited_eta_definition() -> None:
    goal = eta_goal()
    identity = Relation(
        Composition(source.canonical_toda58().element,
                    IteratedSuspension(goal.positive_value.right, 2)),
        goal.element, RelationType.EQUALITY,
    )
    assert provider.eta_identity_indices(identity) == 7
    assert len(provider.expand_eta_identity(identity, three_sources())) == 1
    assert not provider.expand_eta_identity(identity, three_sources()[:2])
    assert provider.eta_identity_indices(replace(identity, rhs=source.canonical_toda58().element)) is None


def test_prop25_uses_exact_r4r7_typed_guard_and_citation() -> None:
    goal = eta_goal()
    result = provider.expand_cited_prop25(goal, three_sources())
    assert len(result) == 1
    proposal = result[0]
    assert proposal.rule.name == provider.CITED_PROP25_RULE
    assert proposal.rule.literature_reference.locator == 'Proposition 2.5'
    assert len(proposal.subgoals) == 3
    assert proposal.subgoals[0] == source.CitedTodaProp25()
    assert proposal.subgoals[1] == source.canonical_toda58()
    assert provider.eta_identity_indices(proposal.subgoals[2]) == 7


def test_missing_cited_prop25_or_58_rejected() -> None:
    goal = eta_goal()
    assert not provider.expand_cited_prop25(goal, three_sources()[0:1])
    assert not provider.expand_cited_prop25(goal, three_sources()[1:])


def test_fake_target_with_wrong_delta_map_rejected() -> None:
    goal = eta_goal()
    forged = replace(goal, map=source.canonical_toda58().map)
    assert not provider.expand_cited_prop25(forged, three_sources())


def test_wrong_dimension_or_unsigned_expression_rejected() -> None:
    goal = eta_goal()
    bad = replace(goal, positive_value=source.canonical_toda58().positive_value)
    assert not provider.expand_cited_prop25(bad, three_sources())
    wrong = replace(goal, element=source.canonical_toda58().element)
    assert not provider.expand_cited_prop25(wrong, three_sources())


def test_proof_requires_all_three_parents() -> None:
    from proof import find_inference_matches_for_rule, apply_inference_match
    goal = eta_goal()
    expansion = provider.expand_cited_prop25(goal, three_sources())[0]
    prop, signed, identity = expansion.subgoals
    fake_inferred = lambda x: ProofStep(x, (), ProofRule.INFERENCE, inference_rule=InferenceRule('test'))
    given = ProofStep(prop, (), ProofRule.GIVEN)
    parents = (given, fake_inferred(signed), fake_inferred(identity))
    match = find_inference_matches_for_rule(expansion.rule, parents)
    assert len(match) == 1
    step = apply_inference_match(match[0])
    assert step.conclusion == goal
    assert step.rule is ProofRule.INFERENCE
    assert not find_inference_matches_for_rule(expansion.rule, parents[:2])
    assert not find_inference_matches_for_rule(
        expansion.rule, (fake_inferred(prop),) + parents[1:],
    )


def test_prop25_sign_is_never_chosen() -> None:
    goal = eta_goal()
    assert goal.positive_value.left.right.coefficient == -1
    assert provider.expand_cited_prop25(goal, three_sources())


def test_no_pi95_group_result_is_registered_by_two_source_types() -> None:
    assert all(not hasattr(x, 'group') for x in three_sources()[:2])
