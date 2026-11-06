"""Generic composition-zero inference, isolated from public proof search.

A verified image f(g)=a∘b and an independently proved a=0 imply f(g)=0.
The source relation and mapped composite are separate typed proof obligations.
"""
from __future__ import annotations

from expression import Composition, Expression, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = "zero left composition factor implies zero generator image"


def expression_endpoints(value: object) -> tuple[int, int] | None:
    """Return (source sphere, target sphere) for explicitly typed composites."""
    if isinstance(value, HomotopyElement):
        if (not all(type(v) is int for v in
                    (value.dimension, value.source, value.target))
                or value.dimension != value.target
                or value.target < 2 or value.source <= value.target):
            return None
        return value.source, value.target
    if isinstance(value, Composition):
        left = expression_endpoints(value.left)
        right = expression_endpoints(value.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    return None


def composite_zero_generator_inputs(
    goal: object,
    composite_image: object,
) -> tuple[GeneratorImage, Relation] | None:
    """Demand a separately proved composite image and zero left-factor fact."""
    if (not isinstance(goal, GeneratorImage)
            or not isinstance(goal.map, TodaSuspensionMap)
            or not isinstance(goal.target_generator, Zero)
            or not isinstance(goal.source_generator, Expression)
            or isinstance(goal.source_generator, Zero)
            or not isinstance(composite_image, GeneratorImage)
            or composite_image.map != goal.map
            or composite_image.source_generator != goal.source_generator
            or not isinstance(composite_image.target_generator, Composition)):
        return None
    domain = goal.map.source_group
    target = goal.map.target_group
    if (not isinstance(domain, TodaPrimaryGroup)
            or not isinstance(target, TodaPrimaryGroup)):
        return None
    degree = domain.group_dimension
    sphere = domain.sphere_dimension
    if (type(degree) is not int or type(sphere) is not int
            or sphere < 2 or degree < sphere
            or target != TodaPrimaryGroup(degree + 1, sphere + 1)):
        return None
    composite = composite_image.target_generator
    if (expression_endpoints(composite) !=
            (degree + 1, sphere + 1)):
        return None
    left = composite.left
    right = composite.right
    if expression_endpoints(left) is None or expression_endpoints(right) is None:
        return None
    return composite_image, Relation(
        lhs=left, rhs=Zero(), relation_type=RelationType.EQUALITY,
    )


def generator_zero_from_composite_rule(
    goal: GeneratorImage, composite_image: GeneratorImage,
) -> InferenceRule:
    """Require both obligations as INFERENCE steps; never add a GIVEN."""
    required = composite_zero_generator_inputs(goal, composite_image)
    if required is None:
        raise ValueError("invalid composite-zero generator image")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and composite_zero_generator_inputs(goal, composite_image) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "If a separately proved generator image is a composition a∘b, "
            "and an independent typed proof establishes a=0, then "
            "the generator maps to zero. No source equation is admitted here."
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


def expand_generator_zero_from_composite(
    goal: object,
    composite_image: object,
) -> tuple[GoalExpansion, ...]:
    """Offer one unproved generic candidate without modifying search providers."""
    required = composite_zero_generator_inputs(goal, composite_image)
    if required is None:
        return ()
    return (GoalExpansion(
        generator_zero_from_composite_rule(goal, composite_image),
        required,
    ),)
