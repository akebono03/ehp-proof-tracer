"""Public backward proposals for R5 and existing equality rules, not proof leaves."""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple, Sum, Suspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10b_registered_stable_family_binding.family_registry import registered_stable_family_pair
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase177_r5_general_suspension_equality_isolated.rule import (
    expand_iterated_notation_equality, expand_suspension_image_equality,
    suspension_image_input,
)
from proof import Relation, RelationType
from relation_rules import equality_transitivity_inference_rule, suspension_preserves_equality_inference_rule


def structural_middle(x: object, z: object) -> object | None:
    """Candidate only: derive the middle spelling from typed family/AST metadata."""
    a, b = typed_endpoints(x), typed_endpoints(z)
    if a is None or b != (a[0] + 2, a[1] + 2):
        return None
    if isinstance(x, HomotopyElement) and isinstance(z, HomotopyElement):
        family = registered_stable_family_pair(x, z)
        if family is None:
            return None
        n = a[1] + 1
        return HomotopyElement(family.name_at(n), n, n + family.stem, n,
                               GeneratorSymbol(family.symbol_family, n))
    if type(x) is type(z) and type(x) in (Composition, Sum):
        left, right = structural_middle(x.left, z.left), structural_middle(x.right, z.right)
        if left is None or right is None:
            return None
        return type(x)(left, right)
    if (type(x) is Multiple and type(z) is Multiple
            and type(x.coefficient) is int and x.coefficient == z.coefficient):
        value = structural_middle(x.expression, z.expression)
        return None if value is None else Multiple(x.coefficient, value)
    return None


def middle_candidates(x: object, z: object, available: tuple[object, ...]) -> tuple[object, ...]:
    """Use only finitely many candidate terms; their equalities stay open goals."""
    candidates = [structural_middle(x, z)]
    for item in available:
        if type(item) is GeneratorImage:
            if item.source_generator == x:
                candidates.append(item.target_generator)
            if item.target_generator == z:
                candidates.append(item.source_generator)
        elif type(item) is Relation and item.relation_type is RelationType.EQUALITY:
            for lhs, rhs in ((item.lhs, item.rhs), (item.rhs, item.lhs)):
                if lhs == Suspension(x):
                    candidates.append(rhs)
                if type(lhs) is Suspension and rhs == z:
                    candidates.append(lhs.expression)
    result = []
    for y in candidates:
        if (y is not None and y != Suspension(x)
                and suspension_image_input(Relation(Suspension(x), y)) is not None
                and suspension_image_input(Relation(Suspension(y), z)) is not None
                and y not in result):
            result.append(y)
    return tuple(result)


def expand_public_suspension_equality(goal: object, available: tuple[object, ...] = ()) -> tuple[GoalExpansion, ...]:
    """Reuse R5 and existing congruence/transitivity; no new inference rule."""
    if not isinstance(available, tuple):
        raise TypeError('available must be tuple')
    if (type(goal) is not Relation or goal.relation_type is not RelationType.EQUALITY
            or goal.source is not None or goal.note is not None or goal.lhs == goal.rhs):
        return ()
    lhs, rhs = goal.lhs, goal.rhs
    span = typed_endpoints(lhs)
    if span is None or typed_endpoints(rhs) != span:
        return ()
    notation = expand_iterated_notation_equality(goal)
    if notation:
        return notation
    options = []
    if type(lhs) is IteratedSuspension and type(lhs.exponent) is int and lhs.exponent == 2:
        x = lhs.expression
        if middle_candidates(x, rhs, available):
            nested = Suspension(Suspension(x))
            options.append(GoalExpansion(equality_transitivity_inference_rule(),
                                         (Relation(lhs, nested), Relation(nested, rhs))))
    elif type(lhs) is Suspension:
        if type(rhs) is Suspension:
            premise = Relation(lhs.expression, rhs.expression)
            if premise.lhs != premise.rhs:
                options.append(GoalExpansion(suspension_preserves_equality_inference_rule(), (premise,)))
        if type(lhs.expression) is Suspension:
            x = lhs.expression.expression
            for y in middle_candidates(x, rhs, available):
                middle = Suspension(y)
                if middle != rhs and middle != lhs:
                    options.append(GoalExpansion(equality_transitivity_inference_rule(),
                                                 (Relation(lhs, middle), Relation(middle, rhs))))
        options.extend(expand_suspension_image_equality(goal))
    return tuple(options)
