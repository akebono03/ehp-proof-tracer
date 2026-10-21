"""Phase 166 R3-AD focused generic transport invariants."""
from phase166_r3ad_stable_transport_audit.audit import audit_structural_transport


def test_generic_stable_transport_for_multiple_stems_and_exponents():
    cases = audit_structural_transport()
    assert len(cases) == 16
    assert all(case["inference_matches"] == 1 for case in cases)
    assert all(case["correct_target"] for case in cases)
    assert all(case["correct_generator"] for case in cases)
