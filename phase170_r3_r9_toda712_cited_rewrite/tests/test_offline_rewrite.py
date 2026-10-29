"""Offline AST checks of R3-R9 typed rewrite; no repository install required."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import sys
from types import ModuleType

import pytest

SOURCE = Path(__file__).resolve().parents[1] / 'replacement' / 'phase168_r2_toda52_transport.py'


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
class Group:
    group_dimension: int
    sphere_dimension: int


class Zero:
    pass


class Suspension:
    pass


class IteratedSuspension:
    pass


@dataclass(frozen=True)
class Finite:
    order: int
    generator: object


@dataclass(frozen=True)
class DirectSum:
    summands: tuple


class RelationType(Enum):
    EQUALITY = 'equality'


@dataclass(frozen=True)
class Relation:
    lhs: object
    rhs: object
    relation_type: RelationType = RelationType.EQUALITY


def _load(monkeypatch):
    expr = ModuleType('expression')
    expr.Composition = Composition
    expr.HomotopyElement = Element
    expr.GeneratorSymbol = Symbol
    expr.Sum = Sum
    expr.Multiple = Multiple
    expr.Suspension = Suspension
    expr.IteratedSuspension = IteratedSuspension
    groups = ModuleType('homotopy_groups')
    groups.FiniteCyclicGroup = Finite
    groups.FreeCyclicGroup = Finite
    groups.TodaPrimaryGroupZeroStatement = Zero
    groups.DirectSumGroup = DirectSum
    other = ModuleType('phase168_r2_8_3_generator_identity.identity')
    other.same_registered_group_presentation = lambda _a, _b: False
    for n, o in [('expression', expr),('homotopy_groups',groups),
                 ('phase168_r2_8_3_generator_identity.identity',other)]:
        monkeypatch.setitem(sys.modules,n,o)
    code=ast.parse(SOURCE.read_text(encoding='utf-8'))
    wanted={'_typed_source_and_target','_eta2_inverse_image',
            '_toda52_cited_generator_equality','_toda52_group_presentation_matches'}
    methods=[x for x in code.body if isinstance(x,ast.FunctionDef) and x.name in wanted]
    assert {x.name for x in methods}==wanted
    globs={'Composition':Composition,'HomotopyElement':Element,
           'GeneratorSymbol':Symbol,'FiniteCyclicGroup':Finite,
           'TodaPrimaryGroup':Group,'Relation':Relation,
           'RelationType':RelationType}
    exec(compile(ast.fix_missing_locations(ast.Module(body=methods,type_ignores=[])),
                 str(SOURCE),'exec'),globs)
    return globs


def _setup():
    eta = Element('eta2',2,3,2,Symbol('η',2))
    mu = Element('muprime',3,14,3,Symbol('muprime'))
    eps = Element('eps',3,11,3,Symbol('eps'))
    nu11 = Element('nu11',11,14,11,Symbol('nu',11))
    nuprime = Element('nuprime',3,6,3,Symbol('nuprime'))
    barnu = Element('barnu6',6,14,6,Symbol('barnu',6))
    nueps = Element('nueps',3,14,3,Symbol('nueps'))
    lhs = Composition(eps,nu11)
    rhs = Composition(nuprime,barnu)
    source=Relation(Group(14,3), DirectSum((Finite(4,mu),Finite(2,lhs),Finite(2,nueps))))
    target=Relation(Group(14,2), DirectSum((Finite(4,Composition(eta,mu)),
               Finite(2,Composition(eta,rhs)),Finite(2,Composition(eta,nueps)))))
    eq=Relation(lhs,rhs)
    return source,target,eq


def test_requires_cited_typed_equality(monkeypatch):
    api=_load(monkeypatch)
    source,target,eq=_setup()
    matches=api['_toda52_group_presentation_matches']
    assert not matches(source,target)
    assert matches(source,target,equality=eq)


def test_reverse_equality_but_not_a_fake_one(monkeypatch):
    api=_load(monkeypatch)
    source,target,eq=_setup()
    matches=api['_toda52_group_presentation_matches']
    assert matches(source,target,equality=Relation(eq.rhs,eq.lhs))
    assert not matches(source,target,equality=Relation(eq.lhs,eq.lhs))
    assert not matches(source,target,equality=Relation(eq.lhs,eq.rhs,relation_type='non-equality'))


def test_wrong_dimensions_rejected(monkeypatch):
    api=_load(monkeypatch)
    source,target,eq=_setup()
    wrong=Relation(eq.lhs,Element('bad',3,15,3,Symbol('bad')))
    assert not api['_toda52_group_presentation_matches'](source,target,equality=wrong)


def test_wrong_cyclic_order_rejected(monkeypatch):
    api=_load(monkeypatch)
    source,target,eq=_setup()
    different=Relation(target.lhs,DirectSum((target.rhs.summands[0],
                     Finite(4,target.rhs.summands[1].generator),
                     target.rhs.summands[2])))
    assert not api['_toda52_group_presentation_matches'](source,different,equality=eq)


def test_no_equality_required_for_directly_matching_existing_component(monkeypatch):
    api=_load(monkeypatch)
    source,target,eq=_setup()
    target_same=Relation(target.lhs,DirectSum((
        target.rhs.summands[0],
        Finite(2,Composition(target.rhs.summands[0].generator.left,eq.lhs)),
        target.rhs.summands[2])))
    assert api['_toda52_group_presentation_matches'](source,target_same)
