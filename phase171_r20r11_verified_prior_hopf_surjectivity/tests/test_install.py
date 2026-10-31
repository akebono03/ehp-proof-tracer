"""Offline syntax and content-preservation tests of the small guarded installer."""
from __future__ import annotations

import ast

import pytest

from phase171_r20r11_verified_prior_hopf_surjectivity.install import (
    ADDED_IMPORT,
    NEW_CANDIDATE,
    NEW_SHARED,
    OLD_CANDIDATE,
    OLD_PARAMS,
    OLD_SHARED,
    IMPORT_ANCHOR,
    RULE_ANCHOR,
    git_blob_sha,
    matches_reviewed_blob,
    preserve_file_format,
    transform_shared,
    transform_source,
)


def _synthetic_source() -> str:
    return (
        "from __future__ import annotations\n"
        + IMPORT_ANCHOR
        + "from proof import InferenceRule\n\n"
        + "def cyclic_generator_image_surjectivity_rule():\n"
        + "    return InferenceRule\n\n"
        + RULE_ANCHOR
        + OLD_PARAMS
        + ") -> tuple:\n"
        + "    proposals = []\n"
        + "    for chain in ():\n"
        + "        for source in ():\n"
        + "            group = None\n"
        + "            candidate = None\n"
        + OLD_CANDIDATE
        + "    return tuple(proposals)\n"
    )


def test_source_has_one_new_rule_and_preserves_existing_rule():
    source = _synthetic_source()
    updated = transform_source(source)
    ast.parse(updated)
    assert updated.count(ADDED_IMPORT) == 1
    assert updated.count("def verified_prior_cyclic_generator_image_surjectivity_rule(") == 1
    assert "def cyclic_generator_image_surjectivity_rule():" in updated
    assert updated.count(NEW_CANDIDATE) == 1
    assert "bridge: object = None" in updated
    with pytest.raises(RuntimeError):
        transform_source(updated)


def test_shared_hook_modifies_only_one_callsite():
    source = "def provider():\n    if True:\n" + OLD_SHARED + "        return 1\n"
    updated = transform_shared(source)
    assert updated == source.replace(OLD_SHARED, NEW_SHARED)
    ast.parse(updated)
    with pytest.raises(RuntimeError):
        transform_shared(updated)


def test_crlf_bom_and_lf_source_preserved():
    original = b"\xef\xbb\xbffrom x import y\r\n"
    result = preserve_file_format(original, "from x import z\n")
    assert result == b"\xef\xbb\xbffrom x import z\r\n"
    assert preserve_file_format(b"x\n", "y\n") == b"y\n"


def test_blob_guard_does_not_accept_changed_code():
    expected = git_blob_sha(b"a\nb\n")
    assert matches_reviewed_blob(b"a\nb\n", expected)
    assert matches_reviewed_blob(b"a\r\nb\r\n", expected)
    assert not matches_reviewed_blob(b"a\nb\nchanged\n", expected)
