"""Standalone AST and source-patch checks; no mathematical stubs for evidence."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r9_shared_abstract_renderer.patch_source import (
    BASELINE_BLOB,
    ANCHOR,
    normalized,
    complete_changed_units,
    transform,
)


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "reviewed_source" / "phase165_r52_r3_web_adapter_BASELINE.py.txt"


def test_source_matches_reviewed_git_blob() -> None:
    import subprocess
    result = subprocess.run(("git", "hash-object", str(BASE)),
                            check=True, capture_output=True, text=True)
    assert result.stdout.strip() == BASELINE_BLOB


def test_exactly_one_shared_adapter_hook() -> None:
    source = BASE.read_bytes()
    patched = transform(source)
    assert normalized(patched).count(b"render_certified_abstract_section(result)") == 1
    assert normalized(patched).count(b"_build_group_proof_rendered_lines(markdown)") == 1


def test_full_module_compiles() -> None:
    ast.parse(transform(BASE.read_bytes()).decode("utf-8"))


def test_full_changed_function_is_exported() -> None:
    text = complete_changed_units(BASE.read_bytes())
    assert "def build_partial_web_group_proof_view(" in text
    assert "render_certified_abstract_section(result)" in text
    assert "from phase165_r52_partial_proof import " in text
    assert "return WebGroupProofView(" in text
    assert "```" in text


def test_existing_complete_and_trace_paths_remain() -> None:
    updated = transform(BASE.read_bytes()).decode("utf-8")
    assert 'if mode == "trace":' in updated
    assert 'if result.status is ProofSearchStatus.COMPLETE:' in updated
    assert 'key=("generic-complete-proof" if result.status is ProofSearchStatus.COMPLETE else "generic-partial-proof")' in updated
    assert 'partial_result=(result.status is not ProofSearchStatus.COMPLETE)' in updated


def test_tampered_reviewed_anchor_fails_closed() -> None:
    original = BASE.read_bytes()
    with pytest.raises(RuntimeError, match="Unreviewed"):
        transform(original.replace(ANCHOR.encode(), b"        rendered_lines = ()\n"))


def test_already_patched_source_fails_closed() -> None:
    with pytest.raises(RuntimeError, match="Unreviewed"):
        transform(transform(BASE.read_bytes()))


def test_crlf_patch_preserves_line_endings() -> None:
    source = BASE.read_bytes().replace(b"\n", b"\r\n")
    patched = transform(source)
    assert b"\r\n" in patched
    assert patched.count(b"\r\n") == patched.count(b"\n")
    ast.parse(patched.decode("utf-8"))


def test_mixed_line_endings_fail_closed() -> None:
    mixed = BASE.read_bytes().replace(b"\n", b"\r\n", 1)
    with pytest.raises(RuntimeError, match="Mixed"):
        transform(mixed)


def test_projection_source_has_no_stem_branches() -> None:
    source = (ROOT / "projection.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "k == 31" not in source
    assert "n == 4" not in source
    assert "ProofSearchStatus.COMPLETE" not in source
    assert "public_search" not in source
    assert "GIVEN" not in source
    assert {node.name for node in tree.body if isinstance(node, ast.FunctionDef)} == {
        "abstract_invariants_latex", "render_certified_abstract_section",
    }
