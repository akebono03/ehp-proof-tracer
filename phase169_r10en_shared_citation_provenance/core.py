"""Resolve registered GIVEN citations of already proved generator images.

This module performs presentation-only provenance checks, not proof replay.
Callers must supply a previously verified Proof Narrative Model and retain
all group-specific inference, source, transport, and suppression checks.
"""
from __future__ import annotations

from phase165_r14_r6_generic_iso import GeneratorImage
from proof import ProofRule


def verified_generator_image_citation_numbers(
    model: object,
    order: tuple[int, ...],
    image_steps: tuple[object, ...] | list[object],
    *,
    require_each: bool,
) -> tuple[int, ...] | None:
    """Use actual linked GIVEN ancestors, preserving their registered order.

    For cyclic proofs require a nonempty union of actual image-ancestor
    citations. For direct sums additionally require a cited GIVEN ancestor
    of *each* image. Any missing, unindexed or unregistered ancestry fails
    closed. Nothing in the input model is modified.
    """
    steps = getattr(model, "steps", None)
    links = getattr(model, "step_citation_numbers", None)
    citations = getattr(model, "citations", None)
    if (not isinstance(steps, tuple)
            or not isinstance(links, tuple)
            or not isinstance(citations, tuple)
            or len(steps) != len(links)
            or not isinstance(order, tuple)
            or not isinstance(image_steps, (tuple, list))
            or not image_steps
            or type(require_each) is not bool
            or any(type(index) is not int or not 0 <= index < len(steps)
                   for index in order)):
        return None
    if len(set(order)) != len(order):
        return None
    by_identity = {id(step): index for index, step in enumerate(steps)}
    if len(by_identity) != len(steps):
        return None
    registered_numbers = tuple(getattr(item, "number", None)
                               for item in citations)
    if any(type(number) is not int or number <= 0
           for number in registered_numbers):
        return None
    if len(set(registered_numbers)) != len(registered_numbers):
        return None
    registered_set = set(registered_numbers)
    all_numbers: set[int] = set()
    image_indices: set[int] = set()
    for image_step in image_steps:
        image_index = by_identity.get(id(image_step))
        if (image_index is None or image_index not in order
                or getattr(image_step, "rule", None) is not ProofRule.INFERENCE
                or not isinstance(getattr(image_step, "conclusion", None), GeneratorImage)
                or links[image_index] or image_index in image_indices):
            return None
        image_indices.add(image_index)
        image_numbers: set[int] = set()
        pending = [image_step]
        visited: set[int] = set()
        while pending:
            step = pending.pop()
            identity = id(step)
            if identity in visited:
                continue
            visited.add(identity)
            index = by_identity.get(identity)
            if index is None or index not in order:
                return None
            if step.rule is ProofRule.GIVEN:
                numbers = links[index]
                if (not isinstance(numbers, tuple)
                        or any(type(number) is not int
                               or number not in registered_set
                               for number in numbers)):
                    return None
                image_numbers.update(numbers)
            pending.extend(step.premises)
        if require_each and not image_numbers:
            return None
        all_numbers.update(image_numbers)
    if not all_numbers:
        return None
    return tuple(number for number in registered_numbers if number in all_numbers)
