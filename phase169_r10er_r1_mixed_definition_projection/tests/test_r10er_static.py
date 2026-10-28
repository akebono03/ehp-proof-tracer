"""Self-contained exact-source and complete-function checks."""
from __future__ import annotations

import ast

import pytest

from phase169_r10er_r1_mixed_definition_projection.patch import (
    GIT_BLOB_SHA1,
    HERE,
    function_span,
    git_blob_hash,
    replacement_content,
)


def test_r10er_source_matches_inspected_git_blob():
    source = (HERE / "projection_reference.py").read_bytes()
    assert git_blob_hash(source) == GIT_BLOB_SHA1
    assert source.decode("utf-8").count("def project_verified_direct_sum_transport(") == 1


def test_r10er_exact_function_and_full_file_exports():
    source = (HERE / "projection_reference.py").read_bytes()
    full_file, full_function = replacement_content(source)
    assert full_file == (HERE / "full_files" / "projection.py").read_bytes()
    assert full_function == (
        HERE / "full_functions" / "project_verified_direct_sum_transport.py"
    ).read_text(encoding="utf-8")
    start, end = function_span(full_file.decode("utf-8"), "project_verified_direct_sum_transport")
    assert full_file.decode("utf-8")[start:end] == full_function
    assert "Definition と" in full_function
    assert "require_each=True" in full_function
    ast.parse(full_file.decode("utf-8"))


def test_r10er_no_import_or_class_changes():
    before = (HERE / "projection_reference.py").read_text(encoding="utf-8")
    after = (HERE / "full_files" / "projection.py").read_text(encoding="utf-8")
    left = ast.parse(before)
    right = ast.parse(after)
    def declarations(tree):
        return [ast.unparse(node) for node in tree.body
                if isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef))]
    assert declarations(left) == declarations(right)


def test_r10er_fail_closed_when_unreviewed_source_changes():
    source = (HERE / "projection_reference.py").read_bytes()
    with pytest.raises(RuntimeError, match="Git blob SHA1 differs"):
        replacement_content(source + b"# unrelated modification\n")
