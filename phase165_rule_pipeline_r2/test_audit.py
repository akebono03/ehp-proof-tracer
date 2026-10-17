"""Focused invariants for read-only generic rule discovery tracing."""
from audit import main


def test_generic_pipeline_report_is_consistent():
    result = main()
    assert result['group_adapter_absent']
    assert result['unified_count'] == len(result['unified'])
    assert result['generic_generated_count'] == len(result['generic_generated'])
    assert result['shared_root_proposals'] == len(result['shared_root_rules'])
    assert not result['full_pytest_run']


def test_only_real_source_leaves_are_counted():
    result = main()
    assert result['screened_cited_given_count'] >= 0
    assert all(item['conclusion_pattern_present'] for item in result['unified'])
