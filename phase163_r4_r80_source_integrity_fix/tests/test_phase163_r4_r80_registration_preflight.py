import json
from pathlib import Path

import pytest

from phase163_r4_r80_source_integrity_fix.phase163_r4_r80_registration_preflight import ORDER, build_review, item_suffix, sha256, write_results

ROOT = Path(__file__).resolve().parents[2]


def load_data():
    source = json.loads((ROOT / 'phase163_r4_r79_output' / 'fixed_statement_preview.json').read_text(encoding='utf-8'))
    source_root = ROOT / 'phase163_r4_r42_tex_extract' / 'inputs'
    return source, source_root


def test_four_references_and_eight_fixed_candidates():
    source, folder = load_data()
    result = build_review(source, folder)
    assert result['reference_candidate_count'] == 4
    assert result['fixed_statement_candidate_count'] == 8


def test_per_reference_component_order():
    source, folder = load_data()
    result = build_review(source, folder)
    for owner, suffixes in ORDER.items():
        rows = [r for r in result['records'] if r['owner'] == owner]
        assert [r['component_position'] for r in rows] == list(range(1, len(suffixes) + 1))
        assert [r['proposed_assertion_key'].split(':')[-1] for r in rows] == suffixes


def test_all_provenance_hashes_verified_against_source():
    source, folder = load_data()
    result = build_review(source, folder)
    assert result['component_position_valid_count'] == 8
    assert all(len(r['source_claim_sha256']) == 64 for r in result['records'])


def test_shared_conditions_retained_in_review():
    source, folder = load_data()
    result = build_review(source, folder)
    assert result['scope_notes_present_count'] == 8
    assert all(r['shared_scope_note'] for r in result['records'])


def test_complex_claims_remain_flagged():
    source, folder = load_data()
    result = build_review(source, folder)
    flagged = {r['proposed_assertion_key'] for r in result['records'] if r['boundary_issues']}
    assert 'proposal:thm:2.4:even_dimension_case' in flagged
    assert 'proposal:prop:4.2:ehp_exact_sequence' in flagged
    assert 'proposal:prop:1-6:first_argument_additivity' in flagged


def test_no_formal_registration_is_implied():
    source, folder = load_data()
    result = build_review(source, folder)
    assert result['semantic_registration_allowed_count'] == 0
    assert not result['production_ids_allocated']
    assert result['duplicate_status'] == 'UNRESOLVED'
    assert all(not r['registration_allowed'] for r in result['records'])


def test_source_perturbation_rejected(tmp_path):
    source, folder = load_data()
    filenames = {entry['source_file'] for entry in source['fixed_statement_previews']}
    for filename in filenames:
        (tmp_path / filename).write_text((folder / filename).read_text(encoding='utf-8'), encoding='utf-8')
    file = tmp_path / 'Toda_01_corrected.tex'
    file.write_text(file.read_text(encoding='utf-8').replace('\\{\\alpha,\\Ex^n\\beta,\\Ex^n\\gamma\\}_n', 'TAMPERED', 1), encoding='utf-8')
    with pytest.raises(AssertionError):
        build_review(source, tmp_path)


def test_source_perturbation_outside_claim_rejected(tmp_path):
    source, folder = load_data()
    filenames = {entry['source_file'] for entry in source['fixed_statement_previews']}
    for filename in filenames:
        (tmp_path / filename).write_bytes((folder / filename).read_bytes())
    path = tmp_path / 'Toda_04_2(2).tex'
    path.write_bytes(b'TAMPERED' + path.read_bytes())
    with pytest.raises(AssertionError, match='changed TeX source file'):
        build_review(source, tmp_path)


def test_write_report(tmp_path):
    source, folder = load_data()
    result = build_review(source, folder)
    write_results(result, tmp_path)
    assert (tmp_path / 'registration_preflight.json').exists()
    assert '登録前の未解決問題' in (tmp_path / 'report.md').read_text(encoding='utf-8')
