"""A verified composite suspension image implies an element equality.

Isolated, general bridge: neither a special eta fact nor a GIVEN is created.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, Suspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


def composite_suspension_equality_input(goal: object) -> GeneratorImage | None:
    """Require typed composite factors and the same degree-one E-image."""
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, Suspension)
            or not isinstance(goal.lhs.expression, Composition)
            or not isinstance(goal.rhs, Composition)):
        return None
    source = goal.lhs.expression
    target = goal.rhs
    if not all(isinstance(factor, HomotopyElement) for factor in
               (source.left, source.right, target.left, target.right)):
        return None
    endpoints_source = expression_endpoints(source)
    endpoints_target = expression_endpoints(target)
    if (endpoints_source is None or endpoints_target is None
            or endpoints_target !=
            (endpoints_source[0] + 1, endpoints_source[1] + 1)):
        return None
    if (not isinstance(endpoints_source[0], int)
            or not isinstance(endpoints_source[1], int)
            or endpoints_source[1] < 2):
        return None
    degree, sphere = endpoints_source
    return GeneratorImage(
        TodaSuspensionMap(
            TodaPrimaryGroup(degree, sphere),
            TodaPrimaryGroup(degree + 1, sphere + 1),
        ),
        source,
        target,
    )


def composite_suspension_equality_rule(goal: Relation) -> InferenceRule:
    """Keep the composite image as an independently proved premise."""
    required = composite_suspension_equality_input(goal)
    if required is None:
        raise ValueError("not a well-typed composite suspension equality")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == required
            and composite_suspension_equality_input(goal) == required
        )

    return InferenceRule(
        name="proved composite suspension image yields typed element equality",
        description=(
            "An independently proved E-image of a typed composite "
            "identifies its suspension with the same target composite."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.INFERENCE,
            statement_type=GeneratorImage,
            statement_pattern=required,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_composite_suspension_equality(goal: object) -> tuple[GoalExpansion, ...]:
    """Return an open backward obligation, never a verified proof step."""
    required = composite_suspension_equality_input(goal)
    if required is None:
        return ()
    return (GoalExpansion(composite_suspension_equality_rule(goal), (required,)),)
