"""Typed proof-goal suggestions from SphereRepository; never evidence."""
from __future__ import annotations

from math import inf
from pathlib import Path
import re

from expression import HomotopyElement, GeneratorSymbol
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType
from repository import SphereRepository


_SIMPLE = re.compile(r"^(η|ν|σ|ι)_?\{?(\d+)\}?((?:\^\{?[23]\}?)?)$")


def _generator_for_target(label: str, base_n: int, target_n: int, k: int):
    match = _SIMPLE.fullmatch(label.strip())
    if match is None:
        return None
    family, index, power = match.groups()
    if int(index) != base_n:
        return None
    if power and family != "η":
        return None
    if family == "η" and k not in (1, 2, 3):
        return None
    if family == "ν" and k != 3:
        return None
    if family == "σ" and k != 7:
        return None
    if family == "ι" and k != 0:
        return None
    notation = family + "_" + str(target_n) + power
    return HomotopyElement(
        name=notation, dimension=target_n, source=target_n + k,
        target=target_n,
        generator=(GeneratorSymbol(family=family, index=target_n)
                   if not power else None),
    )


def database_group_goal_candidates(*, n: int, k: int, csv_path=None):
    """Make targets, NOT ProofSteps. Only unambiguous simple stable labels.

    For a stable target, source data are read from its stable base. If the
    table has unparseable/mixed generator notation, return no candidate.
    """
    if type(n) is not int or type(k) is not int or k < 0 or n < k + 2:
        return ()
    path = Path(csv_path) if csv_path is not None else Path(__file__).resolve().parent / "data" / "sphere.csv"
    if not path.is_file():
        return ()
    repo = SphereRepository(path)
    base_n = k + 2
    source = repo.get_group(base_n, k)
    if not source.components:
        return ()
    pieces = []
    for component in source.components:
        generator = _generator_for_target(component.generator, base_n, n, k)
        if generator is None:
            return ()
        if component.order == inf:
            pieces.append(FreeCyclicGroup(generator))
        elif type(component.order) is int and component.order > 1:
            pieces.append(FiniteCyclicGroup(component.order, generator))
        else:
            return ()
    structure = pieces[0] if len(pieces) == 1 else DirectSumGroup(tuple(pieces))
    return (Relation(TodaPrimaryGroup(n+k, n), structure, RelationType.EQUALITY),)
