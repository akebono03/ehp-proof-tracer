"""Offline tests of one-file proposal logic using minimal typed stand-ins."""
from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest


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
    generator: object


@dataclass(frozen=True)
class Composition:
    left: object
    right: object


@dataclass(frozen=True)
class Cyclic:
    order: int
    generator: object


@dataclass(frozen=True)
class Group:
    group_dimension: int
    sphere_dimension: int


@dataclass(frozen=True)
class Relation:
    lhs: object
    rhs: object
    relation_type: object = "equality"


@dataclass(frozen=True)
class Theorem:
    minimum_i: int = 3
    variable: str = "i"
    map_formula: str = "alpha -> eta_2 o alpha"
    source_group: str = "pi_i^3"
    target_group: str = "pi_i^2"


class Rule:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Pattern:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Expansion:
    def __init__(self, rule, subgoals):
        self.rule = rule
        self.subgoals = subgoals


def load(monkeypatch):
    def put(name, **attrs):
        module = ModuleType(name)
        for k, v in attrs.items():
            setattr(module, k, v)
        monkeypatch.setitem(sys.modules, name, module)
    put("expression", Composition=Composition, GeneratorSymbol=Symbol, HomotopyElement=Element)
    put("homotopy_groups", FiniteCyclicGroup=Cyclic, TodaPrimaryGroup=Group)
    put("phase165_r3_recursive_search", GoalExpansion=Expansion)
    put("phase165_r52_r27_r5_literature", Toda52UniversalStatement=Theorem)
    put("proof", InferenceRule=Rule, LiteratureReference=Rule, PremisePattern=Pattern,
        Relation=Relation, RelationType=SimpleNamespace(EQUALITY="equality"))
    monkeypatch.setitem(sys.modules, "phase168_r2_8_3_generator_identity", ModuleType("phase168_r2_8_3_generator_identity"))
    put("phase168_r2_8_3_generator_identity.identity", same_registered_group_presentation=lambda a, b: a == b)
    path = Path(__file__).resolve().parents[1] / "replacement" / "phase168_r2_toda52_transport.py"
    spec = importlib.util.spec_from_file_location("offline_toda52_patch", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def eta(n):
    return Element(f"eta_{n}", n, n + 1, n, Symbol("η", n))


def goal5():
    return Relation(Group(5, 2), Cyclic(2, Composition(eta(2), Composition(eta(3), eta(4)))))


def source5():
    return Relation(Group(5, 3), Cyclic(2, Composition(eta(3), eta(4))))


def test_no_source_stays_unproved(monkeypatch):
    mod = load(monkeypatch)
    assert mod.expand_toda52_finite_cyclic_goal(goal5(), (Theorem(),)) == ()


def test_no_theorem_stays_unproved(monkeypatch):
    mod = load(monkeypatch)
    assert mod.expand_toda52_finite_cyclic_goal(goal5(), (source5(),)) == ()


def test_valid_pi5_source_creates_two_premise_proposal(monkeypatch):
    mod = load(monkeypatch)
    options = mod.expand_toda52_finite_cyclic_goal(goal5(), (source5(), Theorem()))
    assert len(options) == 1
    assert options[0].subgoals == (source5(), Theorem())
    assert options[0].rule.match_guard(tuple(SimpleNamespace(conclusion=x) for x in options[0].subgoals), {})


def test_wrong_source_does_not_propose(monkeypatch):
    mod = load(monkeypatch)
    wrong = Relation(Group(6, 3), source5().rhs)
    assert mod.expand_toda52_finite_cyclic_goal(goal5(), (wrong, Theorem())) == ()


def test_invalid_composition_is_rejected(monkeypatch):
    mod = load(monkeypatch)
    wrong = Relation(Group(5, 2), Cyclic(2, Composition(eta(2), eta(3))))
    assert mod.expand_toda52_finite_cyclic_goal(wrong, (source5(), Theorem())) == ()


def test_wrong_theorem_is_rejected(monkeypatch):
    mod = load(monkeypatch)
    fake = Theorem(minimum_i=4)
    assert mod.expand_toda52_finite_cyclic_goal(goal5(), (source5(), fake)) == ()


def test_existing_i4_still_proposes(monkeypatch):
    mod = load(monkeypatch)
    old = Relation(Group(4, 2), Cyclic(2, Composition(eta(2), eta(3))))
    options = mod.expand_toda52_finite_cyclic_goal(old, (Theorem(),))
    assert len(options) == 1
    assert options[0].subgoals[0].lhs == Group(4, 3)


def test_general_guard_rejects_wrong_proof(monkeypatch):
    mod = load(monkeypatch)
    p = mod.expand_toda52_finite_cyclic_goal(goal5(), (source5(), Theorem()))[0]
    invalid = Relation(Group(5, 3), Cyclic(8, source5().rhs.generator))
    assert not p.rule.match_guard((SimpleNamespace(conclusion=invalid), SimpleNamespace(conclusion=Theorem())), {})


def test_bad_source_endpoint_rejected(monkeypatch):
    mod = load(monkeypatch)
    bad = Element("bad", 3, 6, 4, Symbol("ν", 3))
    target = Relation(Group(6, 2), Cyclic(4, Composition(eta(2), bad)))
    assert mod.expand_toda52_finite_cyclic_goal(target, (Theorem(),)) == ()


def test_correct_pi6_shape_uses_screened_source(monkeypatch):
    mod = load(monkeypatch)
    nu_prime = Element("nu'", 3, 6, 3, Symbol("nu'"))
    target = Relation(Group(6, 2), Cyclic(4, Composition(eta(2), nu_prime)))
    source = Relation(Group(6, 3), Cyclic(4, nu_prime))
    options = mod.expand_toda52_finite_cyclic_goal(target, (Theorem(), source))
    assert len(options) == 1
    assert options[0].subgoals == (source, Theorem())
