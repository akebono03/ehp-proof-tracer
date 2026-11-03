"""Focused typed tests; canonical formal images are not named identities."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from phase173_r4_r15r3_formal_suspension_bridge.bridge import (
    canonical_formal_suspension,
    expand_canonical_formal_image,
    formal_image_goal,
    is_canonical_formal_image,
)
from phase173_r4_r15r3_formal_suspension_bridge.audit import inspect_k


def element(name: str, source: int, target: int) -> HomotopyElement:
    return HomotopyElement(
        name=name, dimension=target, source=source, target=target,
        generator=GeneratorSymbol(family=name),
    )


def test_nested_compositions_have_unbounded_formal_suspension() -> None:
    first = element("a", 28, 3)
    second = element("b", 32, 28)
    third = element("c", 34, 32)
    source = Composition(first, Composition(second, third))
    image = canonical_formal_suspension(source)
    assert image == Composition(
        IteratedSuspension(first, 1),
        Composition(IteratedSuspension(second, 1), IteratedSuspension(third, 1)),
    )
    assert typed_element_span(source) == (34, 3)
    assert typed_element_span(image) == (35, 4)
    goal = formal_image_goal(source)
    assert goal == GeneratorImage(
        map=TodaSuspensionMap(TodaPrimaryGroup(34, 3), TodaPrimaryGroup(35, 4)),
        source_generator=source, target_generator=image,
    )
    assert is_canonical_formal_image(goal)
    options = expand_canonical_formal_image(goal)
    assert len(options) == 1
    assert options[0].subgoals == ()
    assert options[0].rule.match_guard((), {}) is True
    assert options[0].rule.literature_reference is None


def test_formal_rule_rejects_forged_named_generator_and_wrong_map() -> None:
    source = element("unstable", 34, 3)
    goal = formal_image_goal(source)
    assert goal is not None
    forged = replace(goal, target_generator=element("unrelated", 35, 4))
    assert not is_canonical_formal_image(forged)
    assert expand_canonical_formal_image(forged) == ()
    wrong = replace(goal, map=TodaSuspensionMap(
        TodaPrimaryGroup(34, 3), TodaPrimaryGroup(36, 4),
    ))
    assert not is_canonical_formal_image(wrong)
    assert expand_canonical_formal_image(wrong) == ()


def test_reject_ill_typed_compositions_and_unrelated_objects() -> None:
    a = element("a", 28, 3)
    b = element("b", 34, 4)
    assert canonical_formal_suspension(Composition(a, b)) is None
    assert formal_image_goal(Composition(a, b)) is None
    assert expand_canonical_formal_image("not a typed generator image") == ()


@pytest.mark.parametrize("k,expected_count", ((4, 1), (7, 0), (8, 1), (31, 4)))
def test_real_database_formal_frontier_is_not_named_proof(
    k: int, expected_count: int,
) -> None:
    row = inspect_k(k)
    assert row["abstract_compatible"] is True
    assert row["group_proof_completed"] is False
    assert row["new_given_assertions"] == 0
    assert row["public_route_modified"] is False
    assert row["named_generator_identifications_proved"] == 0
    assert len(row["canonical_formal_images"]) == expected_count
    assert row["all_formal_rules_admissible"] is True


def test_k31_does_not_guess_permutation_of_four_equal_order_targets() -> None:
    row = inspect_k(31)
    assert row["state"] == "FORMAL_IMAGES_AVAILABLE_NAMED_IDENTITIES_PENDING"
    assert row["residual_target_count"] == 4
    assert len(row["canonical_formal_images"]) == 4
    for item in row["canonical_formal_images"]:
        assert item["formal_rule_admissible"] is True
        assert item["possible_named_target_indices_by_order_only"]
        assert len(item["possible_named_target_indices_by_order_only"]) == 4
        assert item["named_target_identification_proved"] is False
