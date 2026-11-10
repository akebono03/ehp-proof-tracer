"""Focused R48R1 regression: only the missing matcher import and guard test."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r48r1_proof_matcher_import_fix.patch import (
    ROOT,
    TARGETS,
    normalized_sha256,
    pending_replacements,
    target_fragments,
)


def test_only_two_audit_files_are_modified() -> None:
    assert TARGETS == (
        "phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/audit.py",
        "phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_static.py",
    )
    before, after = target_fragments(TARGETS[0])
    old = before.read_text(encoding="utf-8")
    new = after.read_text(encoding="utf-8")
    original_import = "    from proof import ProofRule, ProofStep, Relation, RelationType\n"
    revised_import = "\n".join((
        "    from proof import (",
        "        ProofRule,",
        "        ProofStep,",
        "        Relation,",
        "        RelationType,",
        "        find_inference_matches_for_rule,",
        "    )",
        "",
    ))
    assert old.count(original_import) == 1
    assert new.replace(revised_import, original_import) == old
    assert new.count("find_inference_matches_for_rule(") == 1
    ast.parse(new)


def test_only_one_static_regression_was_added() -> None:
    before, after = target_fragments(TARGETS[1])
    old = before.read_text(encoding="utf-8")
    new = after.read_text(encoding="utf-8")
    assert new.startswith(old.rstrip("\n"))
    extension = new[len(old.rstrip("\n")):]
    tree = ast.parse(extension)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert len(functions) == 1
    assert functions[0].name == "test_kernel_diagonal_matcher_is_imported_in_the_audit_function"
    assert "find_inference_matches_for_rule" in extension


def test_repair_is_idempotent_and_pinned_to_expected_files() -> None:
    changes = pending_replacements(ROOT)
    assert len(changes) == 2
    assert all(mode == "ALREADY_REPAIRED" for _, _, mode in changes)
    for destination, replacement, _ in changes:
        assert normalized_sha256(destination.read_bytes()) == normalized_sha256(replacement.read_bytes())


def test_runner_only_runs_r48_and_focused_regressions() -> None:
    script = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in script
    assert "patch --dry-run" in script
    assert "phase174_r3_r7_r48_cited_lower_kernel_tree_frontier\\run.ps1" in script
    assert "--import-mode=importlib" in script
    assert "FULL_PYTEST=False" in script
    assert "git reset" not in script
    assert "git clean" not in script
    assert "install.py" not in script
