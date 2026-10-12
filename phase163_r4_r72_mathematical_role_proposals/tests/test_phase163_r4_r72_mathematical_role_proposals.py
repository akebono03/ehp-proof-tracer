import copy
import csv
import json
from pathlib import Path

import pytest

from phase163_r4_r72_mathematical_role_proposals import CHOICES, propose_roles, write_reports


@pytest.fixture
def source():
    root = Path(__file__).resolve().parents[2]
    return json.loads((root / "phase163_r4_r71_output" / "semantic_review_queue.json").read_text(encoding="utf-8"))


def test_all_237_preserved(source):
    report = propose_roles(source)
    assert len(report["records"]) == 237
    assert {r["r48_index"] for r in report["records"]} == {r["r48_index"] for r in source["records"]}


def test_explicit_review_count(source):
    report = propose_roles(source)
    assert report["editorial_proposal_count"] == len(CHOICES) == 34
    assert report["remaining_unreviewed_count"] == 203


def test_two_overlap_not_new_reference(source):
    rows = {r["r48_index"]: r for r in propose_roles(source)["records"]}
    assert rows[73]["proposed_role"] == "EXISTING_REFERENCE_COMPONENT"
    assert rows[275]["proposed_role"] == "EXISTING_REFERENCE_COMPONENT"
    assert all(not rows[i]["semantic_registration_allowed"] for i in (73, 275))


def test_proof_local_distinguished_from_definition(source):
    rows = {r["r48_index"]: r for r in propose_roles(source)["records"]}
    assert rows[70]["proposed_role"] == "PROOF_LOCAL_CONSTRUCTION_CANDIDATE"
    assert rows[102]["proposed_role"] == "SEPARATE_DEFINITION_CANDIDATE"
    assert rows[65]["proposed_role"] == "PROOF_INTERNAL_CANDIDATE"


def test_no_registration_permissions(source):
    report = propose_roles(source)
    assert report["mathematical_role_verified_count"] == 0
    assert report["semantic_registration_allowed_count"] == 0
    assert not report["production_registry_modified"]
    assert all(r["production_reference_id"] is None for r in report["records"])


def test_mutated_excerpt_is_rejected(source):
    changed = copy.deepcopy(source)
    next(r for r in changed["records"] if r["r48_index"] == 73)["excerpt"] = "altered"
    with pytest.raises(ValueError, match="digest mismatch"):
        propose_roles(changed)


def test_missing_row_is_rejected(source):
    changed = copy.deepcopy(source)
    changed["records"].pop()
    with pytest.raises(ValueError, match="incomplete"):
        propose_roles(changed)


def test_reports_have_237_csv_records(source, tmp_path):
    report = propose_roles(source)
    write_reports(report, tmp_path)
    with (tmp_path / "role_proposals.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 237
    assert len(json.loads((tmp_path / "role_proposals.json").read_text(encoding="utf-8"))["records"]) == 237
    assert "数学的役割の個別判定案" in (tmp_path / "report.md").read_text(encoding="utf-8")


def test_deterministic(source):
    assert propose_roles(source) == propose_roles(source)
