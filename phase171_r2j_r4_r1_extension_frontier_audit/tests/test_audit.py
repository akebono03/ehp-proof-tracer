"""Focused, read-only R2J-R4-R1 regression tests."""
from __future__ import annotations

from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase171_r2j_r4_r1_extension_frontier_audit.audit import (
    _extension_window,
    _generator_image_goal,
    _git,
    _matching_screened_relation,
    ROOT,
)
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import Relation, RelationType
from homotopy_groups import FiniteCyclicGroup
from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple


def test_real_ehp_e_h_window_matches_proposition42_dimensions():
    exact = _extension_window()
    assert prop42_exactness_indices(exact) == (2, 6, "e_h")
    window = exact.window
    assert window.source_term == TodaPrimaryGroup(5, 2)
    assert window.middle_term == TodaPrimaryGroup(6, 3)
    assert window.target_term == TodaPrimaryGroup(6, 5)


def test_generator_image_requires_well_typed_double_and_source():
    eta2 = HomotopyElement(
        name="eta2", dimension=2, source=3, target=2,
        generator=GeneratorSymbol(family="η", index=2),
    )
    eta3 = HomotopyElement(
        name="eta3", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3),
    )
    eta4 = HomotopyElement(
        name="eta4", dimension=4, source=5, target=4,
        generator=GeneratorSymbol(family="η", index=4),
    )
    eta5 = HomotopyElement(
        name="eta5", dimension=5, source=6, target=5,
        generator=GeneratorSymbol(family="η", index=5),
    )
    nu = HomotopyElement(
        name="nu-prime", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    # eta_2^3 is the typed element S^5 -> S^2, not eta_2: S^3 -> S^2.
    eta2_cubed = Composition(eta2, Composition(eta3, eta4))
    eta3_eta4_eta5 = Composition(eta3, Composition(eta4, eta5))
    group = Relation(
        TodaPrimaryGroup(5, 2), FiniteCyclicGroup(2, eta2_cubed),
        RelationType.EQUALITY,
    )
    double = Relation(
        Multiple(2, nu), eta3_eta4_eta5, RelationType.EQUALITY,
    )
    image = _generator_image_goal(group, double)
    assert isinstance(image, GeneratorImage)
    assert image.map.source_group == TodaPrimaryGroup(5, 2)
    assert image.map.target_group == TodaPrimaryGroup(6, 3)
    assert image.source_generator == eta2_cubed
    assert image.target_generator == eta3_eta4_eta5
    assert _generator_image_goal(
        group, Relation(Multiple(3, nu), double.rhs, RelationType.EQUALITY),
    ) is None
    assert _generator_image_goal(
        Relation(TodaPrimaryGroup(5, 3), group.rhs, RelationType.EQUALITY), double,
    ) is None
    assert _generator_image_goal(
        Relation(
            group.lhs, FiniteCyclicGroup(2, eta2), RelationType.EQUALITY,
        ), double,
    ) is None
    assert _generator_image_goal(
        Relation(
            group.lhs, FiniteCyclicGroup(3, eta2_cubed), RelationType.EQUALITY,
        ), double,
    ) is None
    assert _generator_image_goal(
        group,
        Relation(
            Multiple(2, nu), Composition(eta3, Composition(eta5, eta4)),
            RelationType.EQUALITY,
        ),
    ) is None
    wrong_nu = HomotopyElement(
        name="nu-prime", dimension=3, source=7, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    assert _generator_image_goal(
        group, Relation(Multiple(2, wrong_nu), double.rhs, RelationType.EQUALITY),
    ) is None


def test_only_whitelisted_git_reads_are_permitted():
    assert ROOT.is_dir()
    try:
        _git("checkout", "main")
    except ValueError as error:
        assert "read-only" in str(error)
    else:
        raise AssertionError("unsafe Git command was accepted")


def test_unmatched_screened_source_does_not_create_a_given():
    from types import SimpleNamespace
    screened = SimpleNamespace(proof_links=())
    assert _matching_screened_relation(screened, "absent", "missing") is None
