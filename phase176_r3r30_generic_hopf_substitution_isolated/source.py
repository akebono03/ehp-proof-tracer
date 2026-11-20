"""General, type-checked substitution into cited Toda Proposition 2.2.

This module creates no GIVEN and does not assert any particular Hopf image.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2h_prop22_cited_hopf.source import (
    TodaProp22RightFormula, _formula_parts,
)
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from proof import (
    InferenceRule, PremisePattern, ProofRule, Relation, RelationType,
)


def generic_hopf_substitution_inputs(
    goal: object,
) -> tuple[Relation, Relation] | None:
    """Derive the two *independent* proof obligations for H(α∘Eβ)=δ∘Eβ."""
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
    if (not isinstance(alpha, (HomotopyElement, Composition))
            or not isinstance(right, Suspension)
            or not isinstance(right.expression, HomotopyElement)
            or goal.rhs.right != right):
        return None
    delta = goal.rhs.left
    endpoints = expression_endpoints(delta)
    beta_endpoints = expression_endpoints(right.expression)
    if endpoints is None or beta_endpoints is None:
        return None
    suspended = (beta_endpoints[0] + 1, beta_endpoints[1] + 1)
    if endpoints[0] != suspended[1]:
        return None
    formula = Relation(
        goal.lhs, Composition(MapApplication(EHP_H_MAP, alpha), right),
        RelationType.EQUALITY,
    )
    if _formula_parts(formula) != (alpha, right.expression):
        return None
    hopf_value = Relation(
        MapApplication(EHP_H_MAP, alpha), delta, RelationType.EQUALITY,
    )
    return formula, hopf_value


def generic_hopf_substitution_rule(goal: Relation) -> InferenceRule:
    """Keep both required premises checked by ordinary verified proof search."""
    inputs = generic_hopf_substitution_inputs(goal)
    if inputs is None:
        raise ValueError("invalid typed right-Hopf substitution goal")
    formula, hopf_value = inputs

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == formula
            and premises[1].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[1].conclusion == hopf_value
            and generic_hopf_substitution_inputs(goal) == inputs
        )

    return InferenceRule(
        name="substitute independently proved Hopf value into cited right formula",
        description=(
            "From a proved instance H(alpha o E beta)=H(alpha) o E beta "
            "and an independently proved H(alpha)=delta, conclude "
            "H(alpha o E beta)=delta o E beta."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                statement_pattern=formula,
            ),
            PremisePattern(
                statement_type=Relation,
                statement_pattern=hopf_value,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_generic_hopf_substitution(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Never treat a desired Hopf value as an available GIVEN."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if available.count(TodaProp22RightFormula()) != 1:
        return ()
    inputs = generic_hopf_substitution_inputs(goal)
    if inputs is None:
        return ()
    return (GoalExpansion(generic_hopf_substitution_rule(goal), inputs),)
