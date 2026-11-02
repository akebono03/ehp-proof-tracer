"""Small focused tests for the Phase 173 R4-R1 report reader."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase173_r4_r1_frontier_readout.readout import summarize_report, validate_report


def valid_data() -> dict:
    return {
        "phase": "173-R4-R1", "scope": "AUDIT_ONLY",
        "status": "OBSERVATION_ONLY_NOT_A_PROOF", "production_changes": [],
        "preflight": {
            "head": "f9fdaf350ff4de3f6a6f9b3cd6d6901f5b439941",
            "reviewed_source_files_unchanged": True,
            "toda": {
                "specialization_i": 7,
                "specialized_source_groups": ["pi_6^3", "pi_7^7"],
            },
            "existing_rule_inventory": [{
                "function": "rule_a", "defined_exactly_once": True,
                "mentions_premise_pattern": True,
                "mentions_literature_reference": True,
                "mentions_direct_sum": True,
            }],
            "worktree_exceptions": [], "committed_cache_exception": [],
        },
        "public_root": {
            "goal": "pi_7^4", "root_candidate_count": 1,
            "root_proposals": [{
                "rule": "equality symmetry",
                "children": [{
                    "type": "Relation", "repr": "pi_7^4",
                    "exact_screened_given": False,
                    "immediate_child_rule_names": ["equality symmetry"],
                }],
            }],
            "target_is_screened_given": False,
            "discovered_complete_proof": False,
            "prior_pi63": {"eligible": True, "reason": "prior_fixed_source",
                           "source_assertion_id": "earlier", "proven_in_this_audit": False},
            "pi77_db_goal_count": 1, "pi77_proven_in_this_audit": False,
            "prop44_cited_universal_given_count": 1,
            "toda56_decomposition_direct_given_count": 0,
            "screened_given_count": 26,
        },
    }


def test_valid_report_accepted() -> None:
    assert validate_report(valid_data())["phase"] == "173-R4-R1"


def test_readout_reports_frontier_without_certifying_proof() -> None:
    text = summarize_report(valid_data())
    assert "ROOT_1_RULE=equality symmetry" in text
    assert "PRIOR_PI63_ELIGIBLE=True" in text
    assert "COMPLETE_PROOF_CERTIFIED=False" in text
    assert "RULE_1: name=rule_a" in text


@pytest.mark.parametrize("section,value", [
    ("status", "PROVEN"),
    ("scope", "IMPLEMENTATION"),
    ("production_changes", ["toda_rules.py"]),
    ("public_root", "SKIPPED_DRY_RUN"),
])
def test_rejects_untrusted_report_sections(section: str, value: object) -> None:
    data = valid_data()
    data[section] = value
    with pytest.raises(ValueError):
        validate_report(data)


def test_rejects_missing_source_guard() -> None:
    data = valid_data()
    data["preflight"]["reviewed_source_files_unchanged"] = False
    with pytest.raises(ValueError):
        validate_report(data)


def test_rejects_promoted_goal() -> None:
    data = valid_data()
    data["public_root"]["target_is_screened_given"] = True
    with pytest.raises(ValueError):
        validate_report(data)


def test_rejects_mismatched_root_count() -> None:
    data = valid_data()
    data["public_root"]["root_candidate_count"] = 2
    with pytest.raises(ValueError):
        validate_report(data)


def test_rejects_wrong_toda_specialization() -> None:
    data = valid_data()
    data["preflight"]["toda"]["specialization_i"] = 8
    with pytest.raises(ValueError):
        validate_report(data)


def test_json_roundtrip(tmp_path: Path) -> None:
    target = tmp_path / "audit.json"
    target.write_text(json.dumps(valid_data()), encoding="utf-8")
    assert "DIRECT_TODA56_GIVEN=0" in summarize_report(
        json.loads(target.read_text(encoding="utf-8"))
    )
