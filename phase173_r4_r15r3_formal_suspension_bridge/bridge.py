"""Uniform, typed *formal* E images; no named generator identification.

This module never registers a public proof expansion or a new GIVEN source.
A formal E(g) is the definition of suspension. Splitting E(a o b) into
E(a) o E(b) is the functoriality of suspension. Neither statement implies
that a separately named database generator equals that formal expression.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, IteratedSuspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from proof import InferenceRule


FORMAL_RULE_NAME = "canonical formal suspension of typed compositions"


def canonical_formal_suspension(expression: object) -> object | None:
    """Distribute one E over a typed composition without renaming atoms.

    An arbitrary atom becomes an explicit IteratedSuspension even in an
    unstable range. This is *not* a stable-family generator identity.
    """
    span = typed_element_span(expression)
    if span is None or span[1] < 2 or span[0] < span[1]:
        return None
    expected_span = (span[0] + 1, span[1] + 1)
    if isinstance(expression, HomotopyElement):
        result = IteratedSuspension(expression=expression, exponent=1)
    elif isinstance(expression, IteratedSuspension):
        if (type(expression.exponent) is not int
                or expression.exponent < 0):
            return None
        result = IteratedSuspension(
            expression=expression.expression,
            exponent=expression.exponent + 1,
        )
    elif isinstance(expression, Composition):
        left = canonical_formal_suspension(expression.left)
        right = canonical_formal_suspension(expression.right)
        if left is None or right is None:
            return None
        result = Composition(left=left, right=right)
    else:
        return None
    return result if typed_element_span(result) == expected_span else None


def formal_image_goal(expression: object) -> GeneratorImage | None:
    """Build a typed E-image goal for a canonical formal expression only."""
    span = typed_element_span(expression)
    image = canonical_formal_suspension(expression)
    if span is None or image is None:
        return None
    q, n = span
    return GeneratorImage(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(q, n),
            target_group=TodaPrimaryGroup(q + 1, n + 1),
        ),
        source_generator=expression,
        target_generator=image,
    )


def is_canonical_formal_image(statement: object) -> bool:
    """Reject forged endpoints and all named or noncanonical image claims."""
    if not isinstance(statement, GeneratorImage):
        return False
    expected = formal_image_goal(statement.source_generator)
    return expected is not None and statement == expected


def expand_canonical_formal_image(
    statement: object,
) -> tuple[GoalExpansion, ...]:
    """Offer an independently replayable definitional step, not DB equality."""
    if not is_canonical_formal_image(statement):
        return ()

    def guard(premises, bindings):
        return (
            len(premises) == 0
            and not bindings
            and is_canonical_formal_image(statement)
        )

    rule = InferenceRule(
        name=FORMAL_RULE_NAME,
        description=(
            "One formal suspension E of an explicitly typed representative; "
            "suspension preserves composition. No separately named generator "
            "is identified and no source theorem or DB claim is added."
        ),
        premise_patterns=(),
        match_guard=guard,
        conclusion_pattern=statement,
    )
    return (GoalExpansion(rule, ()),)
