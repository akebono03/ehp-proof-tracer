from phase165_rule_registry_r9.audit import factory_inventory, main


def test_factory_identifiers_are_unique():
    factories = factory_inventory()
    identifiers = [row['rule_id_candidate'] for row in factories]
    assert len(identifiers) == len(set(identifiers))


def test_audit_does_not_invoke_retired_catalog():
    result = main()
    assert result['catalog_retired_not_invoked'] is True
    assert result['full_pytest_run'] is False
    assert len(result['rules']) == result['discovered_count']
