"""A proved image f(g)=c and a proved relation c=0 imply f(g)=0.

This is a generic inference, independent of the number of composition factors.
No source theorem, database group presentation or root group is asserted here.
"""
from __future__ import annotations

from expression import Composition, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = "proved composite image and proved composite zero imply generator zero"


def composite_value_zero_inputs(
    goal: object, composite_image: object,
) -> tuple[GeneratorImage, Relation] | None:
    """Require the very same map, generator and typed nonzero composite value."""
    if (not isinstance(goal, GeneratorImage)
            or not isinstance(goal.map, TodaSuspensionMap)
            or not isinstance(goal.target_generator, Zero)
            or not isinstance(composite_image, GeneratorImage)
            or composite_image.map != goal.map
            or composite_image.source_generator != goal.source_generator
            or not isinstance(composite_image.target_generator, Composition)):
        return None
    mapping = goal.map
    domain, codomain = mapping.source_group, mapping.target_group
    if (not isinstance(domain, TodaPrimaryGroup)
            or not isinstance(codomain, TodaPrimaryGroup)):
        return None
    q, n = domain.group_dimension, domain.sphere_dimension
    if (type(q) is not int or type(n) is not int or n < 2 or q < n
            or codomain != TodaPrimaryGroup(q + 1, n + 1)):
        return None
    if (typed_element_span(goal.source_generator) != (q, n)
            or typed_element_span(composite_image.target_generator)
            != (q + 1, n + 1)):
        return None
    return (composite_image, Relation(
        composite_image.target_generator, Zero(), RelationType.EQUALITY,
    ))


def proved_composite_zero_image_rule(
    goal: GeneratorImage, composite_image: GeneratorImage,
) -> InferenceRule:
    """No conclusion is admitted unless both independently proved steps match."""
    required = composite_value_zero_inputs(goal, composite_image)
    if required is None:
        raise ValueError("a typed suspension composite image is required")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and composite_value_zero_inputs(goal, composite_image) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "If a separately verified image E(g)=c and an independently "
            "verified relation c=0 hold, then E(g)=0. The composite may "
            "contain two or more factors; neither premise is created here."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=GeneratorImage,
                statement_pattern=required[0],
                proof_rule=ProofRule.INFERENCE,
            ),
            PremisePattern(
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=required[1],
                proof_rule=ProofRule.INFERENCE,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_proved_composite_zero_image(
    goal: object, composite_image: object,
) -> tuple[GoalExpansion, ...]:
    """Return unproved backward obligations; never insert a ProofStep."""
    required = composite_value_zero_inputs(goal, composite_image)
    if required is None:
        return ()
    return (GoalExpansion(
        rule=proved_composite_zero_image_rule(goal, composite_image),
        subgoals=required,
    ),)
