"""Shared, fail-closed narrative suppression for proved generator transport.

The caller must have verified a complete Proof Tree before presenting it.
This helper derives no group facts, does not mutate ProofSteps or citations,
and does not decide how group-specific generator formulae are rendered.
"""
from __future__ import annotations

from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import ProofRule


def exclusive_generator_inference_indices(
    model: object,
    order: tuple[int, ...],
    image_steps: tuple[object, ...] | list[object],
    root_index: int,
    *,
    require_all: bool,
) -> tuple[int, ...] | None:
    """Select only uncited, exclusively consumed generator-proof inferences.

    Existing rooted image steps are mandatory. All of their proof ancestors
    must be located by object identity in the supplied complete model.
    If require_all is true, no eligible generator step may remain visible;
    this preserves the older direct-sum projection's fail-closed contract.
    Otherwise, independently used ancestors are retained in the narrative.
    """
    steps = getattr(model, "steps", None)
    links = getattr(model, "step_citation_numbers", None)
    if (not isinstance(steps, tuple)
            or not isinstance(links, tuple)
            or len(links) != len(steps)
            or not isinstance(order, tuple)
            or not isinstance(image_steps, (tuple, list))
            or not image_steps
            or type(root_index) is not int
            or not 0 <= root_index < len(steps)
            or root_index not in order
            or type(require_all) is not bool
            or len(set(order)) != len(order)
            or any(type(i) is not int or not 0 <= i < len(steps)
                   for i in order)):
        return None
    by_identity = {id(step): index for index, step in enumerate(steps)}
    if len(by_identity) != len(steps):
        return None

    seed_indices: set[int] = set()
    for image_step in image_steps:
        index = by_identity.get(id(image_step))
        if (index is None or index not in order or index == root_index
                or image_step.rule is not ProofRule.INFERENCE
                or not isinstance(image_step.conclusion, GeneratorImage)
                or links[index]):
            return None
        seed_indices.add(index)
    if len(seed_indices) != len(image_steps):
        return None

    eligible: set[int] = set(seed_indices)
    pending = list(image_steps)
    visited: set[int] = set()
    while pending:
        candidate = pending.pop()
        identity = id(candidate)
        if identity in visited:
            continue
        visited.add(identity)
        index = by_identity.get(identity)
        if index is None or index not in order:
            return None
        if (index != root_index
                and candidate.rule is ProofRule.INFERENCE
                and isinstance(candidate.conclusion,
                               (GeneratorImage, GeneratorSuspension))
                and not links[index]):
            eligible.add(index)
        pending.extend(candidate.premises)

    hidden = set(seed_indices)
    changed = True
    while changed:
        changed = False
        for index in sorted(eligible - hidden):
            candidate = steps[index]
            consumers = {
                consumer_index
                for consumer_index, consumer in enumerate(steps)
                if any(parent is candidate for parent in consumer.premises)
            }
            if consumers and consumers.issubset(hidden | {root_index}):
                hidden.add(index)
                changed = True

    for index in hidden:
        candidate = steps[index]
        consumers = {
            consumer_index
            for consumer_index, consumer in enumerate(steps)
            if any(parent is candidate for parent in consumer.premises)
        }
        if not consumers or not consumers.issubset(hidden | {root_index}):
            return None
    if require_all and hidden != eligible:
        return None
    return tuple(sorted(hidden))
