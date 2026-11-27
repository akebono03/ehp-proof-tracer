"""Audit contract tests; synthetic report records are never proof inputs."""
from copy import deepcopy

import pytest

from phase178_r18_n6_source_first_audit.audit import summarize


def records(complete=False):
    goal = {'type': 'SyntheticGoal', 'repr': 'goal', 'text': 'goal'}
    summary = {'n': 6, 'k': 6, 'status': 'complete' if complete else 'partial',
               'open_goal_count': 0 if complete else 1, 'web_error': None,
               'web_key': 'generic-complete-proof' if complete else 'generic-partial-proof',
               'trust_status': 'VERIFIED' if complete else 'NOT_APPLICABLE_PARTIAL',
               'target_given_count': 0, 'complete_invariants_hold': True}
    detail = {'open_goals': [] if complete else [goal],
              'frontier': [] if complete else [{'goal': goal, 'state': 'CANDIDATES_PRESENT',
                                                'observed_expansions': [{'options': [{'rule': 'candidate'}]}]}],
              'provider_calls': [], 'search_context': {},
              'screened_source_inventory': {'target_group_given_links': []}}
    return summary, detail


def test_partial_candidate_is_not_a_complete_proof():
    summary, detail = records()
    before = deepcopy((summary, detail))
    result = summarize(summary, detail)
    assert result['root_complete'] is False
    assert result['frontier'][0]['rules'] == ['candidate']
    assert (summary, detail) == before


def test_complete_requires_verified_public_root():
    summary, detail = records(True)
    assert summarize(summary, detail)['root_complete'] is True
    summary['trust_status'] = 'NOT_VERIFIED_COMPLETE'
    with pytest.raises(RuntimeError, match='COMPLETE_NOT_VERIFIED'):
        summarize(summary, detail)


@pytest.mark.parametrize('key,value,expected', [
    ('n', 7, 'WRONG_TARGET'),
    ('target_given_count', 1, 'TARGET_GIVEN_FOUND'),
    ('open_goal_count', 0, 'OPEN_GOAL_COUNT_CHANGED'),
    ('web_error', 'error', 'WEB_GAP'),
    ('complete_invariants_hold', False, 'TRUST_CONTRACT_FAILED'),
])
def test_invalid_public_observation_fails_closed(key, value, expected):
    summary, detail = records()
    summary[key] = value
    with pytest.raises(RuntimeError, match=expected):
        summarize(summary, detail)


def test_screened_target_given_is_rejected():
    summary, detail = records()
    detail['screened_source_inventory']['target_group_given_links'] = [{'synthetic': True}]
    with pytest.raises(RuntimeError, match='SCREENED_TARGET_GIVEN'):
        summarize(summary, detail)
