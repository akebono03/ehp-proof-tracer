"""Pure source-contract tests. Does not touch the production repository."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase173_r4_r15r16r3_staged_guard_fix.patches import (
    PROGRESS_NEW,
    patch_progress,
    patch_test,
)
from phase173_r4_r15r16_verified_progress_punctuation.projection_patch import (
    PROJECTION_OLD, patch_projection,
)


def test_replaces_only_previous_special_progress_prose() -> None:
    original = patch_projection(PROJECTION_OLD)
    modified = patch_progress(original)
    assert modified.count("def _verified_abstract_progress_lines(") == 1
    assert "render_verified_tree_progress(" in modified
    assert "def _render_abstract_claim(" in modified
    assert "len(root.premises) != 4" not in modified
    assert "先行データベースの " not in modified
    compile(modified, "reviewed-progress.py", "exec")


def test_does_not_hardcode_theorems_or_generator_names() -> None:
    source = (Path(__file__).resolve().parents[1] / "tree_adapter.py").read_text(encoding="utf-8")
    for forbidden in ("Proposition 4.4", "Lemma 5.4", "epsilon_4",
                      "len(root.premises) == 4", "sphere_dimension == 4"):
        assert forbidden not in source
    assert "render_model_backed_narrative_markdown(scope, model)" in source
    assert "build_proof_narrative_model(scope)" in source
    assert "status=ProofSearchStatus.PARTIAL" in source


def test_existing_test_is_replaced_with_generic_contract() -> None:
    path = (Path(__file__).resolve().parents[2]
            / "phase173_r4_r15r16_verified_progress_punctuation"
            / "tests" / "test_integration.py")
    original = path.read_text(encoding="utf-8")
    if "assert progress.count(\"先行データベースの \") == 2" in original:
        transformed = patch_test(original)
    else:
        transformed = original
    assert "### 検証済み証明木の Reference" in transformed
    assert "### 検証済み ProofStep" in transformed
    compile(transformed, str(path), "exec")


def test_conflicting_source_fails_closed() -> None:
    with pytest.raises(RuntimeError):
        patch_progress("unrelated code")
    with pytest.raises(RuntimeError):
        patch_test("unrelated tests")
