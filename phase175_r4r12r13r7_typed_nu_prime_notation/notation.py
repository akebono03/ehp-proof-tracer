"""Strict notation-only equivalence for one-fold suspension of typed nu-prime.

This helper does not identify different mathematical generators or produce
ProofSteps. The Unicode-prime / ASCII-prime and LaTeX-family spellings are
alternate encodings of the same explicitly typed nu-prime symbol.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Suspension


def _nu_prime_label(value: object) -> bool:
    """Recognize only documented encodings of the typed nu-prime symbol."""
    return isinstance(value, str) and value in ("ν′", "ν'", "\\nu'", "\\nu′")


def _nu_prime_element_alias(left: object, right: object) -> bool:
    """Refuse to collapse names unless every typed field is compatible."""
    if not isinstance(left, HomotopyElement) or not isinstance(right, HomotopyElement):
        return False
    if not (type(left.dimension) is int and type(right.dimension) is int):
        return False
    if (
        left.dimension != right.dimension
        or left.source != right.source
        or left.target != right.target
        or not all(type(x) is int for x in (left.source, left.target, right.source, right.target))
    ):
        return False
    if not (_nu_prime_label(left.name) and _nu_prime_label(right.name)):
        return False
    if not isinstance(left.generator, GeneratorSymbol) or not isinstance(right.generator, GeneratorSymbol):
        return False
    def symbol_is_nu_prime(g: GeneratorSymbol) -> bool:
        return (
            g.index is None
            and (
                (g.family == "ν" and g.decoration in ("′", "'"))
                or (g.family in ("\\nu'", "\\nu′", "ν′", "ν'") and g.decoration is None)
            )
        )
    return symbol_is_nu_prime(left.generator) and symbol_is_nu_prime(right.generator)


def same_typed_generator_notation(left: object, right: object) -> bool:
    """Check equality or strictly equivalent one-suspension nu-prime notation.

    Not a group identity theorem: only syntactically interchangeable encodings
    are recognized; arbitrary homotopy elements never compare equal this way.
    """
    if left == right:
        return True
    if isinstance(left, Suspension) and isinstance(right, IteratedSuspension):
        return type(right.exponent) is int and right.exponent == 1 and _nu_prime_element_alias(
            left.expression, right.expression
        )
    if isinstance(left, IteratedSuspension) and isinstance(right, Suspension):
        return type(left.exponent) is int and left.exponent == 1 and _nu_prime_element_alias(
            left.expression, right.expression
        )
    return False
