import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_16_existing_prose_audit import audit_existing_typed_prose
from proof import ProofRule, ProofStep


def _result():
    return make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.PARTIAL,
        proven_steps=(ProofStep(conclusion="unsupported sentinel", premises=(), rule=ProofRule.GIVEN),),
    )


def test_audit_does_not_mutate_proof_steps():
    result = _result()
    before = result.proven_steps
    audit_existing_typed_prose(result)
    assert result.proven_steps == before


def test_audit_reports_step_index():
    records = audit_existing_typed_prose(_result())
    assert all(record.step_index >= 0 for record in records)


def test_wrong_argument_rejected():
    with pytest.raises(TypeError, match="PartialProofResult"):
        audit_existing_typed_prose(object())


def test_audit_entries_are_immutable():
    records = audit_existing_typed_prose(_result())
    if records:
        with pytest.raises((AttributeError, TypeError)):
            records[0].source = "changed"
