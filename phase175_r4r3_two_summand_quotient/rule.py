"""General EHP quotient rule for an elementary rank-two 2-group.

A = (Z/2){a} + (Z/2){b}, C = (Z/2){z},
C --Delta--> A --E--> B is exact, E onto, Delta(z) is one
of a,b, and E(the other) = y. Then B = (Z/2){y}.

The rule consumes only explicit typed proof goals. It registers no literature
claims, never treats a printed target theorem as a proof, and has no special
sphere-dimension branches. It is NOT wired to public search in R4R3.
"""
from __future__ import annotations

from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from expression import Composition, HomotopyElement, IteratedSuspension
from phase169_r10e5_composite_generator_image.rule import _endpoints
from proof import (
    InferenceRule,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)
from toda_rules import TodaProp42ExactnessStatement


RULE_NAME = "EHP exact rank-two elementary 2-group quotient by a generated summand"


def _rank_two_endpoints(element: object) -> tuple[int, int] | None:
    """Typed endpoints for rank-two generators, including iterated suspension.

    The inner map must itself have valid endpoints. A suspension exponent must
    be a nonnegative exact int, not a bool, symbolic value or negative integer.
    Names alone never certify an expression's endpoints.
    """
    if isinstance(element, IteratedSuspension):
        exponent = element.exponent
        if type(exponent) is not int or exponent < 0:
            return None
        inner = _rank_two_endpoints(element.expression)
        if inner is None:
            return None
        return inner[0] + exponent, inner[1] + exponent
    if isinstance(element, Composition):
        left = _rank_two_endpoints(element.left)
        right = _rank_two_endpoints(element.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    return _endpoints(element)


def two_summand_quotient_inputs(
    goal: object,
    domain_relation: object,
    delta_source_relation: object,
    delta_image: object,
    suspension_image: object,
) -> tuple[object, ...] | None:
    """Check all source, target, generator and consecutive-EHP map types.

    No input is trusted merely because it is constructed as a statement.
    The returned six statements must each be independently proved before the
    inference may be applied. The selected surviving summand is not assumed.
    """
    if (type(goal) is not CyclicStructureStatement
            or type(goal.group) is not TodaPrimaryGroup
            or goal.order != 2
            or type(domain_relation) is not Relation
            or domain_relation.relation_type is not RelationType.EQUALITY
            or type(domain_relation.lhs) is not TodaPrimaryGroup
            or type(domain_relation.rhs) is not DirectSumGroup
            or type(delta_source_relation) is not Relation
            or delta_source_relation.relation_type is not RelationType.EQUALITY
            or type(delta_source_relation.lhs) is not TodaPrimaryGroup
            or type(delta_source_relation.rhs) is not FiniteCyclicGroup
            or delta_source_relation.rhs.order != 2
            or type(delta_image) is not GeneratorImage
            or type(suspension_image) is not GeneratorImage):
        return None

    parts = domain_relation.rhs.summands
    if (type(parts) is not tuple
            or len(parts) != 2
            or any(type(x) is not FiniteCyclicGroup or x.order != 2 for x in parts)):
        return None

    first = parts[0].generator
    second = parts[1].generator
    if first == second:
        return None

    source = delta_source_relation.lhs
    middle = domain_relation.lhs
    target = goal.group
    delta = TodaDeltaMap(source, middle)
    suspension = TodaSuspensionMap(middle, target)
    if (delta_image.map != delta
            or suspension_image.map != suspension
            or delta_image.source_generator != delta_source_relation.rhs.generator
            or suspension_image.target_generator != goal.generator):
        return None

    killed = delta_image.target_generator
    survivor = suspension_image.source_generator
    if not ((killed == first and survivor == second)
            or (killed == second and survivor == first)):
        return None

    # An expression's printed name alone does not type it as a generator.
    if (_rank_two_endpoints(first) != (middle.group_dimension, middle.sphere_dimension)
            or _rank_two_endpoints(second) != (middle.group_dimension, middle.sphere_dimension)
            or _rank_two_endpoints(delta_image.source_generator)
            != (source.group_dimension, source.sphere_dimension)
            or _rank_two_endpoints(goal.generator)
            != (target.group_dimension, target.sphere_dimension)):
        return None

    exactness = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=source,
        middle_term=middle,
        target_term=target,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
    ))
    if prop42_exactness_indices(exactness) is None:
        return None

    return (
        domain_relation,
        delta_source_relation,
        delta_image,
        exactness,
        MapSurjective(suspension),
        suspension_image,
    )


def two_summand_quotient_rule(
    goal: CyclicStructureStatement,
    domain_relation: Relation,
    delta_source_relation: Relation,
    delta_image: GeneratorImage,
    suspension_image: GeneratorImage,
) -> InferenceRule:
    """Apply the quotient only after all six exact premises are proved.

    Earlier group relations may be admitted prior results; the four map and
    exactness facts must be INFERENCE ProofSteps. Provenance/trust for prior
    relations is checked separately by the existing proof-search boundary.
    """
    required = two_summand_quotient_inputs(
        goal, domain_relation, delta_source_relation, delta_image, suspension_image,
    )
    if required is None:
        raise ValueError("not a typed rank-two EHP quotient goal")

    def guard(premises, bindings):
        return (
            len(premises) == 6
            and tuple(step.conclusion for step in premises) == required
            and all(step.rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
                    for step in premises[:2])
            and all(step.rule is ProofRule.INFERENCE for step in premises[2:])
            and two_summand_quotient_inputs(
                goal, domain_relation, delta_source_relation, delta_image,
                suspension_image,
            ) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "If Delta from a proved order-two cyclic group maps its generator "
            "to one direct-sum generator of a proved (Z/2)^2, EHP exactness "
            "identifies the E-kernel with that summand. With independently "
            "proved E surjective and E of the other generator equal to y, "
            "the target is (Z/2){y}."
        ),
        premise_patterns=tuple(
            PremisePattern(
                statement_type=type(statement),
                statement_pattern=statement,
                relation_type=RelationType.EQUALITY
                if isinstance(statement, Relation) else None,
            )
            for statement in required
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_two_summand_quotient(
    goal: object,
    domain_relation: object,
    delta_source_relation: object,
    delta_image: object,
    suspension_image: object,
) -> tuple[GoalExpansion, ...]:
    """Isolated backward proposal: no proof leaf or production registration."""
    required = two_summand_quotient_inputs(
        goal, domain_relation, delta_source_relation, delta_image, suspension_image,
    )
    if required is None:
        return ()
    return (GoalExpansion(
        two_summand_quotient_rule(
            goal, domain_relation, delta_source_relation,
            delta_image, suspension_image,
        ),
        required,
    ),)
