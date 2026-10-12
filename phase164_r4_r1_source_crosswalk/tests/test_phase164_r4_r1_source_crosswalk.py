"""Focused Phase 164 R4-R1 source crosswalk tests; no production mutation."""
import copy
import json
from pathlib import Path

import pytest

from phase164_r4_r1_source_crosswalk import (
    audit_current_repository,
    source_crosswalk,
    write_reports,
)
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"


def _leaves():
    return tuple(step for step in build_phase59_3_data()["premise_steps"]
                 if step.rule is ProofRule.INFERENCE)


def test_two_real_source_locator_candidates_not_authorized():
    report = audit_current_repository(MANIFEST)
    assert report["status"] == "BLOCKED_PENDING_TYPED_BINDING_AND_INDEPENDENT_EVIDENCE"
    assert report["source_locator_candidate_count"] == 2
    assert report["mathematically_verified_bindings"] == 0
    assert report["source_archive_proof_eligible_count"] == 0
    assert [x["source_statement_id"] for x in report["leaves"]] == [
        "toda:tex:ch5:0002", "toda:tex:ch5:0005"]
    assert all(not row["citation_eligible"] for row in report["leaves"])
    assert all(not row["structured_assertion_connected"] for row in report["leaves"])
    assert all(row["legacy_given_root_count"] >= 1 for row in report["leaves"])


def test_missing_source_locator_is_rejected():
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    changed = copy.deepcopy(document)
    entry = next(x for x in changed["assertions"] if x["statement_id"] == "toda:tex:ch5:0005")
    entry["locator"] = "(5.3)-changed"
    with pytest.raises(ValueError, match="expected source ID/locator"):
        source_crosswalk(changed, _leaves())


def test_source_text_tampering_is_rejected():
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    changed = copy.deepcopy(document)
    next(x for x in changed["assertions"] if x["statement_id"] == "toda:tex:ch5:0002")["source_text"] += "tampered"
    with pytest.raises(ValueError, match="SHA-256"):
        source_crosswalk(changed, _leaves())


def test_crosswalk_rejects_one_leaf():
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="two existing literature leaves"):
        source_crosswalk(document, _leaves()[:1])


def test_report_output_is_read_only(tmp_path):
    report = audit_current_repository(MANIFEST)
    write_reports(report, tmp_path)
    saved = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert saved["production_modified"] is False
    assert saved["proof_search_connected"] is False
    assert saved["full_pytest_run"] is False
    assert "原本掲載順未確認" in (tmp_path / "report.md").read_text(encoding="utf-8")
