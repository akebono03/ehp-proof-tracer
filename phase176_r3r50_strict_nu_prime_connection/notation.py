"""Checked notation transport for the same typed nu-prime inside H(alpha o gamma).

No mathematical identity or source registration is introduced. An ordinary
proved canonical equality is a required premise, not an assumed alias fact.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

from expression import Composition, HomotopyElement, MapApplication
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from phase175_r4r12r13r7_typed_nu_prime_notation.notation import _nu_prime_element_alias
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = 'transport proved Hopf equality across strict typed nu-prime notation'


def typed_hopf_composition(value: object) -> Composition | None:
    """Accept only a well-typed binary composition inside an EHP H equality."""
    if (type(value) is not Relation or value.relation_type is not RelationType.EQUALITY
            or type(value.lhs) is not MapApplication or value.lhs.map != EHP_H_MAP
            or type(value.lhs.expression) is not Composition
            or type(value.lhs.expression.left) is not HomotopyElement
            or expression_endpoints(value.lhs.expression) is None):
        return None
    return value.lhs.expression


def strict_nu_prime_alias(left: object, right: object) -> bool:
    """Reuse R13R7's encoding guard, at the actual type of Toda's nu-prime."""
    return (left != right and _nu_prime_element_alias(left, right)
            and expression_endpoints(left) == (6, 3)
            and expression_endpoints(right) == (6, 3))


def alias_hopf_input(goal: object, canonical: object) -> Relation | None:
    """Check the entire equality, allowing only a strict left-factor alias."""
    target = typed_hopf_composition(goal)
    source = typed_hopf_composition(canonical)
    if target is None or source is None:
        return None
    if not strict_nu_prime_alias(target.left, source.left):
        return None
    if target.right != source.right:
        return None
    expected = replace(goal, lhs=MapApplication(EHP_H_MAP, Composition(source.left, target.right)))
    return canonical if canonical == expected else None


def alias_hopf_rule(goal: Relation, canonical: Relation) -> InferenceRule:
    """Transport a proved statement without changing its mathematical content."""
    if alias_hopf_input(goal, canonical) is None:
        raise ValueError('INVALID_TYPED_HOPF_NOTATION_TRANSPORT')

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.INFERENCE
                and premises[0].inference_rule is not None
                and bool(premises[0].premises)
                and premises[0].conclusion == canonical
                and alias_hopf_input(goal, premises[0].conclusion) == canonical)

    return InferenceRule(
        name=RULE_NAME,
        description=('Transfer an independently inferred Hopf equality between strictly '
                     'verified encodings of the same typed nu-prime; the right factor '
                     'and the entire right-hand side are unchanged.'),
        premise_patterns=(PremisePattern(proof_rule=ProofRule.INFERENCE,
                                        statement_type=Relation, statement_pattern=canonical),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def alias_hopf_backward_plan(
    goal: object,
    available: tuple[object, ...],
    strict_planner: Callable[[object, tuple[object, ...]], tuple[tuple[Relation, GoalExpansion], ...]],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Use only a screened witness and the original planner, never an alias GIVEN."""
    if not isinstance(available, tuple):
        raise TypeError('available must be a tuple')
    target = typed_hopf_composition(goal)
    if target is None:
        return ()
    witnesses = []
    for item in available:
        if (type(item) is not Relation or item.relation_type is not RelationType.EQUALITY
                or type(item.lhs) is not MapApplication or item.lhs.map != EHP_H_MAP
                or type(item.rhs) is not HomotopyElement):
            continue
        alpha = item.lhs.expression
        # An existing exact witness must use the ordinary route, not a fallback
        # that could mask a source gate or an ambiguous exact candidate.
        if alpha == target.left:
            return ()
        if strict_nu_prime_alias(target.left, alpha):
            witnesses.append(item)
    if len(witnesses) != 1:
        return ()
    alpha = witnesses[0].lhs.expression
    canonical = replace(goal, lhs=MapApplication(EHP_H_MAP, Composition(alpha, target.right)))
    if alias_hopf_input(goal, canonical) is None:
        return ()
    plan = strict_planner(canonical, available)
    if not plan or plan[-1][0] != canonical or any(target == goal for target, _ in plan):
        return ()
    return plan + ((goal, GoalExpansion(alias_hopf_rule(goal, canonical), (canonical,))),)
