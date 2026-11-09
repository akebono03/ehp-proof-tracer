"""Standalone guard for the sole changed R40 test function."""
from __future__ import annotations

import ast
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1]
BASELINE = FOLDER / "baseline/test_rule.py"
REPLACEMENT = FOLDER / "replacement/test_rule.py"
TEST_NAME = "test_direct_given_for_generator_zero_is_rejected"


def test_only_one_test_function_changes() -> None:
    before = ast.parse(BASELINE.read_text(encoding="utf-8"))
    after = ast.parse(REPLACEMENT.read_text(encoding="utf-8"))
    assert len(before.body) == len(after.body)
    changed = []
    for old, new in zip(before.body, after.body):
        if ast.dump(old, include_attributes=False) != ast.dump(new, include_attributes=False):
            assert isinstance(old, ast.FunctionDef)
            assert isinstance(new, ast.FunctionDef)
            assert old.name == new.name
            changed.append(old.name)
    assert changed == [TEST_NAME]


def test_forged_given_rejection_is_preserved() -> None:
    changed = REPLACEMENT.read_text(encoding="utf-8")
    assert "find_inference_matches_for_rule(rule, (db, forged)) == ()" in changed
    assert "find_inference_matches_for_rule(rule, (forged, db)) == ()" in changed
    assert "find_inference_matches_for_rule(rule, (db,)) == ()" in changed


def test_reversed_valid_order_requires_canonical_premise_match() -> None:
    changed = REPLACEMENT.read_text(encoding="utf-8")
    assert "matches = find_inference_matches_for_rule(rule, (independent, db))" in changed
    assert "assert len(matches) == 1" in changed
    assert "assert matches[0].premises == (db, independent)" in changed
    assert "assert find_inference_matches_for_rule(rule, (independent, db)) == ()" not in changed


def test_full_file_parse_and_original_import_section_preserved() -> None:
    before = ast.parse(BASELINE.read_text(encoding="utf-8"))
    after = ast.parse(REPLACEMENT.read_text(encoding="utf-8"))
    imports_before = tuple(ast.dump(s, include_attributes=False) for s in before.body
                           if isinstance(s, (ast.Import, ast.ImportFrom)))
    imports_after = tuple(ast.dump(s, include_attributes=False) for s in after.body
                          if isinstance(s, (ast.Import, ast.ImportFrom)))
    assert imports_before == imports_after
    assert imports_before
