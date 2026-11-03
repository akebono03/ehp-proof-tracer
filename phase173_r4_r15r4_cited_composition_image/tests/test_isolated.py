"""Standalone typed inference tests using deliberately minimal dependency doubles."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest


@dataclass(frozen=True)
class Component:
    source: int
    target: int


@dataclass(frozen=True)
class Composition:
    left: object
    right: object


@dataclass(frozen=True)
class TodaPrimaryGroup:
    group_dimension: int
    sphere_dimension: int


@dataclass(frozen=True)
class TodaSuspensionMap:
    source_group: object
    target_group: object


@dataclass(frozen=True)
class GeneratorImage:
    map: object
    source_generator: object
    target_generator: object


@dataclass(frozen=True)
class GoalExpansion:
    rule: object
    subgoals: tuple


@dataclass(frozen=True)
class PremisePattern:
    proof_rule: object = None
    statement_type: object = None
    statement_pattern: object = None


@dataclass(frozen=True)
class InferenceRule:
    name: str
    description: str
    premise_patterns: tuple
    conclusion_pattern: object
    match_guard: object


class ProofRule(Enum):
    GIVEN = "given"
    INFERENCE = "inference"


def typed_element_span(expression: object) -> tuple[int, int] | None:
    if isinstance(expression, Component):
        return expression.source, expression.target
    if isinstance(expression, Composition):
        left = typed_element_span(expression.left)
        right = typed_element_span(expression.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    return None


@pytest.fixture
def isolated_bridge(monkeypatch: pytest.MonkeyPatch):
    modules = {
        "expression": {"Composition": Composition},
        "homotopy_groups": {"TodaPrimaryGroup": TodaPrimaryGroup, "TodaSuspensionMap": TodaSuspensionMap},
        "phase165_r14_r6_generic_iso": {"GeneratorImage": GeneratorImage},
        "phase165_r3_recursive_search": {"GoalExpansion": GoalExpansion},
        "phase169_r10eq_r1_universal_stable_definition.definition": {
            "typed_element_span": typed_element_span,
        },
        "proof": {"InferenceRule": InferenceRule, "PremisePattern": PremisePattern, "ProofRule": ProofRule},
    }
    for name, contents in modules.items():
        fake = ModuleType(name)
        for key, value in contents.items():
            setattr(fake, key, value)
        monkeypatch.setitem(sys.modules, name, fake)
    path = Path(__file__).resolve().parents[1] / "bridge.py"
    spec = importlib.util.spec_from_file_location("_isolated_r15r4_bridge", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _example():
    a = Component(7, 3)
    b = Component(34, 7)
    suspended_a = Component(8, 4)
    suspended_b = Component(35, 8)
    return a, b, suspended_a, suspended_b


def test_generic_compound_image_proposes_two_unproved_factor_goals(isolated_bridge) -> None:
    bridge = isolated_bridge
    a, b, ea, eb = _example()
    goal = bridge.generator_image(Composition(a, b), Composition(ea, eb))
    assert goal is not None
    parts = bridge.factor_image_goals(goal)
    assert parts == (bridge.generator_image(a, ea), bridge.generator_image(b, eb))
    proposals = bridge.expand_composed_generator_image(goal)
    assert len(proposals) == 1
    assert proposals[0].subgoals == parts
    assert proposals[0].rule.conclusion_pattern == goal
    assert len(proposals[0].rule.premise_patterns) == 2


def test_compound_guard_requires_both_inferred_atomic_premises(isolated_bridge) -> None:
    bridge = isolated_bridge
    a, b, ea, eb = _example()
    goal = bridge.generator_image(Composition(a, b), Composition(ea, eb))
    proposal = bridge.expand_composed_generator_image(goal)[0]
    left, right = proposal.subgoals
    first = SimpleNamespace(rule=ProofRule.INFERENCE, conclusion=left)
    second = SimpleNamespace(rule=ProofRule.INFERENCE, conclusion=right)
    forged = SimpleNamespace(rule=ProofRule.GIVEN, conclusion=right)
    assert proposal.rule.match_guard((first, second), {})
    assert not proposal.rule.match_guard((first,), {})
    assert not proposal.rule.match_guard((first, forged), {})
    assert not proposal.rule.match_guard((second, first), {})
    assert not proposal.rule.match_guard((), {})


def test_wrong_types_and_unproved_named_atoms_do_not_become_rules(isolated_bridge) -> None:
    bridge = isolated_bridge
    a, b, ea, eb = _example()
    wrong = Component(35, 7)
    assert bridge.generator_image(a, wrong) is None
    assert bridge.generator_image(Composition(a, b), Composition(ea, wrong)) is None
    atomic = bridge.generator_image(a, ea)
    assert atomic is not None
    assert bridge.expand_composed_generator_image(atomic) == ()
    incompatible = Composition(a, Component(35, 6))
    assert bridge.generator_image(incompatible, Composition(ea, eb)) is None


def test_forged_map_cannot_be_composed(isolated_bridge) -> None:
    bridge = isolated_bridge
    a, b, ea, eb = _example()
    goal = bridge.generator_image(Composition(a, b), Composition(ea, eb))
    forged = GeneratorImage(
        map=TodaSuspensionMap(TodaPrimaryGroup(34, 3), TodaPrimaryGroup(99, 4)),
        source_generator=goal.source_generator,
        target_generator=goal.target_generator,
    )
    assert bridge.factor_image_goals(forged) is None
    assert bridge.expand_composed_generator_image(forged) == ()
