from pathlib import Path
from phase165_r14_r37_closure import audit_r37, registry_leaf_audit, strict_search_attempt

TEX = Path(__file__).with_name("toda_51_complete.tex")


def test_all_nine_typed_goals_join_to_adopted_sources():
    assert len(registry_leaf_audit(TEX)) == 9


def test_unverified_source_is_not_promoted():
    rows = registry_leaf_audit(TEX)
    assert all(not row["strict_eligible"] for row in rows)


def test_exact_prop51_id_remains_unresolved():
    rows = registry_leaf_audit(TEX)
    assert sum(row["blocker"] == "EXACT_SOURCE_ID_UNRESOLVED" for row in rows) == 1


def test_strict_search_is_invoked_and_fails_closed():
    proved, reason = strict_search_attempt()
    assert not proved
    assert "expected one registered derivation" in reason


def test_adopted_proof_survives_strict_failure():
    result = audit_r37(TEX)
    assert result["adopted_backward_proof_created"]
    assert not result["strict_registry_proof_created"]


def test_phase_not_falsely_closed():
    result = audit_r37(TEX)
    assert not result["phase165_closed"]
    assert result["registry_assertions_promoted"] == 0
    assert result["full_pytest_run"] is False
