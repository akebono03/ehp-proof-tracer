"""Unit tests for read-only audit helpers; no production repository dependency."""
import sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit import brief, safe_call, summary


def test_brief_preserves_rules_and_subgoals():
    x = SimpleNamespace(rule=SimpleNamespace(name='rule A'), subgoals=('a', 'b'))
    assert brief((x,)) == [{'rule': 'rule A', 'subgoals': ["'a'", "'b'"]}]


def test_safe_call_counts_candidates():
    records = {}
    assert len(safe_call('provider', lambda: (SimpleNamespace(rule=SimpleNamespace(name='A'),subgoals=()),), records)) == 1
    assert records['provider']['count'] == 1


def test_safe_call_fails_closed():
    records = {}
    assert safe_call('broken', lambda: [], records) == ()
    assert records['broken']['status'] == 'ERROR'


def test_safe_call_keeps_exception_details():
    records = {}
    def fail():
        raise ValueError('budget exceeded')
    assert safe_call('broken', fail, records) == ()
    assert records['broken']['message'] == 'budget exceeded'


def test_summary_has_distinct_contexts():
    record = {'status':'PROVIDER_PATHS_AUDITED','goals_found':1,'contexts':{'FULL':{'rule_count':60,'cited_witness_count':17,'paths':{'R26_GENERIC':{'status':'OK','count':7}},'specialization_presence':{}}}}
    result = summary(record)
    assert result['contexts']['FULL']['counts']['R26_GENERIC'] == 7
    assert result['full_pytest_run'] is False
