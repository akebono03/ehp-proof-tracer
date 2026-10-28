"""Definition of the suspension of a stable representative, for any typed element.

This module implements a project *notation convention*, not an additional
Toda theorem.  A registered kinds=0 indexed symbol denotes a chosen stable
class at every stable dimension.  Alternatively an explicit IteratedSuspension
is a witness of its own defining image.  Other names are never equated.

No prior group relation or stable-range isomorphism is manufactured here.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, IteratedSuspension, Multiple, Sum
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10b_registered_stable_family_binding.family_registry import (
    registered_stable_family_pair,
)
from proof import InferenceRule


def typed_element_span(value: object) -> tuple[int, int] | None:
    """Compute the source/target spheres of a typed formal element, or refuse."""
    if isinstance(value, HomotopyElement):
        if (type(value.dimension) is int and type(value.source) is int
                and type(value.target) is int and value.dimension == value.target
                and value.source >= value.target >= 2):
            return (value.source, value.target)
        return None
    if isinstance(value, IteratedSuspension):
        if type(value.exponent) is not int or value.exponent < 0:
            return None
        span = typed_element_span(value.expression)
        if span is None:
            return None
        return (span[0] + value.exponent, span[1] + value.exponent)
    if isinstance(value, Composition):
        left = typed_element_span(value.left)
        right = typed_element_span(value.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return (right[0], left[1])
    if isinstance(value, Sum):
        left = typed_element_span(value.left)
        right = typed_element_span(value.right)
        return left if left is not None and left == right else None
    if isinstance(value, Multiple):
        if type(value.coefficient) is not int:
            return None
        return typed_element_span(value.expression)
    return None


def is_defined_stable_suspension(source: object, target: object) -> bool:
    """Check definitional equality, not arbitrary homotopy-class equality.

    Stable indexed labels are interpreted by the project's declared stable
    representative convention.  Other explicitly suspended elements need no
    CSV entry.  This function intentionally rejects unrelated names.
    """
    first = typed_element_span(source)
    second = typed_element_span(target)
    if first is None or second is None:
        return False
    q, n = first
    k = q - n
    if k < 0 or n < k + 2 or second != (q + 1, n + 1):
        return False
    if (isinstance(target, IteratedSuspension)
            and target.expression == source and target.exponent == 1):
        return True
    if (isinstance(source, IteratedSuspension)
            and isinstance(target, IteratedSuspension)
            and source.expression == target.expression
            and type(source.exponent) is int
            and type(target.exponent) is int
            and target.exponent == source.exponent + 1):
        return True
    if isinstance(source, HomotopyElement) and isinstance(target, HomotopyElement):
        family = registered_stable_family_pair(source, target)
        return (family is not None
                and target.dimension == source.dimension + 1
                and target.source == source.source + 1
                and target.target == source.target + 1)
    if isinstance(source, Composition) and isinstance(target, Composition):
        return (is_defined_stable_suspension(source.left, target.left)
                and is_defined_stable_suspension(source.right, target.right))
    if isinstance(source, Sum) and isinstance(target, Sum):
        return (is_defined_stable_suspension(source.left, target.left)
                and is_defined_stable_suspension(source.right, target.right))
    if isinstance(source, Multiple) and isinstance(target, Multiple):
        return (type(source.coefficient) is int
                and type(target.coefficient) is int
                and source.coefficient == target.coefficient
                and is_defined_stable_suspension(source.expression, target.expression))
    return False


def is_defined_stable_image(goal: object) -> bool:
    """Match the exact typed E map and its two definitional representatives."""
    if (not isinstance(goal, GeneratorImage)
            or not isinstance(goal.map, TodaSuspensionMap)
            or not isinstance(goal.map.source_group, TodaPrimaryGroup)
            or not isinstance(goal.map.target_group, TodaPrimaryGroup)):
        return False
    span = typed_element_span(goal.source_generator)
    if span is None:
        return False
    q, n = span
    if (type(q) is not int or type(n) is not int
            or n < q - n + 2 or q < n
            or goal.map != TodaSuspensionMap(
                TodaPrimaryGroup(q, n), TodaPrimaryGroup(q + 1, n + 1))):
        return False
    return is_defined_stable_suspension(
        goal.source_generator, goal.target_generator,
    )


def expand_defined_stable_element_image(goal: object) -> tuple[GoalExpansion, ...]:
    """Definitional proof (zero premises), guarded for exact stable typing.

    This is not a fabricated external citation or an isomorphism.  Its exact
    conclusion is replayable by the standard ProofStep inference verifier.
    """
    if not is_defined_stable_image(goal):
        return ()

    def guard(premises, bindings):
        return len(premises) == 0 and not bindings and is_defined_stable_image(goal)

    rule = InferenceRule(
        name="stable representative definitional suspension",
        description=(
            "By the project definition of an indexed stable representative, "
            "or by explicit IteratedSuspension notation, apply one E. "
            "This states no relation between unrelated homotopy classes."
        ),
        premise_patterns=(),
        match_guard=guard,
        conclusion_pattern=goal,
    )
    return (GoalExpansion(rule, ()),)
