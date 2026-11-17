"""Conditional, dimension-checked Toda Proposition 2.5 equality inference.

For alpha in pi_(i+1)^(2m+1) and beta in pi_(j-1)^(i-1), the
source proves Delta(alpha) o beta is contained in Delta(alpha o E^2 beta).
Under m odd OR j < 3m-1 the inclusion is equality. Given separately
proved signed Delta(alpha)=+/-x and alpha o E^2 beta=gamma, derive
Delta(gamma)=+/-(x o beta), keeping the sign unresolved.

The alternative 2-primary equality branch is deliberately NOT inferred from
an unproved flag. This isolated rule registers no source statements or GIVEN
and is not connected to public proof search in R4R7.
"""
from __future__ import annotations

from expression import (
    Composition,
    HomotopyElement,
    IteratedSuspension,
    Multiple,
    Sum,
    Suspension,
)
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import (
    InferenceRule,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)
from toda_rules import TodaDeltaImageUpToSignStatement


RULE_NAME = "Toda Proposition 2.5 conditional signed Delta composition equality"


def typed_endpoints(expression: object) -> tuple[int, int] | None:
    """Check the actual sphere source and target, including identity maps."""
    if isinstance(expression, HomotopyElement):
        values = (expression.dimension, expression.source, expression.target)
        if (any(type(value) is not int for value in values)
                or expression.dimension != expression.target
                or expression.target < 2
                or expression.source < expression.target):
            return None
        return expression.source, expression.target
    if isinstance(expression, Composition):
        left = typed_endpoints(expression.left)
        right = typed_endpoints(expression.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    if isinstance(expression, (Suspension, IteratedSuspension)):
        exponent = 1 if isinstance(expression, Suspension) else expression.exponent
        if type(exponent) is not int or exponent < 0:
            return None
        endpoints = typed_endpoints(expression.expression)
        if endpoints is None:
            return None
        return endpoints[0] + exponent, endpoints[1] + exponent
    if isinstance(expression, Multiple):
        if type(expression.coefficient) is not int:
            return None
        return typed_endpoints(expression.expression)
    if isinstance(expression, Sum):
        left = typed_endpoints(expression.left)
        right = typed_endpoints(expression.right)
        if left is None or left != right:
            return None
        return left
    return None


def prop25_inputs(
    goal: object,
    signed_delta: object,
    composition_identity: object,
) -> tuple[TodaDeltaImageUpToSignStatement, Relation] | None:
    """Return the two independently proved obligations or reject the goal.

    Dimensions are reconstructed from the actual typed alpha/beta/gamma and
    Delta maps. Neither a familiar symbol name nor a stated index is trusted.
    This branch uses only the explicitly checkable arithmetic hypotheses of
    Prop 2.5 (m odd or j < 3m-1), not presumed 2-primary membership.
    """
    if (type(goal) is not TodaDeltaImageUpToSignStatement
            or type(signed_delta) is not TodaDeltaImageUpToSignStatement
            or type(composition_identity) is not Relation
            or composition_identity.relation_type is not RelationType.EQUALITY
            or not isinstance(composition_identity.lhs, Composition)
            or not isinstance(composition_identity.lhs.right, IteratedSuspension)
            or type(composition_identity.lhs.right.exponent) is not int
            or composition_identity.lhs.right.exponent != 2):
        return None

    alpha = composition_identity.lhs.left
    beta = composition_identity.lhs.right.expression
    gamma = composition_identity.rhs
    alpha_pair = typed_endpoints(alpha)
    beta_pair = typed_endpoints(beta)
    gamma_pair = typed_endpoints(gamma)
    value_pair = typed_endpoints(signed_delta.positive_value)
    if (alpha_pair is None or beta_pair is None
            or gamma_pair is None or value_pair is None
            or signed_delta.element != alpha):
        return None

    i = alpha_pair[0] - 1
    j = beta_pair[0] + 1
    if ((alpha_pair[1] - 1) % 2 != 0):
        return None
    m = (alpha_pair[1] - 1) // 2
    if (m < 2 or i < 2 * m or j < i
            or beta_pair != (j - 1, i - 1)
            or gamma_pair != (j + 1, 2 * m + 1)
            or value_pair != (i - 1, m)):
        return None
    if not (m % 2 == 1 or j < 3 * m - 1):
        return None

    source_delta = TodaDeltaMap(
        TodaPrimaryGroup(i + 1, 2 * m + 1),
        TodaPrimaryGroup(i - 1, m),
    )
    target_delta = TodaDeltaMap(
        TodaPrimaryGroup(j + 1, 2 * m + 1),
        TodaPrimaryGroup(j - 1, m),
    )
    if (signed_delta.map != source_delta
            or goal.map != target_delta
            or goal.element != gamma
            or goal.positive_value != Composition(signed_delta.positive_value, beta)
            or typed_endpoints(composition_identity.lhs) != gamma_pair
            or typed_endpoints(goal.positive_value) != (j - 1, m)):
        return None
    return signed_delta, composition_identity


def prop25_signed_composition_rule(
    goal: TodaDeltaImageUpToSignStatement,
    signed_delta: TodaDeltaImageUpToSignStatement,
    composition_identity: Relation,
) -> InferenceRule:
    """Require two INFERENCE ProofSteps before concluding a signed image."""
    required = prop25_inputs(goal, signed_delta, composition_identity)
    if required is None:
        raise ValueError("not a typed conditional Proposition 2.5 goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and prop25_inputs(goal, signed_delta, composition_identity) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "With m odd or j<3m-1, Toda Proposition 2.5 turns the "
            "Delta-composition inclusion into equality. A proved signed "
            "Delta(alpha) and independently proved alpha o E^2(beta)=gamma "
            "give Delta(gamma)=+/-(Delta(alpha) representative o beta). "
            "Do not choose the sign or assume 2-primary membership."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaDeltaImageUpToSignStatement,
                statement_pattern=required[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=required[1],
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_prop25_signed_composition(
    goal: object,
    signed_delta: object,
    composition_identity: object,
) -> tuple[GoalExpansion, ...]:
    """An isolated backward proposal, not a source or proof certificate."""
    required = prop25_inputs(goal, signed_delta, composition_identity)
    if required is None:
        return ()
    return (GoalExpansion(
        prop25_signed_composition_rule(goal, signed_delta, composition_identity),
        required,
    ),)
