import pytest

from phase178_r27_stable_boundary_source_first_audit.audit import classify


def test_audited_partial_is_not_completed():
    assert classify('partial', False, 2, 0, 'generic-partial-proof', False) == 'PASS_R27_STABLE_BOUNDARY_AUDIT_OPEN'


def test_verified_complete_is_distinct():
    assert classify('complete', True, 0, 0, 'generic-complete-proof', True) == 'PASS_R27_STABLE_BOUNDARY_VERIFIED_COMPLETE'


@pytest.mark.parametrize('args', [
    ('complete', False, 0, 0, 'generic-complete-proof', True),
    ('complete', True, 1, 0, 'generic-complete-proof', True),
    ('complete', True, 0, 1, 'generic-complete-proof', True),
    ('complete', True, 0, 0, 'generic-complete-proof', False),
    ('complete', True, 0, 0, 'generic-partial-proof', True),
    ('partial', False, 2, 1, 'generic-partial-proof', False),
    ('partial', False, 2, 0, 'generic-complete-proof', False),
    ('partial', True, 2, 0, 'generic-partial-proof', False),
])
def test_invalid_proof_contract_fails_closed(args):
    with pytest.raises(RuntimeError):
        classify(*args)
