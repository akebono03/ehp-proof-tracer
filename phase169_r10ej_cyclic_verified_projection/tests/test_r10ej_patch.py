"""R10EJ patch integrity, exact anchors, encoding and single-function scope."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase169_r10ej_cyclic_verified_projection.patch import (
    NEW_HIDDEN,
    NEW_TEX,
    OLD_HIDDEN,
    OLD_TEX,
    REVIEWED_GIT_BLOB,
    _git_blob,
    transform,
)


@pytest.fixture(scope="module")
def reviewed_source() -> bytes:
    path = Path(__file__).resolve().parents[1] / "_github_r10a_source_verified.py"
    return path.read_bytes()


def test_r10ej_reviewed_source_git_blob(reviewed_source):
    assert _git_blob(reviewed_source) == REVIEWED_GIT_BLOB


def test_r10ej_complete_function_and_no_other_changes(reviewed_source):
    updated, complete_function = transform(reviewed_source)
    ast.parse(updated)
    assert NEW_TEX in complete_function
    assert NEW_HIDDEN in complete_function
    assert OLD_TEX not in complete_function
    assert OLD_HIDDEN not in complete_function
    assert "def project_verified_stable_image_chain" in complete_function
    assert updated != reviewed_source


def test_r10ej_crlf_is_preserved(reviewed_source):
    edited, complete_function = transform(reviewed_source.replace(b"\n", b"\r\n"))
    assert b"\r\n" in edited
    assert b"\n" not in edited.replace(b"\r\n", b"")
    assert "def display_generator_tex" in complete_function


def test_r10ej_refuses_second_application(reviewed_source):
    edited, _ = transform(reviewed_source)
    with pytest.raises(RuntimeError, match="reviewed, unchanged"):
        transform(edited)


def test_r10ej_refuses_modified_blob(reviewed_source):
    with pytest.raises(RuntimeError, match="reviewed, unchanged"):
        transform(reviewed_source.replace(b"Return None rather", b"Return True rather"))


def test_r10ej_refuses_corrupted_anchors(reviewed_source):
    with pytest.raises(RuntimeError, match="anchors changed"):
        transform(reviewed_source.replace(b"    hidden = set(image_indices)",
                                          b"    hidden = set(image_indices)\n    # changed"),
                  require_reviewed=False)
