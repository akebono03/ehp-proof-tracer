"""Pure display projection of a verified typed stable-family composition.

The HyoujiGen.csv row supplies family/type/degree metadata, never a proof of
composition or of a suspension image. The input Composition is not altered.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement
from phase169_r10b_registered_stable_family_binding.family_registry import (
    registered_family_of,
)


def _composition_factors(value: object) -> tuple[HomotopyElement, ...] | None:
    """Flatten a typed composition preserving left-to-right factor order."""
    if isinstance(value, HomotopyElement):
        return (value,)
    if not isinstance(value, Composition):
        return None
    left = _composition_factors(value.left)
    right = _composition_factors(value.right)
    if left is None or right is None:
        return None
    return left + right


def typed_stable_composition_power_latex(value: object) -> str | None:
    """Render α_n∘α_(n+k)∘... as α_n^r only for the same DB-typed family.

    Check every HyoujiGen family ID, source and target degree, positive stem,
    exact indexed generator and consecutive matching dimensions. A CSV name
    cannot assert or certify a mathematical suspension image: this helper
    emits no ProofStep, rule, reference or group relation.
    """
    if not isinstance(value, Composition):
        return None
    factors = _composition_factors(value)
    if factors is None or len(factors) < 2:
        return None
    families = tuple(registered_family_of(factor) for factor in factors)
    first = families[0]
    if (first is None or first.stem <= 0 or
            not all(family is not None and family.family_id == first.family_id
                    for family in families)):
        return None
    start = factors[0].target
    if type(start) is not int or start < first.minimum_n:
        return None
    if any(
        type(factor.target) is not int
        or factor.target != start + i * first.stem
        or factor.source != factor.target + first.stem
        for i, factor in enumerate(factors)
    ):
        return None
    # Reject malformed TeX fragments rather than printing an unbalanced power.
    latex = first.latex
    if (not latex.startswith("\\") or not latex.count("{") == latex.count("}")
            or "\n" in latex or "\r" in latex):
        return None
    return rf"{latex}_{{{start}}}^{{{len(factors)}}}"
