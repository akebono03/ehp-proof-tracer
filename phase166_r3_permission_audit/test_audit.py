"""Targeted tests for Phase 166 R3 audit, no changes to production code."""
from phase166_r3_permission_audit.audit import TARGETS, inspect, inspect_lookup_modes


def test_expected_assertions_are_tracked():
    assert len(TARGETS) == 4
    assert len(set(TARGETS)) == 4


def test_metadata_never_receives_proof_permission():
    result = inspect()
    assert result['proof_permission_granted'] == 0
    assert all(not row['grant_allowed'] for row in result['target_records'])
    assert all(row['migration_statuses'] == ['metadata_only'] for row in result['target_records'])


def test_explicit_verified_id_does_not_approve_metadata():
    result = inspect()
    assert not result['citation_checks']['no_review']['usable']
    assert not result['citation_checks']['id_supplied_not_certification']['usable']


def test_lookup_modes_are_not_silently_considered_equivalent():
    modes = inspect_lookup_modes()
    assert modes['legacy_uses_eligibility_lookup']
    assert modes['typed_reference_uses_direct_lookup']
    assert modes['review_required_for_all_modes'] is False
