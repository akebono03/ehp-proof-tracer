"""Exercise actual new matching functions with locally constructed typed examples."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import sys
from types import ModuleType

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "replacement" / "phase168_r2_toda52_transport.py"


@dataclass(frozen=True)
class Symbol:
    family: str
    index: int | None = None


@dataclass(frozen=True)
class Element:
    name: str
    dimension: int
    source: int
    target: int
    generator: Symbol


@dataclass(frozen=True)
class Composition:
    left: object
    right: object


@dataclass(frozen=True)
class Sum:
    left: object
    right: object


@dataclass(frozen=True)
class Multiple:
    coefficient: int
    expression: object


@dataclass(frozen=True)
class Suspension:
    expression: object

    @property
    def source(self):
        return self.expression.source + 1

    @property
    def target(self):
        return self.expression.target + 1


@dataclass(frozen=True)
class IteratedSuspension:
    expression: object
    exponent: int

    @property
    def source(self):
        return self.expression.source + self.exponent

    @property
    def target(self):
        return self.expression.target + self.exponent


@dataclass(frozen=True)
class Group:
    group_dimension: int
    sphere_dimension: int


@dataclass(frozen=True)
class Zero:
    group: Group


@dataclass(frozen=True)
class Finite:
    order: int
    generator: object


@dataclass(frozen=True)
class Free:
    generator: object


@dataclass(frozen=True)
class DirectSum:
    summands: tuple


class Equality(Enum):
    EQUALITY = "equality"


@dataclass(frozen=True)
class Relation:
    lhs: Group
    rhs: object
    relation_type: Equality = Equality.EQUALITY


def _load_matcher(monkeypatch):
    expr = ModuleType("expression")
    expr.Composition = Composition
    expr.HomotopyElement = Element
    expr.GeneratorSymbol = Symbol
    expr.Multiple = Multiple
    expr.Sum = Sum
    expr.Suspension = Suspension
    expr.IteratedSuspension = IteratedSuspension
    groups = ModuleType("homotopy_groups")
    groups.DirectSumGroup = DirectSum
    groups.FreeCyclicGroup = Free
    groups.FiniteCyclicGroup = Finite
    groups.TodaPrimaryGroupZeroStatement = Zero
    alias = ModuleType("phase168_r2_8_3_generator_identity.identity")
    alias.same_registered_group_presentation = lambda left, right: False
    monkeypatch.setitem(sys.modules, "expression", expr)
    monkeypatch.setitem(sys.modules, "homotopy_groups", groups)
    monkeypatch.setitem(sys.modules, "phase168_r2_8_3_generator_identity.identity", alias)
    full = ast.parse(SOURCE.read_text(encoding="utf-8"))
    methods = [n for n in full.body if isinstance(n, ast.FunctionDef) and n.name in (
        "_eta2_inverse_image", "_toda52_group_presentation_matches",
    )]
    result = {}
    exec(compile(ast.fix_missing_locations(ast.Module(body=methods, type_ignores=[])),
                 str(SOURCE), "exec"), {
        "Composition": Composition, "HomotopyElement": Element,
        "GeneratorSymbol": Symbol, "FiniteCyclicGroup": Finite,
        "TodaPrimaryGroup": Group, "Relation": Relation,
        "RelationType": Equality,
    }, result)
    # Function globals are separate from result due to exec globals/locals.
    globs = {
        "Composition": Composition, "HomotopyElement": Element,
        "GeneratorSymbol": Symbol, "FiniteCyclicGroup": Finite,
        "TodaPrimaryGroup": Group, "Relation": Relation,
        "RelationType": Equality,
    }
    exec(compile(ast.fix_missing_locations(ast.Module(body=methods, type_ignores=[])),
                 str(SOURCE), "exec"), globs)
    return globs["_toda52_group_presentation_matches"]


def _eta2():
    return Element("η₂", 2, 3, 2, Symbol("η", 2))


def _element(name: str, m: int):
    return Element(name, 3, m, 3, Symbol(name))


def test_isolated_finite_cyclic_and_rejects_order_mismatch(monkeypatch):
    matches = _load_matcher(monkeypatch)
    source = _element("ν′", 6)
    left = Relation(Group(6, 3), Finite(4, source))
    target = Relation(Group(6, 2), Finite(4, Composition(_eta2(), source)))
    assert matches(left, target)
    assert not matches(left, Relation(Group(6, 2), Finite(2, Composition(_eta2(), source))))


def test_isolated_zero_and_rejects_wrong_degree(monkeypatch):
    matches = _load_matcher(monkeypatch)
    assert matches(Zero(Group(9, 3)), Zero(Group(9, 2)))
    assert not matches(Zero(Group(9, 3)), Zero(Group(10, 2)))


def test_isolated_direct_sum_permuted_and_additive_generators(monkeypatch):
    matches = _load_matcher(monkeypatch)
    a, b = _element("a", 12), _element("b", 12)
    source = Relation(Group(12, 3), DirectSum((Finite(2, a), Finite(4, b))))
    target = Relation(Group(12, 2), DirectSum((
        Finite(4, Composition(_eta2(), b)),
        Finite(2, Composition(_eta2(), a)),
    )))
    assert matches(source, target)
    added = Relation(Group(12, 3), Finite(2, Sum(a, b)))
    sum_image = Relation(Group(12, 2), Finite(2, Sum(
        Composition(_eta2(), a), Composition(_eta2(), b),
    )))
    assert matches(added, sum_image)


def test_isolated_free_cyclic_and_multiple(monkeypatch):
    matches = _load_matcher(monkeypatch)
    a = _element("a", 17)
    source = Relation(Group(17, 3), Free(Multiple(2, a)))
    target = Relation(Group(17, 2), Free(Multiple(2, Composition(_eta2(), a))))
    assert matches(source, target)
