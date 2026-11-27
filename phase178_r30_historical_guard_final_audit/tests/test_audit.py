from copy import deepcopy
import xml.etree.ElementTree as ET

import pytest

from phase178_r30_historical_guard_final_audit.audit import (
    GUARD, MISSING, TEST_NAMES, PRELUDE, PROP42, ZERO51,
    classify_baseline, validate_observation,
)


def make_xml(tmp_path, failure=GUARD, message=MISSING, extra=None):
    suite = ET.Element('testsuite')
    for name in sorted(TEST_NAMES):
        case = ET.SubElement(suite, 'testcase', name=name)
        if name == failure:
            ET.SubElement(case, 'failure', message=message)
        if name == GUARD and extra is not None:
            ET.SubElement(case, extra)
    path = tmp_path / 'baseline.xml'
    ET.ElementTree(suite).write(path, encoding='utf-8')
    return path


def test_exact_known_failure(tmp_path):
    assert classify_baseline(1, make_xml(tmp_path)) == 'KNOWN_GUARD_REPRODUCED_OPEN'


def test_all_pass_is_not_known_open(tmp_path):
    assert classify_baseline(0, make_xml(tmp_path, failure=None)) == 'PASS_ALL_6_REQUIRES_ROUTE_REVIEW'


@pytest.mark.parametrize('kwargs', [
    {'message': 'different assertion'}, {'failure': None}, {'extra': 'skipped'},
    {'extra': 'error'}, {'failure': 'test_r4c_only_exact_pi64_map_is_eligible'},
])
def test_unexpected_outcomes_fail(tmp_path, kwargs):
    with pytest.raises(RuntimeError):
        classify_baseline(1, make_xml(tmp_path, **kwargs))


def observation():
    sources = [{'type': name, 'premise_count': 0,
                'links': [{'origin': 'FIXED_STATEMENT', 'position': pos}]}
               for name, pos in ((PRELUDE, 7250), (PROP42, 6800), (ZERO51, 7700))]
    return dict(trust_replay='VERIFIED', exact_map_and_branches=True, injection_direct_prelude=True,
                surjection_exactness_and_zero=True, lemma54_screened_given_count=0,
                prelude_position=7250, citing_position=9000,
                missing_historical_types=['TodaProp44UniversalStatement'],
                given_sources=sources, replay_counts=[4, 3], target_group_given_count=0)


def test_valid_observation():
    assert validate_observation('KNOWN_GUARD_REPRODUCED_OPEN', observation()) == 'OUTDATED_TEST_SOURCE_CONTRACT_CONFIRMED'


@pytest.mark.parametrize('key,value', [
    ('trust_replay', 'UNVERIFIED'), ('exact_map_and_branches', False),
    ('injection_direct_prelude', False), ('surjection_exactness_and_zero', False),
    ('lemma54_screened_given_count', 1), ('prelude_position', 7300),
    ('missing_historical_types', []), ('replay_counts', [4, 2]),
    ('target_group_given_count', 1), ('citing_position', 7250),
])
def test_invalid_observation(key, value):
    data = observation()
    data[key] = value
    with pytest.raises(RuntimeError):
        validate_observation('KNOWN_GUARD_REPRODUCED_OPEN', data)


@pytest.mark.parametrize('change', ['missing', 'wrong_type', 'unlinked', 'archive', 'premises'])
def test_missing_or_invalid_source_rejected(change):
    data = deepcopy(observation())
    rows = data['given_sources']
    if change == 'missing':
        rows.pop()
    elif change == 'wrong_type':
        rows[0]['type'] = 'TodaProp44UniversalStatement'
    elif change == 'unlinked':
        rows[0]['links'] = []
    elif change == 'archive':
        rows[0]['links'][0]['origin'] = 'SOURCE_ARCHIVE'
    else:
        rows[0]['premise_count'] = 1
    with pytest.raises(RuntimeError):
        validate_observation('KNOWN_GUARD_REPRODUCED_OPEN', data)


def test_all_pass_requires_new_route_review():
    with pytest.raises(RuntimeError, match='BASELINE_CHANGED_REQUIRES_REVIEW'):
        validate_observation('PASS_ALL_6_REQUIRES_ROUTE_REVIEW', observation())
