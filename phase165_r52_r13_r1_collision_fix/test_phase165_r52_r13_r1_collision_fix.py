"""R52-R13-R1 focused regression: direct fixed Reference vs derived route."""
from dataclasses import dataclass

import pytest

from phase165_r3_recursive_search import (
    GoalExpansion,
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from phase165_r52_r13_reference_registration import register_adopted_composite_reference
from phase165_r52_r12_component_bridge import expand_cited_given_components
from proof import ProofRule


@dataclass(frozen=True)
class SampleClaims:
    fact: int
    companion: str


def _bridge():
    return expand_cited_given_components(register_adopted_composite_reference(
        assertion_id='test:composite',
        locator='Proposition Test',
        source_id='adopted source',
        content=SampleClaims(17, 'another fact'),
    ))


def test_r13_r1_direct_registered_leaf_wins_without_expansion():
    bridge = _bridge()
    calls = []
    def expansion(target):
        calls.append(target)
        return ()
    step = reconstruct_registered_goal(
        17, bridge, 'test:composite', expansion,
        lookup_mode='typed_reference',
    )
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == 17
    assert calls == []


def test_r13_r1_other_registered_component_reusable():
    bridge = _bridge()
    step = reconstruct_registered_goal(
        'another fact', bridge, 'test:composite', lambda target: (),
        lookup_mode='typed_reference',
    )
    assert step.rule is ProofRule.GIVEN


def test_r13_r1_unregistered_goal_keeps_expansion_path():
    bridge = _bridge()
    calls = []
    def expansion(target):
        calls.append(target)
        return ()
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            999, bridge, 'test:composite', expansion,
            lookup_mode='typed_reference',
        )
    assert calls == [999]


def test_r13_r1_real_prop51_pi32_is_direct_leaf():
    from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
    bridge = expand_cited_given_components(build_adopted_prop51_reference())
    parent = bridge.registry.assertion('toda:adopted:prop5.1:finite_dimensional')
    goal = parent.content.pi3_2_group_relation
    step = reconstruct_registered_goal(
        goal, bridge, parent.assertion_id,
        lambda target: (), lookup_mode='typed_reference',
    )
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == goal
