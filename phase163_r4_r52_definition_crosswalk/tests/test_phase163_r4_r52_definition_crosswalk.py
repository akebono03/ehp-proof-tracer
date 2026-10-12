"""Focused R4-R52 tests against the prior phase's genuine source snapshots."""
import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r52_definition_crosswalk import audit, write_results

ROOT = Path(__file__).resolve().parents[2]


def data():
    review = json.loads((ROOT / 'phase163_r4_r51_output' / 'review.json').read_text(encoding='utf-8'))
    catalog = json.loads((ROOT / 'phase163_r4_r47_output' / 'catalog.json').read_text(encoding='utf-8'))
    return review, catalog, ROOT / 'phase163_r4_r42_tex_extract' / 'inputs'


def test_all_19_candidates_are_covered():
    result = audit(*data())
    assert len(result['candidates']) == 19
    assert len({r['r48_index'] for r in result['candidates']}) == 19


def test_no_ids_or_registrations_are_fabricated():
    result = audit(*data())
    assert result['ids_allocated'] is False
    assert result['registration_applied'] is False
    assert all(x['new_registration_status'] == 'NOT_DECIDED' for x in result['candidates'])


def test_no_false_semantic_matches():
    result = audit(*data())
    assert result['direct_definition_match_count'] == 0
    assert result['semantic_overlap_unresolved_count'] == 19
    assert all(x['direct_definition_assertion_id'] is None for x in result['candidates'])


def test_components_remain_attached():
    result = audit(*data())
    rows = {r['r48_index']: r for r in result['candidates']}
    assert 18 in rows[82]['component_indices']
    assert 72 in rows[88]['component_indices']
    assert 22 in rows[83]['component_indices']


def test_review_queue_incomplete_fails():
    review, catalog, inputs = data()
    review['review_queue'].pop()
    with pytest.raises(ValueError, match='incomplete'):
        audit(review, catalog, inputs)


def test_catalog_id_mutation_fails():
    review, catalog, inputs = data()
    catalog['existing_assertion_ids'][0] = 'tampered'
    with pytest.raises(ValueError, match='snapshot'):
        audit(review, catalog, inputs)


def test_changed_tex_digest_fails(tmp_path):
    review, catalog, inputs = data()
    copied = tmp_path / 'inputs'
    copied.mkdir()
    for path in inputs.glob('*.tex'):
        (copied / path.name).write_bytes(path.read_bytes())
    with (copied / 'Toda_03_2(2).tex').open('ab') as file:
        file.write(b'change')
    with pytest.raises(ValueError, match='changed'):
        audit(review, catalog, copied)


def test_changed_role_fails():
    review, catalog, inputs = data()
    row = next(x for x in review['review_queue'] if x['r48_index'] == 238)
    row['role_decision'] = 'PENDING_MATHEMATICAL_REVIEW'
    with pytest.raises(ValueError, match='count'):
        audit(review, catalog, inputs)


def test_deterministic_outputs(tmp_path):
    result = audit(*data())
    write_results(result, tmp_path / 'a')
    write_results(result, tmp_path / 'b')
    for name in ('crosswalk.json', 'crosswalk.csv', 'report.md'):
        assert (tmp_path / 'a' / name).read_bytes() == (tmp_path / 'b' / name).read_bytes()
