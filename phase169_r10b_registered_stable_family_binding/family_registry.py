"""Bind typed indexed generators to kinds=0 HyoujiGen identities.

A DB row supplies candidate identity and degree metadata, NEVER a proof or a
claim that the suspension homomorphism is an isomorphism. R7 still requires
actual prior source, cited Toda (4.5), and proved GeneratorImage premises.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement


_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CSV = _ROOT / "data" / "HyoujiGen.csv"


@dataclass(frozen=True)
class RegisteredStableFamily:
    """A row of naming metadata, not an assertion of mathematical truth."""

    family_id: int
    display: str
    symbol_family: str
    stem: int
    minimum_n: int
    latex: str

    def name_at(self, n: int) -> str:
        return self.display + str(n).translate(_SUB)


@lru_cache(maxsize=8)
def read_registered_stable_families(csv_path: str | Path | None = None) -> tuple[RegisteredStableFamily, ...]:
    """Read all genuine kinds=0 generators; exclude the registered zero row."""
    path = Path(csv_path) if csv_path is not None else _DEFAULT_CSV
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = tuple(csv.DictReader(stream))
    result: list[RegisteredStableFamily] = []
    seen_ids: set[int] = set()
    for row in rows:
        if int(row["kinds"]) != 0:
            continue
        family_id = int(row["id"])
        if family_id == 0:
            continue
        if family_id in seen_ids:
            raise ValueError(f"duplicate HyoujiGen stable-family ID: {family_id}")
        seen_ids.add(family_id)
        stem = int(row["k"])
        minimum_n = int(row["n"])
        display = row["display"].strip()
        latex = row["latex"].strip()
        if stem < 0 or minimum_n < 1 or not display or not latex:
            raise ValueError(f"invalid registered stable-family metadata: {family_id}")
        symbol_family = display if display in {"η", "ν", "σ", "ι"} else latex
        result.append(RegisteredStableFamily(
            family_id=family_id,
            display=display,
            symbol_family=symbol_family,
            stem=stem,
            minimum_n=minimum_n,
            latex=latex,
        ))
    return tuple(result)


def registered_family_of(
    element: object, *, csv_path: str | Path | None = None,
) -> RegisteredStableFamily | None:
    """Match the complete typed member, not an untrusted display label alone."""
    if not isinstance(element, HomotopyElement):
        return None
    symbol = element.generator
    if not isinstance(symbol, GeneratorSymbol) or symbol.decoration is not None:
        return None
    n = symbol.index
    if type(n) is not int or not all(
        type(value) is int
        for value in (element.dimension, element.source, element.target)
    ):
        return None
    if element.dimension != n or element.target != n:
        return None
    matches = tuple(family for family in read_registered_stable_families(csv_path)
                    if n >= family.minimum_n
                    and element.source == n + family.stem
                    and symbol.family == family.symbol_family
                    and element.name in (
                        family.name_at(n), family.display + "_" + str(n),
                    ))
    return matches[0] if len(matches) == 1 else None


def registered_stable_family_pair(
    source: object, target: object, *, csv_path: str | Path | None = None,
) -> RegisteredStableFamily | None:
    """Same DB family ID and increasing indices, without asserting E(source)."""
    earlier = registered_family_of(source, csv_path=csv_path)
    later = registered_family_of(target, csv_path=csv_path)
    if earlier is None or later is None or earlier.family_id != later.family_id:
        return None
    if source.dimension >= target.dimension:
        return None
    return earlier
