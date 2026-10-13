from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r14_r10_premise_audit import audit_pi32_premises, audit_summary


def test_exactly_four_pi32_obligations():
    rows = audit_pi32_premises()
    assert tuple(r.label for r in rows) == (
        "pi2_1_zero", "ehp_e_h_exactness",
        "delta_zero", "ehp_h_delta_exactness",
    )


def test_zero_group_scope_and_source_token():
    rows = audit_pi32_premises()
    assert rows[0].statement == TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(2,1))
    assert rows[0].expected_reference == "(5.1)"
    assert rows[0].source_text_found is True


def test_delta_is_not_deduced_from_pi11_cyclicity():
    row = audit_pi32_premises()[2]
    assert row.expected_reference == "UNRESOLVED"
    assert "NOT implied" in row.reason
    assert row.proof_eligible is False


def test_no_unverified_proof_promotion():
    rows = audit_pi32_premises()
    assert all(r.proof_eligible is False for r in rows)
    report = audit_summary()
    assert report["proof_steps_created"] == 0
    assert report["certified_new_leaves"] == 0
    assert report["legacy_proof_used"] is False


def test_exactness_windows_remain_two_separate_obligations():
    rows = audit_pi32_premises()
    assert rows[1].statement.window != rows[3].statement.window
