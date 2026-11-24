"""Isolated, source-dependent right-Hopf formula for a composite beta.

The existing single-element Toda Proposition 2.2 path remains unchanged.
No desired Hopf value, group structure, or reference is registered as GIVEN.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


COMPOSITE_FORMULA_RULE_NAME = "specialize cited Toda Proposition 2.2 for a composite right factor"
COMPOSITE_SUBSTITUTION_RULE_NAME = "substitute proved Hopf image into composite right formula"


def composite_right_formula_parts(goal: object) -> tuple[object, Composition] | None:
    """Recognize H(alpha o E beta) = H(alpha) o E beta for typed composite beta.

    `Suspension(Composition(...))` has no endpoints in the legacy Expression
    class, so determine its sphere dimensions from the typed, *unsuspended*
    composite, rather than interpreting absent endpoints as a valid match.
    """
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)):
        return None
    product = goal.lhs.expression
    alpha = product.left
    right = product.right
    if (not isinstance(alpha, (HomotopyElement, Composition))
            or not isinstance(right, Suspension)
            or not isinstance(right.expression, Composition)):
        return None
    beta = right.expression
    alpha_endpoints = expression_endpoints(alpha)
    beta_endpoints = expression_endpoints(beta)
    if (alpha_endpoints is None or beta_endpoints is None
            or alpha_endpoints[0] != beta_endpoints[1] + 1):
        return None
    expected_rhs = Composition(MapApplication(EHP_H_MAP, alpha), right)
    return (alpha, beta) if goal.rhs == expected_rhs else None


def composite_right_formula_rule(goal: Relation) -> InferenceRule:
    """Require the independently screened universal source for specialization."""
    if composite_right_formula_parts(goal) is None:
        raise ValueError("not a typed composite-right Toda Proposition 2.2 formula")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == TodaProp22RightFormula()
            and composite_right_formula_parts(goal) is not None
        )

    return InferenceRule(
        name=COMPOSITE_FORMULA_RULE_NAME,
        description=(
            "Specialize the independently cited universal right-Hopf formula "
            "when its suspended right factor is a typed composite."
        ),
        premise_patterns=(PremisePattern(
            statement_type=TodaProp22RightFormula,
            statement_pattern=TodaProp22RightFormula(),
            proof_rule=ProofRule.GIVEN,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def composite_hopf_substitution_inputs(
    goal: object,
) -> tuple[Relation, Relation] | None:
    """Return the cited formula and independent H(alpha)=delta obligations.

    The value delta is checked against the canonical degree of the EHP H map:
    an element S^q -> S^n has H-value S^q -> S^(2n-1). The right-hand
    composite must retain the suspended beta verbatim.
    """
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)
            or not isinstance(goal.rhs, Composition)):
        return None
    product = goal.lhs.expression
    alpha = product.left
    right = product.right
    delta = goal.rhs.left
    if (not isinstance(alpha, (HomotopyElement, Composition))
            or not isinstance(right, Suspension)
            or not isinstance(right.expression, Composition)
            or goal.rhs.right != right):
        return None
    alpha_endpoints = expression_endpoints(alpha)
    delta_endpoints = expression_endpoints(delta)
    beta_endpoints = expression_endpoints(right.expression)
    if (alpha_endpoints is None or delta_endpoints is None
            or beta_endpoints is None):
        return None
    if alpha_endpoints[0] != beta_endpoints[1] + 1:
        return None
    if delta_endpoints != (alpha_endpoints[0], 2 * alpha_endpoints[1] - 1):
        return None
    formula = Relation(
        lhs=goal.lhs,
        rhs=Composition(MapApplication(EHP_H_MAP, alpha), right),
        relation_type=RelationType.EQUALITY,
    )
    if composite_right_formula_parts(formula) != (alpha, right.expression):
        return None
    hopf_value = Relation(
        lhs=MapApplication(EHP_H_MAP, alpha),
        rhs=delta,
        relation_type=RelationType.EQUALITY,
    )
    return formula, hopf_value


def composite_hopf_substitution_rule(goal: Relation) -> InferenceRule:
    """A proof of both subgoals is mandatory; candidate generation proves none."""
    inputs = composite_hopf_substitution_inputs(goal)
    if inputs is None:
        raise ValueError("not a typed composite-right Hopf substitution goal")
    formula, hopf_value = inputs

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == formula
            and premises[1].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[1].conclusion == hopf_value
            and composite_hopf_substitution_inputs(goal) == inputs
        )

    return InferenceRule(
        name=COMPOSITE_SUBSTITUTION_RULE_NAME,
        description=(
            "Substitute an independently proved H(alpha)=delta into a proved "
            "specialization H(alpha o E beta)=H(alpha) o E beta."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=Relation,
                statement_pattern=formula,
                proof_rule=ProofRule.INFERENCE,
            ),
            PremisePattern(
                statement_type=Relation,
                statement_pattern=hopf_value,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_composite_right_hopf(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Offer conservative backward candidates only with one screened source."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if available.count(TodaProp22RightFormula()) != 1:
        return ()
    if composite_right_formula_parts(goal) is not None:
        return (GoalExpansion(
            composite_right_formula_rule(goal),
            (TodaProp22RightFormula(),),
        ),)
    inputs = composite_hopf_substitution_inputs(goal)
    if inputs is None:
        return ()
    return (GoalExpansion(composite_hopf_substitution_rule(goal), inputs),)
