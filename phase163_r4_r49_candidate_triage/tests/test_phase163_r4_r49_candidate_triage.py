import copy
import hashlib
import json
from pathlib import Path

import pytest

from phase163_r4_r49_candidate_triage import parse_displays, strip_comments, triage, save_report


ROOT = Path.cwd()
AUDIT = ROOT / 'phase163_r4_r48_output' / 'audit.json'
CATALOG = ROOT / 'phase163_r4_r47_output' / 'catalog.json'
INPUTS = ROOT / 'phase163_r4_r42_tex_extract' / 'inputs'
if not AUDIT.exists():
    ROOT = Path(__file__).resolve().parents[2]
    AUDIT = ROOT / 'audit(3).json'
    CATALOG = ROOT / 'catalog.json'
    INPUTS = ROOT / 'phase163_r4_r42_tex_extract' / 'inputs'


def fixture_inputs(tmp_path):
    text = r'\[x=1\]' + '\n' + r'\begin{align*}y=2\end{align*}' + '\n'
    raw = text.encode()
    (tmp_path / 'Toda_01_corrected.tex').write_bytes(raw)
    return text


def test_comments_preserve_line_numbers():
    assert strip_comments('x% comment\ny\\%escaped\n') == 'x\ny\\%escaped\n'


def test_spacing_newline_is_not_display():
    text = r'\\[2mm]' + '\n' + r'\[x\]' + '\n'
    assert len([s for s in parse_displays(text) if s['token'] == 'bracket']) == 1


def test_nested_align_is_visible_to_deduplicator():
    text = r'\[\begin{align*}x&=1\end{align*}\]'
    spans = parse_displays(text)
    assert len(spans) == 2
    assert spans[0]['start'] < spans[1]['start'] < spans[1]['end'] < spans[0]['end']


def test_fingerprint_consistent():
    text = r'\[x=1\]'
    assert parse_displays(text) == parse_displays(text)


def test_actual_data_counts():
    audit = json.loads(AUDIT.read_text(encoding='utf-8'))
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    result = triage(audit, catalog, INPUTS)
    assert result['original_candidate_count'] == 316
    assert result['registered_source_count'] == 108
    assert sum(result['status_counts'].values()) == 316
    assert result['status_counts']['DEFINITION_CUE_REVIEW_REQUIRED'] == 20
    assert result['status_counts']['LEXICAL_FALSE_POSITIVE'] == 18
    assert result['status_counts']['NESTED_DISPLAY_FRAGMENT'] == 16
    assert result['status_counts']['DISPLAY_REVIEW_REQUIRED'] == 262
    assert len({x['r48_index'] for x in result['review_queue']}) == 316


def test_original_audit_unchanged():
    audit = json.loads(AUDIT.read_text(encoding='utf-8'))
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    before = json.dumps((audit, catalog), sort_keys=True, ensure_ascii=False)
    triage(audit, catalog, INPUTS)
    assert json.dumps((audit, catalog), sort_keys=True, ensure_ascii=False) == before


def test_catalog_mismatch_fails():
    audit = json.loads(AUDIT.read_text(encoding='utf-8'))
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    changed = copy.deepcopy(catalog)
    changed['source_sha256']['1'] = '0' * 64
    with pytest.raises(ValueError, match='checksums differ'):
        triage(audit, changed, INPUTS)


def test_stable_replay():
    audit = json.loads(AUDIT.read_text(encoding='utf-8'))
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    first = triage(audit, catalog, INPUTS)
    second = triage(audit, catalog, INPUTS)
    assert first == second
    assert first['new_statement_count_confirmed'] == 0
    assert not first['registration_applied']


def test_outputs_are_read_only_reports(tmp_path):
    data = {'phase': '163 R4-R49', 'original_candidate_count': 1,
            'distinct_display_review_count': 1, 'definition_cue_review_count': 0,
            'status_counts': {'DISPLAY_REVIEW_REQUIRED': 1},
            'review_queue': [dict(r48_index=1, chapter=1, source_line=3,
                                  original_category='OUTSIDE_DISPLAY',
                                  triage_status='DISPLAY_REVIEW_REQUIRED',
                                  review_group_id='tex-display:ch01:line00003',
                                  group_primary_r48_index=1, reason='test',
                                  excerpt=r'\[x\]', context='3: x', review_decision='UNREVIEWED')]}
    save_report(data, tmp_path)
    assert (tmp_path / 'triage.json').is_file()
    assert (tmp_path / 'review_queue.csv').is_file()
    assert (tmp_path / 'report.md').is_file()
