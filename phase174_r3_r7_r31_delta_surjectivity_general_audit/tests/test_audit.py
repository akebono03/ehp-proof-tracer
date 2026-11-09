"""R31 focused audit tests: read-only and fail-closed."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r31_delta_surjectivity_general_audit.audit import (
    DEPENDENCIES, PINS, ROOT, SOURCE, git_blob_sha, inspect_toda_source,
    inspect_typed_obligations, matches_pinned_blob, report, verify_checkout,
)


def test_git_blob_computation_and_lf_crlf_allowance():
    raw = b"a\nb\n"
    assert git_blob_sha(raw) == git_blob_sha(b"a\nb\n")
    assert matches_pinned_blob(raw.replace(b"\n", b"\r\n"), git_blob_sha(raw))
    assert not matches_pinned_blob(b"different", git_blob_sha(raw))


def test_toda_proposition_source_dependency_order():
    summary = inspect_toda_source((ROOT / SOURCE).read_text(encoding="utf-8-sig"))
    assert summary["independent_source_verified"] is True
    assert summary["printed_conclusions_not_treated_as_premises"] is True
    assert len(DEPENDENCIES) == 7


def test_toda_source_mutated_lower_kernel_is_rejected():
    original = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    damaged = original.replace(DEPENDENCIES[2][1], r"\(\ker\Delta=0\)", 1)
    with pytest.raises(ValueError, match="lower_delta_kernel"):
        inspect_toda_source(damaged)


def test_all_git_pins_are_whole_file_pins():
    assert len(PINS) >= 10
    for path, sha in PINS.items():
        assert matches_pinned_blob((ROOT / path).read_bytes(), sha)


def test_source_guard_preserves_reviewed_r30_handoff():
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["handoff_mode"] in ("R30_UNCOMMITTED_REVIEWED", "R30_MERGED_REVIEWED")
    assert set(state["accepted_tracked_edits"]).issubset({"phase165_r52_r9_shared_math.py"})


def test_typed_hopf_delta_bridge_has_distinct_independent_goals():
    data = inspect_typed_obligations()
    assert data["prop27_n6_typed"] is True
    assert data["generic_lemma_conditionally_sound"] is True
    assert "KernelMultipleStatement" in data["lower_delta_kernel_goal"]
    assert "ImageZeroStatement" in data["zero_suspension_image_goal"]
    assert data["independent_lower_kernel_certified_in_r31"] is False
    assert data["typed_generator_transport_rule_installed_in_r31"] is False


def test_r31_reports_no_unsupported_completion():
    value = report(dry_run=False)
    assert value["new_givens"] == 0
    assert value["new_math_rules"] == 0
    assert value["production_files_changed"] == 0
    assert value["delta_surjectivity_proved"] is False
    assert value["root_complete"] is False
    assert value["full_pytest"] is False
    assert value["gate"].endswith("LOWER_KERNEL_AND_ZERO_IMAGE_PENDING")
