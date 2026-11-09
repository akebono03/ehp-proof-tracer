"""R36 guarded replacement and scope tests, requiring no project imports."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r7_r36_cited_kernel_provider_wiring.install import (
    GIT_PINS, TARGET, baseline_source, git_blob_sha,
    patch_source, replacement_source,
)


def test_baseline_matches_reviewed_github_blob() -> None:
    assert git_blob_sha(baseline_source().encode("utf-8")) == GIT_PINS[TARGET]


def test_whole_function_replacement_is_idempotent() -> None:
    expected = replacement_source()
    assert patch_source(baseline_source()) == expected
    assert patch_source(expected) == expected
    ast.parse(expected)


def test_top_level_imports_and_function_signature_unchanged() -> None:
    old, new = ast.parse(baseline_source()), ast.parse(replacement_source())
    assert [ast.dump(item) for item in old.body[:4]] == [
        ast.dump(item) for item in new.body[:4]
    ]
    old_functions = [item for item in old.body if isinstance(item, ast.FunctionDef)]
    new_functions = [item for item in new.body if isinstance(item, ast.FunctionDef)]
    assert len(old_functions) == len(new_functions) == 1
    assert ast.dump(old_functions[0].args) == ast.dump(new_functions[0].args)
    assert new_functions[0].name == "build_context_expansion_provider_registry"


def test_unreviewed_changes_rejected() -> None:
    with pytest.raises(ValueError):
        patch_source(baseline_source().replace("context statements must be tuples", "changed"))
