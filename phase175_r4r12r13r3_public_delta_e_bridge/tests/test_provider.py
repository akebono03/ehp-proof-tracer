"""Focused source-first tests of conditional R13R3 public proposals."""
from __future__ import annotations

from dataclasses import replace

from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup,
    TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r3_public_delta_e_bridge import installer
from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
    delta_free_coordinate_proposals,
)
from proof import Relation, RelationType


def target_fixture():
    signed = canonical_toda58()
    return Relation(
        lhs=TodaPrimaryGroup(7, 4),
        rhs=DirectSumGroup((
            FreeCyclicGroup(signed.positive_value.left.expression),
            FiniteCyclicGroup(4, signed.positive_value.right.expression),
        )),
        relation_type=RelationType.EQUALITY,
    )


def test_cited_toda58_conditional_branch_has_three_unproved_parents():
    signed = canonical_toda58()
    options = delta_free_coordinate_proposals(
        MapInjective(signed.map), cited58=True,
        database_lookup=lambda n, k: target_fixture() if (n, k) == (4, 3) else None,
    )
    assert len(options) == 1
    source, target, image = options[0].subgoals
    assert source.rhs == FreeCyclicGroup(signed.element)
    assert target == target_fixture()
    assert image == signed


def test_missing_citation_and_incorrect_target_fail_closed():
    signed = canonical_toda58()
    goal = MapInjective(signed.map)
    assert delta_free_coordinate_proposals(goal, cited58=False,
        database_lookup=lambda n, k: target_fixture()) == ()
    wrong = replace(target_fixture(), lhs=TodaPrimaryGroup(8, 4))
    assert delta_free_coordinate_proposals(goal, cited58=True,
        database_lookup=lambda n, k: wrong) == ()


def test_installer_idempotent_and_anchor_required():
    text = "def shared_expansion_provider(bridge, extra_providers=()):\n" + installer.ANCHOR + "    return extra_providers\n"
    updated, required = installer.render(text)
    assert required
    assert updated.count("build_public_delta_e_provider") == 2
    assert installer.render(updated) == (updated, False)


def test_installer_rejects_unreviewed_source():
    import pytest
    with pytest.raises(RuntimeError, match="ANCHOR"):
        installer.render("def other_provider(): pass\n")


def test_e_surjective_backward_route_has_three_obligations():
    from phase175_r4r12r13r2_delta_injective_e_surjective.rule import (
        expand_e_surjective_from_delta_injective,
    )
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)))
    expansion = expand_e_surjective_from_delta_injective(goal)
    assert len(expansion) == 1
    assert len(expansion[0].subgoals) == 3
    assert expansion[0].subgoals[0] == MapInjective(canonical_toda58().map)
