import hashlib
import json
import re
from pathlib import Path

import pytest

from phase163_r4_r48_coverage_audit import audit, classify_chapter, clean_source, write_report


def fixture(raw: bytes):
    source = clean_source(raw.decode('utf-8'))
    m = source.index(r'\begin{proposition}')
    e = source.index(r'\end{proposition}') + len(r'\end{proposition}')
    return {'source_line': source.count('\n', 0, m) + 1,
            'kind': 'proposition', 'sha256_tex_body': hashlib.sha256(source[m:e].encode()).hexdigest()}


def test_comment_line_position_preserved():
    assert clean_source('a% comment\nb\\%c\n') == 'a\nb\\%c\n'


def test_outside_display_and_definition_cue():
    raw = ('\\begin{proposition}\n\\[x=y\\]\n\\end{proposition}\n'
           '\\[u=v\\]\n$A$ を定義する.\n').encode()
    rows, details = classify_chapter(1, raw, [fixture(raw)])
    assert details['registered_count'] == 1
    assert [row['category'] for row in rows] == ['OUTSIDE_DISPLAY', 'PROSE_DEFINITION_CUE']


def test_nested_equation_tracked_without_new_registration():
    raw = ('\\begin{proposition}\n\\begin{equation}a\\end{equation}\n'
           '\\end{proposition}\n').encode()
    # Only the parent is supplied for this unit test; unmatched nested equation must fail closed.
    with pytest.raises(ValueError, match='REGISTERED_COUNT_MISMATCH|UNMATCHED_ENVIRONMENT'):
        classify_chapter(1, raw, [fixture(raw)])


def test_hash_mismatch_fails_closed():
    raw = b'\\begin{proposition}x\\end{proposition}'
    entry = fixture(raw)
    entry['sha256_tex_body'] = '0' * 64
    with pytest.raises(ValueError, match='BODY_HASH_MISMATCH'):
        classify_chapter(1, raw, [entry])


def test_missing_catalog_unit_fails_closed():
    raw = b'\\begin{proposition}x\\end{proposition}'
    with pytest.raises(ValueError, match='UNMATCHED_ENVIRONMENT'):
        classify_chapter(1, raw, [])


def test_report_output(tmp_path):
    report = {'registered_count': 108, 'candidate_count': 1,
              'nested_registered_environment_count': 0,
              'chapters': [{'chapter': 1, 'registered_count': 2, 'nested_count': 0}],
              'candidate_counts': {'OUTSIDE_DISPLAY': 1},
              'candidates': [{'chapter': 1, 'source_line': 2, 'category': 'OUTSIDE_DISPLAY',
                              'reason': 'review', 'excerpt': 'x', 'review_status': 'UNREVIEWED'}]}
    write_report(report, tmp_path)
    assert json.loads((tmp_path / 'audit.json').read_text())['candidate_count'] == 1
    assert 'OUTSIDE_DISPLAY' in (tmp_path / 'candidates.csv').read_text(encoding='utf-8-sig')


def test_publication_order_rejects_changes(tmp_path):
    catalog = {'items': [{'publication_position': 3, 'TEX_REGISTERED': True}] * 108}
    with pytest.raises(ValueError, match='Publication positions'):
        audit(catalog, tmp_path)


def test_real_catalog(tmp_path):
    root = Path(__file__).resolve().parents[2]
    path = root / 'phase163_r4_r47_output' / 'catalog.json'
    inputs = root / 'phase163_r4_r42_tex_extract' / 'inputs'
    if not path.exists():
        path = root / 'phase163_r4_r47_validation_output' / 'catalog.json'
    if not path.exists() or not inputs.exists():
        pytest.skip('Real phase outputs are not available')
    result = audit(json.loads(path.read_text(encoding='utf-8')), inputs)
    assert result['registered_count'] == 108
    assert result['existing_reference_count'] == 23
    assert result['existing_assertion_count'] == 67


def test_nested_equation_registered_once_per_existing_environment():
    raw = ('\\begin{proposition}\n\\begin{equation}a\\end{equation}\n'
           '\\end{proposition}\n').encode()
    parent = fixture(raw)
    clean = clean_source(raw.decode())
    m = re.search(r'\\begin\{equation\}', clean)
    assert m is not None
    e = clean.index(r'\end{equation}', m.start()) + len(r'\end{equation}')
    child = {'source_line': 2, 'kind': 'equation',
             'sha256_tex_body': hashlib.sha256(clean[m.start():e].encode()).hexdigest()}
    rows, info = classify_chapter(1, raw, [parent, child])
    assert info['nested_count'] == 1
    assert not rows
