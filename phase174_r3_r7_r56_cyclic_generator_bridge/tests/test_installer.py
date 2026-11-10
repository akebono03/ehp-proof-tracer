"""Reviewed patch scope, idempotence, fail-closed guards, and syntax tests."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r56_cyclic_generator_bridge.install import (
    PINNED_SHA,
    PROVIDER_AFTER,
    PROVIDER_BEFORE,
    SHARED_SEARCH_AFTER,
    SHARED_SEARCH_BEFORE,
    _git_blob,
    _normalize,
    _replace_once,
    patch_shared,
)


def _fixture_source() -> str:
    return (
        "def shared_expansion_provider():\n"
        + PROVIDER_BEFORE
        + "    return extra_providers\n\n"
        + "def search_shared_group_goal():\n"
        + SHARED_SEARCH_BEFORE
        + "    )\n"
    )


def test_common_patch_adds_both_rules_and_nonzero_source_bound_provider() -> None:
    updated = patch_shared(_fixture_source())
    ast.parse(updated)
    assert "expand_cyclic_generator_from_hopf" in updated
    assert "expand_delta_surjectivity_from_generator" in updated
    assert "build_public_source_bound_kernel_provider" in updated
    assert updated.count("expand_upper_delta_surjectivity") == 1


def test_patch_rejects_missing_or_repeated_anchor() -> None:
    with pytest.raises(RuntimeError):
        patch_shared("def nothing():\n    return None\n")
    with pytest.raises(RuntimeError):
        _replace_once("same same", "same", "new", "duplicate")


def test_file_eol_preserved_with_no_sha_normalization() -> None:
    raw = b"first\r\nsecond\r\n"
    content, bom, style = _normalize(raw)
    assert content == "first\nsecond\n"
    assert bom == b""
    assert style == "\r\n"
    assert _git_blob(raw) != _git_blob(raw.replace(b"\r\n", b"\n"))
    assert len(PINNED_SHA) == 40


def test_no_group_specific_narrative_or_direct_given_added() -> None:
    root = Path(__file__).resolve().parents[1]
    source = (root / "rule.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "ProofRule.GIVEN" in source
    assert "GIVEN" not in {x.id for x in ast.walk(tree) if isinstance(x, ast.Name)}
    assert "render_" not in source
    assert "n == 6" not in source
    assert "k == 5" not in source
    assert "ProofStep(" not in source


def test_only_shared_provider_is_existing_production_patch_target() -> None:
    root = Path(__file__).resolve().parents[1]
    installer = (root / "install.py").read_text(encoding="utf-8")
    assert 'SHARED = "phase165_r52_r9_shared_math.py"' in installer
    assert "git reset" not in installer
    assert "git checkout" not in installer
