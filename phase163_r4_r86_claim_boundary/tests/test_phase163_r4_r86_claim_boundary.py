import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r86_claim_boundary import split_units, write_outputs


CATALOG = Path(__file__).resolve().parents[1] / "phase163_source_archive_catalog.json"


def source():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_nine_units_from_eight_transcripts():
    result = split_units(source())
    assert result["review_unit_count"] == 9
    assert result["review_counts_by_owner"]["thm:2.4"] == 3
    assert result["split_item_count"] == 1


def test_every_claim_is_exact_source_fragment():
    data = source()
    result = split_units(data)
    by_source = {(r["owner"], r["component_position"]): r for r in data["records"]}
    for item in result["records"]:
        original = by_source[item["source_owner"], item["component_position"]]
        assert item["claim_text"] in original["claim_text"]
        assert item["source_excerpt_sha256"] == original["source_claim_sha256"]


def test_even_dimension_isomorphisms_are_separate():
    records = split_units(source())["records"]
    pieces = [r for r in records if r["source_owner"] == "thm:2.4" and r["component_position"] == 2]
    assert len(pieces) == 2
    assert "i<(p+1)m-1" in pieces[0]["claim_text"]
    assert "全ての $i$" in pieces[1]["claim_text"]


def test_relative_composition_shares_equality_conditions():
    records = split_units(source())["records"]
    pieces = [r for r in records if r["source_owner"] == "prop:2.5"]
    assert len(pieces) == 2
    assert pieces[0]["inherited_equality_conditions"] == pieces[1]["inherited_equality_conditions"]
    assert "j<3m-1" in pieces[0]["inherited_equality_conditions"]


def test_archive_claims_not_proof_eligible():
    result = split_units(source())
    assert all(r["proof_eligible"] is False for r in result["records"])
    assert all(r["mathematical_semantics_verified"] is False for r in result["records"])
    assert result["production_ids_allocated"] is False


def test_transcript_tampering_rejected():
    catalog = source()
    catalog["records"][0]["claim_text"] += "tampered"
    with pytest.raises(ValueError, match="altered source transcript"):
        split_units(catalog)


def test_shared_equality_scope_deletion_rejected():
    catalog = source()
    row = next(r for r in catalog["records"] if r["owner"] == "prop:2.5" and r["component_position"] == 2)
    row["claim_text"] = row["claim_text"].replace("j<3m-1", "j<3m-2")
    import hashlib
    row["source_claim_sha256"] = hashlib.sha256(row["claim_text"].encode("utf-8")).hexdigest()
    with pytest.raises(ValueError, match="shared equality conditions incomplete"):
        split_units(catalog)


def test_report_and_json_output(tmp_path):
    result = split_units(source())
    write_outputs(result, tmp_path)
    assert json.loads((tmp_path / "claim_review_catalog.json").read_text(encoding="utf-8"))["review_unit_count"] == 9
    assert "数学的認定" in (tmp_path / "report.md").read_text(encoding="utf-8")
