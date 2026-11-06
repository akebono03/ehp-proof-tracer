"""Generic reassociation of a proved composition-valued generator image.

A typed proof that E(g) is a right-associated composite implies that it
is the equivalent left-associated composite. This isolated rule does not
prove E(g), the cited Toda annihilator, or any group presentation.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from proof import InferenceRule, PremisePattern, ProofRule

RULE_NAME = "composition associativity transports a verified generator image"


def typed_composition_factors(value: object) -> tuple[HomotopyElement, ...] | None:
    """Flatten only well-typed compositions of actual typed sphere maps."""
    if isinstance(value, HomotopyElement):
        if expression_endpoints(value) is None:
            return None
        return (value,)
    if not isinstance(value, Composition) or expression_endpoints(value) is None:
        return None
    left = typed_composition_factors(value.left)
    right = typed_composition_factors(value.right)
    if left is None or right is None:
        return None
    return left + right


def right_associated_composition(value: object) -> Composition | None:
    """Keep every factor and its order; alter parentheses only."""
    factors = typed_composition_factors(value)
    if factors is None or len(factors) < 3:
        return None
    result: object = factors[-1]
    for factor in reversed(factors[:-1]):
        result = Composition(factor, result)
    if not isinstance(result, Composition):
        return None
    if expression_endpoints(result) != expression_endpoints(value):
        return None
    return result


def generator_image_associativity_inputs(
    goal: object,
) -> tuple[GeneratorImage] | None:
    """Demand a proved right-associated image for the original same g and E."""
    if not isinstance(goal, GeneratorImage):
        return None
    mapping = goal.map
    if not isinstance(mapping, TodaSuspensionMap):
        return None
    domain, target = mapping.source_group, mapping.target_group
    if not isinstance(domain, TodaPrimaryGroup) or not isinstance(target, TodaPrimaryGroup):
        return None
    degree, sphere = domain.group_dimension, domain.sphere_dimension
    if (type(degree) is not int or type(sphere) is not int
            or sphere < 2 or degree < sphere
            or target != TodaPrimaryGroup(degree + 1, sphere + 1)):
        return None
    if (expression_endpoints(goal.source_generator) != (degree, sphere)
            or expression_endpoints(goal.target_generator) != (degree + 1, sphere + 1)):
        return None
    normalized = right_associated_composition(goal.target_generator)
    if normalized is None or normalized == goal.target_generator:
        return None
    return (GeneratorImage(mapping, goal.source_generator, normalized),)


def generator_image_associativity_rule(goal: GeneratorImage) -> InferenceRule:
    """Allow only one independently inferred and identically typed premise."""
    required = generator_image_associativity_inputs(goal)
    if required is None:
        raise ValueError("goal has no valid nontrivial composition reassociation")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == required[0]
            and generator_image_associativity_inputs(goal) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "Composition is associative in the homotopy category. A separately "
            "proved image of precisely the same generator under precisely "
            "the same map may be rebracketed without adding any source fact."
        ),
        premise_patterns=(PremisePattern(
            statement_type=GeneratorImage,
            statement_pattern=required[0],
            proof_rule=ProofRule.INFERENCE,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_generator_image_associativity(goal: object) -> tuple[GoalExpansion, ...]:
    """Create an unproved backward branch without changing public providers."""
    inputs = generator_image_associativity_inputs(goal)
    if inputs is None:
        return ()
    return (GoalExpansion(generator_image_associativity_rule(goal), inputs),)
