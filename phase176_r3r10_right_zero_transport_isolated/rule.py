"""Isolated generic right-composition transport for a zero suspension image.

No provider registration or source/goal assertion is performed here.
A proven E(a)=0 implies E(a o b)=0 for a well-typed composite.
"""
from __future__ import annotations

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
from proof import InferenceRule, PremisePattern, ProofRule


RULE_NAME = "zero suspension image transports over typed right composition"


def right_zero_transport_inputs(
    goal: object, base: object,
) -> tuple[GeneratorImage] | None:
    """Require the same typed E, zero image, exact source prefix, and one right factor.

    Flattening source factors uses the associativity of composition. The
    source generator is never selected by its display name. Both zero-image
    statements are proof obligations, not assumptions.
    """
    if type(goal) is not GeneratorImage or type(base) is not GeneratorImage:
        return None
    if (type(goal.map) is not TodaSuspensionMap
            or type(base.map) is not TodaSuspensionMap
            or type(goal.target_generator) is not Zero
            or type(base.target_generator) is not Zero):
        return None
    for statement in (goal, base):
        source = statement.map.source_group
        target = statement.map.target_group
        if type(source) is not TodaPrimaryGroup or type(target) is not TodaPrimaryGroup:
            return None
        degree, sphere = source.group_dimension, source.sphere_dimension
        if (type(degree) is not int or type(sphere) is not int
                or sphere < 2 or degree < sphere
                or target != TodaPrimaryGroup(degree + 1, sphere + 1)
                or expression_endpoints(statement.source_generator) != (degree, sphere)):
            return None
    whole_source = goal.map.source_group
    base_source = base.map.source_group
    if (whole_source.sphere_dimension != base_source.sphere_dimension
            or whole_source.group_dimension <= base_source.group_dimension):
        return None
    whole_factors = typed_composition_factors(goal.source_generator)
    base_factors = typed_composition_factors(base.source_generator)
    if (whole_factors is None or base_factors is None
            or len(base_factors) < 2
            or len(whole_factors) != len(base_factors) + 1
            or whole_factors[:len(base_factors)] != base_factors):
        return None
    # Composition is well-typed both before and after suspending, and the
    # extra factor is exactly the final right-hand factor of the goal.
    trailing = whole_factors[-1]
    if expression_endpoints(trailing) != (
        whole_source.group_dimension, base_source.group_dimension,
    ):
        return None
    return (base,)


def right_zero_transport_rule(goal: GeneratorImage, base: GeneratorImage) -> InferenceRule:
    required = right_zero_transport_inputs(goal, base)
    if required is None:
        raise ValueError("right zero transport requires exact typed composite data")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == required[0]
            and right_zero_transport_inputs(goal, base) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "For a suspension map, E(a)=0 implies E(a composed on the right "
            "with b)=0 by functoriality and the zero-map law. The exact typed "
            "prefix, map dimensions and inferred antecedent are required."
        ),
        premise_patterns=(PremisePattern(
            statement_type=GeneratorImage,
            statement_pattern=base,
            proof_rule=ProofRule.INFERENCE,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_right_zero_transport(
    goal: object, base: object,
) -> tuple[GoalExpansion, ...]:
    inputs = right_zero_transport_inputs(goal, base)
    if inputs is None:
        return ()
    return (GoalExpansion(
        rule=right_zero_transport_rule(goal, base),
        subgoals=inputs,
    ),)
