import copy
import csv
import json
from pathlib import Path

import pytest

from phase163_r4_r75_boundary_ownership import review, write_reports

ROOT = Path(__file__).resolve().parents[2]


def source():
    return json.loads((ROOT/'phase163_r4_r74_output'/'remaining_boundary_proposals.json').read_text(encoding='utf-8'))


def test_focus_counts():
    result = review(source())
    assert result['focused_boundary_count'] == 11
    assert result['hold_review_count'] == 7
    assert result['unnumbered_assertion_review_count'] == 4
    assert result['untouched_r74_count'] == 54


def test_preservation():
    before = source()
    saved = copy.deepcopy(before)
    review(before)
    assert before == saved


def test_grouping_not_false_uniqueness():
    result = review(source())
    assert result['ownership_groups']['ch1:coset-comparison:1004-1027'] == [67, 68, 69]
    assert result['ownership_groups']['ch2:cohomology-maps:560-578'] == [122, 123]
    assert result['ownership_group_count'] < 11


def test_read_only_gate():
    result = review(source())
    assert result['source_boundary_verified_count'] == 0
    assert result['semantic_registration_allowed_count'] == 0
    assert not result['production_registry_modified']
    assert not result['production_ids_allocated']
    assert not result['full_suite_run']


def test_input_not_original_r74_rejected():
    before = source()
    before['source_phase'] = 'other'
    with pytest.raises(ValueError):
        review(before)


def test_excerpt_tampering_rejected():
    before = source()
    before['proposals'][0]['excerpt'] += 'tampered'
    with pytest.raises(ValueError):
        review(before)


def test_role_tampering_rejected():
    before = source()
    target = next(x for x in before['proposals'] if x['r48_index'] == 66)
    target['proposed_review_role'] = 'PROOF_CONTEXT_REVIEW'
    with pytest.raises(ValueError):
        review(before)


def test_anchor_tampering_rejected():
    before = source()
    target = next(x for x in before['proposals'] if x['r48_index'] == 256)
    target['context'] = 'no evidence'
    with pytest.raises(ValueError):
        review(before)


def test_reports_multiline_tex_csv(tmp_path):
    result = review(source())
    write_reports(result, tmp_path)
    restored = json.loads((tmp_path/'ownership_proposals.json').read_text(encoding='utf-8'))
    assert restored['focused_boundary_count'] == 11
    with (tmp_path/'ownership_proposals.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 11
    assert any('\n' in x['excerpt'] for x in rows)
    assert 'R48 #66' in (tmp_path/'report.md').read_text(encoding='utf-8')
