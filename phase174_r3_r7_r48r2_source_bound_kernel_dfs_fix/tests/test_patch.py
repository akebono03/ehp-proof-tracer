"""R48R2 must only source-bind the existing public R35 rule's domain."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r48r2_source_bound_kernel_dfs_fix.patch import (
    EXPECTED_HASHES,
    PACKAGE,
    TARGETS,
    fragments,
    normalized_sha256,
    pending_replacements,
)


def test_repair_is_limited_to_two_r48_audit_files() -> None:
    assert TARGETS == (
        "phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/audit.py",
        "phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_static.py",
    )
    assert len(EXPECTED_HASHES) == 2
    for path in TARGETS:
        baseline, replacement = fragments(path)
        expected_old, expected_new = EXPECTED_HASHES[path]
        assert normalized_sha256(baseline.read_bytes()) == expected_old
        assert normalized_sha256(replacement.read_bytes()) == expected_new
        assert expected_old != expected_new


def test_source_bound_replacement_retains_mathematical_rule() -> None:
    baseline, replacement = fragments(TARGETS[0])
    old = baseline.read_text(encoding="utf8")
    new = replacement.read_text(encoding="utf8")
    assert "GoalExpansion, SourceBoundGoal" in new
    assert "SourceBoundGoal(conclusion=domain, source=option.subgoals[0])" in new
    assert "rule=expansions[0].rule" in new
    assert "selected.append((domain, diagonal_options))" in new
    assert "GoalExpansion, SourceBoundGoal" not in old
    assert "ProofStep(" not in new
    assert "from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE" in new
    ast.parse(new)
    assert new.replace(
        "    from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal\n", ""
    ).count("from phase165_r14_r6_generic_iso import GeneratorImage") == 1


def test_repair_is_idempotent_and_requires_reviewed_local_bytes(tmp_path: Path) -> None:
    for relative in TARGETS:
        source, revised = fragments(relative)
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(source.read_bytes())
    changes = pending_replacements(tmp_path)
    assert [mode for _, _, mode in changes] == ["REPLACE", "REPLACE"]
    for destination, replacement, _ in changes:
        destination.write_bytes(replacement.read_bytes())
    assert all(mode == "ALREADY_REPAIRED" for _, _, mode in pending_replacements(tmp_path))
    candidate = tmp_path / TARGETS[0]
    candidate.write_text("unreviewed mutation", encoding="utf8")
    import pytest
    with pytest.raises(RuntimeError, match="not the reviewed"):
        pending_replacements(tmp_path)


def test_repair_has_no_full_suite_or_production_mutation() -> None:
    script = (PACKAGE / "run.ps1").read_text(encoding="utf8")
    assert "--dry-run" in script
    assert "phase174_r3_r7_r48_cited_lower_kernel_tree_frontier\\run.ps1" in script
    assert "tests/test_patch.py" in script
    assert "FULL_PYTEST=False" in script
    assert "git reset" not in script
    assert "git clean" not in script
    assert "install.py" not in script
