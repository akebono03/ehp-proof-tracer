import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r62_remaining_definitions import audit_remaining, write_reports


@pytest.fixture
def inputs():
    root = Path(__file__).resolve().parents[2]
    paths = [
        root / "phase163_r4_r52_output" / "crosswalk.json",
        root / "phase163_r4_r53_output" / "overlap_audit.json",
        root / "phase163_r4_r61_output" / "registration_gate.json",
    ]
    return tuple(json.loads(p.read_text(encoding="utf-8")) for p in paths)


def test_sixteen_remain(inputs):
    result = audit_remaining(*inputs)
    assert result["remaining_definition_candidate_count"] == 16
    assert result["previously_reviewed_count"] == 3


def test_all_are_unanchored(inputs):
    result = audit_remaining(*inputs)
    assert result["no_direct_catalog_unit_count"] == 16
    assert all(x["matched_locator"] is None for x in result["records"])


def test_no_invented_semantics_or_ids(inputs):
    result = audit_remaining(*inputs)
    assert all(x["defined_symbol_verified"] is None and x["production_reference_id"] is None for x in result["records"])
    assert result["semantic_registration_approved_count"] == 0


def test_excludes_reviewed_three(inputs):
    result = audit_remaining(*inputs)
    assert {x["editorial_key"] for x in result["records"]}.isdisjoint({"delta_homomorphism","inverse_delta","pi_i_n_subgroup"})


def test_preserve_source_locations(inputs):
    result = audit_remaining(*inputs)
    assert all(x["source_line"] > 0 and x["source_excerpt"] for x in result["records"])
    assert [(x["chapter"],x["source_line"]) for x in result["records"]] == sorted((x["chapter"],x["source_line"]) for x in result["records"])


def test_mismatched_catalog_rejected(inputs):
    a,b,c=copy.deepcopy(inputs)
    b["catalog_snapshot_sha256"]="unexpected"
    with pytest.raises(ValueError,match="snapshots"):
        audit_remaining(a,b,c)


def test_changed_evidence_rejected(inputs):
    a,b,c=copy.deepcopy(inputs)
    b["candidates"][0]["excerpt"]="modified"
    with pytest.raises(ValueError,match="source evidence"):
        audit_remaining(a,b,c)


def test_newly_anchored_item_requires_review(inputs):
    a,b,c=copy.deepcopy(inputs)
    b["candidates"][0]["matched_locator"]="(1.2)"
    with pytest.raises(ValueError,match="catalog anchor"):
        audit_remaining(a,b,c)


def test_output_files(inputs,tmp_path):
    report=audit_remaining(*inputs)
    write_reports(report,tmp_path)
    assert len(json.loads((tmp_path/"remaining_definitions.json").read_text(encoding="utf-8"))["records"])==16
    assert len((tmp_path/"remaining_definitions.csv").read_text(encoding="utf-8-sig").splitlines())==17
    assert "16件" in (tmp_path/"report.md").read_text(encoding="utf-8")
