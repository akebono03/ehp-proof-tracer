"""No application source may be patched without matching audited Git blob content."""
from __future__ import annotations

import ast
import pytest

from phase169_r4g_hopf_reference.apply import (
    BLOBS,
    CLASS_NEW,
    VERIFY_FUNCTION,
    git_blob,
    source_matches_blob,
    replace_exact,
)


def test_r4g_patch_is_bound_to_two_reviewed_files():
    assert set(BLOBS) == {
        "phase165_r52_r27_r5_literature.py",
        "phase168_r3_37c_reference_projection.py",
    }
    assert len(set(BLOBS.values())) == 2


def test_r4g_class_and_verifier_are_complete_python():
    source = "from dataclasses import dataclass\nfrom pathlib import Path\n" + CLASS_NEW + "\n" + VERIFY_FUNCTION
    ast.parse(source)
    assert "preceding_hopf_fibration_dimensions" in CLASS_NEW
    assert "Steenrod1951" in VERIFY_FUNCTION


def test_r4g_missing_anchor_rejected():
    with pytest.raises(RuntimeError, match="missing or ambiguous"):
        replace_exact("not expected source", "missing", "injected")
    with pytest.raises(RuntimeError, match="missing or ambiguous"):
        replace_exact("two two", "two", "injected")


def test_r4g_git_blob_checksum_sensitive_to_edit():
    expected = git_blob("a\r\nb\r\n")
    assert source_matches_blob("a\nb\n", expected)
    assert not source_matches_blob("a\nb changed\n", expected)
