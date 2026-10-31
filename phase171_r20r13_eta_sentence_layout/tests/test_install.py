"""Installer guards and whole-function preservation (no live repository needed)."""
from __future__ import annotations

import ast

import pytest

from phase171_r20r13_eta_sentence_layout.install import OLD, NEW, transform


def test_replaces_exactly_one_complete_renderer_return():
    fixture = 'def renderer():\n' + OLD
    output = transform(fixture)
    assert NEW in output
    assert output.count("format_complete_proof_sentences") == 2
    assert len([x for x in ast.parse(output).body if isinstance(x, ast.FunctionDef)]) == 1


def test_refuses_unreviewed_source_and_duplicate_anchor():
    with pytest.raises(RuntimeError):
        transform("def unrelated():\n    return 1\n")
    with pytest.raises(RuntimeError):
        transform("def renderer():\n" + OLD + OLD)


def test_output_only_changes_renderer_tail():
    fixture = 'def renderer():\n    x = 1\n' + OLD
    changed = transform(fixture)
    assert changed.startswith('def renderer():\n    x = 1\n')
    assert changed.endswith(NEW)


def test_valid_python_source_and_no_proof_engine_patch():
    fixture = 'def renderer():\n' + OLD
    ast.parse(transform(fixture))
    assert "ProofStep(" not in NEW
    assert "GIVEN" not in NEW
