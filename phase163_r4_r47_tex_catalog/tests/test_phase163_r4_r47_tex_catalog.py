"""Focused, self-contained tests for the R4-R47 source catalog."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase163_r4_r47_tex_catalog import build_catalog, enforce_compatible, write_catalog


def fixtures():
    entry_a = {'chapter': 1, 'order': 1, 'kind': 'proposition', 'line': 7,
               'labels': ['prop:1-2'], 'tags': [], 'locator_candidate': 'Proposition 1.2',
               'tex': '\\begin{proposition}日本語 $a=b$\\end{proposition}', 'unclosed': False}
    entry_b = {'chapter': 1, 'order': 2, 'kind': 'equation', 'line': 9,
               'labels': [], 'tags': [], 'locator_candidate': None,
               'tex': '\\begin{equation}x=y\\end{equation}', 'unclosed': False}
    entry_c = {'chapter': 2, 'order': 1, 'kind': 'lemma', 'line': 5,
               'labels': ['lem:2.1'], 'tags': [], 'locator_candidate': 'Lemma 2.1',
               'tex': '\\begin{lemma}条件 $n>0$\\end{lemma}', 'unclosed': False}
    import hashlib
    def h(x):
        return hashlib.sha256(x.encode('utf-8')).hexdigest()
    chapters = [
        {'chapter': 1, 'source_file': 'one.tex', 'sha256': 'hash1', 'items': [entry_a, entry_b]},
        {'chapter': 2, 'source_file': 'two.tex', 'sha256': 'hash2', 'items': [entry_c]},
        {'chapter': 3, 'source_file': 'three.tex', 'sha256': 'hash3', 'items': []},
        {'chapter': 4, 'source_file': 'four.tex', 'sha256': 'hash4', 'items': []},
        {'chapter': 5, 'source_file': 'five.tex', 'sha256': 'hash5', 'items': []},
    ]
    extraction = {'phase': '163 R4-R42', 'registration_applied': False,
                  'missing_sources': [], 'item_count': 3, 'chapters': chapters}
    defs = [(entry_a, 'EXISTING_REFERENCE', 'toda:Proposition 1.2', None),
            (entry_b, 'UNNUMBERED_ENVIRONMENT', None, None),
            (entry_c, 'NEW_REFERENCE_CANDIDATE', None, 'toda:Lemma 2.1')]
    rows = []
    sources = []
    for item, status, existing, proposed in defs:
        row = {'chapter': item['chapter'], 'source_order': item['order'], 'kind': item['kind'],
               'source_line': item['line'], 'labels': item['labels'], 'tags': item['tags'],
               'locator_candidate': item['locator_candidate'], 'status': status,
               'existing_reference_id': existing, 'proposed_reference_id': proposed,
               'sha256_tex_body': h(item['tex'])}
        rows.append(row)
        sources.append({'chapter': item['chapter'], 'source_order': item['order'],
                        'kind': item['kind'], 'source_line': item['line'],
                        'sha256_tex_body': h(item['tex']), 'tex_body': item['tex'],
                        'mapping_status': status, 'existing_reference_id': existing})
    mapping = {'phase': '163 R4-R43', 'registration_applied': False, 'id_allocated': False,
               'source_sha256': {str(c['chapter']): c['sha256'] for c in chapters},
               'item_count': 3, 'duplicate_locator_candidates': {}, 'rows': rows}
    crosswalk = {'phase': '163 R4-R44', 'reference_units': sources,
                 'assertion_crosswalk': [{'assertion_id': 'boundary:Proposition 1.2:fact'}]}
    return extraction, mapping, crosswalk


def build():
    return build_catalog(*fixtures(), {'toda:Proposition 1.2'},
                         {'boundary:Proposition 1.2:fact'})


def test_registers_full_tex_and_chapter_order():
    result = build()
    assert [x['publication_position'] for x in result['items']] == [1, 2, 3]
    assert result['items'][0]['tex_body'].startswith('\\begin{proposition}日本語')
    assert all(x['TEX_REGISTERED'] and not x['STRUCTURED'] and not x['SOURCE_VERIFIED']
               for x in result['items'])


def test_existing_reference_and_assertion_ids_preserved():
    result = build()
    assert result['items'][0]['reference_id'] == 'toda:Proposition 1.2'
    assert result['existing_assertion_ids'] == ['boundary:Proposition 1.2:fact']
    assert result['production_registry_modified'] is False
    assert result['production_ids_allocated'] is False


def test_unnumbered_environment_gets_only_internal_identity():
    result = build()
    unnumbered = result['items'][1]
    assert unnumbered['locator'] is None
    assert unnumbered['reference_id'] is None
    assert unnumbered['reference_id_candidate'] is None
    assert unnumbered['source_unit_id'] == 'tex-unit:toda:ch01:0002'


def test_new_reference_candidate_not_claimed_as_registered():
    item = build()['items'][2]
    assert item['reference_id'] is None
    assert item['reference_id_candidate'] == 'toda:Lemma 2.1'


def test_wrong_hash_rejected():
    ext, mapping, crosswalk = fixtures()
    mapping['rows'][0]['sha256_tex_body'] = 'bad'
    with pytest.raises(ValueError, match='fingerprint'):
        build_catalog(ext, mapping, crosswalk, {'toda:Proposition 1.2'},
                      {'boundary:Proposition 1.2:fact'})


def test_unclosed_environment_rejected():
    ext, mapping, crosswalk = fixtures()
    ext['chapters'][0]['items'][0]['unclosed'] = True
    with pytest.raises(ValueError, match='unclosed'):
        build_catalog(ext, mapping, crosswalk, {'toda:Proposition 1.2'},
                      {'boundary:Proposition 1.2:fact'})


def test_changed_registry_snapshot_rejected():
    current = build()
    previous = copy.deepcopy(current)
    previous['existing_assertion_ids'].append('new')
    with pytest.raises(ValueError, match='Registry changed'):
        enforce_compatible(previous, current)


def test_changed_source_unit_rejected():
    current = build()
    previous = copy.deepcopy(current)
    previous['items'][0]['tex_body'] = 'altered'
    with pytest.raises(ValueError, match='source unit'):
        enforce_compatible(previous, current)


def test_repeatable_write_and_guard(tmp_path: Path):
    catalog = build()
    write_catalog(catalog, tmp_path)
    write_catalog(catalog, tmp_path)
    assert json.loads((tmp_path / 'catalog.json').read_text(encoding='utf-8')) == catalog
    assert len((tmp_path / 'catalog.csv').read_text(encoding='utf-8-sig').splitlines()) == 4
    modified = copy.deepcopy(catalog)
    modified['source_sha256']['1'] = 'changed'
    with pytest.raises(ValueError, match='source files changed'):
        write_catalog(modified, tmp_path)
