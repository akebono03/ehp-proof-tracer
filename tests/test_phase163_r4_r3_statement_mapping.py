import pytest

from phase163_r4_r3_statement_mapping import analyze, write_audit


BOUNDARY = '''
_FIXED_RULE_COMPONENT_KEYS = {"known rule": "a", "aggregate": None}
_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME = {"known rule": "Proposition 1", "aggregate": "Proposition 1"}
_FIXED_RULE_COMPONENT_KEYS.update({"missing": "nope"})
_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME.update({"missing": "Proposition 1"})
TodaFixedStatementComponent(reference_locator="Proposition 1", component_key="a", statement_role=Role.RELATION, order=1)
TodaFixedStatementComponent(reference_locator="Proposition 1", component_key="b", statement_role=Role.RELATION, order=None)
'''
RULES = '''
InferenceRule(name="known rule")
InferenceRule(name="not listed")
InferenceRule(name=make_name())
'''


def test_correspondence_and_unlinked_component():
    result = analyze(BOUNDARY, {'toda_rules.py': RULES})
    status = {r['rule_name']: r['status'] for r in result['mapping_rows']}
    assert status == {'aggregate': 'aggregate_or_no_component',
                      'known rule': 'candidate_mapped_metadata_only',
                      'missing': 'component_not_in_catalog'}
    assert len(result['unlinked_components']) == 1
    assert result['unlinked_components'][0]['key'] == 'b'


def test_dynamic_and_unlisted_rule_names_are_not_assumed_mapped():
    result = analyze(BOUNDARY, {'toda_rules.py': RULES})
    assert result['counts']['site_status'] == {
        'dynamic_name_unverified': 1, 'listed_in_boundary_mapping': 1,
        'not_listed_in_boundary_mapping': 1}


def test_missing_locator_remains_unresolved():
    result = analyze('_FIXED_RULE_COMPONENT_KEYS = {"r": "c"}', {})
    assert result['mapping_rows'][0]['status'] == 'locator_unresolved'


def test_duplicate_component_identity_rejected():
    source = '''
TodaFixedStatementComponent(reference_locator="P", component_key="k")
TodaFixedStatementComponent(reference_locator="P", component_key="k")
'''
    with pytest.raises(ValueError, match='duplicate boundary component'):
        analyze(source, {})


def test_output_contains_detail_csv_and_report(tmp_path):
    (tmp_path / 'toda_literature_statement_boundary.py').write_text(BOUNDARY, encoding='utf-8')
    (tmp_path / 'toda_rules.py').write_text(RULES, encoding='utf-8')
    summary = write_audit(tmp_path, tmp_path / 'out')
    assert summary['counts']['boundary_components'] == 2
    for name in ('report.md', 'summary.json', 'rule_mapping.csv',
                 'rule_sites.csv', 'unlinked_components.csv'):
        assert (tmp_path / 'out' / name).exists()


def test_absent_core_file_fails_explicitly(tmp_path):
    with pytest.raises(FileNotFoundError):
        write_audit(tmp_path, tmp_path / 'out')
