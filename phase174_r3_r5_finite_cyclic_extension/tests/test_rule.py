"""Focused type-safety, proof-rule, and public-backward-branch tests for R3-R5."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import (
    FiniteCyclicGroup, TodaDeltaMap, TodaIteratedSuspensionMap, TodaPrimaryGroup,
)
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r5_finite_cyclic_extension.rule import (
    Toda48IndexTwoDoubleSuspensionStatement,
    Toda48UniversalConditionalStatement,
    expand_finite_index_two_cyclic_structure,
    expand_toda48_index_two,
    finite_index_two_cyclic_conclusion,
    finite_index_two_cyclic_rule,
    toda48_delta_goal,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule
from toda_rules import TodaDeltaZeroStatement


def configuration(n: int = 4, m: int = 4):
    """Synthetic group-theory fixtures: no external claim is certified."""
    a = TodaPrimaryGroup(2 * n - 2, n - 1)
    b = TodaPrimaryGroup(2 * n, n + 1)
    generator_a = HomotopyElement("a", n - 1, 2 * n - 2, n - 1)
    generator_b = HomotopyElement("b", n + 1, 2 * n, n + 1)
    index = Toda48IndexTwoDoubleSuspensionStatement(TodaIteratedSuspensionMap(2, a, b))
    prior = Relation(a, FiniteCyclicGroup(m, generator_a), RelationType.EQUALITY)
    double = Relation(
        Multiple(2, generator_b), IteratedSuspension(generator_a, 2),
        RelationType.EQUALITY,
    )
    goal = CyclicStructureStatement(b, generator_b, 2 * m)
    return index, prior, double, goal


def test_toda48_even_dimension_checks_and_delta_endpoints() -> None:
    index, _, _, _ = configuration(4)
    delta = toda48_delta_goal(index)
    assert delta == TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    assert len(expand_toda48_index_two(index)) == 1
    assert expand_toda48_index_two(index)[0].subgoals == (
        delta, Toda48UniversalConditionalStatement(),
    )
    assert toda48_delta_goal(configuration(5)[0]) is None
    assert toda48_delta_goal(replace(index, quotient_order=3)) is None
    assert toda48_delta_goal(Toda48IndexTwoDoubleSuspensionStatement(
        TodaIteratedSuspensionMap(1, index.map.source_group, index.map.target_group)
    )) is None
    assert toda48_delta_goal(Toda48IndexTwoDoubleSuspensionStatement(
        TodaIteratedSuspensionMap(2, index.map.source_group, TodaPrimaryGroup(9, 5))
    )) is None


def test_toda48_index_inference_rejects_given_delta_and_missing_source() -> None:
    index, _, _, _ = configuration()
    proposal = expand_toda48_index_two(index)[0]
    delta, source = proposal.subgoals
    inferred = ProofStep(delta, (), ProofRule.INFERENCE)
    cited = ProofStep(source, (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(proposal.rule, (inferred, cited))
    assert len(matches) == 1
    assert derive_inference_proof_step(matches[0]).conclusion == index
    assert not find_inference_matches_for_rule(
        proposal.rule, (ProofStep(delta, (), ProofRule.GIVEN), cited)
    )
    assert not find_inference_matches_for_rule(
        proposal.rule, (inferred, ProofStep(source, (), ProofRule.INFERENCE))
    )
    assert not find_inference_matches_for_rule(
        proposal.rule,
        (ProofStep(toda48_delta_goal(configuration(6)[0]), (), ProofRule.INFERENCE), cited),
    )


def test_even_order_cyclic_extension_valid_and_odd_order_rejected() -> None:
    index, prior, double, goal = configuration()
    assert finite_index_two_cyclic_conclusion(index, prior, double) == goal
    assert finite_index_two_cyclic_conclusion(*configuration(m=3)[:3]) is None
    rule = finite_index_two_cyclic_rule(goal, index, prior, double)
    inputs = (
        ProofStep(index, (), ProofRule.INFERENCE),
        ProofStep(prior, (), ProofRule.INFERENCE),
        ProofStep(double, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(rule, inputs)
    assert len(matches) == 1
    assert derive_inference_proof_step(matches[0]).conclusion == goal
    assert not find_inference_matches_for_rule(rule, (
        inputs[0], inputs[1], ProofStep(double, (), ProofRule.GIVEN),
    ))
    assert not find_inference_matches_for_rule(rule, (
        ProofStep(index, (), ProofRule.GIVEN), inputs[1], inputs[2],
    ))


def test_wrong_generator_wrong_map_wrong_relation_all_rejected() -> None:
    index, prior, double, goal = configuration()
    bad_prior = Relation(
        prior.lhs,
        FiniteCyclicGroup(4, HomotopyElement("c", 3, 6, 3)),
        RelationType.EQUALITY,
    )
    bad_double = Relation(
        Multiple(2, HomotopyElement("c", 5, 8, 5)),
        double.rhs,
        RelationType.EQUALITY,
    )
    assert finite_index_two_cyclic_conclusion(index, bad_prior, double) is None
    assert finite_index_two_cyclic_conclusion(index, prior, bad_double) is not None
    assert finite_index_two_cyclic_conclusion(index, prior, bad_double) != goal
    reversed_double = Relation(double.rhs, double.lhs, RelationType.EQUALITY)
    assert finite_index_two_cyclic_conclusion(index, prior, reversed_double) is None
    wrong_index = Toda48IndexTwoDoubleSuspensionStatement(TodaIteratedSuspensionMap(
        2, index.map.source_group, TodaPrimaryGroup(10, 6),
    ))
    assert finite_index_two_cyclic_conclusion(wrong_index, prior, double) is None
    with pytest.raises(ValueError):
        finite_index_two_cyclic_rule(goal, wrong_index, prior, double)


def test_public_pi85_cyclic_root_and_delta_proposals_reached() -> None:
    """Use the real source-screened public provider, not a synthetic proposal."""
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    assert len(goals) == 1
    goal = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    assert citing is not None
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    ))
    provider = shared_expansion_provider(screened, proof_target=goal)
    cyclic = CyclicStructureStatement(goal.lhs, goal.rhs.generator, 8)
    options = tuple(x for x in provider(cyclic)
                    if x.rule.name == "finite cyclic extension by an index-two injective image")
    assert len(options) == 1
    index, prior, double = options[0].subgoals
    assert prior.lhs == TodaPrimaryGroup(6, 3)
    assert prior.rhs.order == 4
    assert index.map.source_group == prior.lhs
    assert index.map.target_group == goal.lhs
    assert double.lhs == Multiple(2, goal.rhs.generator)
    index_options = tuple(x for x in provider(index)
                          if x.rule.name == "Toda (4.8) conditional index-two double suspension")
    assert len(index_options) == 1
    delta = index_options[0].subgoals[0]
    assert delta == TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    assert any(x.rule.name == "EHP injective suspension and Delta-E exactness imply zero Delta"
               for x in provider(delta))
    # In R3-R6 only the general source formulae are GIVEN; concrete
    # index-two and doubled relations still require independent inference.
    from phase174_r3_r6_source_extension.source import Toda55UniversalDoubleStatement
    assert any(link.step is not None and link.step.rule is ProofRule.GIVEN
               and link.step.conclusion == index_options[0].subgoals[1]
               for link in screened.proof_links)
    assert any(link.step is not None and link.step.rule is ProofRule.GIVEN
               and link.step.conclusion == Toda55UniversalDoubleStatement()
               for link in screened.proof_links)
    assert not any(link.step is not None and link.step.rule is ProofRule.GIVEN
                   and link.step.conclusion in (goal, cyclic, index, double)
                   for link in screened.proof_links)
