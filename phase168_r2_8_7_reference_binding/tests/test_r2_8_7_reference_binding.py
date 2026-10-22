from pathlib import Path

from phase168_r2_8_7_reference_binding.patch import prepared_changes


def test_guarded_changes_syntactically_valid():
    changes = prepared_changes()
    assert len(changes) == 2
    assert all(original != updated for _, original, updated in changes)


def test_metadata_preserves_published_locator():
    changes = prepared_changes()
    gate = changes[0][2]
    assert 'locator=locator,' in gate
    assert 'registered_reference_step(assertion, original_links[0].step)' in gate
    assert 'precedes_citing_assertion(' in gate


def test_transport_rule_has_specific_citation():
    changes = prepared_changes()
    transport = changes[1][2]
    assert 'label="Toda (5.2)", locator="(5.2)"' in transport
    assert 'isinstance(theorem, Toda52UniversalStatement)' in transport
