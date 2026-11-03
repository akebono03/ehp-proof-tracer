"""Executable pure-rule tests with substitute types, not substitute evidence."""
from __future__ import annotations

from dataclasses import dataclass, replace
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest


@pytest.fixture
def isolated_bridge(monkeypatch: pytest.MonkeyPatch):
    @dataclass(frozen=True)
    class HomotopyElement:
        name: str
        dimension: int
        source: int
        target: int

    @dataclass(frozen=True)
    class IteratedSuspension:
        expression: object
        exponent: int

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
        source_group: TodaPrimaryGroup
        target_group: TodaPrimaryGroup

    @dataclass(frozen=True)
    class GeneratorImage:
        map: TodaSuspensionMap
        source_generator: object
        target_generator: object

    @dataclass(frozen=True)
    class InferenceRule:
        name: str
        description: str
        premise_patterns: tuple
        match_guard: object
        conclusion_pattern: object

    @dataclass(frozen=True)
    class GoalExpansion:
        rule: InferenceRule
        subgoals: tuple

    def typed_element_span(value: object):
        if isinstance(value, HomotopyElement):
            return (value.source, value.target) if (
                type(value.dimension) is int and value.dimension == value.target
                and value.source >= value.target >= 2
            ) else None
        if isinstance(value, IteratedSuspension):
            span = typed_element_span(value.expression)
            return ((span[0] + value.exponent, span[1] + value.exponent)
                    if span and type(value.exponent) is int and value.exponent >= 0
                    else None)
        if isinstance(value, Composition):
            left, right = typed_element_span(value.left), typed_element_span(value.right)
            return (right[0], left[1]) if (
                left is not None and right is not None and left[0] == right[1]
            ) else None
        return None

    mapping = {
        "expression": (Composition, HomotopyElement, IteratedSuspension),
        "homotopy_groups": (TodaPrimaryGroup, TodaSuspensionMap),
        "phase165_r14_r6_generic_iso": (GeneratorImage,),
        "phase165_r3_recursive_search": (GoalExpansion,),
        "phase169_r10eq_r1_universal_stable_definition.definition": (typed_element_span,),
        "proof": (InferenceRule,),
    }
    parent = ModuleType("phase169_r10eq_r1_universal_stable_definition")
    parent.__path__ = []
    monkeypatch.setitem(sys.modules, parent.__name__, parent)
    for name, items in mapping.items():
        module = ModuleType(name)
        for item in items:
            setattr(module, item.__name__, item)
        monkeypatch.setitem(sys.modules, name, module)
    path = Path(__file__).resolve().parents[1] / "bridge.py"
    spec = importlib.util.spec_from_file_location("_phase173_r4_r15r3_isolated_bridge", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return SimpleNamespace(
        module=module,
        HomotopyElement=HomotopyElement,
        Composition=Composition,
        IteratedSuspension=IteratedSuspension,
        TodaSuspensionMap=TodaSuspensionMap,
        TodaPrimaryGroup=TodaPrimaryGroup,
        GeneratorImage=GeneratorImage,
        span=typed_element_span,
    )


def test_arbitrary_unstable_composition_formal_images(isolated_bridge) -> None:
    t = isolated_bridge
    a = t.HomotopyElement("delta_3", 3, 27, 3)
    b = t.HomotopyElement("sigma_27", 27, 34, 27)
    source = t.Composition(a, b)
    formal = t.module.canonical_formal_suspension(source)
    assert formal == t.Composition(t.IteratedSuspension(a, 1), t.IteratedSuspension(b, 1))
    assert t.span(formal) == (35, 4)
    goal = t.module.formal_image_goal(source)
    assert goal.map == t.TodaSuspensionMap(
        t.TodaPrimaryGroup(34, 3), t.TodaPrimaryGroup(35, 4)
    )
    assert t.module.is_canonical_formal_image(goal)
    options = t.module.expand_canonical_formal_image(goal)
    assert len(options) == 1
    assert options[0].subgoals == ()
    assert options[0].rule.match_guard((), {}) is True


def test_wrong_named_image_and_map_are_refused(isolated_bridge) -> None:
    t = isolated_bridge
    a = t.HomotopyElement("phi_prime", 3, 28, 3)
    goal = t.module.formal_image_goal(a)
    named = t.HomotopyElement("unrelated", 4, 29, 4)
    forged = replace(goal, target_generator=named)
    assert t.module.expand_canonical_formal_image(forged) == ()
    wrong_map = replace(goal, map=t.TodaSuspensionMap(
        t.TodaPrimaryGroup(28, 3), t.TodaPrimaryGroup(30, 4)
    ))
    assert t.module.expand_canonical_formal_image(wrong_map) == ()


def test_ill_typed_composition_not_accepted(isolated_bridge) -> None:
    t = isolated_bridge
    a = t.HomotopyElement("a", 3, 27, 3)
    b = t.HomotopyElement("b", 4, 34, 4)
    invalid = t.Composition(a, b)
    assert t.module.canonical_formal_suspension(invalid) is None
    assert t.module.formal_image_goal(invalid) is None
