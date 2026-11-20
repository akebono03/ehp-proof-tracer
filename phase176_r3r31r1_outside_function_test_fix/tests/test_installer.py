"""Focused regression for the R3R31R1 test-only fix."""
from __future__ import annotations

import ast
import pytest

from phase176_r3r31r1_outside_function_test_fix.installer import (
    OLD_FUNCTION, NEW_FUNCTION, replace_test,
)


def test_original_replaced_and_replacement_parses() -> None:
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    source = (root / "phase176_r3r31_generic_hopf_public_connection"
              / "tests" / "test_installer.py").read_text(encoding="utf-8-sig")
    assert source.count(NEW_FUNCTION) == 1
    assert source.count(OLD_FUNCTION) == 0
    ast.parse(source)


def test_idempotent_replacement() -> None:
    assert replace_test(NEW_FUNCTION) == NEW_FUNCTION


def test_unrelated_text_fails_closed() -> None:
    with pytest.raises(ValueError, match="BASELINE_MISMATCH"):
        replace_test("def unrelated():\n    pass\n")
