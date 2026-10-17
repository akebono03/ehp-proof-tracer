"""R12-R12: target-scoped typed EHP consequences and source ancestry."""
from __future__ import annotations

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import (
    build_adopted_prop42_general_reference,
    build_prop42_specialization_provider,
)
from phase165_r12_r12_ehp_consequences import (
    EHPImageEqualsKernelStatement,
    expand_ehp_exactness_consequences,
    proof_has_general_prop42_ancestor,
)
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from proof import ProofRule
from toda_rules import TodaProp42ExactnessStatement


def exactness(a, b, c, f, g):
    return TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        TodaPrimaryGroup(*a), TodaPrimaryGroup(*b), TodaPrimaryGroup(*c), f, g,
    ))


def provider_for(bridge):
    source_provider = build_prop42_specialization_provider(bridge)

    def provide(goal):
        return expand_ehp_exactness_consequences(goal) + source_provider(goal)

    return provide


def test_r12_both_pi32_and_pi43_image_kernel_have_one_universal_source():
    bridge = build_adopted_prop42_general_reference()
    source_id = next(iter(bridge.registry._assertions))
    for exact in (
        exactness((2, 1), (3, 2), (3, 3), EHP_E_MAP, EHP_H_MAP),
        exactness((5, 5), (3, 2), (4, 3), EHP_DELTA_MAP, EHP_E_MAP),
        exactness((3, 2), (4, 3), (4, 5), EHP_E_MAP, EHP_H_MAP),
    ):
        goal = EHPImageEqualsKernelStatement(exact.window)
        proof = reconstruct_registered_goal(
            goal, bridge, citing_assertion_id=source_id,
            expansion_provider=provider_for(bridge), lookup_mode="typed_reference",
        )
        assert proof.conclusion == goal
        assert proof.rule is ProofRule.INFERENCE
        assert len(proof.premises) == 1
        assert proof.premises[0].rule is ProofRule.INFERENCE
        assert proof_has_general_prop42_ancestor(proof)


def test_r12_surjection_has_unproved_zero_target_obligation():
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3)))
    expansion, = expand_ehp_exactness_consequences(goal)
    exact, zero = expansion.subgoals
    assert isinstance(exact, TodaProp42ExactnessStatement)
    assert zero == TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(4, 5))
    assert expand_ehp_exactness_consequences(zero) == ()


def test_r12_no_uncited_zero_group_can_close_surjection():
    bridge = build_adopted_prop42_general_reference()
    source_id = next(iter(bridge.registry._assertions))
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3)))
    try:
        reconstruct_registered_goal(
            goal, bridge, citing_assertion_id=source_id,
            expansion_provider=provider_for(bridge), lookup_mode="typed_reference",
        )
    except RegisteredGoalUnresolved:
        pass
    else:
        raise AssertionError("zero-target proof must not be invented")


def test_r12_wrong_dimensional_window_not_accepted():
    bad = exactness((5, 5), (3, 2), (4, 4), EHP_DELTA_MAP, EHP_E_MAP)
    assert expand_ehp_exactness_consequences(EHPImageEqualsKernelStatement(bad.window)) == ()


def test_r12_missing_general_reference_has_no_proof_expansion():
    bridge = build_adopted_prop42_general_reference()
    source = next(iter(bridge.registry._assertions))
    # Screening out the one universal reference leaves no valid source proof.
    from phase163_r4_registry_bridge import RegistryBridgeResult
    excluded = RegistryBridgeResult(bridge.registry, bridge.records, ())
    exact = exactness((5, 5), (3, 2), (4, 3), EHP_DELTA_MAP, EHP_E_MAP)
    goal = EHPImageEqualsKernelStatement(exact.window)
    try:
        reconstruct_registered_goal(
            goal, excluded, citing_assertion_id=source,
            expansion_provider=provider_for(excluded), lookup_mode="typed_reference",
        )
    except RegisteredGoalUnresolved:
        pass
    else:
        raise AssertionError("uncited exactness must not be inferred")


def test_r12_pi32_proof_source_is_internal_ancestry_not_renderer_text():
    bridge = build_adopted_prop42_general_reference()
    source = next(iter(bridge.registry._assertions))
    exact = exactness((2, 1), (3, 2), (3, 3), EHP_E_MAP, EHP_H_MAP)
    step = reconstruct_registered_goal(
        exact, bridge, citing_assertion_id=source,
        expansion_provider=provider_for(bridge), lookup_mode="typed_reference",
    )
    assert step.rule is ProofRule.INFERENCE
    assert proof_has_general_prop42_ancestor(step)
    assert len(step.premises) == 1
    assert step.premises[0].rule is ProofRule.GIVEN
