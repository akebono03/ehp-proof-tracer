"""Focused public proposal and patch contracts."""
from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, MapApplication, Multiple
from phase176_r3r40r1_eta_notation_bridge.tests.test_notation import example
from phase176_r3r40r1_eta_notation_bridge.source import connection_backward_plan
from phase176_r3r41_public_quadruple_connection.source import (
    build_public_quadruple_connection_provider, public_quadruple_backward_plan,
)
from phase176_r3r41_public_quadruple_connection.apply import TARGET, SETUP, DISPATCH, updated_source
from proof import Relation


def test_public_plan_matches_audited_obligations():
    transported, forward, available = example()
    goal = Relation(transported.lhs, forward.lhs)
    plan = public_quadruple_backward_plan(goal, available)
    expected = connection_backward_plan(transported, forward, available)
    assert len(plan) == 21
    assert [(t, x.rule.name, x.subgoals) for t, x in plan] == [
        (t, x.rule.name, x.subgoals) for t, x in expected]
    assert transported not in dict(plan) and forward not in dict(plan)


def test_source_gate_rejects_missing_and_duplicate_citations():
    transported, forward, available = example()
    goal = Relation(transported.lhs, forward.lhs)
    for i in range(len(available)):
        assert public_quadruple_backward_plan(goal, available[:i] + available[i+1:]) == ()
        assert public_quadruple_backward_plan(goal, available + (available[i],)) == ()
    with pytest.raises(TypeError):
        public_quadruple_backward_plan(goal, list(available))


def test_provider_replays_all_stages_in_own_context():
    transported, forward, available = example()
    goal = Relation(transported.lhs, forward.lhs)
    plan = public_quadruple_backward_plan(goal, available)
    provider = build_public_quadruple_connection_provider(available)
    assert provider(plan[0][0]) == ()
    assert len(provider(goal)) == 1
    for target, option in reversed(plan):
        actual, = provider(target)
        assert actual.rule.name == option.rule.name and actual.subgoals == option.subgoals
    assert provider(transported) == () and provider(forward) == ()
    assert build_public_quadruple_connection_provider(available)(plan[0][0]) == ()


def test_wrong_multiple_and_generator_are_rejected():
    transported, forward, available = example()
    goal = Relation(transported.lhs, forward.lhs)
    assert public_quadruple_backward_plan(replace(goal, rhs=Multiple(2, forward.lhs.expression)), available) == ()
    wrong = replace(forward.lhs.expression, generator=GeneratorSymbol('η', index=5))
    assert public_quadruple_backward_plan(replace(goal, rhs=Multiple(4, wrong)), available) == ()
    lhs = goal.lhs
    alpha = replace(lhs.expression.left, name='not a cited generator')
    assert public_quadruple_backward_plan(replace(goal, lhs=MapApplication(lhs.map, Composition(alpha, lhs.expression.right))), available) == ()


def test_patch_is_lf_idempotent_and_minimal():
    current = TARGET.read_bytes().decode('utf-8')
    assert '\r' not in current
    assert updated_source(current) == current
    assert current.count(SETUP) == current.count(DISPATCH) == 1
    baseline = current.replace(SETUP, '').replace(DISPATCH, '')
    assert updated_source(baseline) == current
    with pytest.raises(ValueError):
        updated_source(current.replace(DISPATCH, ''))
    with pytest.raises(ValueError):
        updated_source(current.replace('\n', '\r\n'))
