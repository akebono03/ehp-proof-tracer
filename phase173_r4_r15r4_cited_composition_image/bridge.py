"""Compose separately verified suspension images with a source-neutral rule.

Never assume an atomic generator identity from matching database labels.
Every composite proof has two strictly smaller GeneratorImage premises.
"""
from __future__ import annotations

from expression import Composition
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from proof import InferenceRule, PremisePattern, ProofRule


COMPOSITION_IMAGE_RULE = "suspension image of composition from verified factor images"


def generator_image(source: object, target: object) -> GeneratorImage | None:
    """Form the unique typed one-suspension GeneratorImage for two expressions."""
    source_span = typed_element_span(source)
    target_span = typed_element_span(target)
    if source_span is None or target_span is None:
        return None
    if target_span != (source_span[0] + 1, source_span[1] + 1):
        return None
    q, n = source_span
    if q < n or n < 2:
        return None
    return GeneratorImage(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(q, n),
            target_group=TodaPrimaryGroup(q + 1, n + 1),
        ),
        source_generator=source,
        target_generator=target,
    )


def factor_image_goals(goal: object) -> tuple[GeneratorImage, GeneratorImage] | None:
    """Split a typed composite image without deciding either atomic identity."""
    if not isinstance(goal, GeneratorImage):
        return None
    source = goal.source_generator
    target = goal.target_generator
    if not isinstance(source, Composition) or not isinstance(target, Composition):
        return None
    if generator_image(source, target) != goal:
        return None
    left = generator_image(source.left, target.left)
    right = generator_image(source.right, target.right)
    if left is None or right is None:
        return None
    return (left, right)


def expand_composed_generator_image(goal: object) -> tuple[GoalExpansion, ...]:
    """Propose the functorial image with *required* inferred factor premises."""
    factors = factor_image_goals(goal)
    if factors is None:
        return ()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(p.rule is ProofRule.INFERENCE for p in premises)
            and tuple(p.conclusion for p in premises) == factors
            and factor_image_goals(goal) == factors
        )

    rule = InferenceRule(
        name=COMPOSITION_IMAGE_RULE,
        description=(
            "The suspension of a typed composition is the composition "
            "of the separately proved factor images. No unproved named "
            "generator identity is inferred from group or order metadata."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=factors[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=factors[1],
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )
    return (GoalExpansion(rule, factors),)
