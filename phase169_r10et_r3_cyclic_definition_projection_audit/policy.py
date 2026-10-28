"""Read-only cyclic provenance experiment; never manufactures proof or citations.

The policy is a diagnostic candidate, NOT a production replacement. Only apply
it after a completed search has passed the standard Proof Tree trust replay.
"""
from __future__ import annotations

from typing import Callable


def _indices(model: object, order: tuple[int, ...]) -> dict[int, int] | None:
    steps = getattr(model, "steps", None)
    citations = getattr(model, "citations", None)
    links = getattr(model, "step_citation_numbers", None)
    if (not isinstance(steps, tuple)
            or not isinstance(citations, tuple)
            or not isinstance(links, tuple)
            or len(links) != len(steps)
            or not isinstance(order, tuple)
            or len(set(order)) != len(order)
            or any(type(x) is not int or x < 0 or x >= len(steps) for x in order)):
        return None
    by_id = {id(step): index for index, step in enumerate(steps)}
    if len(by_id) != len(steps):
        return None
    numbered = tuple(getattr(cite, "number", None) for cite in citations)
    if (any(type(x) is not int or x <= 0 for x in numbered)
            or len(set(numbered)) != len(numbered)):
        return None
    allowed = set(numbered)
    if any(not isinstance(row, tuple) or any(
        type(number) is not int or number not in allowed for number in row
    ) for row in links):
        return None
    return by_id


def _given_ancestor_numbers(model, order: tuple[int, ...], by_id: dict[int, int],
                            step: object, given_rule: object) -> set[int] | None:
    pending = [step]
    seen: set[int] = set()
    found: set[int] = set()
    while pending:
        current = pending.pop()
        identity = id(current)
        if identity in seen:
            continue
        seen.add(identity)
        index = by_id.get(identity)
        if index is None or index not in order:
            return None
        if getattr(current, "rule", None) == given_rule:
            found.update(model.step_citation_numbers[index])
        premises = getattr(current, "premises", None)
        if not isinstance(premises, tuple):
            return None
        pending.extend(premises)
    return found


def proposed_cyclic_image_citations(
    model: object,
    order: tuple[int, ...],
    image_steps: tuple[object, ...] | list[object],
    *,
    legacy_checker: Callable,
    canonical_definition_checker: Callable[[object], bool],
    given_rule: object,
    inference_rule: object,
) -> tuple[int, ...] | None:
    """Retain cited-image support, accept exact definition-only images if rooted.

    This is a *shadow candidate*: the real project must independently replay
    all ProofSteps. Root prior and isomorphism require separately traced,
    registered GIVEN evidence. A non-definition image still requires the
    existing strict ancestry checker. No lookup by family name or text.
    """
    by_id = _indices(model, order)
    if by_id is None or not isinstance(image_steps, (tuple, list)) or not image_steps:
        return None
    root_index = getattr(model, "root_index", None)
    if (type(root_index) is not int or root_index not in order
            or root_index < 0 or root_index >= len(model.steps)):
        return None
    root = model.steps[root_index]
    premises = getattr(root, "premises", None)
    if (getattr(root, "rule", None) != inference_rule
            or not isinstance(premises, tuple) or len(premises) < 3):
        return None
    prior_numbers = _given_ancestor_numbers(model, order, by_id, premises[0], given_rule)
    iso_numbers = _given_ancestor_numbers(model, order, by_id, premises[1], given_rule)
    if not prior_numbers or not iso_numbers or not (prior_numbers - iso_numbers) or not (iso_numbers - prior_numbers):
        return None
    indexes = [by_id.get(id(step)) for step in image_steps]
    if (any(index is None or index not in order for index in indexes)
            or len(set(indexes)) != len(indexes)
            or any(getattr(step, "rule", None) != inference_rule
                   or model.step_citation_numbers[by_id[id(step)]]
                   for step in image_steps)):
        return None
    cited = []
    for step in image_steps:
        if not canonical_definition_checker(step):
            cited.append(step)
    if cited:
        found = legacy_checker(model, order, tuple(cited), require_each=False)
        if found is None or not found:
            return None
        return found
    return ()
