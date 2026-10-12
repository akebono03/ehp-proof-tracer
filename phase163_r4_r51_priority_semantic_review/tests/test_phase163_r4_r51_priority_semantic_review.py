import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r51_priority_semantic_review import DECISIONS, review, write_results

ROOT = Path(__file__).resolve().parents[2]


def data():
    previous = json.loads((ROOT/'phase163_r4_r50_output'/'review.json').read_text(encoding='utf-8'))
    catalog = json.loads((ROOT/'phase163_r4_r47_output'/'catalog.json').read_text(encoding='utf-8'))
    sources = ROOT/'phase163_r4_r42_tex_extract'/'inputs'
    return previous, catalog, sources


def test_complete_queue_and_indices():
    result = review(*data())
    assert len(result['review_queue']) == 316
    assert [r['r48_index'] for r in result['review_queue']] == list(range(1,317))


def test_reviewed_chapter_three_stable_definitions():
    rows = {r['r48_index']:r for r in review(*data())['review_queue']}
    assert rows[238]['role_decision'] == 'DEFINITION_CANDIDATE'
    assert rows[239]['paired_prose_index'] == 238
    assert rows[243]['role_decision'] == 'DEFINITION_CANDIDATE'
    assert rows[245]['paired_prose_index'] == 243


def test_reviewed_chapter_five_generators():
    rows = {r['r48_index']:r for r in review(*data())['review_queue']}
    assert all(rows[i]['role_decision'] == 'DEFINITION_CANDIDATE' for i in (277,278,293))
    assert rows[315]['role_decision'] == 'PROOF_LOCAL_CONSTRUCTION'


def test_existing_r50_reviews_preserved():
    before, catalog, sources = data()
    after = review(before,catalog,sources)
    for old,new in zip(before['review_queue'],after['review_queue']):
        if old['r48_index'] not in DECISIONS:
            assert old == new


def test_count_only_newly_reviewed():
    result=review(*data())
    assert result['newly_context_reviewed_count'] == len(DECISIONS)
    assert result['pending_mathematical_review_count'] == 253-len(DECISIONS)


def test_read_only_states():
    result=review(*data())
    assert result['registration_applied'] is False
    assert result['registry_modified'] is False
    assert result['ids_allocated'] is False
    assert result['distinct_new_statement_count_confirmed'] == 0


def test_rejects_changed_source_digest():
    prev,cat,sources = data()
    cat['source_sha256']['3']='wrong'
    with pytest.raises(ValueError):
        review(prev,cat,sources)


def test_rejects_missing_index():
    prev,cat,sources = data()
    prev['review_queue'].pop()
    with pytest.raises(ValueError):
        review(prev,cat,sources)


def test_deterministic_results_and_output(tmp_path):
    args=data()
    a=review(*args)
    b=review(*args)
    assert a==b
    write_results(a,tmp_path)
    assert (tmp_path/'review.json').exists()
    assert (tmp_path/'review_queue.csv').exists()
    assert (tmp_path/'report.md').exists()
    assert json.loads((tmp_path/'review.json').read_text(encoding='utf-8')) == a
