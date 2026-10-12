"""Phase 164 R4 targeted, read-only real-manifest regression tests."""
from pathlib import Path

import pytest

from phase164_r4_real_registry_audit import (
    _equal_conclusion,
    audit_phase164_r4,
    write_phase164_r4_report,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"


@pytest.fixture(scope="module")
def audited():
    return audit_phase164_r4(MANIFEST)


def test_r4_manifest_remains_archival_only(audited):
    report = audited.report
    assert report["source_archive_reference_count"] == 108
    assert report["source_archive_assertion_count"] == 117
    assert report["source_archive_proof_eligible_count"] == 0
    assert report["source_archive_promoted"] is False
    assert report["mathematical_certification_claimed"] is False


def test_r4_real_bridge_does_not_fabricate_r3_evidence(audited):
    report = audited.report
    assert len(report["literature_leaves"]) == 2
    assert report["real_registry_r3_reconstruction_attempted"] is False
    assert report["real_registry_r3_status"] == "BLOCKED_PENDING_INDEPENDENT_CITATION_EVIDENCE"
    assert report["production_modified"] is False


def test_r4_existing_proof_and_narrative_regression(audited):
    report = audited.report
    assert report["exactness_given_leaf_count"] == 4
    assert report["legacy_derived_step_count"] == 7
    assert report["legacy_provenance_verified_inferences"] >= 7
    assert "## 証明" in audited.narrative
    assert audited.narrative.rstrip().endswith("□")


def test_r4_structural_equality_rejects_unverified_equivalence():
    assert _equal_conclusion("proof", "proof")
    assert not _equal_conclusion("proof", 42)
    assert not _equal_conclusion("proof", "other")


def test_r4_reports_are_written_without_modifying_sources(audited, tmp_path):
    write_phase164_r4_report(audited, tmp_path)
    assert (tmp_path / "report.json").exists()
    assert (tmp_path / "report.md").exists()
    assert (tmp_path / "legacy_narrative.md").read_text(encoding="utf-8") == audited.narrative
