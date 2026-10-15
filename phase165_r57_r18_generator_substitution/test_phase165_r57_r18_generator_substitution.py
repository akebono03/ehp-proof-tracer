"""Focused R57-R18 runtime checks. Run against the installed project."""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules
from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
from phase165_r57_r18_generator_substitution import finite_cyclic_generator_substitution_rule
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step


def eta(index: int, name: str) -> HomotopyElement:
    return HomotopyElement(name=name, dimension=index, source=index + 1, target=index,
                           generator=GeneratorSymbol(family="η", index=index))


def test_r18_registered_eta3_spelling_has_root_expansion():
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(3, "η_3")))
    candidates = expand_existing_pi43_rules(goal)
    assert len(candidates) == 1
    assert len(retain_ordered_root_expansions(goal, goal, candidates)) == 1
    assert candidates[0].subgoals[1].lhs == goal.rhs.generator


def test_r18_canonical_eta3_spelling_has_root_expansion():
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(3, "η₃")))
    assert len(expand_existing_pi43_rules(goal)) == 1


def test_r18_unrelated_generator_is_not_accepted():
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(4, "η_4")))
    assert expand_existing_pi43_rules(goal) == ()


def test_r18_generator_substitution_requires_proved_identity():
    target = TodaPrimaryGroup(4, 3)
    old = Suspension(expression=eta(2, "η₂"))
    new = eta(3, "η_3")
    first = ProofStep(conclusion=Relation(target, FiniteCyclicGroup(2, old)),
                      premises=(), rule=ProofRule.GIVEN)
    second = ProofStep(conclusion=Relation(new, old), premises=(), rule=ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(finite_cyclic_generator_substitution_rule(), (first, second))
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.conclusion == Relation(target, FiniteCyclicGroup(2, new))
    assert derived.rule is ProofRule.INFERENCE


def test_r18_root_gate_continues_rejecting_self_specialization():
    root = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(3, "η_3")))
    expansion = GoalExpansion(finite_cyclic_generator_substitution_rule(), (root,))
    assert retain_ordered_root_expansions(root, root, (expansion,)) == ()


def test_r18_rejects_generator_substitution_without_matching_equality():
    old = Suspension(expression=eta(2, "η₂"))
    first = ProofStep(conclusion=Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, old)),
                      premises=(), rule=ProofRule.GIVEN)
    second = ProofStep(conclusion=Relation(eta(3, "η_3"), eta(3, "η₃")),
                       premises=(), rule=ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(finite_cyclic_generator_substitution_rule(), (first, second))
    assert matches == () or len(matches) == 0
