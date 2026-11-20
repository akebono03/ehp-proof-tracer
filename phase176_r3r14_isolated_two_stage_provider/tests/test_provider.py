"""Minimal typed contracts for the isolated two-stage backward provider."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase176_r3r14_isolated_two_stage_provider.provider import preceding_zero_image
from phase176_r3r10_right_zero_transport_isolated.rule import right_zero_transport_inputs


def fixture():
    a = HomotopyElement("a", dimension=2, source=3, target=2)
    b = HomotopyElement("b", dimension=3, source=6, target=3)
    c = HomotopyElement("c", dimension=6, source=7, target=6)
    goal = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        Composition(a, Composition(b, c)), Zero(),
    )
    return goal


def test_generic_prefix_has_correct_typed_zero_image():
    goal = fixture()
    base = preceding_zero_image(goal)
    assert base is not None
    assert right_zero_transport_inputs(goal, base) == (base,)


def test_nonzero_target_rejected():
    goal = fixture()
    assert preceding_zero_image(replace(goal, target_generator=goal.source_generator)) is None


def test_two_factor_goal_rejected():
    goal = fixture()
    assert preceding_zero_image(replace(goal, source_generator=goal.source_generator.right)) is None


def test_no_candidate_for_non_generator_image():
    assert preceding_zero_image("untyped") is None
