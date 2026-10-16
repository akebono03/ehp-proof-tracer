import json
from pathlib import Path
from audit import classify_candidate, run


def test_adapter_is_not_silently_approved():
    item = classify_candidate({'category': 'ACTIVE_GROUP_SPECIFIC_ADAPTER', 'file': 'sample.py', 'function': 'expand', 'line': 10, 'reachable_by_imports': True})
    assert item['disposition'] == 'REPLACE_WITH_GENERIC_RULE_BEFORE_REMOVAL'


def test_group_type_is_not_automatically_removed():
    item = classify_candidate({'category': 'GROUP_TYPE_BRANCH_REVIEW', 'file': 'sample.py', 'function': 'expand', 'line': 10})
    assert item['disposition'] == 'MANUAL_REVIEW_GROUP_TYPE_BRANCH'


def test_bounded_report(tmp_path):
    source = tmp_path / 'classification.json'
    source.write_text(json.dumps({'records': [
        {'category': 'NAMED_GROUP_BRANCH_REVIEW', 'file': 'x.py', 'function': 'expand', 'line': 1, 'conditions': [{'expression': 'pi43'}]},
        {'category': 'REACHABLE_COMMON_OR_UNCLASSIFIED', 'file': 'y.py', 'function': 'search', 'line': 2}
    ]}), encoding='utf-8')
    report = run(source, tmp_path / 'out')
    assert report['reviewed_candidates'] == 1
    assert (tmp_path / 'out' / 'triage.md').exists()
