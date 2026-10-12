from types import SimpleNamespace

import pytest

from phase163_r4_r81_duplicate_audit import audit


def sample():
    owners = [("prop:1-6", 3), ("thm:2.4", 2), ("prop:2.5", 2), ("prop:4.2", 1)]
    return {"phase": "163 R4-R80", "production_registry_modified": False,
            "records": [{"owner": owner, "component_position": i, "registration_allowed": False,
                         "permanent_id_allocated": False, "boundary_issues": []}
                        for owner, count in owners for i in range(1, count + 1)]}


class Registry:
    def __init__(self, present=()):
        self.present = set(present)

    def reference(self, key):
        if key not in self.present:
            raise KeyError(key)
        return SimpleNamespace(reference_id=key)

    def assertions_for(self, key):
        return (1,) if key in self.present else ()


def bridge(present=()):
    return SimpleNamespace(registry=Registry(present))


def test_empty_catalog_is_not_proof_of_semantic_nonduplication():
    result = audit(sample(), {}, bridge())
    assert result["exact_locator_overlap_count"] == 0
    assert all(row["semantic_nonduplication_verified"] is False for row in result["records"])


def test_real_locator_overlap_detected():
    result = audit(sample(), {"Proposition 2.5": (1,)}, bridge(("toda:Proposition 2.5",)))
    assert result["exact_locator_overlap_count"] == 1
    assert result["records"][2]["existing_bridge_assertion_count"] == 1


def test_equation_alias_remains_separate_review():
    result = audit(sample(), {"(4.4)": (1,)}, bridge())
    assert result["embedded_equation_alias_review_count"] == 1
    assert result["records"][3]["alias_review"][0]["existing_boundary_component_count"] == 1


def test_component_positions_enforced():
    data = sample()
    data["records"][0]["component_position"] = 2
    with pytest.raises(ValueError, match="order"):
        audit(data, {}, bridge())


def test_registration_not_allowed():
    result = audit(sample(), {}, bridge())
    assert result["semantic_registration_allowed_count"] == 0
    assert result["production_registry_modified"] is False


def test_wrong_phase_rejected():
    data = sample()
    data["phase"] = "wrong"
    with pytest.raises(ValueError, match="R80"):
        audit(data, {}, bridge())


def test_wrong_owner_rejected():
    data = sample()
    data["records"][0]["owner"] = "other"
    with pytest.raises(ValueError, match="owner"):
        audit(data, {}, bridge())
