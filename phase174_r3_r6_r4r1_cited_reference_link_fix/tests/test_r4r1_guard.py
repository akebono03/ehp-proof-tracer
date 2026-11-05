"""Read-only contract checks for the two scoped Reference display edits."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r6_r4r1_cited_reference_link_fix.patch import (
    PACKAGE,
    ROOT,
    _normalized_sha256,
    _reapply_eol,
    REVIEWED_R4_SHA256,
    REVIEWED_SOURCE_SHA256,
)


def test_both_originals_match_the_reviewed_local_artifacts() -> None:
    original_ref = (ROOT / "phase174_r3_r6_r4_common_reference" / "output"
                    / "phase168_r3_37c_reference_projection.py.FULL.py")
    original_source = (ROOT / PACKAGE / "output"
                       / "phase174_r3_r6_r4_common_reference__projection.py.BASELINE.py")
    assert _normalized_sha256(original_ref.read_bytes()) == REVIEWED_R4_SHA256
    assert _normalized_sha256(original_source.read_bytes()) == REVIEWED_SOURCE_SHA256


def test_only_one_existing_reference_function_is_replaced() -> None:
    old = (ROOT / "phase174_r3_r6_r4_common_reference" / "output"
           / "phase168_r3_37c_reference_projection.py.FULL.py").read_text(encoding="utf-8")
    new = (ROOT / PACKAGE / "output"
           / "phase168_r3_37c_reference_projection.py.FULL.py").read_text(encoding="utf-8")
    def functions(text: str) -> dict[str, str]:
        tree = ast.parse(text)
        lines = text.splitlines(keepends=True)
        return {
            node.name: "".join(lines[node.lineno - 1:node.end_lineno])
            for node in tree.body if isinstance(node, ast.FunctionDef)
        }
    before, after = functions(old), functions(new)
    assert before.keys() == after.keys()
    assert set(name for name in before if before[name] != after[name]) == {
        "project_cited_proof_step_reference_bodies",
    }
    assert "project_verified_cited_toda_given_reference_body" in after[
        "project_cited_proof_step_reference_bodies"
    ]
    assert before["project_reference_bodies"] == after["project_reference_bodies"]


def test_source_formula_is_shared_between_two_reviewed_reference_paths() -> None:
    old = (ROOT / PACKAGE / "output"
           / "phase174_r3_r6_r4_common_reference__projection.py.BASELINE.py").read_text(encoding="utf-8")
    new = (ROOT / PACKAGE / "output"
           / "phase174_r3_r6_r4_common_reference__projection.py.FULL.py").read_text(encoding="utf-8")
    assert old.count(r"$\Delta(\iota_{2n-1})=0$") == 1
    assert new.count(r"$\Delta(\iota_{2n-1})=0$") == 1
    assert new.count(r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$.") == 1
    assert "verify_extension_texts()" in new
    assert "step.rule is not ProofRule.GIVEN" in new
    assert "source_locator != locator" in new
    ast.parse(new)


def test_preserve_bom_and_crlf_and_reject_mixed_newlines() -> None:
    changed = _reapply_eol(b"\xef\xbb\xbfbefore\r\nafter\r\n", b"before\nchanged\n")
    assert changed == b"\xef\xbb\xbfbefore\r\nchanged\r\n"
    assert _reapply_eol(b"before\nafter\n", b"before\nchanged\n") == b"before\nchanged\n"
    with pytest.raises(ValueError, match="Mixed"):
        _reapply_eol(b"before\r\nafter\n", b"before\nchanged\n")
