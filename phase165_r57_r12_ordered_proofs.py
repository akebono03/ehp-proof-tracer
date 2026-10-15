"""R57-R12: explicit proof-use ordering for prior internal proof ancestry.

This class does not assert the chosen positions are historically verified.
The caller must supply reviewed order indices, not simply sort discovered facts.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_r17_internal_dependency import CompletedInternalProof, validate_ancestry
from proof import ProofStep


@dataclass(frozen=True)
class OrderedCompletedProof:
    proof: CompletedInternalProof
    order: int

    def __post_init__(self) -> None:
        if not isinstance(self.proof, CompletedInternalProof):
            raise TypeError("proof must be CompletedInternalProof")
        if isinstance(self.order, bool) or not isinstance(self.order, int) or self.order < 0:
            raise ValueError("order must be nonnegative integer")
        validate_ancestry(self.proof.root)


def validate_prior_internal_proofs(
    ordered: tuple[OrderedCompletedProof, ...],
    target_order: int | None,
    legacy_unordered: tuple = (),
) -> tuple[CompletedInternalProof, ...]:
    """Admit only explicitly ordered, earlier inference proofs; fail closed.

    A caller-supplied rank alone is not a certification of its correctness.
    The registry's proof-order metadata must eventually provide that evidence.
    """
    if not isinstance(ordered, tuple) or not isinstance(legacy_unordered, tuple):
        raise TypeError("proof collections must be tuples")
    if legacy_unordered:
        raise ValueError("unranked completed_internal_proofs are forbidden by proof-use ordering")
    if not ordered:
        if target_order is not None and (
            isinstance(target_order, bool) or not isinstance(target_order, int) or target_order < 0
        ):
            raise ValueError("target_order must be nonnegative integer")
        return ()
    if isinstance(target_order, bool) or not isinstance(target_order, int) or target_order < 0:
        raise ValueError("target_order is required for ordered proof reuse")
    result = []
    seen = []
    for item in ordered:
        if not isinstance(item, OrderedCompletedProof):
            raise TypeError("ordered proofs must contain OrderedCompletedProof")
        if item.order >= target_order:
            raise ValueError("internal proof order must precede the current target")
        root = item.proof.root
        validate_ancestry(root)
        if any(type(root.conclusion) is type(x) and root.conclusion == x for x in seen):
            raise ValueError("duplicate internal proof conclusion")
        seen.append(root.conclusion)
        result.append(item.proof)
    return tuple(result)
