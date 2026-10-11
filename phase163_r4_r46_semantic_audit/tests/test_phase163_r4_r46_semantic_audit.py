import hashlib

import pytest

from phase163_r4_r46_semantic_audit import RULES, anchor_in_lines, audit, compact, write_results


def test_rule_catalog_covers_23_distinct_components():
    assert len(RULES) == 23
    assert len(set(RULES)) == 23


def test_tex_anchor_handles_line_breaks():
    lines = [r'\pi^{2}_{3}=\gen{\eta_2}', '  ', r'H(\eta_2)=\iota_3']
    assert anchor_in_lines(lines, RULES['pi3_2_group_relation'][1], 1, 3)['line_start'] == 1


def test_missing_anchor_is_not_silent_confirmation():
    assert anchor_in_lines(['\u03b1'], RULES['nu_prime_hopf_relation'][1], 1, 1) is None
    assert RULES['diagonal_suspension_isomorphism'][0] == 'NOT_LOCATED'


def test_bad_prior_review_is_rejected():
    with pytest.raises(ValueError, match='R4-R45'):
        audit({'phase': 'other'}, 'abc')


def test_source_hash_mismatch_is_rejected():
    with pytest.raises(ValueError, match='fingerprint mismatch'):
        audit({'phase': '163 R4-R45', 'mode': 'READ_ONLY_COMPONENT_EVIDENCE'}, 'abc', expected_sha256='invalid')


def test_compact_only_removes_whitespace():
    assert compact('\\pi ^ {n} \n = 0') == '\\pi^{n}=0'


def test_missing_assertion_is_rejected():
    packets = [dict(chapter=5, reference_id='toda:(5.1)', source_line=1,
                    tex_lines=[], assertions=[]) for _ in range(5)]
    with pytest.raises(ValueError, match='23 assertions'):
        audit({'phase': '163 R4-R45', 'mode': 'READ_ONLY_COMPONENT_EVIDENCE',
               'packets': packets}, 'x')


def test_write_results_does_not_require_registry(tmp_path):
    data = {'results': [{'reference_id': 'toda:(5.1)', 'assertion_id': 'a',
                         'component_position_existing': None, 'status': 'NOT_LOCATED',
                         'tex_witness': None, 'editorial_note': 'not found'}]}
    write_results(data, tmp_path)
    assert (tmp_path / 'audit.json').exists()
    assert 'NOT_LOCATED' in (tmp_path / 'report.md').read_text(encoding='utf-8')
