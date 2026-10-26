"""Read-only tests for the cited higher-eta codomain and current proof boundary."""
from __future__ import annotations

import pytest

from phase169_r3v_hopf_codomain_audit.audit import examine


@pytest.fixture(scope="module")
def audit_report():
    return examine()


def test_pi53_proof_stays_complete(audit_report):
    assert audit_report["pi53_proof_status"] == "complete"
    assert audit_report["production_files_modified"] is False
    assert audit_report["full_pytest_run"] is False


def test_screened_prop51_higher_eta_source_matches_hopf_target(audit_report):
    assert audit_report["screened_generic_source_count"] >= 1
    assert audit_report["unique_generic_source_contents"] >= 1
    assert audit_report["eta_generator_matches_h_image"] is True
    assert all(record["is_prior"] for record in audit_report["generic_source_records"])


def test_current_hopf_terminal_has_not_yet_attached_pi65(audit_report):
    assert audit_report["hopf_current_subgoals"] == [
        "Relation", "TodaProp51FiniteDimensionalStatement"
    ]
    assert audit_report["hopf_has_concrete_pi65_premise"] is False
