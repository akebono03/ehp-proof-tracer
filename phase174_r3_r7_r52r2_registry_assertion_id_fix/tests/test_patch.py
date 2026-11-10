"""R52R2 regression tests: dictionary keys must not be treated as assertion values."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r52r2_registry_assertion_id_fix.patch import (
    EXPECTED_HASHES, PACKAGE, TARGETS, normalized_sha256,
    pending_replacements, reviewed_paths,
)


def test_reviewed_targets_are_audit_and_static_test_only() -> None:
    assert TARGETS == (
        "phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py",
        "phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_static.py",
    )
    assert len(EXPECTED_HASHES) == 2
    for relative in TARGETS:
        baseline, replacement = reviewed_paths(relative)
        assert normalized_sha256(baseline.read_bytes()) == EXPECTED_HASHES[relative][0]
        assert normalized_sha256(replacement.read_bytes()) == EXPECTED_HASHES[relative][1]


def test_registry_lookup_uses_assertion_values_and_is_python310_compatible() -> None:
    source = (PACKAGE / "replacement/audit.py").read_text(encoding="utf-8")
    ast.parse(source, feature_version=(3, 10))
    assert (
        "next(iter(original_bridge.registry._assertions.values())).assertion_id"
        in source
    )
    assert (
        "next(iter(original_bridge.registry._assertions)).assertion_id"
        not in source
    )
    class Assertion:
        def __init__(self, assertion_id: str) -> None:
            self.assertion_id = assertion_id
    items = {"string-key": Assertion("linked-assertion")}
    assert next(iter(items.values())).assertion_id == "linked-assertion"


def test_guard_rejects_unreviewed_file(tmp_path: Path) -> None:
    for relative in TARGETS:
        before, _ = reviewed_paths(relative)
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(before.read_bytes())
    statuses = pending_replacements(tmp_path)
    assert all(mode == "REPLACE" for _, _, mode in statuses)
    first, _, _ = statuses[0]
    first.write_text("# tampered", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Unreviewed R52 working file"):
        pending_replacements(tmp_path)


def test_patch_idempotence(tmp_path: Path) -> None:
    for relative in TARGETS:
        before, after = reviewed_paths(relative)
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(before.read_bytes())
        assert normalized_sha256(target.read_bytes()) == normalized_sha256(before.read_bytes())
        target.write_bytes(after.read_bytes())
    results = pending_replacements(tmp_path)
    assert all(mode == "ALREADY_REPAIRED" for _, _, mode in results)


def test_regression_is_a_full_test_function_in_the_r52_static_module() -> None:
    source = (PACKAGE / "replacement/tests/test_static.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert any(
        isinstance(node, ast.FunctionDef)
        and node.name == "test_citing_id_comes_from_registry_assertion_value_not_dict_key"
        for node in tree.body
    )
    assert all(node.value is not Ellipsis for node in ast.walk(tree) if isinstance(node, ast.Constant))
