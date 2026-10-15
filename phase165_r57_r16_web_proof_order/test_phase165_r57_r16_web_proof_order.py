"""Targeted proof-order policy checks: no saved proofs or manufactured claims."""
import ast
from pathlib import Path

import pytest

from install import replace_function


PACKAGE = Path(__file__).resolve().parent


def test_reviewed_order_is_explicit_not_generated():
    text = (PACKAGE / "phase165_r57_r16_web_proof_order.py").read_text(encoding="utf8")
    assert "REVIEWED_PROOF_TARGET_ORDER" in text
    assert "(2, 1)" in text and "(3, 1)" in text and "(4, 1)" in text
    assert "for n in range" not in text
    assert "ProofStep(" not in text
    assert "ProofRule.GIVEN" not in text


def test_catalog_uses_registered_candidates_and_no_completed_roots():
    text = (PACKAGE / "phase165_r57_r16_web_proof_order.py").read_text(encoding="utf8")
    assert "registered_group_goal_candidates" in text
    assert "len(candidates) != 1" in text
    assert "ProofOrderRecord(" in text
    assert "completed=" not in text


def test_web_selector_supplies_catalog_automatically():
    tree = ast.parse((PACKAGE / "search_group_from_registered_goal.py.txt").read_text(encoding="utf8"))
    fn = tree.body[0]
    assert fn.name == "search_group_from_registered_goal"
    assert [a.arg for a in fn.args.kwonlyargs] == ["n", "k", "bridge", "proof_order_catalog"]
    source = ast.unparse(fn)
    assert "resolve_reviewed_order_catalog" in source
    assert "proof_order_catalog=proof_order_catalog" in source
    assert "ProofSearchStatus.SEARCH_FAILED" in source


def test_existing_explicit_catalog_not_overwritten():
    src = (PACKAGE / "search_group_from_registered_goal.py.txt").read_text(encoding="utf8")
    assert "if proof_order_catalog is None:" in src


def test_installer_is_idempotent_and_fail_closed():
    before = "def f():\n    return 1\n"
    after = "def f():\n    return 2\n"
    output, changed = replace_function(before, "f", before, after)
    assert changed
    repeated, changed = replace_function(output, "f", before, after)
    assert not changed and repeated == output
    with pytest.raises(RuntimeError, match="unexpected"):
        replace_function("def f():\n    return 9\n", "f", before, after)


def test_outside_reviewed_scope_has_no_catalog():
    text = (PACKAGE / "phase165_r57_r16_web_proof_order.py").read_text(encoding="utf8")
    assert "if key not in REVIEWED_PROOF_TARGET_ORDER:" in text
    assert "return None, None" in text
