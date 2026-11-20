"""Compose existing screened Lemma 5.7 and typed right-zero rules in isolation.

This callable is NOT registered in the shared production proof search.
It generates candidate goals, never completed steps or GIVEN statements.
"""
from __future__ import annotations

from typing import Callable

from expression import Composition, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
from phase175_r3r9_lemma57_explicit_public.rule import expand_cited_lemma57_explicit_zero
from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
from phase176_r3r8_lemma57_provider_binding.audit import source_bound_provider
from phase176_r3r10_right_zero_transport_isolated.rule import expand_right_zero_transport


def preceding_zero_image(goal: object) -> GeneratorImage | None:
    """Construct exactly one typed prefix zero-image obligation, when valid."""
    if (type(goal) is not GeneratorImage
            or type(goal.map) is not TodaSuspensionMap
            or type(goal.target_generator) is not Zero):
        return None
    factors = typed_composition_factors(goal.source_generator)
    if factors is None or len(factors) < 3:
        return None
    prefix = factors[0]
    for factor in factors[1:-1]:
        prefix = Composition(prefix, factor)
    from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
    ends = expression_endpoints(prefix)
    if ends is None:
        return None
    degree, sphere = ends
    if sphere != goal.map.source_group.sphere_dimension:
        return None
    return GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(degree, sphere),
                          TodaPrimaryGroup(degree + 1, sphere + 1)),
        prefix, Zero(),
    )


def build_isolated_two_stage_provider(
    ordinary: Callable[[object], object],
    screened_source_steps: tuple[object, ...],
) -> Callable[[object], tuple[object, ...]]:
    """Retain ordinary options and independently guarded inferred subgoals."""
    bound = source_bound_provider(
        ordinary,
        screened_source_steps,
        TodaLemma57ExplicitNuPrimeZero,
        expand_cited_lemma57_explicit_zero,
    )

    def expand(goal: object) -> tuple[object, ...]:
        options = tuple(bound(goal))
        base = preceding_zero_image(goal)
        if base is None:
            return options
        return tuple(expand_right_zero_transport(goal, base)) + options

    return expand
