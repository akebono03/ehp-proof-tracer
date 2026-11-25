"""Focused audit diagnostics; real source-first searches run in audit.main."""
from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase177_r7_left_composition_reuse_audit.audit import (
    HEAD, LEFT_RULE, PINS, audit_cases, classify, composition_target, has_exact_candidate,
)
from proof import Relation, RelationType


@pytest.mark.parametrize('label', ['eta','nu_cited','sigma_cited','epsilon_cited','formal_stable','formal_unstable'])
def test_audit_case_is_well_typed(label):
    alpha, premise, target = audit_cases()[label]
    assert target == Relation(Composition(alpha, premise.lhs), Composition(alpha, premise.rhs))
    assert typed_endpoints(target.lhs) == typed_endpoints(target.rhs)
    assert premise.lhs != premise.rhs


def test_rejects_wrong_left_factor_and_relation():
    alpha, premise, _ = audit_cases()['eta']
    wrong = HomotopyElement('bad', 2, 3, 2)
    with pytest.raises(ValueError, match='COMPOSABLE_TYPED_ENDPOINTS_REQUIRED'):
        composition_target(wrong, premise)
    with pytest.raises(ValueError, match='EQUALITY_REQUIRED'):
        composition_target(alpha, replace(premise, relation_type=RelationType.ORDER))
    with pytest.raises(ValueError, match='COMPOSABLE_TYPED_ENDPOINTS_REQUIRED'):
        composition_target(alpha, Relation(premise.lhs, wrong))


@pytest.mark.parametrize('flags,expected', [
    ((True,True,True,True), 'PUBLIC_COMPOSITION_PROVED'),
    ((True,True,True,False), 'PUBLIC_COMPOSITION_PROVED'),
    ((False,False,False,False), 'PREMISE_FRONTIER'),
    ((True,False,False,False), 'EXISTING_RULE_REPLAY_FRONTIER'),
    ((True,True,False,True), 'PUBLIC_CANDIDATE_REPLAY_FRONTIER'),
    ((True,True,False,False), 'PUBLIC_BACKWARD_CONNECTION_FRONTIER'),
])
def test_classify(flags, expected):
    assert classify(*flags) == expected


def test_exact_candidate_is_not_merely_a_rule_name():
    _, premise, _ = audit_cases()['eta']
    assert not has_exact_candidate({'target_calls': []}, premise)
    assert not has_exact_candidate({'target_calls': [[{'rule':LEFT_RULE,'subgoals':['wrong']}]]}, premise)
    assert has_exact_candidate({'target_calls': [[{'rule':LEFT_RULE,'subgoals':[repr(premise)]}]]}, premise)


def test_review_pins():
    assert HEAD == '59d7a79aa632dbc5d1999b8478361cebd77df540'
    assert 'phase177_r6_general_suspension_public/provider.py' in PINS
    assert all(len(pin) == 40 for pin in PINS.values())
