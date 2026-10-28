"""Local transformation guards, independent of the user's checkout."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from patch import git_blob, patch_model, patch_renderer, replace_once, transform, MODEL


def test_r6c_git_blob_is_git_compatible():
    raw = b"hello\n"
    assert git_blob(raw) == hashlib.sha1(b"blob 6\0hello\n").hexdigest()


def test_r6c_model_two_exact_anchors_are_transformed():
    source = (
        "def build_proof_narrative_model(\n    result,\n):\n"
        "    # Locator is the printed source position. Labels are presentation metadata,\n"
        "    for step_index, step in enumerate(steps):\n"
        "        linked: list[tuple[LiteratureReference, str | None, str | None]] = []\n"
    )
    patched = patch_model(source)
    assert patched.count("def root_ancestor_step_indices(") == 1
    assert "if step_index not in citation_scope:" in patched
    assert "result.status is ProofSearchStatus.COMPLETE" in patched


def test_r6c_renderer_changes_only_completed_order():
    source = (
        "    from phase168_r3_29_order_projection import project_narrative_order\n"
        "    else:\n"
        "        chains = project_exactness_chains(model)\n"
        "        suppressed_exactness = {index for chain in chains for index in chain.step_indices}\n"
        "        order = tuple(entry.step_index for entry in project_narrative_order(model, suppressed_exactness))\n"
        "        lines = [\"使用する結果\", \"\"]\n"
    )
    patched = patch_renderer(source)
    assert "if entry.step_index in root_scope" in patched
    assert "if all(index in root_scope for index in chain.step_indices)" in patched
    assert patched.count("root_ancestor_step_indices") == 2


def test_r6c_anchor_mismatch_fails_closed():
    with pytest.raises(RuntimeError,match="expected one exact anchor"):
        replace_once("x", "not here", "replacement", "synthetic")
    with pytest.raises(RuntimeError,match="source guard failed"):
        transform(MODEL,b"invalid")
