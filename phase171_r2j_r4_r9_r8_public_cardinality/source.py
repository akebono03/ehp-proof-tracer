"""Source-anchored, generic EHP middle-cardinality backward expansion.

This module creates proof obligations, never mathematical GIVEN steps. Both
finite end-group candidates come from earlier screened fixed statements or
checked specialization of a screened symbolic statement; the short exact
sequence and all end-group claims must be independently proved by search.
"""
from __future__ import annotations

from homotopy_groups import (
    FiniteCyclicGroup,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation,
    specialize_eta_group_relation,
)
from phase171_r2j_r4_r5_short_exact_sequence.source import (
    EHPShortExactSequence,
    expand_ehp_short_exact,
)
from phase171_r2j_r4_r6_middle_cardinality.source import (
    FiniteGroupCardinality,
    expand_finite_cardinality_from_short_exact,
)
from proof import Relation, RelationType


def _unique_relations(candidates: tuple[object, ...]) -> tuple[Relation, ...]:
    """Keep different typed presentations distinct, dropping identical copies."""
    distinct: list[Relation] = []
    for candidate in candidates:
        if not (
            isinstance(candidate, Relation)
            and candidate.relation_type is RelationType.EQUALITY
            and isinstance(candidate.lhs, TodaPrimaryGroup)
            and isinstance(candidate.rhs, FiniteCyclicGroup)
            and type(candidate.rhs.order) is int
            and candidate.rhs.order > 0
        ):
            continue
        if candidate not in distinct:
            distinct.append(candidate)
    return tuple(distinct)


def _cited_finite_group_candidates(
    group: TodaPrimaryGroup, available: tuple[object, ...]
) -> tuple[Relation, ...]:
    """Select exact cited finite groups or an admissible cited eta schema.

    A specialized Relation is a search goal, not a proved conclusion. Its
    underlying source must still be admitted by the existing proof engine.
    """
    candidates: list[object] = []
    n = group.sphere_dimension
    for claim in available:
        if isinstance(claim, Relation) and claim.lhs == group:
            candidates.append(claim)
        if _is_generic_eta_group_relation(claim) and type(n) is int and n >= 4:
            specialized = specialize_eta_group_relation(claim, n)
            if specialized.lhs == group:
                candidates.append(specialized)
    return _unique_relations(tuple(candidates))


def expand_cited_ehp_middle_cardinality(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose |B|=|A||C| only with unique earlier typed end-group claims.

    Canonical EHP indices are derived from the goal group B=pi_q^n:
    A=pi_(q-1)^(n-1), C=pi_q^(2n-1). This is dimension-generic, not a
    special-case pi_6^3 proof or an import of a previously completed tree.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple of screened fixed claims")
    if not isinstance(goal, FiniteGroupCardinality):
        return ()
    middle = goal.group
    if not isinstance(middle, TodaPrimaryGroup):
        return ()
    q = middle.group_dimension
    n = middle.sphere_dimension
    if (
        type(q) is not int or type(n) is not int
        or type(goal.order) is not int or goal.order <= 0
        or n < 3 or q < max(n + 1, 2 * n - 1)
    ):
        return ()
    left_group = TodaPrimaryGroup(q - 1, n - 1)
    right_group = TodaPrimaryGroup(q, 2 * n - 1)
    sequence = EHPShortExactSequence(
        source_group=left_group,
        middle_group=middle,
        target_group=right_group,
        injection=TodaSuspensionMap(left_group, middle),
        projection=TodaHopfInvariantMap(middle, right_group),
    )
    # The existing typed EHP rule checks map indices and exactness shapes.
    if len(expand_ehp_short_exact(sequence)) != 1:
        return ()
    left = _cited_finite_group_candidates(left_group, available)
    right = _cited_finite_group_candidates(right_group, available)
    if len(left) != 1 or len(right) != 1:
        return ()
    options = expand_finite_cardinality_from_short_exact(
        goal, left[0], sequence, right[0],
    )
    if len(options) != 1 or options[0].subgoals != (left[0], sequence, right[0]):
        return ()
    return options
