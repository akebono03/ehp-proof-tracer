"""Focused source-integrity contracts of the R4-R13R1 guard update."""
from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path

import pytest

from phase173_r4_r13r1_head_lineage_fix.repair import (
    NEW_SHA256,
    OLD_SHA256,
    AUDIT_PATH,
    replacement_audit,
)


PACKAGE = Path(__file__).resolve().parents[1]
REPOSITORY = PACKAGE.parent


def test_reviewed_replacement_is_compilable_and_content_pinned() -> None:
    original = (REPOSITORY / AUDIT_PATH).read_bytes()
    fixture = (PACKAGE / "replacement_audit.py.txt").read_bytes()
    assert sha256(fixture).hexdigest() == NEW_SHA256
    assert sha256(original).hexdigest() in (OLD_SHA256, NEW_SHA256)
    compile(fixture.decode("utf-8"), AUDIT_PATH, "exec")
    if sha256(original).hexdigest() == OLD_SHA256:
        assert replacement_audit(original, fixture) == fixture


def test_other_audit_components_are_unchanged() -> None:
    original = (REPOSITORY / AUDIT_PATH).read_bytes()
    fixture = (PACKAGE / "replacement_audit.py.txt").read_bytes()
    source = original if sha256(original).hexdigest() == OLD_SHA256 else fixture
    before = ast.parse(source.decode("utf-8"))
    after = ast.parse(fixture.decode("utf-8"))
    names = lambda tree: [(type(node).__name__, getattr(node, "name", None))
                          for node in tree.body]
    assert names(before) == names(after)
    assert len([node for node in after.body
                if isinstance(node, ast.FunctionDef)
                and node.name == "source_guard"]) == 1


def test_unreviewed_bytes_are_refused() -> None:
    original = (REPOSITORY / AUDIT_PATH).read_bytes()
    fixture = (PACKAGE / "replacement_audit.py.txt").read_bytes()
    source = original if sha256(original).hexdigest() == OLD_SHA256 else fixture
    with pytest.raises(RuntimeError):
        replacement_audit(source + b"\n# unreviewed\n", fixture)


def test_altered_replacement_is_refused() -> None:
    original = (REPOSITORY / AUDIT_PATH).read_bytes()
    fixture = (PACKAGE / "replacement_audit.py.txt").read_bytes()
    source = original if sha256(original).hexdigest() == OLD_SHA256 else fixture
    with pytest.raises(RuntimeError):
        replacement_audit(source, fixture + b"\n# extra\n")
