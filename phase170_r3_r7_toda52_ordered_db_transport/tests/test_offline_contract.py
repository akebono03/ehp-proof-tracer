"""Offline integrity checks; these require no network or project installation."""
from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parent
SOURCE = PACKAGE / "replacement" / "phase168_r2_toda52_transport.py"
ORIGINAL_SHA256 = "52a89e1ab91313c33d36253d1ce67075154503934ad5fe83d5fdf08916230afe"


def test_r3r7_complete_source_is_compilable_and_contains_all_functions() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    compile(text, str(SOURCE), "exec")
    tree = ast.parse(text)
    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert functions.count("expand_toda52_finite_cyclic_goal") == 1
    for name in (
        "_expand_toda52_screened_cyclic_goal",
        "_eta2_inverse_image",
        "_toda52_group_presentation_matches",
        "_toda52_ordered_db_rule",
    ):
        assert functions.count(name) == 1


def test_r3r7_existing_math_is_not_rewritten() -> None:
    original = (PACKAGE / "baseline" / "phase168_r2_toda52_transport.py").read_bytes()
    assert sha256(original).hexdigest() == ORIGINAL_SHA256
    after = SOURCE.read_text(encoding="utf-8")
    before = original.decode("utf-8")
    assert after.startswith(before.replace(
        "def expand_toda52_finite_cyclic_goal(",
        "def _expand_toda52_screened_cyclic_goal(",
        1,
    ).rstrip())


def test_r3r7_script_is_complete_and_rollback_is_explicit() -> None:
    code = (PACKAGE / "runner.py").read_text(encoding="utf-8")
    tree = ast.parse(code)
    assert any(isinstance(node, ast.FunctionDef) and node.name == "run" for node in tree.body)
    assert "target.write_bytes(original)" in code
    assert "PHASE170_R3R7_ROLLBACK" in code
    assert "git(root, \"rev-parse\"" in code
    assert "FULL_PYTEST=False" in code


def test_r3r7_no_unrelated_production_replacement() -> None:
    replacements = list((PACKAGE / "replacement").rglob("*.py"))
    assert [file.name for file in replacements] == ["phase168_r2_toda52_transport.py"]


def test_r3r7_n2_degrees_require_earlier_db_and_original_theorem() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    assert "precedes_db_goal(source_n, source_k, n, k)" in text
    assert "exact_prior_database_result(source_n, source_k)" in text
    assert "_toda52_theorem_is_exact(item)" in text
    assert "dimension < 6" in text
    assert "source, theorem" in text
