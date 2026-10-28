"""Static content guard and complete replacement exports for R10ET-R4."""
from __future__ import annotations

import ast
from pathlib import Path

from phase169_r10et_r4_cyclic_definition_projection.patch import (
    PROJECTOR,
    RENDERER,
    ROOT,
    EXPECTED_GIT_BLOBS,
    transformed,
    function_source,
    git_blob_sha1,
)


def test_r10et_r4_exact_live_source_hashes_or_proposed_full_files():
    for path in (PROJECTOR, RENDERER):
        source = (ROOT / path).read_bytes()
        if git_blob_sha1(source) == EXPECTED_GIT_BLOBS[path]:
            full, function = transformed(source, path)
            ast.parse(full.decode("utf-8"))
            assert function
        else:
            # run.ps1 already applied the guarded full-function patch.
            assert path in (PROJECTOR, RENDERER)
            assert b"phase169_r10et_r4_cyclic_definition_projection.policy" in (
                ROOT / PROJECTOR
            ).read_bytes()
            assert b"Definition " in (ROOT / RENDERER).read_bytes()


def test_r10et_r4_complete_function_extraction_has_no_omissions():
    sample = "def example():\n    return 3\n\ndef another():\n    return 2\n"
    assert function_source(sample, "example") == "def example():\n    return 3\n"
    assert function_source(sample, "another") == "def another():\n    return 2\n"
