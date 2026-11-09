"""R41 exact one-file patch and no-target-specific-rule static guards."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.source_guard import (
    ANCHOR, INSERT, TARGET, BASE_BLOB, expected_replacement, matches_blob,
)

PACKAGE = Path(__file__).resolve().parents[1]


def test_patch_is_one_callsite_only_and_anchored():
    assert TARGET == "phase165_r52_r9_shared_math.py"
    assert len(BASE_BLOB) == 40
    assert "build_public_adopted_zero_image_provider" in INSERT
    assert "proof_target=proof_target" in INSERT
    assert "    # R4-4 stage4:" in ANCHOR
    assert "GIVEN" in INSERT


def test_no_new_group_specific_result_or_synthetic_givens():
    source = (PACKAGE / "provider.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert not any(isinstance(node, ast.Expr)
                   and isinstance(node.value, ast.Constant)
                   and node.value.value is Ellipsis
                   for node in ast.walk(tree))
    assert "TodaPrimaryGroup(12, 7)" not in source
    assert "ProofStep(" not in source
    assert "ProofRule.INFERENCE" not in source
    assert "add_assertion(" not in source
    assert "expand_source_bound_zero_image_chain" in source


def test_complete_functions_and_scripts_present():
    for filename in ("provider.py", "source_guard.py", "install.py", "audit.py", "run.ps1"):
        assert (PACKAGE / filename).is_file()
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "$DryRun" in script
    assert "pytest" in script
    assert "R40_RULE_REGRESSION" in script


def test_expected_replacement_rejects_unknown_or_already_patched_source():
    import pytest
    with pytest.raises(RuntimeError):
        expected_replacement(b"unreviewed\n" + ANCHOR.encode())
    assert matches_blob(b"any data", BASE_BLOB) is False
