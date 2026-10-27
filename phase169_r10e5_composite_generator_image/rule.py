"""A typed suspension-of-composition inference, with no new source axioms.

The equality E(f o g) = E(f) o E(g) is used only when both component
GeneratorImage obligations have independently replayable INFERENCE proofs.
A source/target generator name or a database row is never proof evidence.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule


def _endpoints(element: object) -> tuple[int, int] | None:
    """For a typed map S^source -> S^target return (source, target)."""
    if isinstance(element, HomotopyElement):
        if not all(type(x) is int for x in (
            element.dimension, element.source, element.target,
        )):
            return None
        if (element.dimension != element.target or element.target < 2
                or element.source <= element.target):
            return None
        return (element.source, element.target)
    if isinstance(element, Composition):
        left = _endpoints(element.left)
        right = _endpoints(element.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return (right[0], left[1])
    return None


def component_image_obligations(
    goal: object,
) -> tuple[GeneratorImage, GeneratorImage] | None:
    """Decompose a valid E(f o g) obligation into E(f) and E(g) goals.

    This checks source/target dimensions and the composability at both ends.
    It does not claim that either factor image has been proved.
    """
    if (not isinstance(goal, GeneratorImage)
            or not isinstance(goal.map, TodaSuspensionMap)
            or not isinstance(goal.source_generator, Composition)
            or not isinstance(goal.target_generator, Composition)):
        return None
    source = goal.source_generator
    target = goal.target_generator
    source_end = _endpoints(source)
    target_end = _endpoints(target)
    if source_end is None or target_end is None:
        return None
    if (target_end != (source_end[0] + 1, source_end[1] + 1)
            or goal.map.source_group != TodaPrimaryGroup(*source_end)
            or goal.map.target_group != TodaPrimaryGroup(*target_end)):
        return None
    parts: list[GeneratorImage] = []
    for earlier, later in (
        (source.left, target.left),
        (source.right, target.right),
    ):
        source_part = _endpoints(earlier)
        target_part = _endpoints(later)
        if (source_part is None or target_part is None
                or target_part != (source_part[0] + 1, source_part[1] + 1)):
            return None
        parts.append(GeneratorImage(
            map=TodaSuspensionMap(
                TodaPrimaryGroup(*source_part),
                TodaPrimaryGroup(*target_part),
            ),
            source_generator=earlier,
            target_generator=later,
        ))
    return parts[0], parts[1]


def composite_generator_image_rule(goal: GeneratorImage) -> InferenceRule:
    """Require two independently inferred and typed suspension images."""
    expected = component_image_obligations(goal)
    if expected is None:
        raise ValueError("not a well-typed suspension of a composite")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == expected
            and component_image_obligations(goal) == expected
        )

    return InferenceRule(
        name="suspension preserves composition of separately proved maps",
        description=(
            "A composite generator image follows from two typed, "
            "independently inferred factor suspension images."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=expected[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=expected[1],
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_composite_generator_image(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Propose only two typed proof obligations, never a GIVEN or direct fact."""
    expected = component_image_obligations(goal)
    if expected is None:
        return ()
    return (GoalExpansion(
        composite_generator_image_rule(goal), expected,
    ),)
