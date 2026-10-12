import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r53_semantic_overlap_audit import audit, catalog_digest, write_results


DATA_ROOT = Path(__file__).resolve().parent.parent.parent


def data():
    root = DATA_ROOT
    return (json.loads((root / "phase163_r4_r52_output" / "crosswalk.json").read_text(encoding="utf-8")),
            json.loads((root / "phase163_r4_r47_output" / "catalog.json").read_text(encoding="utf-8")),
            root / "phase163_r4_r42_tex_extract" / "inputs")


def test_real_input_invariant_and_complete_19():
    crosswalk, catalog, inputs = data()
    result = audit(crosswalk, catalog, inputs)
    assert result["definition_candidate_count"] == 19
    assert sum(result["status_counts"].values()) == 19
    assert {row["r48_index"] for row in result["candidates"]} == {row["r48_index"] for row in crosswalk["candidates"]}


def test_numbered_definitions_have_catalog_unit_but_no_registered_reference():
    crosswalk, catalog, inputs = data()
    results = {row["editorial_key"]: row for row in audit(crosswalk, catalog, inputs)["candidates"]}
    for key, locator in (("delta_homomorphism", "(2.9)"), ("inverse_delta", "(2.10)"), ("pi_i_n_subgroup", "(4.3)")):
        assert results[key]["matched_locator"] == locator
        assert results[key]["tex_catalog_containment_status"] == "CATALOG_UNIT_WITHOUT_EXISTING_REFERENCE"
        assert results[key]["existing_reference_id"] is None


def test_no_mathematical_equivalence_or_new_id_claim():
    crosswalk, catalog, inputs = data()
    result = audit(crosswalk, catalog, inputs)
    assert result["mathematical_content_equivalence_verified"] is False
    assert result["semantic_overlap_unresolved_count"] == 19
    assert result["new_statement_confirmed_count"] == 0
    assert all(not item["new_statement_confirmed"] for item in result["candidates"])
    assert all(item["existing_assertion_ids_inferred"] == [] for item in result["candidates"])


def test_crosswalk_digest_mismatch_rejected():
    c, cat, inp = data()
    c["catalog_snapshot_sha256"] = "x"
    with pytest.raises(ValueError, match="Catalog snapshot"):
        audit(c, cat, inp)


def test_invalid_edition_claim_rejected():
    c, cat, inp = data()
    c["candidates"][0]["original_edition_verified"] = True
    with pytest.raises(ValueError, match="registered/verified"):
        audit(c, cat, inp)


def test_candidate_duplicate_rejected():
    c, cat, inp = data()
    c["candidates"][1]["r48_index"] = c["candidates"][0]["r48_index"]
    with pytest.raises(ValueError, match="unique"):
        audit(c, cat, inp)


def test_source_hash_rejected(tmp_path):
    c, cat, inp = data()
    for path in inp.iterdir():
        if path.is_file() and path.suffix == ".tex":
            (tmp_path / path.name).write_bytes(path.read_bytes())
    (tmp_path / "Toda_03_2(2).tex").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="TeX source changed"):
        audit(c, cat, tmp_path)


def test_read_only_and_publication_position_preserved():
    c, cat, inp = data()
    original = catalog_digest(cat)
    result = audit(c, cat, inp)
    assert catalog_digest(cat) == original
    assert result["registration_applied"] is False
    assert result["ids_allocated"] is False
    assert result["live_registry_verified"] is False
    assert result["pending_other_candidates_count"] == 237


def test_export_three_files(tmp_path):
    c, cat, inp = data()
    result = audit(c, cat, inp)
    write_results(result, tmp_path)
    assert {p.name for p in tmp_path.iterdir()} == {"overlap_audit.json", "overlap_audit.csv", "report.md"}
    reloaded = json.loads((tmp_path / "overlap_audit.json").read_text(encoding="utf-8"))
    assert len(reloaded["candidates"]) == 19
