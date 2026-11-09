"""Offline-verifiable pure audit helper tests, with no repository imports."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r31_delta_surjectivity_general_audit.audit import (
    DEPENDENCIES, END, START, SUPPORTING,
    git_blob_sha, inspect_toda_source, matches_pinned_blob,
)


def fixture_toda_proof() -> str:
    before = r"\Delta(\iota_{11})=\nu_5\circ\eta_8"
    proof = "\n".join(token for _, token in DEPENDENCIES)
    sources = "\n".join(SUPPORTING)
    return before + "\n" + START + "\n" + sources + "\n" + proof + "\n" + END


def test_pure_blob_hash_variants():
    raw = b"first\nsecond\n"
    sha = git_blob_sha(raw)
    assert matches_pinned_blob(raw.replace(b"\n", b"\r\n"), sha)
    assert not matches_pinned_blob(b"tampered", sha)


def test_synthetic_toda_dependencies_pass():
    value = inspect_toda_source(fixture_toda_proof())
    assert value["independent_source_verified"] is True
    assert value["lower_delta_requires_independent_kernel_proof"] is True


def test_missing_hopf_relation_fails_closed():
    source = fixture_toda_proof().replace(DEPENDENCIES[3][1], "missing", 1)
    with pytest.raises(ValueError, match="prop27_typed_witness"):
        inspect_toda_source(source)
