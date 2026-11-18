"""Strict R4R11 report, source and full-install gate contracts."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase175_r4r12_public_two_summand_quotient import audit


def prior_success_report() -> dict[str, object]:
    return {
        "phase": "175-R4R11",
        "dry_run": False,
        "gate": audit.PRIOR_GATE,
        "new_given": 0,
        "new_mathematical_rules": 1,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
        "preflight": {"head": "abf619040d52aa9fd61c5bca60db81e28912e24d"},
        "public": {
            "r4r10_signed_delta_route_present": True,
            "r4r11_exact_delta_route_present": True,
            "prior_eta7_order_two_route_present": True,
            "exact_database_generator_identity_reused": True,
            "three_proof_obligations_preserved": True,
            "group_conclusion_completed": False,
        },
        "install": {
            "production_path": "phase165_r52_r9_shared_math.py",
            "full_function_exported": True,
        },
    }


def test_prior_success_is_not_a_root_proof_certificate() -> None:
    result = audit.validate_prior(prior_success_report())
    assert result["r4r11_success_verified"]
    assert "pi95_completed" not in result


@pytest.mark.parametrize("field,value", (
    ("gate", "PASS_R4R11_SIGNED_ETA_TORSION_DRYRUN"),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 0),
    ("pi95_proof_complete", True),
    ("full_pytest_executed", True),
    ("prior_proof_search_executed", True),
))
def test_invalid_prior_gate_rejected(field: str, value: object) -> None:
    report = prior_success_report()
    report[field] = value
    with pytest.raises(RuntimeError, match="R4R12_PRIOR_GATE_OR_SCOPE_INVALID"):
        audit.validate_prior(report)


@pytest.mark.parametrize("field", (
    "r4r10_signed_delta_route_present",
    "r4r11_exact_delta_route_present",
    "prior_eta7_order_two_route_present",
    "exact_database_generator_identity_reused",
    "three_proof_obligations_preserved",
))
def test_no_missing_public_evidence_accepted(field: str) -> None:
    report = deepcopy(prior_success_report())
    report["public"][field] = False
    with pytest.raises(RuntimeError, match="R4R12_PRIOR_EVIDENCE_NOT_AUTHENTIC"):
        audit.validate_prior(report)


def test_wrong_prior_head_rejected() -> None:
    report = prior_success_report()
    report["preflight"]["head"] = "0" * 40
    with pytest.raises(RuntimeError, match="R4R12_PRIOR_EVIDENCE_NOT_AUTHENTIC"):
        audit.validate_prior(report)


def test_wrong_production_path_rejected() -> None:
    report = prior_success_report()
    report["install"]["production_path"] = "proof.py"
    with pytest.raises(RuntimeError, match="R4R12_PRIOR_EVIDENCE_NOT_AUTHENTIC"):
        audit.validate_prior(report)
