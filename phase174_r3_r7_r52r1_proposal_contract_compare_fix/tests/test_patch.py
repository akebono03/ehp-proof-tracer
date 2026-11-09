"""R52R1: source-hash and stable-proposal-comparison regressions."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r52r1_proposal_contract_compare_fix.patch import (
    EXPECTED_HASHES,
    PACKAGE,
    TARGETS,
    bundled_paths,
    normalized_sha256,
    pending_replacements,
)


def test_patch_has_only_two_reviewed_r52_targets() -> None:
    assert TARGETS == (
        "phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py",
        "phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py",
    )
    for relative in TARGETS:
        baseline, replacement = bundled_paths(relative)
        expected_before, expected_after = EXPECTED_HASHES[relative]
        assert normalized_sha256(baseline.read_bytes()) == expected_before
        assert normalized_sha256(replacement.read_bytes()) == expected_after
        ast.parse(replacement.read_text(encoding="utf-8"))


def test_reviewed_patch_is_idempotent_and_rejects_unaudited_input(tmp_path: Path) -> None:
    for relative in TARGETS:
        before, after = bundled_paths(relative)
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(before.read_bytes())
    first = pending_replacements(tmp_path)
    assert len(first) == 2
    assert all(mode == "REPLACE" for _, _, mode in first)
    for destination, replacement, _ in first:
        destination.write_bytes(replacement.read_bytes())
    assert all(mode == "ALREADY_REPAIRED" for _, _, mode in pending_replacements(tmp_path))
    (tmp_path / TARGETS[0]).write_text("unreviewed", encoding="utf-8")
    with pytest.raises(RuntimeError, match="not reviewed"):
        pending_replacements(tmp_path)


def test_audit_checks_stable_contract_not_regenerated_closure_identity() -> None:
    source = (PACKAGE / "replacement/audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "if probe(goal) != original(goal)" not in source
    assert "contract(item) for item in probe(goal)" in source
    assert "contract(item) for item in original(goal)" in source
    assert "rule.premise_patterns, rule.conclusion_pattern" in source
    assert "rule.literature_reference, option.subgoals" in source
    assert "ProofStep(" not in source
    assert not any(
        isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
        and node.value.value is Ellipsis for node in ast.walk(tree)
    )


def test_probe_regression_has_new_guard_comparison_fixture() -> None:
    source = (PACKAGE / "replacement/tests/test_probe.py").read_text(encoding="utf-8")
    assert "test_generated_rule_closure_identity_does_not_change_root_contract" in source
    assert "wrapper(root) == provider(root)" not in source
    assert "wrapper(kernel) == provider(kernel)" not in source
    assert "after[-len(before):] == before" not in source
    assert "proposal_contract(x) for x in wrapper(root)" in source
    assert "proposal_contract(x) for x in after[-len(before):]" in source
    assert "assert first[0].rule.match_guard is not second[0].rule.match_guard" in source
