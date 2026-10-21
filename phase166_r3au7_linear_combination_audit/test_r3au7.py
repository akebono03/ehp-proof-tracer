from phase166_r3au7_linear_combination_audit.audit import inspect


def test_r3au7_positions_join_group_ids_not_Element_ids():
    rows = [
        {'n': '4', 'k': '3', 'id': '0', 'Element': '8 9', 'gen_coe': '1 1 0', 'generator': ''},
        {'n': '4', 'k': '3', 'id': '1', 'Element': '10', 'gen_coe': '0 1 0'},
    ]
    summary, details = inspect(rows)
    assert summary['multi_nonzero_rows'] == 1
    assert details[0]['all_component_ids_present'] is True
    assert '"target_Element": "10"' in details[0]['coefficient_terms_by_id']


def test_r3au7_missing_group_component_is_visible():
    summary, details = inspect([{'n': '4', 'k': '3', 'id': '0', 'Element': '8', 'gen_coe': '1 -2 0'}])
    assert summary['component_lookup_status']['MISSING_COMPONENT_ID'] == 1
    assert details[0]['all_component_ids_present'] is False


def test_r3au7_zero_vectors_are_excluded_and_reference_optional():
    summary, details = inspect([{'n': '2', 'k': '1', 'id': '0', 'Element': '0', 'gen_coe': '0 0 0', 'generator': ''}])
    assert details == []
    assert summary['reference_generator_optional'] is True
    assert summary['full_pytest_run'] is False
