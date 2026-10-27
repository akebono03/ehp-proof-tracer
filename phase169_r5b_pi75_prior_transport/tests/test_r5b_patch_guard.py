"""Pure guard/AST tests independent of the external project modules."""
from __future__ import annotations

import ast

import pytest

from phase169_r5b_pi75_prior_transport.patch import OLD, NEW, build_patched_provider, full_function


def test_r5b_patch_inserts_only_one_reference_to_adapter():
    fixture = "def shared_expansion_provider():\n    def expand(goal):\n" + OLD + "        return options\n    return expand\n"
    patched = build_patched_provider(fixture.encode(), fixture.encode())
    assert patched.decode().count("expand_prior_cited_toda45_composite_transport(") == 1
    assert patched.decode().count("expand_cited_toda45_composite_transport(") == 1
    ast.parse(patched)
    assert "shared_expansion_provider" in full_function(patched)


def test_r5b_patch_rejects_unreviewed_worktree():
    fixture = "def shared_expansion_provider():\n    def expand(goal):\n" + OLD + "        return options\n    return expand\n"
    with pytest.raises(RuntimeError, match="differs"):
        build_patched_provider((fixture + "# Modified!\n").encode(), fixture.encode())


def test_r5b_patch_rejects_duplicate_or_missing_anchor():
    fixture = "def shared_expansion_provider():\n    def expand(goal):\n" + OLD + "        return options\n    return expand\n"
    with pytest.raises(RuntimeError, match="anchor"):
        build_patched_provider(fixture.replace(OLD, "").encode(), fixture.replace(OLD, "").encode())
    with pytest.raises(RuntimeError, match="anchor"):
        build_patched_provider(fixture.replace(OLD, OLD + OLD).encode(), fixture.replace(OLD, OLD + OLD).encode())
