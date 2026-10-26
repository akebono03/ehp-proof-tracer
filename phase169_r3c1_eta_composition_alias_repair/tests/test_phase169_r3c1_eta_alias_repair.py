"""R3C1 regression: the actual ID-database generator names also expand."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r21_eta_generator_chain import (
    _composition_eta_suspensions,
    expand_cited_eta_generator,
)
from phase165_r14_r6_generic_iso import GeneratorImage
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from toda_rules import toda_eta_family_definition_statement


def _database_style_eta(index: int) -> HomotopyElement:
    canonical = toda_eta_family_definition_statement(index).element
    subscript = str(index).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
    return replace(canonical, name="η" + subscript)


def _database_style_image(n: int = 2) -> GeneratorImage:
    a = _database_style_eta(n)
    b = _database_style_eta(n + 1)
    c = _database_style_eta(n + 2)
    return GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(n + 2, n), TodaPrimaryGroup(n + 3, n + 1)),
        Composition(a, b),
        Composition(b, c),
    )


def test_unicode_subscript_eta_aliases_expand_to_exact_canonical_subgoals():
    for n in (2, 3, 5):
        goal = _database_style_image(n)
        (option,) = expand_cited_eta_generator(goal)
        first, second = option.subgoals
        assert first.source_generator == toda_eta_family_definition_statement(n).element
        assert first.target_generator == toda_eta_family_definition_statement(n + 1).element
        assert second.source_generator == toda_eta_family_definition_statement(n + 1).element
        assert second.target_generator == toda_eta_family_definition_statement(n + 2).element
        assert all(len(expand_cited_eta_generator(premise)) == 1 for premise in option.subgoals)


def test_real_registered_pi53_generator_uses_same_canonical_proof_path():
    lower_goals = database_structured_group_goal_candidates(n=2, k=2)
    upper_goals = database_structured_group_goal_candidates(n=3, k=2)
    assert len(lower_goals) == len(upper_goals) == 1
    lower, upper = lower_goals[0], upper_goals[0]
    assert isinstance(lower.rhs, FiniteCyclicGroup)
    assert isinstance(upper.rhs, FiniteCyclicGroup)
    image = GeneratorImage(
        TodaSuspensionMap(lower.lhs, upper.lhs),
        lower.rhs.generator,
        upper.rhs.generator,
    )
    (option,) = expand_cited_eta_generator(image)
    assert len(option.subgoals) == 2
    assert all(len(expand_cited_eta_generator(subgoal)) == 1 for subgoal in option.subgoals)


def test_alias_match_does_not_accept_wrong_family_even_when_name_is_eta():
    goal = _database_style_image()
    factor = goal.source_generator.left
    bad = replace(factor, generator=GeneratorSymbol(family="ν", index=2))
    forged = replace(goal, source_generator=Composition(bad, goal.source_generator.right))
    assert _composition_eta_suspensions(forged) is None
    assert expand_cited_eta_generator(forged) == ()


def test_alias_match_does_not_accept_wrong_dimension_or_suspension():
    goal = _database_style_image()
    factor = goal.source_generator.left
    forged_dim = replace(goal, source_generator=Composition(
        replace(factor, dimension=factor.dimension + 1), goal.source_generator.right,
    ))
    assert expand_cited_eta_generator(forged_dim) == ()
    forged_map = replace(goal, map=TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3),
    ))
    assert expand_cited_eta_generator(forged_map) == ()


def test_invalid_partial_eta_name_not_treated_as_verified_alias():
    goal = _database_style_image()
    factor = goal.source_generator.left
    bad = replace(factor, name="eta2_unregistered")
    forged = replace(goal, source_generator=Composition(bad, goal.source_generator.right))
    assert expand_cited_eta_generator(forged) == ()
