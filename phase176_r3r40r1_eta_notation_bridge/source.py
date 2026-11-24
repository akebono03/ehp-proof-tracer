"""Audit-only eta notation transport using independently proved old rules."""
from __future__ import annotations

from expression import Composition, HomotopyElement, Suspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r12_r28_presentation_connection import _matching_eta_name
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2i_eta_hopf_bridge.source import cited_eta_suspension_equality_rule
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from phase176_r3r27r1_toda55_quadruple_isolated.source import expand_cited_quadruple
from phase176_r3r39_public_equality_transport.source import right_hopf_transport_backward_plan
from proof import Relation, RelationType
from relation_rules import (
    equality_preserved_under_left_composition_inference_rule,
    equality_preserved_under_right_composition_inference_rule,
    equality_symmetry_inference_rule,
    equality_transitivity_inference_rule,
)
from toda_rules import toda_eta_family_definition_statement


def eta_notation_backward_plan(
    left: object, right: object, available: tuple[object, ...],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Propose exact notation equalities, without identifying unequal objects.

    Each unequal leaf needs two inferred suspension equalities with the same
    canonical witness. Composition is handled by the old congruence rules.
    The empty result means no proof plan (or no change is needed).
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if available.count(TodaEtaFamilyGeneralDefinition()) != 1:
        return ()
    if left == right:
        return ()
    stages: dict[Relation, GoalExpansion] = {}

    def add(lhs, rhs, rule, premises):
        target = Relation(lhs, rhs, RelationType.EQUALITY)
        old = stages.get(target)
        if old is not None:
            if old.rule.name != rule.name or old.subgoals != premises:
                raise ValueError("CONFLICTING_NOTATION_STAGE")
        else:
            stages[target] = GoalExpansion(rule, premises)
        return target

    def build(a, b):
        span = expression_endpoints(a)
        if span is None or span != expression_endpoints(b):
            return False
        if isinstance(a, HomotopyElement) and isinstance(b, HomotopyElement):
            n = a.target
            if type(n) is not int or n < 4:
                return False
            older = toda_eta_family_definition_statement(n - 1).element
            canonical = toda_eta_family_definition_statement(n).element
            if not (_matching_eta_name(a, canonical) and _matching_eta_name(b, canonical)):
                return False
            if a == b:
                return True
            witness = GeneratorSuspension(
                TodaSuspensionMap(TodaPrimaryGroup(n, n - 1), TodaPrimaryGroup(n + 1, n)),
                older, canonical,
            )
            suspended = Suspension(older)
            first = Relation(suspended, a)
            second = Relation(suspended, b)
            ea = add(suspended, a, cited_eta_suspension_equality_rule(first, witness), (witness,))
            eb = add(suspended, b, cited_eta_suspension_equality_rule(second, witness), (witness,))
            reverse = add(a, suspended, equality_symmetry_inference_rule(), (ea,))
            add(a, b, equality_transitivity_inference_rule(), (reverse, eb))
            return True
        if not isinstance(a, Composition) or not isinstance(b, Composition):
            return False
        if not build(a.left, b.left) or not build(a.right, b.right):
            return False
        if a == b:
            return True
        middle = Composition(b.left, a.right)
        parts = []
        if a.left != b.left:
            parts.append(add(a, middle,
                equality_preserved_under_right_composition_inference_rule(a.right),
                (Relation(a.left, b.left),)))
        if a.right != b.right:
            parts.append(add(middle, b,
                equality_preserved_under_left_composition_inference_rule(b.left),
                (Relation(a.right, b.right),)))
        if len(parts) == 2:
            add(a, b, equality_transitivity_inference_rule(), tuple(parts))
        return True

    if not build(left, right):
        return ()
    target = Relation(left, right)
    if target not in stages:
        return ()
    return tuple(stages.items())


def connection_backward_plan(
    transported: Relation, forward: Relation, available: tuple[object, ...],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Connect separately provable R3R39 and Toda (5.5) premises."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if len(right_hopf_transport_backward_plan(transported, available)) != 6:
        return ()
    if len(expand_cited_quadruple(forward, available)) != 1:
        return ()
    reverse = Relation(forward.rhs, forward.lhs)
    goal = Relation(transported.lhs, forward.lhs)
    stages = []
    if transported.rhs != forward.rhs:
        notation = eta_notation_backward_plan(transported.rhs, forward.rhs, available)
        if not notation:
            return ()
        stages.extend(notation)
        aligned = Relation(transported.lhs, forward.rhs)
        stages.append((aligned, GoalExpansion(equality_transitivity_inference_rule(),
                                             (transported, Relation(transported.rhs, forward.rhs)))))
    else:
        aligned = transported
    stages.append((reverse, GoalExpansion(equality_symmetry_inference_rule(), (forward,))))
    stages.append((goal, GoalExpansion(equality_transitivity_inference_rule(), (aligned, reverse))))
    if len({target for target, _ in stages}) != len(stages):
        raise ValueError("DUPLICATE_CONNECTION_STAGE")
    return tuple(stages)
