"""Focused read-only R4-R61 input consistency and safety tests."""
import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r61_registration_gate import assess, write_outputs


@pytest.fixture
def inputs():
    root = Path(__file__).resolve().parents[2]
    names = (
        "phase163_r4_r58_output/readiness.json",
        "phase163_r4_r59_output/id_order_trial.json",
        "phase163_r4_r60_output/collision_audit.json",
    )
    return tuple(json.loads((root / name).read_text(encoding="utf-8")) for name in names)


def test_three_candidates_blocked_for_semantics(inputs):
    result = assess(*inputs)
    assert result["candidate_count"] == 3
    assert result["gate_blocked_count"] == 3
    assert result["semantic_registration_allowed_count"] == 0
    assert result["proof_eligible_count"] == 0


def test_ids_and_positions_independent(inputs):
    result = assess(*inputs)
    assert [r["original_publication_position"] for r in result["records"]] == [40, 41, 65]
    assert [r["simulated_publication_position"] for r in result["records"]] == [40, 42, 66]
    assert all(r["id_stable_under_insertion"] for r in result["records"])


def test_unresolved_conditions_preserved(inputs):
    result = assess(*inputs)
    assert result["unresolved_semantics_count"] == 9
    assert all(len(r["unresolved_semantics"]) == 3 for r in result["records"])


def test_source_unit_mismatch_rejected(inputs):
    a, b, c = copy.deepcopy(inputs)
    b["records"][0]["source_unit_id"] = "different-source"
    with pytest.raises(ValueError, match="source units"):
        assess(a, b, c)


def test_reused_reference_id_rejected(inputs):
    a, b, c = copy.deepcopy(inputs)
    c["records"][1]["trial_reference_id"] = c["records"][0]["trial_reference_id"]
    with pytest.raises(ValueError, match="reference identity"):
        assess(a, b, c)


def test_existing_locator_overlap_rejected(inputs):
    a, b, c = copy.deepcopy(inputs)
    c["records"][0]["locator_overlap_requires_review"] = True
    with pytest.raises(ValueError, match="locator overlap"):
        assess(a, b, c)


def test_semantic_promotion_rejected(inputs):
    a, b, c = copy.deepcopy(inputs)
    a["records"][0]["semantic_registration_status"] = "READY"
    with pytest.raises(ValueError, match="semantic boundary"):
        assess(a, b, c)


def test_production_mutation_rejected(inputs):
    a, b, c = copy.deepcopy(inputs)
    c["production_ids_allocated"] = True
    with pytest.raises(ValueError, match="production mutation"):
        assess(a, b, c)


def test_outputs_written_without_registration(inputs, tmp_path):
    result = assess(*inputs)
    write_outputs(result, tmp_path)
    assert (tmp_path / "registration_gate.json").is_file()
    assert (tmp_path / "registration_gate.csv").is_file()
    assert "正式登録を保留" in (tmp_path / "report.md").read_text(encoding="utf-8")
    assert result["production_registry_modified"] is False
