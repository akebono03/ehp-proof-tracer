"""R57-R14: recompute earlier proofs on demand; never store finished ProofSteps.

The catalog contains only independently reviewed positions and typed targets.
Every invocation has its own local cache and rejects cached/persisted roots.
"""
from __future__ import annotations

from collections.abc import Callable

from phase165_r52_r17_internal_dependency import CompletedInternalProof, same_statement
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase165_r57_r12_ordered_proofs import OrderedCompletedProof
from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
from proof import ProofRule, ProofStep


def search_recursively_in_proof_order(
    catalog: ProofOrderCatalog,
    goal: object,
    search_one: Callable[[object, tuple[OrderedCompletedProof, ...], int], PartialProofResult],
) -> PartialProofResult:
    """Run earlier searches afresh, then search the goal using proven earlier roots.

    Incomplete earlier results are never promoted. Only this invocation's local
    memoization is used; the catalog is not modified. A root must be an inferred
    step whose conclusion matches its registered target exactly.
    """
    if not isinstance(catalog, ProofOrderCatalog):
        raise TypeError("catalog must be ProofOrderCatalog")
    if not callable(search_one):
        raise TypeError("search_one must be callable")
    records = tuple(catalog._records)
    if any(record.completed is not None for record in records):
        raise ValueError("on-demand mode forbids registered completed proofs")
    matching = tuple(record for record in records if same_statement(record.statement, goal))
    if len(matching) != 1:
        raise ValueError("target has no unique registered proof order")
    ordered = tuple(sorted(records, key=lambda record: record.position))
    cache: dict[int, PartialProofResult] = {}
    completed: dict[int, CompletedInternalProof] = {}

    def resolve(position: int) -> PartialProofResult:
        if position in cache:
            return cache[position]
        record = next((item for item in ordered if item.position == position), None)
        if record is None:
            raise ValueError("unregistered proof position")
        for predecessor in ordered:
            if predecessor.position >= position:
                break
            resolve(predecessor.position)
        available = tuple(
            OrderedCompletedProof(completed[item.position], item.position)
            for item in ordered
            if item.position < position and item.position in completed
        )
        result = search_one(record.statement, available, position)
        if not isinstance(result, PartialProofResult):
            raise TypeError("search_one must return PartialProofResult")
        if result.status is ProofSearchStatus.COMPLETE:
            if not same_statement(result.conclusion, record.statement):
                raise ValueError("completed conclusion differs from registered target")
            roots = tuple(
                step for step in result.proven_steps
                if isinstance(step, ProofStep)
                and same_statement(step.conclusion, record.statement)
            )
            if len(roots) != 1 or roots[0].rule is not ProofRule.INFERENCE:
                raise ValueError("completed proof requires exactly one inferred root")
            completed[position] = CompletedInternalProof(roots[0])
        cache[position] = result
        return result

    return resolve(matching[0].position)
