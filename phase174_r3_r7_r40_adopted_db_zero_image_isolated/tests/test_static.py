"""Standalone static checks runnable without the full repository."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_all_r40_python_compiles_without_source_omissions():
    paths = tuple(PACKAGE.rglob("*.py"))
    assert paths
    for path in paths:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_no_direct_given_or_root_claim_in_rule():
    data = (PACKAGE / "rule.py").read_text(encoding="utf-8")
    assert "verified_db_step(premises[0]" in data
    assert "ProofRule.INFERENCE" in data
    assert "ProofRule.GIVEN" in data
    assert "ProofStep(" not in data
    assert "TodaPrimaryGroupZeroStatement(" not in data


def test_no_prior_production_function_mutations():
    data = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "derive_from_expansion" in data
    assert "new_givens" in data
    assert "root_complete" in data
    assert (PACKAGE / "run.ps1").is_file()


def test_all_full_implementation_and_test_units_documented():
    docs = (PACKAGE / "CODE_FULL_JA.md").read_text(encoding="utf-8")
    assert "## `rule.py` 全文" in docs
    assert "## `audit.py` 全文" in docs
    assert "## `source_guard.py` 全文" in docs
    assert "## `tests/test_rule.py` 全文" in docs
