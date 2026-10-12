import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r82_source_archive import archive_source_assertions
from phase163_r4_registry_bridge import build_registry_bridge


ROOT = Path(__file__).resolve().parents[2]


def evidence():
    return (json.loads((ROOT / "phase163_r4_r80_output/registration_preflight.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "phase163_r4_r81_output/duplicate_audit.json").read_text(encoding="utf-8")))


def bridge():
    return build_registry_bridge().registry


def test_archive_adds_three_refs_and_eight_source_entries():
    p, d = evidence()
    registry = bridge()
    result = archive_source_assertions(registry, p, d)
    assert result["reference_added_count"] == 3
    assert result["source_text_assertion_added_count"] == 8
    assert len(registry.assertions_for("toda:Proposition 2.5")) >= 3


def test_no_proof_eligibility():
    p, d = evidence()
    registry = bridge()
    result = archive_source_assertions(registry, p, d)
    for key in result["added_source_text_ids"]:
        assert registry.assertion(key).content["proof_eligible"] is False


def test_replay_rejects_duplicate_ids():
    p, d = evidence()
    registry = bridge()
    archive_source_assertions(registry, p, d)
    with pytest.raises((ValueError, AssertionError)):
        archive_source_assertions(registry, p, d)


def test_source_tampering_rejected():
    p, d = evidence()
    p = copy.deepcopy(p)
    p["records"][0]["claim_text"] += "CHANGED"
    with pytest.raises(ValueError, match="checksum"):
        archive_source_assertions(bridge(), p, d)


def test_audit_identity_change_rejected():
    p, d = evidence()
    d = copy.deepcopy(d)
    d["records"][0]["locator"] = "Proposition 9.9"
    with pytest.raises(ValueError, match="locator"):
        archive_source_assertions(bridge(), p, d)


def test_order_mutation_rejected():
    p, d = evidence()
    p = copy.deepcopy(p)
    p["records"][0]["component_position"] = 3
    with pytest.raises(ValueError, match="order"):
        archive_source_assertions(bridge(), p, d)


def test_prior_semantic_approval_rejected():
    p, d = evidence()
    d = copy.deepcopy(d)
    d["semantic_registration_allowed_count"] = 1
    with pytest.raises(ValueError, match="approval"):
        archive_source_assertions(bridge(), p, d)
