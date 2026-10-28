"""Inspect linked GIVEN provenance of already checked generator-image steps.

This is diagnostic only. It never treats names, publication labels, or latex
text as evidence and never grants permission to hide or infer a ProofStep.
"""
from __future__ import annotations

from dataclasses import dataclass

from proof import ProofRule


@dataclass(frozen=True)
class ImageProvenance:
    image_step_index: int
    given_step_indices: tuple[int, ...]
    registered_citation_numbers: tuple[int, ...]
    unregistered_citation_numbers: tuple[int, ...]
    missing_ancestor_indices: bool


def trace_generator_image_citations(
    model: object,
    order: tuple[int, ...],
    image_steps: tuple[object, ...] | list[object],
) -> tuple[ImageProvenance, ...] | None:
    """Trace actual GIVEN ancestors by ProofStep identity; fail on invalid shape."""
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
            or len(set(order)) != len(order)
            or any(type(index) is not int or index < 0 or index >= len(steps)
                   for index in order)):
        return None
    indexed = {id(step): index for index, step in enumerate(steps)}
    if len(indexed) != len(steps):
        return None
    registered_numbers = tuple(citation.number for citation in citations)
    if (len(set(registered_numbers)) != len(registered_numbers)
            or any(type(number) is not int or number < 1
                   for number in registered_numbers)):
        return None
    registered = set(registered_numbers)
    findings: list[ImageProvenance] = []
    for image in image_steps:
        image_index = indexed.get(id(image))
        if image_index is None or image_index not in order:
            return None
        found_given: set[int] = set()
        found_numbers: set[int] = set()
        unresolved = False
        stack = [image]
        seen: set[int] = set()
        while stack:
            step = stack.pop()
            key = id(step)
            if key in seen:
                continue
            seen.add(key)
            index = indexed.get(key)
            if index is None or index not in order:
                unresolved = True
                continue
            if step.rule is ProofRule.GIVEN:
                found_given.add(index)
                found_numbers.update(links[index])
            stack.extend(step.premises)
        findings.append(ImageProvenance(
            image_step_index=image_index,
            given_step_indices=tuple(sorted(found_given)),
            registered_citation_numbers=tuple(
                number for number in registered_numbers if number in found_numbers
            ),
            unregistered_citation_numbers=tuple(sorted(found_numbers - registered)),
            missing_ancestor_indices=unresolved,
        ))
    if len({item.image_step_index for item in findings}) != len(findings):
        return None
    return tuple(findings)


def summarize_image_provenance(
    findings: tuple[ImageProvenance, ...],
    citation_numbers: tuple[int, ...],
) -> dict:
    """Compare each proof's citations to existing projected citations."""
    linked = {number for item in findings for number in item.registered_citation_numbers}
    displayed = set(citation_numbers)
    return {
        "image_count": len(findings),
        "images_with_cited_given": sum(bool(item.registered_citation_numbers)
                                       for item in findings),
        "every_image_has_cited_given": bool(findings) and all(
            bool(item.registered_citation_numbers) for item in findings
        ),
        "missing_ancestors": sum(item.missing_ancestor_indices for item in findings),
        "unregistered_citations": sorted({
            number for item in findings
            for number in item.unregistered_citation_numbers
        }),
        "projected_citation_numbers": list(citation_numbers),
        "linked_citation_numbers": sorted(linked),
        "projection_matches_union": displayed == linked,
    }
