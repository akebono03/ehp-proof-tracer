"""Focused public hookup guardrails."""
from __future__ import annotations

import pytest

from phase176_r3r31_generic_hopf_public_connection.installer import (
    MARKER, NEW_LINES, proposed_code, changed_function_text,
)


def baseline():
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + MARKER + "\n"
        "        return options\n"
        "    return expand\n"
    )


def test_additive_patch_inserts_once() -> None:
    proposed = proposed_code(baseline())
    assert proposed.count("expand_generic_hopf_substitution(goal, tuple(available))") == 1
    assert MARKER in proposed
    assert "def shared_expansion_provider" in changed_function_text(proposed)


def test_patch_rejects_repeated_insertion() -> None:
    with pytest.raises(ValueError, match="ALREADY_APPLIED"):
        proposed_code(proposed_code(baseline()))


def test_patch_rejects_missing_anchor() -> None:
    with pytest.raises(ValueError, match="EXPECTED_SINGLE"):
        proposed_code("def shared_expansion_provider():\n    return None\n")


def test_patch_rejects_outside_function() -> None:
    incorrect = (
        "def shared_expansion_provider():\n"
        "    return None\n"
        "\n"
        "def unrelated():\n"
        "    if True:\n"
        + MARKER + "\n"
        "    return None\n"
    )
    with pytest.raises(ValueError, match="ANCHOR_OUTSIDE_SHARED_PROVIDER"):
        proposed_code(incorrect)


def test_patch_keeps_existing_code_unchanged() -> None:
    initial = baseline()
    result = proposed_code(initial)
    assert result.replace(NEW_LINES, "") == initial
