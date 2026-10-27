"""Test-only, nonvalidated model mutations checking projection refusal.

These modified models are deliberately NOT valid proof certificates and must
never be passed through the public Web proof trust boundary as real evidence.
"""
from __future__ import annotations

from dataclasses import replace

from proof import ProofRule, ProofStep
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)


def rejection_checks(model: object, order: tuple[int, ...]) -> dict[str, bool]:
    """Return true for each deliberately invalid projection that is rejected."""
    steps = model.steps
    root_index = model.root_index
    if not isinstance(root_index, int):
        raise ValueError("expected a real complete proof model")
    root = steps[root_index]
    if len(root.premises) < 4:
        raise ValueError("expected a genuine direct-sum transport root")
    by_identity = {id(step): i for i, step in enumerate(steps)}
    first_image = root.premises[2]
    image_index = by_identity[id(first_image)]

    def changed_root(new_premises):
        changed = list(steps)
        changed[root_index] = replace(root, premises=tuple(new_premises))
        return replace(model, steps=tuple(changed))

    shuffled = list(root.premises)
    shuffled[2], shuffled[3] = shuffled[3], shuffled[2]
    directly_cited = list(model.step_citation_numbers)
    directly_cited[image_index] = (model.citations[0].number,)
    external = ProofStep(first_image.conclusion, (first_image,), ProofRule.INFERENCE)

    invalid = {
        "missing_root": (replace(model, root_index=None), order),
        "duplicate_order": (model, order + (order[0],)),
        "missing_image_in_order": (model, tuple(i for i in order if i != image_index)),
        "missing_root_image": (changed_root(root.premises[:-1]), order),
        "permuted_root_images": (changed_root(shuffled), order),
        "uncited_proof_tree": (
            replace(model, citations=(),
                    step_citation_numbers=tuple(() for _ in steps)), order,
        ),
        "forged_citation_number": (
            replace(model,
                    step_citation_numbers=tuple((999999,) if numbers else ()
                                                for numbers in model.step_citation_numbers)), order,
        ),
        "cited_intermediate_image": (
            replace(model, step_citation_numbers=tuple(directly_cited)), order,
        ),
        "outside_consumer": (
            replace(model, steps=steps + (external,),
                    step_citation_numbers=model.step_citation_numbers + ((),)),
            order + (len(steps),),
        ),
    }
    return {
        key: project_verified_direct_sum_transport(changed, changed_order) is None
        for key, (changed, changed_order) in invalid.items()
    }
