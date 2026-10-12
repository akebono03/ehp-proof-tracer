import copy
import hashlib

import pytest

from phase163_r4_r45_component_review import PRIORITY, make_review


def fixture():
    units = []
    rows = []
    for i, rid in enumerate(PRIORITY, 1):
        body = f'\\begin{{equation}}\n{x if (x := i) else i}\n\\end{{equation}}'
        units.append({'existing_reference_id': rid, 'chapter': 5, 'source_order': i,
                      'source_line': i * 10, 'tex_body': body,
                      'sha256_tex_body': hashlib.sha256(body.encode()).hexdigest()})
        rows.append({'assertion_id': f'a{i}', 'reference_id': rid, 'match_level': 'REFERENCE_ONLY',
                     'component_position_existing': i if i % 2 else None,
                     'scope_existing': None, 'content_type': 'TodaFixedStatementComponent'})
    return {'source_sha256': {'5': 'fixture'}, 'existing_reference_count': 5, 'existing_assertion_count': 5,
            'reference_units': units, 'assertion_crosswalk': rows}


def test_priority_packets_keep_ids_and_no_automatic_matches():
    result = make_review(fixture(), {})
    assert result['priority_assertion_count'] == 5
    assert result['semantic_matches_confirmed'] == 0
    assert result['positions_newly_confirmed'] == 0
    assert result['registration_applied'] is False
    assert all(a['candidate_span_start'] is None for p in result['packets'] for a in p['assertions'])


def test_missing_reference_rejected():
    data = fixture()
    data['reference_units'].pop()
    with pytest.raises(ValueError):
        make_review(data, {})


def test_duplicate_assertion_rejected():
    data = fixture()
    data['assertion_crosswalk'][1]['assertion_id'] = 'a1'
    with pytest.raises(ValueError, match='duplicate assertion'):
        make_review(data, {})


def test_preconfirmed_match_rejected():
    data = fixture()
    data['assertion_crosswalk'][0]['match_level'] = 'SEMANTIC_MATCH'
    with pytest.raises(ValueError, match='pre-confirmed'):
        make_review(data, {})


def test_nonpriority_assertions_not_lost():
    data = fixture()
    data['reference_units'].append({'existing_reference_id': 'toda:Other'})
    data['existing_reference_count'] += 1
    data['assertion_crosswalk'].append({**copy.deepcopy(data['assertion_crosswalk'][0]),
                                       'assertion_id': 'other', 'reference_id': 'toda:Other'})
    data['existing_assertion_count'] += 1
    result = make_review(data, {})
    assert result['other_assertion_count'] == 1
    assert result['remaining_assertions'][0]['assertion_id'] == 'other'
