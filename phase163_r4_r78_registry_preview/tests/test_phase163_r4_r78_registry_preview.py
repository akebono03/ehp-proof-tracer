import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r78_registry_preview import create_preview, load_json, write_reports

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def inputs():
    return (
        load_json(ROOT / "phase163_r4_r77_output" / "proof_ownership.json"),
        load_json(ROOT / "phase163_r4_r75_output" / "ownership_proposals.json"),
    )


def test_counts(inputs):
    result = create_preview(*inputs)
    assert result["candidate_count"] == 11
    assert result["preview_reference_count"] == 4
    assert result["preview_proof_internal_count"] == 10
    assert result["paraphrase_hold_count"] == 1


def test_owners_and_multiple_assertions(inputs):
    result = create_preview(*inputs)
    by_owner = {r["locator"]: r["assertion_candidate_count"] for r in result["reference_previews"]}
    assert by_owner == {"Proposition 1.6": 3, "Theorem 2.4": 4,
                        "Proposition 2.5": 2, "Proposition 4.2": 1}


def test_paraphrase_not_duplicated(inputs):
    result = create_preview(*inputs)
    row = next(r for r in result["records"] if r["r48_index"] == 66)
    assert row["preview_status"] == "PARAPHRASE_HOLD"
    assert row["preview_reference_id"] is None
    assert row["preview_assertion_id"] is None


def test_only_temporary_ids(inputs):
    result = create_preview(*inputs)
    assert all(r["preview_reference_id"].startswith("preview:")
               for r in result["reference_previews"])
    assert all(r["preview_assertion_id"].startswith("preview:")
               for r in result["records"] if r["preview_assertion_id"])
    assert not result["production_ids_allocated"]


def test_reject_hash_drift(inputs):
    r77, r75 = copy.deepcopy(inputs)
    r75["focused_proposals"][0]["excerpt_sha256"] = "0" * 64
    with pytest.raises(ValueError):
        create_preview(r77, r75)


def test_reject_unapproved_role_upgrade(inputs):
    r77, r75 = copy.deepcopy(inputs)
    r77["records"][0]["registration_allowed"] = True
    with pytest.raises(ValueError):
        create_preview(r77, r75)


def test_reject_duplicate_candidate(inputs):
    r77, r75 = copy.deepcopy(inputs)
    r77["records"][1]["r48_index"] = r77["records"][0]["r48_index"]
    with pytest.raises(ValueError):
        create_preview(r77, r75)


def test_inputs_unchanged(inputs):
    before = copy.deepcopy(inputs)
    create_preview(*inputs)
    assert inputs == before


def test_reports(inputs, tmp_path):
    result = create_preview(*inputs)
    write_reports(result, tmp_path)
    saved = json.loads((tmp_path / "registry_preview.json").read_text(encoding="utf-8"))
    assert saved == result
    assert "Proposition 1.6" in (tmp_path / "report.md").read_text(encoding="utf-8")
