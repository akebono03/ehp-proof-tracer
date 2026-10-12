import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r59_id_order_trial import (
    build_trial_registry,
    read_readiness,
    simulate_insertion,
    write_outputs,
)


@pytest.fixture
def records():
    root = Path(__file__).resolve().parents[2]
    return read_readiness(root / "phase163_r4_r58_output" / "readiness.json")["records"]


def test_three_source_grounded_trial_records(records):
    assert [r["locator"] for r in records] == ["(2.9)", "(2.10)", "(4.3)"]


def test_trial_reference_ids_unchanged(records):
    result = simulate_insertion(records)
    assert result["stable_reference_id_count"] == 3
    assert all(r["id_preserved"] for r in result["records"])


def test_trial_assertion_ids_unchanged(records):
    result = simulate_insertion(records)
    assert result["stable_assertion_id_count"] == 3
    assert all(r["assertion_id"].startswith("trial:r55:") for r in result["records"])


def test_published_order_can_shift_without_id_change(records):
    result = simulate_insertion(records)
    assert [r["position_before"] for r in result["records"]] == [40, 41, 65]
    assert [r["position_after"] for r in result["records"]] == [40, 42, 66]


def test_component_position_independent(records):
    result = simulate_insertion(records)
    assert [p for _, p in result["synthetic_component_order"]] == [1, 2, 3]
    assert result["component_positions_independent"] is True


def test_unmodified_original_registry(records):
    original, snapshots = build_trial_registry(records)
    simulate_insertion(records)
    assert [original.reference(s.reference.reference_id).publication_position for s in snapshots] == [40, 41, 65]


def test_rejects_duplicate_trial_ids(records):
    broken = copy.deepcopy(records)
    broken[1]["trial_reference_id"] = broken[0]["trial_reference_id"]
    with pytest.raises(ValueError, match="duplicate reference_id"):
        build_trial_registry(broken)


def test_no_production_promotion(records):
    result = simulate_insertion(records)
    assert result["production_ids_allocated"] is False
    assert result["production_registry_modified"] is False
    assert result["mathematical_semantics_verified"] is False
    assert result["proof_search_connected"] is False


def test_writes_three_reports(records, tmp_path):
    write_outputs(simulate_insertion(records), tmp_path)
    assert json.loads((tmp_path / "id_order_trial.json").read_text(encoding="utf-8"))["ids_preserved"] is True
    assert (tmp_path / "id_order_trial.csv").exists()
    assert (tmp_path / "report.md").exists()
