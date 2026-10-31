"""R20R13R2 installer guard tests; no live target mutation."""
from __future__ import annotations

import ast
import hashlib

import pytest

from phase171_r20r13r2_multiple_blank_eta_merge.install import (
    CORRECTED_SHA256, ORIGINAL_SHA256, transform,
)
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def test_exact_reviewed_source_hashes_and_compilation():
    original = (HERE / "reviewed_projection.py").read_text(encoding="utf-8")
    corrected = (HERE / "corrected_projection.py").read_text(encoding="utf-8")
    assert hashlib.sha256(original.encode("utf-8")).hexdigest() == ORIGINAL_SHA256
    assert hashlib.sha256(corrected.encode("utf-8")).hexdigest() == CORRECTED_SHA256
    assert transform(original) == corrected
    ast.parse(corrected)


def test_unreviewed_anchors_fail_closed():
    with pytest.raises(RuntimeError):
        transform("def unrelated():\n    return None\n")


def test_only_whitespace_separator_walk_changed():
    original = (HERE / "reviewed_projection.py").read_text(encoding="utf-8")
    corrected = transform(original)
    assert original.count("def combine_adjacent_verified_eta_sentences") == 1
    assert corrected.count("def combine_adjacent_verified_eta_sentences") == 1
    assert original.split("def combine_adjacent_verified_eta_sentences")[0] == corrected.split("def combine_adjacent_verified_eta_sentences")[0]
    assert "ProofStep(" not in corrected


def test_does_not_change_verified_citation_eligibility():
    original = (HERE / "reviewed_projection.py").read_text(encoding="utf-8")
    corrected = transform(original)
    first = original.split("def combine_adjacent_verified_eta_sentences")[0]
    assert first == corrected.split("def combine_adjacent_verified_eta_sentences")[0]
    assert "verified_eta_display_sentences(model)" in corrected
