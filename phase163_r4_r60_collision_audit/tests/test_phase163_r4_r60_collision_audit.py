import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r60_collision_audit import audit, write_outputs


@pytest.fixture
def order():
    root = Path(__file__).resolve().parents[2]
    path = root / "phase163_r4_r59_output" / "id_order_trial.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def ids():
    return ({"toda:(5.3)": "(5.3)", "toda:Proposition 5.3": "Proposition 5.3"},
            {"boundary:(5.3):nu_prime_membership": "toda:(5.3)"})


def test_three_candidates_no_id_conflicts(order, ids):
    result = audit(order, *ids)
    assert result["candidate_count"] == 3
    assert result["candidate_reference_id_collision_count"] == 0
    assert result["candidate_assertion_id_collision_count"] == 0


def test_reference_id_reuse_detected(order, ids):
    refs, assertions = ids
    refs = {**refs, order["records"][0]["reference_id"]: "different locator"}
    assert audit(order, refs, assertions)["candidate_reference_id_collision_count"] == 1


def test_assertion_id_reuse_detected(order, ids):
    refs, assertions = ids
    assertions = {**assertions, order["records"][0]["assertion_id"]: "toda:(5.3)"}
    assert audit(order, refs, assertions)["candidate_assertion_id_collision_count"] == 1


def test_cross_namespace_reuse_detected(order, ids):
    refs, assertions = ids
    assertions = {**assertions, order["records"][0]["reference_id"]: "toda:(5.3)"}
    assert audit(order, refs, assertions)["candidate_reference_id_collision_count"] == 1


def test_locator_overlap_is_not_id_collision(order, ids):
    refs, assertions = ids
    refs = {**refs, "toda:(2.9)": "(2.9)"}
    result = audit(order, refs, assertions)
    assert result["candidate_locator_overlap_review_count"] == 1
    assert result["candidate_reference_id_collision_count"] == 0


def test_duplicate_trial_reference_rejected(order, ids):
    broken = copy.deepcopy(order)
    broken["records"][1]["reference_id"] = broken["records"][0]["reference_id"]
    broken["records"][1]["assertion_id"] = broken["records"][0]["assertion_id"]
    with pytest.raises(ValueError, match="duplicate candidate"):
        audit(broken, *ids)


def test_promotion_flag_rejected(order, ids):
    broken = copy.deepcopy(order)
    broken["records"][0]["id_is_trial_only"] = False
    with pytest.raises(ValueError, match="unverified candidate"):
        audit(broken, *ids)


def test_live_namespace_conflict_rejected(order, ids):
    refs, assertions = ids
    with pytest.raises(ValueError, match="namespace overlaps"):
        audit(order, refs, {**assertions, "toda:(5.3)": "toda:(5.3)"})


def test_write_results_and_no_mutation(order, ids, tmp_path):
    before = copy.deepcopy(order)
    result = audit(order, *ids)
    write_outputs(result, tmp_path)
    assert order == before
    assert (tmp_path / "collision_audit.json").exists()
    assert (tmp_path / "collision_audit.csv").exists()
    assert (tmp_path / "report.md").exists()
    assert result["production_registry_modified"] is False
