"""Phase 176 R3R39: existing-rule expansion and source-gate tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
from map_facts import EHP_H_MAP
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r38_equality_transport_isolated.source import (
    right_hopf_transport_inputs,
)
from phase176_r3r39_public_equality_transport.source import (
    build_public_right_hopf_transport_provider,
    right_hopf_transport_backward_plan,
)
from proof import ProofRule, ProofStep, Relation, RelationType, apply_inference_match, find_inference_match


def _example():
    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    delta = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = Composition(eta6, eta7)
    goal = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)),
                    Composition(delta, gamma), RelationType.EQUALITY)
    value = Relation(MapApplication(EHP_H_MAP, alpha), delta, RelationType.EQUALITY)
    return goal, (TodaProp22RightFormula(), value)


def test_six_stages_use_only_the_existing_rules_in_order():
    goal, available = _example()
    plan = right_hopf_transport_backward_plan(goal, available)
    assert len(plan) == 6
    assert plan[-1][0] == goal
    assert [expansion.rule.name for _target, expansion in plan] == [
        "equality preserved under left composition",
        "EHP H preserves equality",
        "equality symmetry",
        "equality preserved under left composition",
        "equality transitivity",
        "equality transitivity",
    ]
    beta = Composition(goal.rhs.left, goal.rhs.right.left)
    substituted, suspension = right_hopf_transport_inputs(goal, beta)
    assert plan[0][1].subgoals == (suspension,)
    assert plan[3][1].subgoals == (suspension,)
    assert plan[4][1].subgoals[1] == substituted
    assert plan[5][1].subgoals == (plan[4][0], plan[3][0])


def test_provider_maintains_stages_in_one_dfs_and_is_deterministic():
    goal, available = _example()
    provider = build_public_right_hopf_transport_provider(available)
    assert provider(goal) == provider(goal)
    plan = right_hopf_transport_backward_plan(goal, available)
    for target, expansion in reversed(plan):
        chosen = provider(target)
        assert len(chosen) == 1
        assert chosen[0].rule.name == expansion.rule.name
        assert chosen[0].subgoals == expansion.subgoals
    assert provider("unrelated") == ()


def test_proof_tree_replays_six_existing_steps_with_two_input_obligations():
    goal, available = _example()
    plan = right_hopf_transport_backward_plan(goal, available)
    beta = Composition(goal.rhs.left, goal.rhs.right.left)
    substituted, suspension = right_hopf_transport_inputs(goal, beta)
    # Synthetic inputs are fixtures only, never production proof certificates.
    input_steps = {
        substituted: ProofStep(substituted, (), ProofRule.INFERENCE),
        suspension: ProofStep(suspension, (), ProofRule.INFERENCE),
    }
    for target, expansion in plan:
        premises = tuple(input_steps[subgoal] for subgoal in expansion.subgoals)
        match = find_inference_match(expansion.rule, premises)
        assert match is not None
        result = apply_inference_match(match)
        assert result.conclusion == target
        assert result.premises == premises
        assert result.rule is ProofRule.INFERENCE
        input_steps[target] = result
    assert input_steps[goal].premises == (
        input_steps[plan[4][0]], input_steps[plan[3][0]],
    )


def test_missing_or_ambiguous_screened_sources_fail_closed():
    goal, available = _example()
    for bad in ((), (available[0],), (available[1],),
                available + (available[0],), available + (available[1],)):
        assert right_hopf_transport_backward_plan(goal, bad) == ()
    with pytest.raises(TypeError, match="available must be a tuple"):
        right_hopf_transport_backward_plan(goal, list(available))
    with pytest.raises(TypeError, match="available must be a tuple"):
        build_public_right_hopf_transport_provider(list(available))


def test_invalid_shape_and_dimensions_fail_closed():
    goal, available = _example()
    assert right_hopf_transport_backward_plan(replace(goal, rhs=goal.rhs.left), available) == ()
    assert right_hopf_transport_backward_plan(replace(goal, lhs=goal.rhs), available) == ()
    assert right_hopf_transport_backward_plan(
        replace(goal, rhs=Composition(
            replace(goal.rhs.left, target=4), goal.rhs.right,
        )), available,
    ) == ()
    assert right_hopf_transport_backward_plan(
        replace(goal, lhs=MapApplication(EHP_H_MAP, Composition(
            replace(goal.lhs.expression.left, source=100), goal.rhs.right,
        ))), available,
    ) == ()


def test_not_hardcoded_to_eta_or_nu_names():
    goal, _available = _example()
    alpha = replace(goal.lhs.expression.left, name="formal-alpha", generator=None)
    delta = replace(goal.rhs.left, name="formal-delta", generator=None)
    abstract_goal = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, goal.rhs.right)),
        Composition(delta, goal.rhs.right), RelationType.EQUALITY,
    )
    cited_value = Relation(MapApplication(EHP_H_MAP, alpha), delta, RelationType.EQUALITY)
    plan = right_hopf_transport_backward_plan(
        abstract_goal, (TodaProp22RightFormula(), cited_value),
    )
    assert len(plan) == 6


def test_shared_patch_has_unique_anchors_and_is_idempotent():
    from phase176_r3r39_public_equality_transport.apply import (
        NEW_DISPATCH,
        NEW_SETUP,
        TARGET,
        updated_source,
    )
    original = TARGET.read_text(encoding="utf-8-sig")
    patched = updated_source(original)
    assert patched == original
    assert original.count(NEW_SETUP) == 1
    assert original.count(NEW_DISPATCH) == 1
    assert original.count("options.extend(expand_composite_suspension_equality(goal))") == 1
    assert original.count("options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))") == 1


def test_root_order_gate_does_not_discard_intermediate_transport_expansion():
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
    goal, available = _example()
    root = Relation(TodaPrimaryGroup(8, 3),
                    FiniteCyclicGroup(2, goal.lhs.expression))
    candidate = build_public_right_hopf_transport_provider(available)(goal)
    assert len(candidate) == 1
    assert retain_ordered_root_expansions(root, goal, candidate) == candidate
