"""Pure proof-model projection of narrative display order.

This module does not infer results, references, or new proof steps.
It only moves a quotient presentation after an existing later domain
presentation, retaining original step indices for provenance.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase165_r12_r2_quotient_rules import QuotientIsomorphismStatement
from proof import Relation, RelationType


@dataclass(frozen=True)
class NarrativeOrderEntry:
    step_index: int
    after_indices: tuple[int, ...] = ()


def project_narrative_order(
    model: ProofNarrativeModel,
    suppressed_exactness: frozenset[int] | set[int] = frozenset(),
) -> tuple[NarrativeOrderEntry, ...]:
    """Preserve proof order except for justified quotient placement.

    A quotient is moved only behind an already present later equality
    that explicitly describes its domain. Every recorded step index is
    from the input model; there are no invented steps or citations.
    """
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if any(type(i) is not int or not 0 <= i < len(model.steps)
           for i in suppressed_exactness):
        raise ValueError("invalid suppressed proof-step index")
    postponed: dict[int, list[int]] = {}
    for index, step in enumerate(model.steps):
        statement = step.conclusion
        if not isinstance(statement, QuotientIsomorphismStatement):
            continue
        for later in range(index + 1, len(model.steps)):
            if later in suppressed_exactness:
                continue
            candidate = model.steps[later].conclusion
            if (isinstance(candidate, Relation)
                    and candidate.relation_type is RelationType.EQUALITY
                    and candidate.lhs == statement.domain):
                postponed.setdefault(later, []).append(index)
                break
    held = {i for group in postponed.values() for i in group}
    return tuple(
        NarrativeOrderEntry(index, tuple(postponed.get(index, ())))
        for index in range(len(model.steps))
        if index not in suppressed_exactness and index not in held
    )
