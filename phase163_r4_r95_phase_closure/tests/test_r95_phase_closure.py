"""R95 targeted-only closure tests. Never collect the full test suite."""
import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r95_phase_closure.r95_phase_closure import (
    audit_closure, verify_manifest, write_outputs,
)

ROOT = Path(__file__).resolve().parents[2]
R94 = ROOT / "phase163_r4_r94_output" / "manifest.json"
CATALOG = ROOT / "phase163_r4_r91_output" / "source_catalog.json"
AUDIT = ROOT / "phase163_r4_r92_output" / "audit.json"
SOURCE = ROOT / "sources" / "toda"


@pytest.fixture(scope="module")
def manifest():
    return json.loads(R94.read_text(encoding="utf-8"))


def test_counts_and_origin_contract(manifest):
    out = verify_manifest(manifest)
    assert out["reference_count"] == 108
    assert out["assertion_count"] == 117
    assert out["source_origin_counts"] == {"R91": 96, "R92": 9, "R93": 12}


def test_all_statement_ids_unique(manifest):
    assert len({x["statement_id"] for x in manifest["assertions"]}) == 117


def test_subitem_order_and_parent_link(manifest):
    rows = {x["statement_id"]: x for x in manifest["assertions"]}
    assert len([x for x in rows.values() if x["source_origin"] == "R92"]) == 9
    for row in rows.values():
        if row["source_origin"] == "R92":
            assert row["reference_id"] == rows[row["parent_statement_id"]]["reference_id"]


def test_number_revisions_not_silently_promoted(manifest):
    assert verify_manifest(manifest)["number_review_count"] == 8
    assert manifest["original_edition_verified"] is False


def test_digest_tampering_rejected(manifest):
    wrong = copy.deepcopy(manifest)
    wrong["assertions"][0]["source_text"] += "changed"
    with pytest.raises(ValueError, match="SHA-256"):
        verify_manifest(wrong)


def test_duplicate_statement_id_rejected(manifest):
    wrong = copy.deepcopy(manifest)
    wrong["assertions"][1]["statement_id"] = wrong["assertions"][0]["statement_id"]
    with pytest.raises(ValueError, match="duplicate Statement ID"):
        verify_manifest(wrong)


def test_proof_promotion_rejected(manifest):
    wrong = copy.deepcopy(manifest)
    wrong["proof_eligible_count"] = 1
    with pytest.raises(ValueError, match="safety gate"):
        verify_manifest(wrong)


def test_rebuild_and_archival_only(manifest):
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    result = audit_closure(manifest, catalog, audit, SOURCE)
    assert result["reproducible_manifest"] is True
    assert result["proof_search_connected"] is False
    assert result["mathematical_semantics_verified_count"] == 0
    assert result["full_suite_run"] is False


def test_final_report_explicitly_excludes_full_pytest(manifest, tmp_path):
    out = {"reference_count": 108, "assertion_count": 117,
           "number_review_count": 8, "bridge_reference_reused_count": 23}
    write_outputs(out, tmp_path)
    assert json.loads((tmp_path / "closure.json").read_text(encoding="utf-8")) == out
    assert "全体 pytest: 実施しない" in (tmp_path / "closure_report.md").read_text(encoding="utf-8")
