from expression import Composition, GeneratorSymbol, HomotopyElement, Suspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase176_r3r34_composite_suspension_isolated.source import (
    composite_suspension_equality_input,
    expand_composite_suspension_equality,
)
from proof import ProofRule, Relation, RelationType, ProofStep


def elements():
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    return eta5, eta6, eta7


def goal():
    a, b, c = elements()
    # Source endpoints (7,5); target endpoints (8,6).
    return Relation(Suspension(Composition(a, b)),
                    Composition(b, c), RelationType.EQUALITY)


def test_composite_image_is_independent_subgoal():
    candidate = composite_suspension_equality_input(goal())
    assert isinstance(candidate, GeneratorImage)
    assert candidate.source_generator == goal().lhs.expression
    assert candidate.target_generator == goal().rhs
    options = expand_composite_suspension_equality(goal())
    assert len(options) == 1
    assert options[0].subgoals == (candidate,)


def test_rejects_mismatched_target():
    a, b, c = elements()
    wrong = Relation(Suspension(Composition(a, b)),
                     Composition(a, c), RelationType.EQUALITY)
    assert expand_composite_suspension_equality(wrong) == ()


def test_rejects_reversed_equality():
    original = goal()
    reversed_goal = Relation(original.rhs, original.lhs, RelationType.EQUALITY)
    assert expand_composite_suspension_equality(reversed_goal) == ()


def test_requires_inferred_proof_not_given():
    option = expand_composite_suspension_equality(goal())[0]
    premise = option.subgoals[0]
    guard = option.rule.match_guard
    assert guard((ProofStep(conclusion=premise, premises=(), rule=ProofRule.GIVEN),), {}) is False
    assert guard((ProofStep(conclusion=premise, premises=(), rule=ProofRule.INFERENCE),), {}) is True
