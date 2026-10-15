"""Explicit free-cyclic eta-family goals for the shared typed Web search.

The goal describes a claim to prove; the construction is never a proof premise.
"""
from __future__ import annotations

import re
from dataclasses import replace

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase165_r52_partial_proof import GroupStructureStatus, PartialProofResult, ProofSearchStatus
from phase165_r52_r9_shared_math import search_shared_group_goal


def parse_explicit_free_cyclic_eta_goal(*, n: int, k: int, generator: str) -> FreeCyclicGroup:
    """Parse eta_n for a free cyclic goal with compatible source and target."""
    if type(n) is not int or n < 2:
        raise ValueError("n must be an integer >= 2")
    if type(k) is not int or k < 0:
        raise ValueError("k must be a nonnegative integer")
    match = re.fullmatch(r"eta_([0-9]+)", generator.strip())
    if match is None:
        raise ValueError("Generator must be written eta_n, for example eta_2")
    index = int(match.group(1))
    if index != n or k != 1:
        raise ValueError("eta_n has source n+1 and target n; require k=1 and generator eta_n")
    element = HomotopyElement(
        name=f"η{str(index).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))}",
        dimension=n, source=n + 1, target=n,
        generator=GeneratorSymbol(family="η", index=index),
    )
    return FreeCyclicGroup(element)


def build_explicit_free_cyclic_eta_web_view(
    *, n: int, k: int, generator: str, max_depth: int = 2, mode: str = "narrative"
):
    """Run the existing shared search, then adapt its actual steps to the Web view."""
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")
    group_structure = parse_explicit_free_cyclic_eta_goal(n=n, k=k, generator=generator)
    result = search_shared_group_goal(n=n, k=k, group_structure=group_structure)
    if isinstance(result, PartialProofResult) and result.status is ProofSearchStatus.COMPLETE:
        result = replace(result, structure_status=GroupStructureStatus.KNOWN)
    return build_partial_web_group_proof_view(result, max_depth=max_depth, mode=mode)
