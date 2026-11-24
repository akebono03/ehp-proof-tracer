"""Focused regression for the R3R37 minimal public-hook installer."""
from __future__ import annotations

import ast

import pytest

from phase176_r3r37_composite_right_hopf_public.installer import (
    MARKER, PATCH, PATCH_CALL, R3R31_MARKER, changed_function_text,
    proposed_code,
)


def _baseline() -> str:
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + R3R31_MARKER + "\n"
        + MARKER + "\n"
        "        return tuple(options)\n"
        "    return expand\n"
    )


def test_inserts_once_without_changing_prior_hooks() -> None:
    original = _baseline()
    proposed = proposed_code(original)
    assert proposed.replace(PATCH, "", 1) == original
    assert proposed.count(PATCH_CALL) == 1
    assert proposed.count(R3R31_MARKER) == 1
    assert proposed.count(MARKER) == 1
    assert proposed_code(proposed) == proposed
    ast.parse(proposed)
    assert PATCH_CALL in changed_function_text(proposed)


def test_handles_windows_line_endings() -> None:
    original = _baseline().replace("\n", "\r\n")
    changed = proposed_code(original)
    assert changed.count(PATCH_CALL) == 1
    assert proposed_code(changed) == changed
    assert "\n" not in changed.replace("\r\n", "")


def test_missing_r3r35_anchor_fails_closed() -> None:
    with pytest.raises(ValueError, match="R3R35_ANCHOR_NOT_UNIQUE"):
        proposed_code(_baseline().replace(MARKER + "\n", ""))


def test_anchor_outside_nested_expand_fails_closed() -> None:
    original = (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + R3R31_MARKER + "\n"
        "        return tuple(options)\n"
        "    return expand\n"
        "def unrelated():\n"
        "    if True:\n"
        "        options = []\n"
        + MARKER + "\n"
        "        return options\n"
    )
    with pytest.raises(ValueError, match="OUTSIDE_NESTED_EXPAND"):
        proposed_code(original)


def test_duplicate_or_conflicting_patch_fails_closed() -> None:
    proposed = proposed_code(_baseline())
    with pytest.raises(ValueError, match="DUPLICATE_R3R37_PROVIDER"):
        proposed_code(proposed + "\n# " + PATCH_CALL + "\n")
    conflicting = proposed.replace(
        "        # Phase 176 R3R37: source-screened composite-right Hopf candidates.\n",
        "        # changed without review\n",
    )
    with pytest.raises(ValueError, match="CONFLICTING_R3R37_PATCH"):
        proposed_code(conflicting)


def test_non_source_or_duplicate_anchor_fails_closed() -> None:
    with pytest.raises(TypeError, match="source must be str"):
        proposed_code(None)
    duplicate = _baseline().replace(MARKER + "\n", MARKER + "\n" + MARKER + "\n")
    with pytest.raises(ValueError, match="R3R35_ANCHOR_NOT_UNIQUE"):
        proposed_code(duplicate)
