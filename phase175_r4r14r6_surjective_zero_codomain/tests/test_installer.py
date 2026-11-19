"""No repeat patch, no unreviewed source, no premature completion."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r14r6_surjective_zero_codomain.installer import (
    ANCHOR, INSERT, next_source,
)


def test_anchor_adds_once_and_retains_old_delta_route() -> None:
    before = (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        build_public_composite_zero_transport_provider(bridge)\n"
        + ANCHOR + "\n"
        "        return ()\n"
        "    return expand\n"
    )
    after = next_source(before)
    assert after.count(INSERT) == 1
    assert ANCHOR in after
    ast.parse(after)
    assert next_source(after) == after


def test_changed_anchor_fails_closed() -> None:
    with pytest.raises(RuntimeError, match="EXPECTED_EHP_ROOT_ANCHOR_MISSING"):
        next_source("def unrelated():\n    return None\n")


def test_no_source_or_group_given_is_inserted() -> None:
    assert "GIVEN" not in INSERT
    assert "Toda (5.9)" not in INSERT
    assert "pi_10" not in INSERT
    assert "expand_surjective_zero_codomain(goal)" in INSERT
