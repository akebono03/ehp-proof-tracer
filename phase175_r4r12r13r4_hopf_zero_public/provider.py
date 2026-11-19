"""Connect two ordinary generic EHP expansions to public backward search.

No hard-coded homotopy group, generator, route, or source assertion is supplied.
"""
from __future__ import annotations

from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r12r13r4_hopf_zero_public.rule import (
    expand_hopf_zero_from_injective_delta,
    expand_suspension_surjective_from_zero_hopf,
)


def expand_public_hopf_zero_ehp(goal: object) -> tuple[GoalExpansion, ...]:
    """Do not assert conclusions: return obligations for recursive resolution."""
    return (
        expand_hopf_zero_from_injective_delta(goal)
        + expand_suspension_surjective_from_zero_hopf(goal)
    )
