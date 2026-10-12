import pytest

from phase163_r4_r84_apply import (
    NEW_ENUM,
    transformed_archive,
    transformed_registry,
)
from phase163_source_archive_registry import build_registry_with_source_archive
from unified_statement_registry import AssertionOrigin


def test_archive_origin_is_separate_from_fixed_and_internal():
    assert AssertionOrigin.SOURCE_ARCHIVE.value == "source_archive"
    assert AssertionOrigin.SOURCE_ARCHIVE is not AssertionOrigin.FIXED_STATEMENT
    assert AssertionOrigin.SOURCE_ARCHIVE is not AssertionOrigin.PROOF_INTERNAL


def test_r83_archive_entries_are_source_only():
    registry, summary = build_registry_with_source_archive()
    assert len(summary["source_text_assertion_ids"]) == 8
    for key in summary["source_text_assertion_ids"]:
        entry = registry.assertion(key)
        assert entry.origin is AssertionOrigin.SOURCE_ARCHIVE
        assert entry.available_after_position is None
        assert entry.content["proof_eligible"] is False
        assert entry.content["mathematics_verified"] is False


def test_existing_fixed_boundary_not_retyped():
    registry, summary = build_registry_with_source_archive()
    item = registry.assertions_for("toda:Proposition 2.5")
    assert any(entry.origin is AssertionOrigin.FIXED_STATEMENT for entry in item)
    assert sum(entry.origin is AssertionOrigin.SOURCE_ARCHIVE for entry in item) == 2


def test_cannot_apply_origin_patch_twice():
    with pytest.raises(ValueError):
        transformed_registry(NEW_ENUM)


def test_patch_rejects_unknown_registry_format():
    with pytest.raises(ValueError):
        transformed_registry("class AssertionOrigin: pass")


def test_patch_rejects_missing_archive_target():
    with pytest.raises(ValueError):
        transformed_archive("unrelated")


def test_builder_preserves_reference_reuse():
    _, summary = build_registry_with_source_archive()
    assert summary["reference_reused_count"] == 1
    assert summary["reference_added_count"] == 3
    assert summary["proof_eligible_count"] == 0
