"""Phase R10ET-R5 deterministic, full-function guarded source patch tests."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase169_r10et_r5_common_definition_provider.patch import (
    EXPECTED_BLOBS,
    NEW_EXPAND_START,
    OLD_FALLBACK,
    PROVIDER,
    REPLACEMENTS,
    complete_function,
    git_blob,
    git_bytes,
    transform,
)


def test_r5_changes_only_the_complete_shared_provider():
    root = Path(__file__).resolve().parents[2]
    original = git_bytes(root, PROVIDER)
    assert git_blob(original) == EXPECTED_BLOBS[PROVIDER]
    revised, functions = transform(PROVIDER, original)
    assert list(functions) == ["shared_expansion_provider"]
    method = functions["shared_expansion_provider"]
    assert NEW_EXPAND_START in method
    assert OLD_FALLBACK not in method
    assert revised.decode("utf-8").count("def shared_expansion_provider(") == 1
    assert "def expand(goal: object)" in method
    tree = ast.parse(revised.decode("utf-8"))
    assert tree is not None
    before = original.decode("utf-8").replace("\r\n", "\n")
    after = revised.decode("utf-8").replace("\r\n", "\n")
    assert after.replace(method, complete_function(before, "shared_expansion_provider"), 1) == before


@pytest.mark.parametrize("path", tuple(path for path in EXPECTED_BLOBS if path != PROVIDER))
def test_r5_related_test_changes_are_full_functions_or_fixture_only(path):
    root = Path(__file__).resolve().parents[2]
    original = git_bytes(root, path)
    changed, full_functions = transform(path, original)
    assert changed != original
    assert git_blob(original) == EXPECTED_BLOBS[path]
    if path.endswith("test_r10el_live.py"):
        assert "(24, 9, \"direct_sum\", 13, 39)" in changed.decode("utf-8")
        assert not full_functions
    else:
        assert full_functions
        for name, text in full_functions.items():
            assert "def " + name + "(" in text
            assert text == complete_function(changed.decode("utf-8"), name)


def test_r5_refuses_unreviewed_bytes():
    with pytest.raises(RuntimeError, match="unreviewed or modified"):
        transform(PROVIDER, b"# not the reviewed shared provider\n")
    assert len(REPLACEMENTS[PROVIDER]) == 2
