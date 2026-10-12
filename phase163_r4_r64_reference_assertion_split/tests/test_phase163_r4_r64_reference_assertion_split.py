import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r64_reference_assertion_split import load_source, make_proposals, write_reports


@pytest.fixture
def source_data():
    root = Path(__file__).resolve().parents[2]
    return load_source(root / 'phase163_r4_r63_output' / 'source_boundaries.json')


def test_counts_and_archival_only(source_data):
    result = make_proposals(source_data)
    assert result['reference_proposal_count'] == 16
    assert result['assertion_proposal_count'] == 21
    assert result['semantic_registration_allowed_count'] == 0
    assert result['production_ids_allocated'] is False


def test_two_assertions_at_five_locations(source_data):
    result = make_proposals(source_data)
    multiple = {r['editorial_key'] for r in result['records'] if len(r['assertions']) == 2}
    assert multiple == {'addition_inverse_suspension', 'stable_homotopy_group', 'nu_n_notation', 'eta_n_cubed_notation', 'nu_n_squared_notation'}


def test_external_context_and_adjacent_groups(source_data):
    result = make_proposals(source_data)
    assert result['external_context_review_count'] == 5
    assert result['shared_adjacent_notation_count'] == 2


def test_component_order_independent_of_publication(source_data):
    result = make_proposals(source_data)
    for record in result['records']:
        assert record['publication_position'] is None
        assert [a['component_position_proposal'] for a in record['assertions']] == list(range(1, len(record['assertions']) + 1))


def test_duplicate_editorial_identity_rejected(source_data):
    broken = copy.deepcopy(source_data)
    broken['records'][1]['editorial_key'] = broken['records'][0]['editorial_key']
    with pytest.raises(ValueError, match='Candidate identities'):
        make_proposals(broken)


def test_missing_source_marker_rejected(source_data):
    broken = copy.deepcopy(source_data)
    target = next(r for r in broken['records'] if r['editorial_key'] == 'nu_n_squared_notation')
    target['source_span_text'] = target['source_span_text'].replace(r'\nu^2:=', 'removed-marker')
    with pytest.raises(ValueError, match='Source marker absent'):
        make_proposals(broken)


def test_no_production_ids_accepted(source_data):
    broken = copy.deepcopy(source_data)
    broken['records'][0]['production_reference_id'] = 'toda:made-up'
    with pytest.raises(ValueError, match='production ID'):
        make_proposals(broken)


def test_false_semantic_approval_rejected(source_data):
    broken = copy.deepcopy(source_data)
    broken['records'][0]['semantic_registration_allowed'] = True
    with pytest.raises(ValueError, match='Semantic registration boundary'):
        make_proposals(broken)


def test_input_phase_and_count_rejected(source_data):
    broken = copy.deepcopy(source_data)
    broken['phase'] = '163 R4-R62'
    with pytest.raises(ValueError, match='R4-R63 input'):
        # Test the same input gate without editing the real input.
        path = Path(__file__).resolve().parents[2] / 'phase163_r4_r63_output' / 'source_boundaries.json'
        assert path.is_file()
        from phase163_r4_r64_reference_assertion_split import load_source as original_loader
        from unittest.mock import patch
        with patch.object(Path, 'read_text', return_value=json.dumps(broken)):
            original_loader(path)


def test_report_generation(source_data, tmp_path):
    result = make_proposals(source_data)
    write_reports(result, tmp_path)
    assert json.loads((tmp_path / 'split_proposals.json').read_text(encoding='utf-8'))['assertion_proposal_count'] == 21
    assert len((tmp_path / 'split_proposals.csv').read_text(encoding='utf-8-sig').splitlines()) == 22
    assert '正式' in (tmp_path / 'report.md').read_text(encoding='utf-8')
