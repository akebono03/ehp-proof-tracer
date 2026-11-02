"""Installer-only tests; no production module imports or Git mutation."""
from __future__ import annotations

import ast

import pytest

from phase173_r4_r1_public_connection.install import (
    ANCHOR, HOOK, EXPECTED_TARGET_BLOB,
    blob_hash, normalize, restored_source, transform,
)


def test_transform_inserts_single_hook_inside_whole_function() -> None:
    original = (
        "def search_shared_group_goal():\n"
        "    if bridge is None:\n"
        "        bridge = build_shared_typed_bridge()\n"
        "    assertions = tuple(bridge.registry._assertions.values())\n"
        "    return assertions\n"
    )
    assert ANCHOR in original
    result = transform(original)
    assert result.count(HOOK) == 1
    assert "    return assertions\n" in result
    ast.parse(result)


def test_transform_rejects_duplicate_hook() -> None:
    original = (
        "def search_shared_group_goal():\n"
        "    if bridge is None:\n"
        "        bridge = build_shared_typed_bridge()\n"
        + HOOK +
        "    assertions = tuple(bridge.registry._assertions.values())\n"
    )
    with pytest.raises(RuntimeError, match="already exists"):
        transform(original)


def test_transform_refuses_another_named_function() -> None:
    source = (
        "def different_function():\n"
        "    if bridge is None:\n"
        "        bridge = build_shared_typed_bridge()\n"
        "    assertions = tuple(bridge.registry._assertions.values())\n"
    )
    with pytest.raises(RuntimeError, match="canonical search"):
        transform(source)


def test_transform_rejects_ambiguous_anchor() -> None:
    source = (
        "def search_shared_group_goal():\n"
        "    if bridge is None:\n"
        "        bridge = build_shared_typed_bridge()\n"
        "    assertions = tuple(bridge.registry._assertions.values())\n"
        "    if bridge is None:\n"
        "        bridge = build_shared_typed_bridge()\n"
        "    assertions = tuple(bridge.registry._assertions.values())\n"
    )
    with pytest.raises(RuntimeError, match="exactly once"):
        transform(source)


def test_normalize_crlf() -> None:
    assert normalize(b"a\r\nb\r\n") == b"a\nb\n"


def test_git_blob_identity_is_not_raw_sha1() -> None:
    from hashlib import sha1
    assert blob_hash(b"a\n") != sha1(b"a\n").hexdigest()
    assert len(EXPECTED_TARGET_BLOB) == 40


def test_restoration_refuses_unreviewed_payload() -> None:
    with pytest.raises(RuntimeError, match="unreviewed"):
        restored_source("def x():\n    pass\n" + HOOK)


def test_restoration_requires_unique_hook() -> None:
    with pytest.raises(RuntimeError, match="absent or duplicated"):
        restored_source("def x():\n    pass\n")
    with pytest.raises(RuntimeError, match="absent or duplicated"):
        restored_source(HOOK + HOOK)


def test_actual_reviewed_function_anchor_and_dependency() -> None:
    from pathlib import Path
    here = Path(__file__).resolve().parents[2]
    source_file = here / "phase165_r52_r9_shared_math.py"
    if not source_file.exists():
        pytest.skip("Production source is checked in the target repository")
    src = source_file.read_bytes()
    text = normalize(src).decode("utf-8")
    if HOOK not in text:
        assert ANCHOR in text
    else:
        assert text.count(HOOK) == 1


def test_full_replacement_function_is_complete_and_consistent() -> None:
    from pathlib import Path
    package = Path(__file__).resolve().parents[1]
    full = (package / "search_shared_group_goal_FULL.py.txt").read_text(encoding="utf-8")
    assert full.count(HOOK) == 1
    assert transform(full.replace(HOOK, "")) == full
    functions = [node for node in ast.parse(full).body if isinstance(node, ast.FunctionDef)]
    assert len(functions) == 1
    assert functions[0].name == "search_shared_group_goal"
