"""Legacy-free public group search entry, Phase 165 R27-R52.

This module intentionally does not import TodaCalculation or ProofRepository.
"""
from __future__ import annotations

from toda_group_query import TodaGroupQuery


def build_toda_partial_result(query: TodaGroupQuery):
    """Search for a group without assuming its structure in advance."""
    if not isinstance(query, TodaGroupQuery):
        raise TypeError("query must be a TodaGroupQuery")
    from phase165_r52_r5_auto_search import search_group_structure_automatically
    return search_group_structure_automatically(n=query.n, k=query.k)


def build_standard_toda_partial_result(n: int, k: int):
    """Search for a group given its sphere dimension and stem."""
    return build_toda_partial_result(TodaGroupQuery(n=n, k=k))
