"""Typed repository-integrated assertions; no proof steps are installed."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import (
    MapInjective,
    MapSurjective,
    expand_generic_iso_goal,
)
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge,
    shared_expansion_provider,
)
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r2_ehp_chain_audit.audit import typed_chain_goals
from proof import ProofRule


def test_toda42_has_both_exact_type_checked_windows() -> None:
    goals = typed_chain_goals()
    assert prop42_exactness_indices(goals["delta_e_exactness"]) == (6, 12, "delta_e")
    assert prop42_exactness_indices(goals["e_h_exactness"]) == (6, 12, "e_h")
    assert goals["terminal_zero"] == TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 13))
    assert goals["target_zero"] == TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))


def test_delta_iso_only_generates_new_unproved_subgoals() -> None:
    iso = typed_chain_goals()["delta_isomorphism"]
    proposal, = expand_generic_iso_goal(iso)
    injective, surjective = proposal.subgoals
    assert injective == MapInjective(iso.map)
    assert surjective == MapSurjective(iso.map)
    assert proposal.rule.name == "generic injective and surjective imply isomorphism"


def test_existing_source_first_zero_root_remains_closed_to_unproved_given() -> None:
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation

    goal = typed_chain_goals()["target_zero"]
    bridge = build_shared_typed_bridge()
    screened = prefer_universal_prop42_derivation(
        screen_independent_sources_for_derived_goal(bridge, goal=goal)
    )
    assert not any(
        link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == goal
        for link in screened.proof_links
    )
    provider = shared_expansion_provider(screened, proof_target=goal)
    assert provider(goal) == ()
