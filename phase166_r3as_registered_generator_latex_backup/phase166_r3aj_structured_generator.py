"""Reconstruct typed generator compositions from the existing ID database.

The representation is a Goal only; this module never creates a ProofStep.
"""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension

_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def _base_element(row, dimension):
    """Reconstruct a factor from the generator registry at its actual dimension."""
    family = str(row["display"]).strip()
    initial_n = int(row["n"])
    stem = int(row["k"])
    kinds = int(row["kinds"])
    if dimension < initial_n:
        return None
    if kinds == 0:
        # Stable-family symbols in HyoujiGen.csv carry their canonical TeX.
        # Preserve the existing names for the four familiar families.
        if family in {"η", "ν", "σ", "ι"}:
            symbol_family = family
        else:
            symbol_family = str(row["latex"]).strip()
            if not symbol_family or symbol_family.lower() == "nan":
                return None
        return HomotopyElement(
            name=family + str(dimension).translate(_SUB),
            dimension=dimension,
            source=dimension + stem,
            target=dimension,
            generator=GeneratorSymbol(family=symbol_family, index=dimension),
        )
    # Exceptional classes must retain their original name plus suspension.
    label = family.replace("'", "′")
    original = HomotopyElement(
        name=label,
        dimension=initial_n,
        source=initial_n + stem,
        target=initial_n,
    )
    exponent = dimension - initial_n
    return original if exponent == 0 else IteratedSuspension(original, exponent)

def structured_generator_from_ids(*, ids, start_dimension, generator_csv):
    """Build an actual Composition (not display text) from Element IDs."""
    if type(start_dimension) is not int or start_dimension < 2:
        return None
    if not ids or any(type(i) is not int for i in ids):
        return None
    gen = pd.read_csv(Path(generator_csv)).set_index("id")
    current_dimension = start_dimension
    factors = []
    for identifier in ids:
        if identifier not in gen.index:
            return None
        row = gen.loc[identifier]
        if not isinstance(row, pd.Series):
            return None
        factor = _base_element(row, current_dimension)
        if factor is None:
            return None
        factors.append(factor)
        current_dimension += int(row["k"])
    if len(factors) == 1:
        return factors[0]
    result = factors[-1]
    for factor in reversed(factors[:-1]):
        result = Composition(factor, result)
    return result


def database_structured_group_goal_candidates(*, n, k, csv_path=None, generator_csv=None):
    """Build typed Goal from complete Element IDs and component orders only.

    Rows without reconstruction metadata remain unsupported rather than
    receiving a made-up atom, relation, or fake proof.
    """
    from math import inf
    from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
    from proof import Relation, RelationType
    from repository import SphereRepository

    if type(n) is not int or type(k) is not int or n < 2 or k < 0:
        return ()
    directory = Path(__file__).resolve().parent / "data"
    source_file = Path(csv_path) if csv_path is not None else directory / "sphere.csv"
    gen_file = Path(generator_csv) if generator_csv is not None else directory / "HyoujiGen.csv"
    if not source_file.is_file() or not gen_file.is_file():
        return ()
    repo = SphereRepository(source_file)
    rows = repo.df[(repo.df["n"] == n) & (repo.df["k"] == k)]
    source_n = n if not rows.empty else k + 2
    if source_n > n:
        return ()
    components = repo.get_group(source_n, k).components
    if not components or any(not component.element for component in components):
        return ()
    parts = []
    for component in components:
        generator = structured_generator_from_ids(
            ids=component.element, start_dimension=n, generator_csv=gen_file
        )
        if generator is None:
            return ()
        if component.order == inf:
            parts.append(FreeCyclicGroup(generator))
        elif type(component.order) is int and component.order > 1:
            parts.append(FiniteCyclicGroup(component.order, generator))
        else:
            return ()
    rhs = parts[0] if len(parts) == 1 else DirectSumGroup(tuple(parts))
    return (Relation(TodaPrimaryGroup(n+k, n), rhs, RelationType.EQUALITY),)
