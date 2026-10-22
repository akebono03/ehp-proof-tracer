"""Conservative correspondence of concrete generator presentations to HyoujiGen IDs.

Only identity of registered eta/nu/nu-prime factors is recognized.  This
module does not derive relations, specialize general propositions, or prove
that two arbitrary presentations describe the same homotopy element.
"""
from __future__ import annotations

import csv
from pathlib import Path

from expression import Composition, HomotopyElement, IteratedSuspension, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup


def _master_records():
    path = Path(__file__).resolve().parent.parent / "data" / "HyoujiGen.csv"
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return {int(row["id"]): row for row in csv.DictReader(stream)}


def _factor_identity(expression, records):
    suspensions = 0
    while isinstance(expression, (Suspension, IteratedSuspension)):
        if isinstance(expression, Suspension):
            suspensions += 1
        elif type(expression.exponent) is int and expression.exponent >= 0:
            suspensions += expression.exponent
        else:
            return None
        expression = expression.expression
    if not isinstance(expression, HomotopyElement):
        return None
    if type(expression.dimension) is not int or expression.generator is None:
        return None
    symbol = expression.generator
    family = symbol.family
    index = symbol.index
    decoration = symbol.decoration
    actual_dimension = expression.dimension + suspensions
    matches = []
    for identifier, record in records.items():
        if identifier not in (2, 3, 4):
            continue
        base_n, stem = int(record["n"]), int(record["k"])
        if identifier == 2:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        elif identifier == 4:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        else:
            is_symbol = ((family == record["latex"] and index is None and decoration is None)
                         or (family == "ν" and index == base_n and decoration in ("′", "'")))
            if expression.dimension != base_n:
                continue
        if not is_symbol:
            continue
        if expression.source is not None and expression.source != expression.dimension + stem:
            continue
        if expression.target is not None and expression.target != expression.dimension:
            continue
        matches.append((identifier, actual_dimension, actual_dimension + stem, actual_dimension))
    return matches[0] if len(matches) == 1 else None


def _factor_sequence(expression, records):
    if isinstance(expression, Composition):
        left = _factor_sequence(expression.left, records)
        right = _factor_sequence(expression.right, records)
        if left is None or right is None:
            return None
        return left + right
    value = _factor_identity(expression, records)
    return None if value is None else (value,)


def _generator_identity(expression, records):
    factors = _factor_sequence(expression, records)
    if not factors:
        return None
    for first, second in zip(factors, factors[1:]):
        if first[2] != second[3]:
            return None
    return tuple((identifier, dimension) for identifier, dimension, _, _ in factors)


def _group_identity(group, records):
    if isinstance(group, FiniteCyclicGroup):
        generator = _generator_identity(group.generator, records)
        return None if generator is None else ("finite", group.order, generator)
    if isinstance(group, FreeCyclicGroup):
        generator = _generator_identity(group.generator, records)
        return None if generator is None else ("free", generator)
    if isinstance(group, DirectSumGroup):
        terms = tuple(_group_identity(item, records) for item in group.summands)
        return None if any(item is None for item in terms) else ("direct_sum", terms)
    return None


def same_registered_group_presentation(left, right):
    """Only certify a concrete, uniquely ID-resolved, equally ordered presentation."""
    if type(left) is not type(right):
        return False
    try:
        records = _master_records()
    except (OSError, ValueError, KeyError):
        return False
    left_key = _group_identity(left, records)
    right_key = _group_identity(right, records)
    return left_key is not None and left_key == right_key
