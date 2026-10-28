"""Ensure only the two reviewed existing functions change."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase169_r10en_shared_citation_provenance.patch import (
    FILES,
    PACKAGE,
    checked_change,
)


@pytest.mark.parametrize("relative,before_name,after_name", FILES)
def test_r10en_patch_replays_exact_reviewed_file(relative, before_name, after_name):
    before = (PACKAGE / before_name).read_bytes()
    after = (PACKAGE / after_name).read_bytes()
    assert checked_change(relative, before) == after
    assert before != after
    assert ast.parse(before.decode("utf-8"))
    assert ast.parse(after.decode("utf-8"))


@pytest.mark.parametrize("relative,before_name,after_name", FILES)
def test_r10en_rejects_changed_target_bytes(relative, before_name, after_name):
    before = (PACKAGE / before_name).read_bytes()
    with pytest.raises(ValueError, match="source mismatch"):
        checked_change(relative, before + b"\n# external edit\n")


def test_r10en_rejects_unlisted_target():
    with pytest.raises(ValueError, match="not an R10EN reviewed target"):
        checked_change("phase168_r3_5_model_renderer.py", b"other")


def test_r10en_exports_full_functions():
    names = (
        ("r10a_after.py.FULL", "project_verified_stable_image_chain"),
        ("r10ec_after.py.FULL", "project_verified_direct_sum_transport"),
    )
    for name, function_name in names:
        source = (PACKAGE / name).read_text(encoding="utf-8")
        tree = ast.parse(source)
        node = next(node for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == function_name)
        lines = source.splitlines(keepends=True)
        expected = "".join(lines[node.lineno - 1:node.end_lineno])
        assert expected == (PACKAGE / f"{function_name}_FULL.py").read_text(
            encoding="utf-8"
        )
