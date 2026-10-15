"""Isolated tests for Phase 165 R5-R5 source analysis."""
from audit import definition_call_sites, reference_sites


def test_from_import_and_aliased_call():
    source = 'from shared_module import render_part as helper\ndef run():\n    return helper()\n'
    rows = reference_sites(source, 'sample.py', {'shared_module'})
    assert any(row['kind'] == 'import_from' and row['function'] == 'render_part' for row in rows)
    assert any(row['kind'] == 'call' and row['function'] == 'render_part' and row['line'] == 3 for row in rows)


def test_module_import_and_attribute_call():
    source = 'import shared_module as sm\ndef run():\n    return sm.render_part()\n'
    rows = reference_sites(source, 'sample.py', {'shared_module'})
    assert any(row['kind'] == 'call' and row['target'] == 'shared_module' and row['function'] == 'render_part' for row in rows)


def test_unrelated_calls_are_not_recorded():
    source = 'from unrelated import render_part\ndef run():\n    return render_part()\n'
    assert reference_sites(source, 'sample.py', {'shared_module'}) == []


def test_same_module_call_site():
    source = 'def render_part():\n    return "yes"\ndef execute():\n    return render_part()\n'
    assert definition_call_sites(source, 'sample.py', {'render_part'}) == {'render_part': [4]}


def test_does_not_count_reference_without_call():
    source = 'from shared_module import render_part\ndef execute():\n    return render_part\n'
    rows = reference_sites(source, 'sample.py', {'shared_module'})
    assert not any(row['kind'] == 'call' for row in rows)
