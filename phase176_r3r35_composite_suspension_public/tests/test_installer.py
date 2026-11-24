"""Installer guard tests: no dependency on a full project import graph."""
from __future__ import annotations

import ast
import pytest

from phase176_r3r35_composite_suspension_public.installer import (
    MARKER,
    PATCH,
    proposed_code,
    changed_function_text,
)


def baseline() -> str:
    return (
        "def shared_expansion_provider(bridge):\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + MARKER + "\n"
        "        return tuple(options)\n"
        "    return expand\n"
    )


def test_patch_adds_exactly_one_nested_provider() -> None:
    revised = proposed_code(baseline())
    ast.parse(revised)
    assert revised.count("options.extend(expand_composite_suspension_equality(goal))") == 1
    assert PATCH in revised
    assert "def shared_expansion_provider(" in changed_function_text(revised)


def test_patch_is_idempotent() -> None:
    revised = proposed_code(baseline())
    assert proposed_code(revised) == revised


def test_patch_rejects_missing_or_external_anchor() -> None:
    with pytest.raises(ValueError, match="EXPECTED_ONE_R3R31_ANCHOR"):
        proposed_code("def shared_expansion_provider():\n    return None\n")
    wrong = (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        return ()\n"
        "    return expand\n\n"
        "def unrelated():\n"
        + MARKER + "\n"
    )
    with pytest.raises(ValueError, match="R3R31_ANCHOR_OUTSIDE_NESTED_EXPAND"):
        proposed_code(wrong)


def test_patch_rejects_conflicting_insertion() -> None:
    incorrect = baseline() + "\n# expand_composite_suspension_equality(goal)\n"
    with pytest.raises(ValueError, match="CONFLICTING_R3R35_PATCH"):
        proposed_code(incorrect)
