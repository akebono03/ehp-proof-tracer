"""Self-contained safety tests for Phase 170 R3-R9R2 repair tooling."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from fix_source712 import (
    EXPECTED_CLAUSE,
    build_minimal_replacement,
    run_audit,
    verify_reviewed_toda712,
)


TODA_FIXTURE = (
    "Earlier text\n"
    "\\begin{equation}\n"
    "% \\noindent\n"
    "% \\textbf{(7.12).}\\\n"
    + EXPECTED_CLAUSE
    + "\n\\end{equation}\n"
    "Later text\n"
)
MODULE_FIXTURE = (
    "from __future__ import annotations\n"
    "CLAUSE = r\"\\varepsilon_3\\circ\\nu_{11} = \\nu'\\circ\\bar{\\nu}_6\"\n"
    "\n"
    "def verified_toda712_generator_equality():\n"
    "    vii = 'some cited data'\n"
    "    if vii.count(CLAUSE) != 1:\n"
    "        raise ValueError('reviewed Toda (7.12) equality missing or ambiguous')\n"
    "    return vii.index(CLAUSE)\n"
)


def test_reviewed_equation_is_unique_and_anchored() -> None:
    assert verify_reviewed_toda712(TODA_FIXTURE) == TODA_FIXTURE.index(EXPECTED_CLAUSE)
    with pytest.raises(ValueError):
        verify_reviewed_toda712(TODA_FIXTURE + TODA_FIXTURE)
    with pytest.raises(ValueError):
        verify_reviewed_toda712(TODA_FIXTURE.replace(r"\ov{\nu}", r"\bar{\nu}"))
    with pytest.raises(ValueError):
        verify_reviewed_toda712(TODA_FIXTURE.replace("% \\textbf{(7.12).}", ""))


def test_ast_patch_changes_only_literal_and_preserves_function() -> None:
    changed, result = build_minimal_replacement(MODULE_FIXTURE)
    assert result == "PATCH_REQUIRED"
    assert ast.literal_eval(next(
        item.value for item in ast.parse(changed).body
        if isinstance(item, ast.Assign) and any(
            isinstance(name, ast.Name) and name.id == "CLAUSE" for name in item.targets
        )
    )) == EXPECTED_CLAUSE
    assert changed.endswith(MODULE_FIXTURE.split("def verified_toda712_generator_equality():", 1)[1])
    unchanged, status = build_minimal_replacement(changed)
    assert unchanged == changed
    assert status == "ALREADY_ALIGNED"


def test_fails_closed_when_source_verifier_guard_missing() -> None:
    with pytest.raises(ValueError, match="guard"):
        build_minimal_replacement(MODULE_FIXTURE.replace("vii.count(CLAUSE) != 1", "True"))


def test_audit_and_apply_on_isolated_fixture(tmp_path: Path) -> None:
    tex = tmp_path / "sources" / "toda" / "Toda_07_2.tex"
    module = tmp_path / "phase170_r3_r9_toda712_cited_rewrite" / "source712.py"
    tex.parent.mkdir(parents=True)
    module.parent.mkdir(parents=True)
    tex.write_text(TODA_FIXTURE, encoding="utf-8")
    module.write_text(MODULE_FIXTURE, encoding="utf-8")
    assert run_audit(tmp_path)["status"] == "PATCH_REQUIRED"
    assert module.read_text(encoding="utf-8") == MODULE_FIXTURE
    assert run_audit(tmp_path, apply=True)["status"] == "PATCHED"
    assert run_audit(tmp_path)["status"] == "ALREADY_ALIGNED"
    assert "def verified_toda712_generator_equality():" in module.read_text(encoding="utf-8")
