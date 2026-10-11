import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase163_r4_r44_assertion_audit import audit, validate_tex_sources, write_report


def fixture_data():
    body = r'\begin{proposition}\label{prop:5.1}式\end{proposition}'
    checksum = hashlib.sha256(body.encode('utf-8')).hexdigest()
    tex = {'phase': '163 R4-R42', 'mode': 'READ_ONLY_EXTRACTION',
           'registration_applied': False, 'missing_sources': [], 'item_count': 1,
           'chapters': [{'chapter': 5, 'source_file': 'Toda_05.tex',
                         'sha256': 'abc', 'items': [{
                             'chapter': 5, 'order': 1, 'kind': 'proposition',
                             'line': 20, 'labels': ['prop:5.1'], 'tags': [],
                             'locator_candidate': 'Proposition 5.1', 'tex': body}]}]}
    mapping = {'phase': '163 R4-R43', 'mode': 'READ_ONLY_MAPPING',
               'registration_applied': False, 'id_allocated': False,
               'item_count': 1, 'source_sha256': {'5': 'abc'},
               'duplicate_locator_candidates': {},
               'rows': [{'chapter': 5, 'source_order': 1, 'kind': 'proposition',
                         'source_line': 20, 'labels': ['prop:5.1'], 'tags': [],
                         'locator_candidate': 'Proposition 5.1',
                         'existing_reference_id': 'toda:Proposition 5.1',
                         'proposed_reference_id': None, 'status': 'EXISTING_REFERENCE',
                         'sha256_tex_body': checksum,
                         'tex_registered': False, 'structured': False,
                         'source_verified': False}]}
    ref_id = 'toda:Proposition 5.1'
    registry = SimpleNamespace(
        _references={ref_id: SimpleNamespace(locator='Proposition 5.1')},
        _assertions={
            'old:a': SimpleNamespace(assertion_id='old:a', reference_id=ref_id,
                component_position=1, scope=None,
                kind=SimpleNamespace(value='statement'),
                origin=SimpleNamespace(value='fixed_statement'), content=object()),
            'old:b': SimpleNamespace(assertion_id='old:b', reference_id=ref_id,
                component_position=None, scope='n>=3',
                kind=SimpleNamespace(value='statement'),
                origin=SimpleNamespace(value='fixed_statement'), content=object()),
        })
    return mapping, tex, registry


def test_complete_existing_assertion_crosswalk_preserves_ids():
    mapping, extraction, registry = fixture_data()
    result = audit(mapping, extraction, registry)
    assert [x['assertion_id'] for x in result['assertion_crosswalk']] == ['old:a', 'old:b']
    assert result['existing_reference_count'] == 1
    assert result['existing_assertion_count'] == 2
    assert result['component_positions_unknown_count'] == 1
    assert result['assertion_match_levels'] == {'REFERENCE_ONLY': 2}
    assert all(x['requires_semantic_review'] and not x['tex_span_identified']
               for x in result['assertion_crosswalk'])
    assert not result['registration_applied']


def test_reject_changed_tex_body():
    mapping, extraction, registry = fixture_data()
    extraction['chapters'][0]['items'][0]['tex'] += ' changed'
    with pytest.raises(ValueError, match='TeX body changed'):
        audit(mapping, extraction, registry)


def test_reject_unmapped_existing_reference():
    mapping, extraction, registry = fixture_data()
    registry._references['toda:Lemma 5.2'] = SimpleNamespace(locator='Lemma 5.2')
    with pytest.raises(ValueError, match='registry references not exactly mapped'):
        audit(mapping, extraction, registry)


def test_reject_unmapped_assertion_and_duplicate_position():
    mapping, extraction, registry = fixture_data()
    registry._assertions['old:c'] = SimpleNamespace(
        assertion_id='old:c', reference_id='toda:Lemma 5.2',
        component_position=None)
    with pytest.raises(ValueError, match='unknown assertion reference'):
        audit(mapping, extraction, registry)
    registry._assertions.pop('old:c')
    registry._assertions['old:b'].component_position = 1
    with pytest.raises(ValueError, match='duplicate component_position'):
        audit(mapping, extraction, registry)


def test_numberless_candidate_is_retained_without_new_id():
    mapping, extraction, registry = fixture_data()
    registry._references.clear()
    registry._assertions.clear()
    row = mapping['rows'][0]
    row.update(status='UNNUMBERED_ENVIRONMENT', locator_candidate=None,
               existing_reference_id=None, proposed_reference_id=None,
               labels=[])
    item = extraction['chapters'][0]['items'][0]
    item.update(locator_candidate=None, labels=[])
    result = audit(mapping, extraction, registry)
    assert result['unresolved_locator_count'] == 1
    assert result['reference_units'][0]['tex_body'] == item['tex']
    assert result['reference_units'][0]['existing_reference_id'] is None
    assert result['existing_assertion_count'] == 0


def test_report_contains_full_body_and_csv(tmp_path):
    mapping, extraction, registry = fixture_data()
    result = audit(mapping, extraction, registry)
    write_report(result, tmp_path)
    data = json.loads((tmp_path / 'crosswalk.json').read_text(encoding='utf-8'))
    assert data['reference_units'][0]['tex_body'] == extraction['chapters'][0]['items'][0]['tex']
    assert 'old:a' in (tmp_path / 'assertions.csv').read_text(encoding='utf-8-sig')
    assert '2' in (tmp_path / 'report.md').read_text(encoding='utf-8')


def test_validate_tex_source_digest(tmp_path):
    mapping, extraction, registry = fixture_data()
    raw = '命題'.encode('utf-8')
    (tmp_path / 'Toda_05.tex').write_bytes(raw)
    extraction['chapters'][0]['sha256'] = hashlib.sha256(raw).hexdigest()
    validate_tex_sources(extraction, tmp_path)
    (tmp_path / 'Toda_05.tex').write_bytes(raw + b'!')
    with pytest.raises(ValueError, match='changed TeX source'):
        validate_tex_sources(extraction, tmp_path)


def test_reject_mutating_prior_mapping():
    mapping, extraction, registry = fixture_data()
    mapping['id_allocated'] = True
    with pytest.raises(ValueError, match='not read-only'):
        audit(mapping, extraction, registry)


def test_no_mutation_of_input_records():
    mapping, extraction, registry = fixture_data()
    before_map, before_tex = copy.deepcopy(mapping), copy.deepcopy(extraction)
    before_refs = set(registry._references)
    before_assertions = set(registry._assertions)
    audit(mapping, extraction, registry)
    assert mapping == before_map
    assert extraction == before_tex
    assert set(registry._references) == before_refs
    assert set(registry._assertions) == before_assertions
