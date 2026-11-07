"""Final report acceptance requires live R18, including unresolved public Delta."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase174_r3_r7_r18r2_local_evidence_recovery.audit import verify_public_report


def _report() -> dict:
    return {
        "phase": "174-R3-R7-R18",
        "gate": "PASS_ISOLATED_GENERIC_DELTA_IMAGE_SURJECTIVITY_FRONTIER",
        "new_group_given": 0,
        "new_math_rules_in_production": 0,
        "full_pytest_run": False,
        "completion_claimed": False,
        "prior_evidence": {
            "174-R3-R7-R17": "LIVE_PUBLIC_BOUNDARY_REVALIDATED_NO_LOCAL_REPORT",
            "174-R3-R7-R17R1": "CORRECTED_TEST_SOURCE_PINNED_NO_LOCAL_REPORT",
            "recovery": {
                "mode": "LIVE_REVALIDATED_NO_SYNTHETIC_REPORT",
                "missing_local_reports": ["phase174_r3_r7_r17/typed_map_public_audit.json"],
                "public_root_candidates": 1,
                "delta_surjectivity_candidates": 0,
                "verified_steps": 0,
                "corrected_historical_test_pinned_by_source_guard": True,
            },
        },
        "live": {
            "public_root_proposals": 1,
            "public_delta_surjectivity_proposals": 0,
            "isolated_delta_surjectivity_proposals": 1,
            "new_proof_steps_created": 0,
            "completion_claimed": False,
            "production_provider_changed": False,
            "search_status": "search_failed",
        },
    }


def test_live_revalidation_gate_accepts_unfinished_frontier() -> None:
    result = verify_public_report(_report())
    assert result["gate"] == "PASS_R18_LIVE_R17_BOUNDARY_REVALIDATED_NO_PRIOR_JSON_COPY"
    assert result["evidence_mode"] == "LIVE_RECOVERY"
    assert result["root_complete"] is False


def test_existing_valid_report_mode_is_distinguished() -> None:
    data = _report()
    del data["prior_evidence"]["recovery"]
    assert verify_public_report(data)["evidence_mode"] == "VALIDATED_LOCAL_REPORTS"


@pytest.mark.parametrize("path,value", (
    (("gate",), "UNVERIFIED"),
    (("new_group_given",), 1),
    (("new_math_rules_in_production",), 1),
    (("full_pytest_run",), True),
    (("completion_claimed",), True),
    (("live", "public_delta_surjectivity_proposals"), 1),
    (("live", "public_root_proposals"), 0),
    (("live", "isolated_delta_surjectivity_proposals"), 0),
    (("live", "new_proof_steps_created"), 1),
    (("live", "search_status"), "complete"),
    (("prior_evidence", "recovery", "verified_steps"), 1),
    (("prior_evidence", "recovery", "mode"), "SKIP_VALIDATION"),
))
def test_broken_post_report_is_rejected(path: tuple[str, ...], value: object) -> None:
    data = deepcopy(_report())
    node = data
    for field in path[:-1]:
        node = node[field]
    node[path[-1]] = value
    with pytest.raises(RuntimeError):
        verify_public_report(data)
