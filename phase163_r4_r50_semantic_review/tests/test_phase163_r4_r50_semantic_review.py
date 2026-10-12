import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r50_semantic_review import evaluate, write_report

ROOT = Path(__file__).resolve().parents[2]


def data():
    triage_path = ROOT / 'phase163_r4_r49_output' / 'triage.json'
    catalog_path = ROOT / 'phase163_r4_r47_output' / 'catalog.json'
    sources_path = ROOT / 'phase163_r4_r42_tex_extract' / 'inputs'
    return (
        json.loads(triage_path.read_text(encoding='utf-8')),
        json.loads(catalog_path.read_text(encoding='utf-8')),
        sources_path,
    )


def test_preserves_all_original_indices():
    result = evaluate(*data())
    assert len(result['review_queue']) == 316
    assert [r['r48_index'] for r in result['review_queue']] == list(range(1,317))


def test_prose_review_is_context_limited():
    result = evaluate(*data())
    rows = {r['r48_index']:r for r in result['review_queue']}
    assert rows[82]['role_decision'] == 'DEFINITION_CANDIDATE'
    assert rows[85]['role_decision'] == 'PROOF_LOCAL_CONSTRUCTION'
    assert rows[246]['role_decision'] == 'PROOF_LOCAL_CONSTRUCTION'


def test_display_prose_deduplication():
    rows = {r['r48_index']:r for r in evaluate(*data())['review_queue']}
    assert rows[72]['role_decision'] == 'DEFINITION_COMPONENT'
    assert rows[72]['paired_prose_index'] == 88


def test_unreviewed_displays_remain_pending():
    rows = {r['r48_index']:r for r in evaluate(*data())['review_queue']}
    assert rows[2]['role_decision'] == 'PENDING_MATHEMATICAL_REVIEW'


def test_lexical_exclusions_not_reclassified():
    result = evaluate(*data())
    assert result['role_counts']['LEXICALLY_EXCLUDED'] == 34


def test_read_only_state():
    result = evaluate(*data())
    assert result['registration_applied'] is False
    assert result['registry_modified'] is False
    assert result['ids_allocated'] is False
    assert result['distinct_new_statement_count_confirmed'] == 0


def test_changed_source_digest_fails():
    triage, catalog, sources = data()
    catalog['source_sha256']['1'] = 'invalid'
    with pytest.raises(ValueError):
        evaluate(triage, catalog, sources)


def test_missing_record_fails():
    triage, catalog, sources = data()
    triage['review_queue'].pop()
    with pytest.raises(ValueError):
        evaluate(triage, catalog, sources)


def test_deterministic_output_and_files(tmp_path):
    args = data()
    a, b = evaluate(*args), evaluate(*args)
    assert a == b
    write_report(a, tmp_path)
    assert (tmp_path/'review.json').exists()
    assert (tmp_path/'review_queue.csv').exists()
    assert '数学的' in (tmp_path/'report.md').read_text(encoding='utf-8')
