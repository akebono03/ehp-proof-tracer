import csv
import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r74_remaining_context_review import PROPOSALS, review, write_reports

ROOT = Path(__file__).resolve().parents[2]


def source():
    return json.loads((ROOT / 'phase163_r4_r73_output' / 'role_decisions.json').read_text(encoding='utf-8'))


def test_all_remaining_candidates_covered():
    result = review(source())
    assert result['new_boundary_review_proposal_count'] == 65
    assert len(result['proposals']) == 65
    assert {p['r48_index'] for p in result['proposals']} == set().union(*PROPOSALS.values())


def test_previous_172_preserved():
    before = source()
    after = review(before)
    assert after['preserved_prior_editorial_proposal_count'] == 172
    assert len([r for r in before['records'] if r['proposed_role'] != 'UNREVIEWED']) == 172


def test_no_production_mutations():
    result = review(source())
    assert result['production_registry_modified'] is False
    assert result['production_ids_allocated'] is False
    assert result['mathematical_role_verified_count'] == 0
    assert all(p['registration_allowed'] is False for p in result['proposals'])


def test_holds_are_explicit():
    result = review(source())
    assert {p['r48_index'] for p in result['proposals'] if p['proposed_review_role'] == 'HOLD_BOUNDARY_REVIEW'} == {66, 67, 68, 69, 133, 142, 256}


def test_source_integrity_gate():
    before = source()
    target = next(r for r in before['records'] if r['proposed_role'] == 'UNREVIEWED')
    target['excerpt'] += 'altered'
    with pytest.raises(ValueError, match='hash'):
        review(before)


def test_missing_candidate_rejected():
    before = source()
    before['records'] = [r for r in before['records'] if r['r48_index'] != 133]
    with pytest.raises(ValueError):
        review(before)


def test_deterministic_and_no_input_mutation():
    before = source()
    copy_before = copy.deepcopy(before)
    assert review(before) == review(before)
    assert before == copy_before


def test_csv_multiline_count(tmp_path):
    result = review(source())
    write_reports(result, tmp_path)
    with (tmp_path / 'remaining_boundary_proposals.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 65
    assert any('\n' in row['excerpt'] for row in rows)
    assert len(json.loads((tmp_path / 'remaining_boundary_proposals.json').read_text(encoding='utf-8'))['proposals']) == 65
    assert (tmp_path / 'report.md').exists()
