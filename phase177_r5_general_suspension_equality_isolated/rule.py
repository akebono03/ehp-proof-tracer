"""Typed general suspension-image and iterated-notation equality rules.

No family names, stable-range assumption, source registration or public wiring.
"""
from __future__ import annotations

from expression import IteratedSuspension, Suspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType

IMAGE_RULE = 'proved typed suspension image yields element equality'
NOTATION_RULE = 'typed iterated suspension notation composition'


def suspension_image_input(goal: object) -> GeneratorImage | None:
    """E(x)=y needs the exact typed one-step image of x, not an index guess."""
    if (type(goal) is not Relation or goal.relation_type is not RelationType.EQUALITY
            or type(goal.lhs) is not Suspension):
        return None
    x, y = goal.lhs.expression, goal.rhs
    a, b = typed_endpoints(x), typed_endpoints(y)
    if a is None or b != (a[0]+1, a[1]+1):
        return None
    return GeneratorImage(TodaSuspensionMap(TodaPrimaryGroup(*a), TodaPrimaryGroup(*b)), x, y)


def expand_suspension_image_equality(goal: object) -> tuple[GoalExpansion, ...]:
    required = suspension_image_input(goal)
    if required is None:
        return ()

    def guard(premises, bindings):
        return (len(premises) == 1 and premises[0].rule is ProofRule.INFERENCE
                and premises[0].conclusion == required
                and suspension_image_input(goal) == required)

    rule = InferenceRule(
        name=IMAGE_RULE,
        description='An independently inferred one-step E-image gives the identical typed element equality.',
        premise_patterns=(PremisePattern(proof_rule=ProofRule.INFERENCE,
                         statement_type=GeneratorImage, statement_pattern=required),),
        match_guard=guard, conclusion_pattern=goal,
    )
    return (GoalExpansion(rule, (required,)),)


def suspension_layers(value: object) -> tuple[object, int, int] | None:
    """Return exact base, total exponent and number of suspension wrappers."""
    if typed_endpoints(value) is None:
        return None
    total = layers = 0
    while type(value) in (Suspension, IteratedSuspension):
        exponent = 1 if type(value) is Suspension else value.exponent
        if type(exponent) is not int or exponent < 0:
            return None
        total += exponent
        layers += 1
        value = value.expression
    return value, total, layers


def is_iterated_notation_equality(goal: object) -> bool:
    """Only alternate parentheses/exponents of the very same typed base.

    E^1 versus E is already covered by the existing one-step bridge.
    Neither a stable-family identification nor suspension cancellation is used.
    """
    if (type(goal) is not Relation or goal.relation_type is not RelationType.EQUALITY
            or goal.lhs == goal.rhs):
        return False
    left, right = suspension_layers(goal.lhs), suspension_layers(goal.rhs)
    return (left is not None and right is not None
            and left[:2] == right[:2] and left[1] >= 2
            and min(left[2], right[2]) >= 1 and max(left[2], right[2]) >= 2
            and typed_endpoints(goal.lhs) == typed_endpoints(goal.rhs))


def expand_iterated_notation_equality(goal: object) -> tuple[GoalExpansion, ...]:
    if not is_iterated_notation_equality(goal):
        return ()

    def guard(premises, bindings):
        return not premises and not bindings and is_iterated_notation_equality(goal)

    rule = InferenceRule(
        name=NOTATION_RULE,
        description='Repeated suspension is defined by composition; only parentheses and exponents change.',
        premise_patterns=(), match_guard=guard, conclusion_pattern=goal,
    )
    return (GoalExpansion(rule, ()),)
