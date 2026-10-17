from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r12_r31_proven_cyclic_reuse import expand_free_cyclic_structure_from_relation
from proof import ProofRule, ProofStep, Relation, apply_inference_match, find_inference_matches_for_rule


def example():
    generator = HomotopyElement("g", 5, generator=GeneratorSymbol("g", 5))
    return CyclicStructureStatement(TodaPrimaryGroup(7, 5), generator, None)


def test_r31_generates_exact_free_cyclic_relation_subgoal():
    goal = example()
    proposals = expand_free_cyclic_structure_from_relation(goal)
    assert len(proposals) == 1
    assert proposals[0].subgoals == (Relation(goal.group, FreeCyclicGroup(goal.generator)),)


def test_r31_rule_preserves_real_proof_ancestry():
    goal = example()
    proposal = expand_free_cyclic_structure_from_relation(goal)[0]
    premise = ProofStep(proposal.subgoals[0], (), ProofRule.RELATION)
    matches = find_inference_matches_for_rule(proposal.rule, (premise,))
    assert len(matches) == 1
    derived = apply_inference_match(matches[0])
    assert derived.conclusion == goal
    assert derived.rule is ProofRule.INFERENCE
    assert derived.premises == (premise,)


def test_r31_finite_and_unrelated_goals_are_not_expanded():
    goal = example()
    assert expand_free_cyclic_structure_from_relation(CyclicStructureStatement(goal.group, goal.generator, 2)) == ()
    assert expand_free_cyclic_structure_from_relation(Relation(goal.group, FreeCyclicGroup(goal.generator))) == ()
