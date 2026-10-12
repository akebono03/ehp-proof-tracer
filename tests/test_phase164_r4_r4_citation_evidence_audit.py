"""R4-R4 focused evidence validation; no eligibility promotion."""
from copy import deepcopy
import json
from pathlib import Path

import pytest

from phase164_r4_r4_citation_evidence_audit import (
    REQUIRED_EVIDENCE,
    assess_citation_evidence,
    audit_current,
    write_report,
)
from phase164_r4_r1_source_crosswalk import source_crosswalk
from phase164_r4_r3_independent_semantic_audit import assess_typed_clauses
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def inputs():
    manifest = json.loads((ROOT / "phase163_r4_r94_output" / "manifest.json").read_text(encoding="utf-8"))
    leaves = tuple(
        step for step in build_phase59_3_data()["premise_steps"]
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    crosswalk = source_crosswalk(manifest, leaves)
    return crosswalk, assess_typed_clauses(crosswalk, leaves)


def test_two_references_remain_blocked(inputs):
    report = assess_citation_evidence(*inputs)
    assert report["source_locator_candidates"] == 2
    assert report["typed_checks_passed"] == 5
    assert report["evidence_authenticated_count"] == 0
    assert [r["source_statement_id"] for r in report["leaves"]] == ["toda:tex:ch5:0002", "toda:tex:ch5:0005"]
    assert all(r["reference_available_after_position"] is None for r in report["leaves"])
    assert not report["citation_eligible"]
    assert not report["proof_search_connected"]


def test_external_flags_cannot_authorize_even_when_all_true(inputs):
    evidence = {name: {key: True for key in REQUIRED_EVIDENCE}
                for name in ("prop51_finite_dimensional", "nu_prime_hopf")}
    report = assess_citation_evidence(*inputs, external_evidence=evidence)
    assert report["evidence_authenticated_count"] == 0
    assert report["citation_eligible"] is False
    assert report["typed_binding_written"] is False


def test_tampered_source_hash_rejected(inputs):
    crosswalk, typed = inputs
    bad = deepcopy(crosswalk)
    bad["leaves"][0]["source_text_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="hash mismatch"):
        assess_citation_evidence(bad, typed)


def test_unsupported_source_publication_scope_rejected(inputs):
    crosswalk, typed = inputs
    bad = deepcopy(crosswalk)
    bad["leaves"][0]["source_publication_position_scope"] = "ORIGINAL_VERIFIED"
    with pytest.raises(ValueError, match="evidence boundary"):
        assess_citation_evidence(bad, typed)


def test_missing_typed_check_rejected(inputs):
    crosswalk, typed = inputs
    bad = deepcopy(typed)
    del bad["typed_checks"]["nu_prime_hopf_eta5"]
    with pytest.raises(ValueError, match="typed clause checks incomplete"):
        assess_citation_evidence(crosswalk, bad)


def test_archive_promotion_rejected(inputs):
    crosswalk, typed = inputs
    bad = deepcopy(crosswalk)
    bad["source_archive_proof_eligible_count"] = 1
    with pytest.raises(ValueError, match="proof eligibility changed"):
        assess_citation_evidence(bad, typed)


def test_invalid_external_evidence_rejected(inputs):
    with pytest.raises(ValueError, match="external evidence keys"):
        assess_citation_evidence(*inputs, external_evidence={})


def test_report_writer_preserves_blocked_decision(inputs, tmp_path):
    report = assess_citation_evidence(*inputs)
    write_report(report, tmp_path)
    loaded = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert loaded["citation_eligible"] is False
    assert "未認証" in (tmp_path / "report.md").read_text(encoding="utf-8")


def test_current_audit_does_not_write_binding():
    report = audit_current(ROOT / "phase163_r4_r94_output" / "manifest.json")
    assert report["typed_binding_written"] is False
    assert report["production_modified"] is False
    assert report["full_pytest_run"] is False
