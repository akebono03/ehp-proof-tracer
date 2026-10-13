from dataclasses import replace
import pytest

from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r3_source_scope import (
    ADJACENT_TEX, ARCHIVE_ID, CLAUSES, collect_toda51_scope,
)


@pytest.fixture
def bridge():
    value, _ = build_phase165_r5_manifest_bridge()
    return value


def test_six_clauses_are_associated_with_single_reference(bridge):
    result = collect_toda51_scope(bridge)
    assert result["source_clause_count"] == 6
    assert result["reference_id"] == "phase163:archive:toda:(5.1)"
    assert len({item["key"] for item in result["clauses"]}) == 6


def test_existing_two_schemas_preserved(bridge):
    result = collect_toda51_scope(bridge)
    assert result["typed_schema_count"] == 2
    assert {c["typed_schema"] for c in result["clauses"] if c["typed_schema"]} == {
        "sphere_one_zero", "diagonal_infinite_cyclic"
    }


def test_adjacent_display_is_explicitly_unverified(bridge):
    result = collect_toda51_scope(bridge)
    assert result["adjacent_source_status"] == "USER_SUPPLIED_NOT_ARCHIVE_VERIFIED"
    assert result["registry_modified"] is False
    assert result["new_proof_eligible"] == 0
    assert result["proof_steps_created"] == 0


def test_rejects_changed_adjacent_tex(bridge):
    with pytest.raises(ValueError, match="differs"):
        collect_toda51_scope(bridge, ADJACENT_TEX.replace("G_0", "G_1"))


def test_rejects_corrupted_archive_checksum(bridge):
    original = bridge.registry.assertion(ARCHIVE_ID)
    altered = dict(original.content)
    altered["source_text"] = "corrupted"
    bridge.registry._assertions[ARCHIVE_ID] = replace(original, content=altered)
    with pytest.raises(ValueError, match="checksum"):
        collect_toda51_scope(bridge)


def test_archive_does_not_gain_additional_assertions(bridge):
    prior = len(bridge.registry._assertions)
    collect_toda51_scope(bridge)
    assert len(bridge.registry._assertions) == prior


def test_clause_source_spans_differ(bridge):
    result = collect_toda51_scope(bridge)
    assert [c["source_part"] for c in result["clauses"]] == (
        ["numbered_equation"] * 3 + ["adjacent_display"] * 3
    )
