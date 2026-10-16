import ast
from audit import inspect, TARGETS

def test_all_targets_classified():
    assert len(TARGETS) == 6
    assert all(isinstance(item,list) for item in inspect()['usages'].values())

def test_audit_never_modifies_production():
    result = inspect()
    assert result['production_modified'] is False
    assert result['full_pytest_run'] is False

def test_all_reported_locations_have_line_numbers():
    result = inspect()
    assert all(item['line'] > 0 for items in result['usages'].values() for item in items)
