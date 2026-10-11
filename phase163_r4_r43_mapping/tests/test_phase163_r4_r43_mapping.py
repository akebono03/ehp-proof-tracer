from pathlib import Path

import pytest

from phase163_r4_r43_mapping import build_mapping, check_sources, classify, write_output


def item(order, locator, labels=None, kind='equation'):
    return {'chapter': 1, 'order': order, 'kind': kind, 'line': order + 1,
            'labels': labels or [], 'tags': [], 'locator_candidate': locator,
            'tex': f'\\begin{{{kind}}}{order}\\end{{{kind}}}'}


def extraction(*items):
    return {'phase': '163 R4-R42', 'mode': 'READ_ONLY_EXTRACTION',
            'missing_sources': [], 'item_count': len(items),
            'chapters': [{'chapter': 1, 'source_file': 'a.tex', 'sha256': 'x', 'items': list(items)}]}


def test_matching_reuses_existing_reference_without_allocation():
    report = build_mapping(extraction(item(1, 'Proposition 1.2', ['prop:1-2'], 'proposition')),
                           {'toda:Proposition 1.2', 'toda:(5.3)'})
    assert report['matched_existing_reference_count'] == 1
    assert report['rows'][0]['existing_reference_id'] == 'toda:Proposition 1.2'
    assert report['unmatched_existing_reference_ids'] == ['toda:(5.3)']
    assert report['registration_applied'] is False
    assert report['id_allocated'] is False


def test_symbolic_and_unnumbered_do_not_get_invented_ids():
    report = build_mapping(extraction(item(1, None, ['eq:H-def']), item(2, None)), set())
    assert [row['status'] for row in report['rows']] == [
        'UNRESOLVED_SYMBOLIC_LABEL', 'UNNUMBERED_ENVIRONMENT']
    assert all(row['proposed_reference_id'] is None for row in report['rows'])


def test_new_numbered_candidate_and_duplicate_detection():
    report = build_mapping(extraction(item(1, '(1.1)'), item(2, '(1.1)')), set())
    assert report['status_counts'] == {'NEW_REFERENCE_CANDIDATE': 2}
    assert report['duplicate_locator_candidates'] == {'(1.1)': [(1, 2), (1, 3)]}


def test_mismatched_extraction_is_rejected():
    source = extraction(item(1, '(1.1)'))
    source['item_count'] = 2
    with pytest.raises(ValueError, match='item_count'):
        build_mapping(source, set())


def test_source_hash_guards_against_changed_tex(tmp_path: Path):
    source = tmp_path / 'a.tex'
    source.write_bytes(b'abc')
    record = extraction(item(1, '(1.1)'))
    with pytest.raises(ValueError, match='changed TeX'):
        check_sources(record, tmp_path)


def test_output_is_reviewable_without_mutation(tmp_path: Path):
    report = build_mapping(extraction(item(1, None)), set())
    write_output(report, tmp_path)
    assert (tmp_path / 'mapping.json').exists()
    assert 'UNNUMBERED_ENVIRONMENT' in (tmp_path / 'report.md').read_text(encoding='utf-8')
    assert (tmp_path / 'mapping.csv').exists()
