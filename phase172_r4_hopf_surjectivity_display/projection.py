"""Suppress a repeated Hopf surjectivity sentence backed by the same proof.

Only the display index is returned; every original ProofStep remains in the
verified proof model, including the second derived surjectivity statement.
"""
from __future__ import annotations

from homotopy_groups import TodaHopfInvariantMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from proof import ProofRule
from toda_rules import (
    TodaDeltaZeroStatement,
    TodaHopfInvariantSurjectiveStatement,
    TodaProp42ExactnessStatement,
)


def redundant_hopf_surjectivity_indices(
    model: object,
    display_order: tuple[int, ...],
    already_hidden: set[int] | frozenset[int] = frozenset(),
) -> frozenset[int]:
    """Hide only a later, uncited repetition of an earlier visible H-surjection.

    The later MapSurjective must be inferred from a Delta-zero step and an
    exactness step. The Delta-zero step must itself depend on the same exactness
    and a visible, cited-ancestor TodaHopfInvariantSurjectiveStatement for the
    identical typed Hopf map. This proves the repeated wording is redundant
    without relying on a TeX match or imposing a special pi_6^3 exception.
    """
    if (getattr(model, "status", None) is not ProofSearchStatus.COMPLETE
            or getattr(model, "open_goals", ())):
        return frozenset()
    steps = getattr(model, "steps", None)
    numbers = getattr(model, "step_citation_numbers", None)
    root = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple) or not isinstance(numbers, tuple)
            or len(steps) != len(numbers) or type(root) is not int):
        return frozenset()
    try:
        ancestry = root_ancestor_step_indices(steps, root)
    except ValueError:
        return frozenset()
    order = tuple(display_order)
    if (any(type(i) is not int or i not in ancestry for i in order)
            or len(set(order)) != len(order)):
        return frozenset()
    visible = set(order).difference(already_hidden)
    identities = {id(step): i for i, step in enumerate(steps)}
    if len(identities) != len(steps):
        return frozenset()

    def index(step: object) -> int | None:
        by_identity = identities.get(id(step))
        if by_identity is not None:
            return by_identity
        by_value = [i for i, recorded in enumerate(steps) if recorded == step]
        return by_value[0] if len(by_value) == 1 else None

    def premises(step: object, count: int) -> tuple[int, ...] | None:
        parents = getattr(step, "premises", ())
        if len(parents) != count:
            return None
        found = tuple(index(parent) for parent in parents)
        if (any(i is None or i not in ancestry for i in found)
                or len(set(found)) != len(found)):
            return None
        return found

    def has_cited_given(index_: int) -> bool:
        try:
            ancestors = root_ancestor_step_indices(steps, index_)
        except ValueError:
            return False
        return any(
            steps[i].rule is ProofRule.GIVEN and bool(numbers[i])
            for i in ancestors
        )

    hidden: set[int] = set()
    for later_index in order:
        if later_index not in visible or later_index == root:
            continue
        later = steps[later_index]
        later_statement = later.conclusion
        if (later.rule is not ProofRule.INFERENCE
                or numbers[later_index]
                or not isinstance(later_statement, MapSurjective)
                or not isinstance(later_statement.map, TodaHopfInvariantMap)
                or typed_sentence(later_statement, later) is None):
            continue
        pair = premises(later, 2)
        if pair is None:
            continue
        delta_candidates = [i for i in pair if isinstance(steps[i].conclusion, TodaDeltaZeroStatement)]
        exact_candidates = [i for i in pair if isinstance(steps[i].conclusion, TodaProp42ExactnessStatement)]
        if len(delta_candidates) != 1 or len(exact_candidates) != 1:
            continue
        delta_index = delta_candidates[0]
        exact_index = exact_candidates[0]
        delta = steps[delta_index]
        exact = steps[exact_index]
        if (delta.rule is not ProofRule.INFERENCE
                or exact.rule is not ProofRule.INFERENCE
                or not has_cited_given(exact_index)):
            continue
        delta_parents = premises(delta, 2)
        if delta_parents is None or exact_index not in delta_parents:
            continue
        earlier_index = next(i for i in delta_parents if i != exact_index)
        earlier = steps[earlier_index]
        earlier_statement = earlier.conclusion
        if (earlier_index not in visible
                or order.index(earlier_index) >= order.index(later_index)
                or earlier.rule is not ProofRule.INFERENCE
                or not isinstance(earlier_statement, TodaHopfInvariantSurjectiveStatement)
                or not isinstance(earlier_statement.map, TodaHopfInvariantMap)
                or earlier_statement.map != later_statement.map
                or typed_sentence(earlier_statement, earlier) is None
                or not has_cited_given(earlier_index)):
            continue
        hidden.add(later_index)
    return frozenset(hidden)
