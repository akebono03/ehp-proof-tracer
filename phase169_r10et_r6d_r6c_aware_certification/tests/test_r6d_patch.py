"""Focused, pure tests for R6D's narrow audit-source certification update."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase169_r10et_r6d_r6c_aware_certification.patch import (
    FUNCTION, ORIGINAL_SHA256, R6C_PATCH_SHA256, sha256_hex, transform_r6_audit,
    whole_function,
)


ORIGINAL = Path(__file__).resolve().parents[1] / (
    "reviewed_sources/r6_audit_BEFORE_FULL.py"
)


def test_r6d_reviewed_original_is_exactly_guarded():
    original = ORIGINAL.read_bytes()
    assert sha256_hex(original) == ORIGINAL_SHA256


def test_r6d_transform_changes_one_complete_audit_function():
    original = ORIGINAL.read_bytes()
    updated = transform_r6_audit(original)
    original_text = original.decode("utf-8")
    new_text = updated.decode("utf-8")
    assert original_text.count("def certify_reviewed_production(") == 1
    assert new_text.count("def certify_reviewed_production(") == 1
    assert new_text.count("def summarize_dependency(") == 1
    assert original_text.split("def summarize_dependency(", 1)[1] == new_text.split("def summarize_dependency(", 1)[1]
    assert original_text.split("def certify_reviewed_production(", 1)[0] == new_text.split("def certify_reviewed_production(", 1)[0]
    assert "transform_r6c(path, before)" in whole_function(updated)
    assert "if (root / path).read_bytes() != after:" in whole_function(updated)
    assert "reviewed R6C" in whole_function(updated)


def test_r6d_rejects_unknown_audit_source():
    with pytest.raises(RuntimeError, match="not the reviewed original"):
        transform_r6_audit(b"unknown source")


def test_r6d_rejects_repeat_patch():
    with pytest.raises(RuntimeError, match="not the reviewed original"):
        transform_r6_audit(transform_r6_audit(ORIGINAL.read_bytes()))


def test_r6d_requires_exact_reviewed_r6c_transform_source():
    import hashlib
    package_root = Path(__file__).resolve().parents[2]
    r6c = package_root / "phase169_r10et_r6c_root_reachable_citations/patch.py"
    assert hashlib.sha256(r6c.read_bytes()).hexdigest() == R6C_PATCH_SHA256


def test_r6d_function_has_complete_r4_r5d_r6c_source_guards():
    for token in (
        "R4_COMMITTED", "EXPECTED_BLOBS", "transform(path, before)",
        "EXPECTED_GIT_BLOBS", "MODEL", "RENDERER",
        "r6c_expected_sha256", "transform_r6c(path, before)",
        "phase169_r10a_verified_stable_chain_projection/projection.py",
    ):
        assert token in FUNCTION


def test_r6d_reviewed_full_sources_are_replayable():
    actual = (Path(__file__).resolve().parents[1] / "reviewed_sources/r6_audit_AFTER_FULL.py").read_bytes()
    assert transform_r6_audit(ORIGINAL.read_bytes()) == actual
    function = (Path(__file__).resolve().parents[1] / "reviewed_sources/certify_reviewed_production_AFTER_FULL.py").read_text(encoding="utf-8")
    assert whole_function(actual) == function
