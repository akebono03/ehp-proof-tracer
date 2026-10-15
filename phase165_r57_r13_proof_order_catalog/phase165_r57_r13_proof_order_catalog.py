"""R57-R13: registered, strictly earlier internal proof lookup.

Order positions are reviewed proof-use metadata, not publication order or
an inference from group dimensions. No repository replay is performed.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_r17_internal_dependency import (
    CompletedInternalProof,
    depends_on,
    same_statement,
    validate_ancestry,
)
from phase165_r57_r12_ordered_proofs import OrderedCompletedProof, validate_prior_internal_proofs
from proof import ProofStep


@dataclass(frozen=True)
class ProofOrderRecord:
    """Registered target with an independently reviewed proof-use position."""
    statement: object
    position: int
    completed: CompletedInternalProof | None = None

    def __post_init__(self) -> None:
        if self.statement is None:
            raise ValueError("statement is required")
        if isinstance(self.position, bool) or not isinstance(self.position, int) or self.position < 0:
            raise ValueError("position must be a nonnegative integer")
        if self.completed is not None:
            if not isinstance(self.completed, CompletedInternalProof):
                raise TypeError("completed must be CompletedInternalProof")
            validate_ancestry(self.completed.root)
            if not same_statement(self.completed.root.conclusion, self.statement):
                raise ValueError("registered proof does not prove its statement")


class ProofOrderCatalog:
    """Register reviewed positions once; look up prior proof steps per goal."""

    def __init__(self) -> None:
        self._records: list[ProofOrderRecord] = []

    def register(self, record: ProofOrderRecord) -> None:
        if not isinstance(record, ProofOrderRecord):
            raise TypeError("record must be ProofOrderRecord")
        if any(same_statement(item.statement, record.statement) for item in self._records):
            raise ValueError("duplicate target statement")
        if any(item.position == record.position for item in self._records):
            raise ValueError("duplicate proof position")
        self._records.append(record)

    def select_prior(self, goal: object) -> tuple[tuple[CompletedInternalProof, ...], int]:
        """Fail closed without a registered target; exclude current/later roots."""
        matches = [item for item in self._records if same_statement(item.statement, goal)]
        if len(matches) != 1:
            raise ValueError("target has no unique registered proof order")
        target = matches[0]
        earlier = sorted(
            (item for item in self._records if item.position < target.position and item.completed is not None),
            key=lambda item: item.position,
        )
        ordered = []
        for item in earlier:
            assert item.completed is not None
            validate_ancestry(item.completed.root)
            if depends_on(item.completed.root, goal):
                raise ValueError("earlier proof depends on current goal")
            ordered.append(OrderedCompletedProof(item.completed, item.position))
        return validate_prior_internal_proofs(tuple(ordered), target.position), target.position
