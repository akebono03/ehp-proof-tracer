"""Actual source-first searches and strict typed backward proposal checks."""
from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, IteratedSuspension
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r7_left_composition_reuse_audit.audit import (
    LEFT_RULE, audit_cases, has_exact_candidate, public_search, replay_left, rule_name,
)
from phase177_r7r1_left_composition_public.provider import (
    expand_public_left_composition, left_composition_input,
)
from proof import ProofRule, Relation, RelationType

LABELS = tuple(audit_cases())


def ancestors(step):
    yield step
    for parent in step.premises:
        yield from ancestors(parent)


def verify_left_ancestor(step, target, premise):
    """Accept direct or symmetric paths, replay the actual congruence node."""
    for node in ancestors(step):
        if rule_name(node) != LEFT_RULE or node.rule is not ProofRule.INFERENCE:
            continue
        if node.conclusion == target:
            expected = premise
        elif node.conclusion == Relation(target.rhs, target.lhs):
            expected = Relation(premise.rhs, premise.lhs)
        else:
            continue
        parent, = node.premises
        assert parent.conclusion == expected
        verified = replay_left(node.conclusion.lhs.left, parent, node.conclusion)
        assert verified.conclusion == node.conclusion
        assert verified.premises == (parent,)
        return
    pytest.fail('No actual typed left congruence ancestor for target or its reverse')


@pytest.fixture(scope='module')
def context():
    invocation, result, calls, model, view = capture()
    assert model is not None and invocation['goal'].lhs == result.target
    print('PHASE177_R7R1_ROOT_STATUS='+result.status.value)
    print('PHASE177_R7R1_ROOT_OPEN_GOALS='+str(len(result.open_goals)))
    return invocation


@pytest.mark.parametrize('label', LABELS)
def test_exact_candidate(label):
    alpha, premise, target = audit_cases()[label]
    assert left_composition_input(target) == premise
    option, = expand_public_left_composition(target)
    assert option.rule.name == LEFT_RULE
    assert option.subgoals == (premise,)
    reverse, = expand_public_left_composition(Relation(target.rhs, target.lhs))
    assert reverse.subgoals == (Relation(premise.rhs, premise.lhs),)


def test_arbitrary_right_factors_without_suspension():
    alpha = HomotopyElement('left', 2, 4, 2)
    beta = HomotopyElement('b', 4, 8, 4)
    gamma = HomotopyElement('c', 4, 8, 4)
    goal = Relation(Composition(alpha, beta), Composition(alpha, gamma))
    option, = expand_public_left_composition(goal)
    assert option.subgoals == (Relation(beta, gamma),)
    # No premise is proved merely by proposing this candidate.


def test_rejects_wrong_types_and_no_progress():
    alpha, premise, target = audit_cases()['eta']
    wrong = HomotopyElement('bad', 2, 3, 2)
    different = replace(alpha, name='unrelated')
    bad = (
        Relation(Composition(alpha, premise.lhs), Composition(different, premise.rhs)),
        Relation(Composition(wrong, premise.lhs), Composition(wrong, premise.rhs)),
        Relation(target.lhs, target.lhs),
        Relation(premise.lhs, premise.rhs),
        replace(target, relation_type=RelationType.ORDER),
        replace(target, note='not a plain equality'),
        Relation(target.lhs, Composition(alpha, IteratedSuspension(premise.lhs, 1))),
    )
    for goal in bad:
        assert left_composition_input(goal) is None
        assert not expand_public_left_composition(goal)


@pytest.mark.parametrize('label', LABELS)
def test_public_composition(label, context):
    _, premise, target = audit_cases()[label]
    provider = shared_expansion_provider(context['bridge'], proof_target=context['goal'])
    options = provider(target)
    assert any(o.rule.name == LEFT_RULE and o.subgoals == (premise,) for o in options)
    step, row = public_search(target, context, provider)
    assert step is not None, row
    assert step.rule is ProofRule.INFERENCE and step.conclusion == target
    verify_left_ancestor(step, target, premise)
    print('PHASE177_R7R1_CASE='+label+':PUBLIC_COMPOSITION_PROVED')


def test_actual_captured_provider(context):
    _, premise, target = audit_cases()['eta']
    step, row = public_search(target, context, context['expansion_provider'])
    assert step is not None, row
    assert step.rule is ProofRule.INFERENCE
    verify_left_ancestor(step, target, premise)
    print('PHASE177_R7R1_CAPTURED_ETA_COMPOSITION_PROVED=TRUE')
