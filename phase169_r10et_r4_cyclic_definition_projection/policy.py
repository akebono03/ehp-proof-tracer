"""Verified cyclic projection provenance for cited or Definition-only images.

Presentation-only. Call on an independently replayed, trusted Proof Narrative
Model. This module never constructs a ProofStep or changes a Reference.
"""
from __future__ import annotations

from phase169_r10en_shared_citation_provenance.core import (
    verified_generator_image_citation_numbers,
)
from proof import InferenceRule, ProofRule, find_inference_matches_for_rule
from phase169_r10eq_r1_universal_stable_definition.definition import (
    expand_defined_stable_element_image,
)


def canonical_definition_image(step: object) -> bool:
    """Certify the exact replayable, zero-premise stable Definition rule."""
    if (getattr(step, "rule", None) is not ProofRule.INFERENCE
            or getattr(step, "premises", None) != ()
            or not isinstance(getattr(step, "inference_rule", None), InferenceRule)):
        return False
    candidates = expand_defined_stable_element_image(step.conclusion)
    if len(candidates) != 1 or candidates[0].subgoals:
        return False
    actual, canonical = step.inference_rule, candidates[0].rule
    return (
        actual.name == canonical.name
        and actual.description == canonical.description
        and actual.premise_patterns == canonical.premise_patterns
        and actual.conclusion_pattern == canonical.conclusion_pattern
        and actual.conclusion_builder is None
        and actual.literature_reference is None
        and len(find_inference_matches_for_rule(actual, ())) == 1
    )


def _verified_index(model: object, order: tuple[int, ...]) -> dict[int, int] | None:
    steps = getattr(model, "steps", None)
    citations = getattr(model, "citations", None)
    links = getattr(model, "step_citation_numbers", None)
    if (not isinstance(steps, tuple)
            or not isinstance(citations, tuple)
            or not isinstance(links, tuple)
            or len(links) != len(steps)
            or not isinstance(order, tuple)
            or len(set(order)) != len(order)
            or any(type(index) is not int or index < 0 or index >= len(steps)
                   for index in order)):
        return None
    by_id = {id(step): index for index, step in enumerate(steps)}
    if len(by_id) != len(steps):
        return None
    numbers = tuple(getattr(item, "number", None) for item in citations)
    if (any(type(number) is not int or number <= 0 for number in numbers)
            or len(set(numbers)) != len(numbers)):
        return None
    registered = set(numbers)
    for link in links:
        if (not isinstance(link, tuple)
                or any(type(number) is not int or number not in registered
                       for number in link)):
            return None
    return by_id


def _ancestor_given_numbers(model: object, order: tuple[int, ...],
                            by_id: dict[int, int], step: object) -> set[int] | None:
    stack = [step]
    visited: set[int] = set()
    found: set[int] = set()
    while stack:
        current = stack.pop()
        identity = id(current)
        if identity in visited:
            continue
        visited.add(identity)
        index = by_id.get(identity)
        if index is None or index not in order:
            return None
        if current.rule is ProofRule.GIVEN:
            found.update(model.step_citation_numbers[index])
        premises = getattr(current, "premises", None)
        if not isinstance(premises, tuple):
            return None
        stack.extend(premises)
    return found


def verified_cyclic_generator_image_citation_numbers(
    model: object,
    order: tuple[int, ...],
    image_steps: tuple[object, ...] | list[object],
) -> tuple[int, ...] | None:
    """Keep cited proofs intact; also admit exact replayed Definition images.

    On a Definition-dependent proof, require separate registered GIVEN support
    for the prior group and Toda (4.5) iso. Cited image steps keep their actual
    ancestor references; only canonical Definition images may be citation-free.
    """
    original = verified_generator_image_citation_numbers(
        model, order, image_steps, require_each=False,
    )
    if original is not None:
        return original
    by_id = _verified_index(model, order)
    if by_id is None or not isinstance(image_steps, (tuple, list)) or not image_steps:
        return None
    root_index = getattr(model, "root_index", None)
    if (type(root_index) is not int or root_index not in order
            or root_index < 0 or root_index >= len(model.steps)):
        return None
    root = model.steps[root_index]
    if (root.rule is not ProofRule.INFERENCE
            or not isinstance(root.premises, tuple)
            or len(root.premises) < 3):
        return None
    prior = _ancestor_given_numbers(model, order, by_id, root.premises[0])
    iso = _ancestor_given_numbers(model, order, by_id, root.premises[1])
    if (not prior or not iso
            or not (prior - iso) or not (iso - prior)):
        return None
    found: set[int] = set()
    seen: set[int] = set()
    cited_steps: list[object] = []
    for step in image_steps:
        index = by_id.get(id(step))
        if (index is None or index not in order or index in seen
                or step.rule is not ProofRule.INFERENCE
                or model.step_citation_numbers[index]):
            return None
        seen.add(index)
        if not canonical_definition_image(step):
            cited_steps.append(step)
    if cited_steps:
        citations = verified_generator_image_citation_numbers(
            model, order, tuple(cited_steps), require_each=False,
        )
        if not citations:
            return None
        found.update(citations)
    return tuple(citation.number for citation in model.citations
                 if citation.number in found)
