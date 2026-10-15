"""R57-R15 focused integration and installer tests."""
import ast
from pathlib import Path

import pytest

from install import replace_function


def test_new_shared_search_has_automatic_catalog_recursion():
    text = (Path(__file__).parent / "search_shared_group_goal.py.txt").read_text(encoding="utf8")
    tree = ast.parse(text)
    assert len([n for n in tree.body if isinstance(n, ast.FunctionDef)]) == 1
    assert "recursive_proof_order_catalog = proof_order_catalog" in text
    assert "on-demand mode forbids registered completed proofs" in text
    assert "search_recursively_in_proof_order" in text


def test_selector_preserves_original_nk_contract():
    text = (Path(__file__).parent / "search_group_from_registered_goal.py.txt").read_text(encoding="utf8")
    node = ast.parse(text).body[0]
    assert node.name == "search_group_from_registered_goal"
    assert [v.arg for v in node.args.kwonlyargs] == ["n", "k", "bridge", "proof_order_catalog"]
    assert "proof_order_catalog=proof_order_catalog" in text


def test_installer_is_idempotent_and_fail_closed():
    old = "def f(x):\n    return x\n"
    new = "def f(x):\n    return x + 1\n"
    updated, changed = replace_function(old, "f", old, new)
    assert changed and "return x + 1" in updated
    same, changed = replace_function(updated, "f", old, new)
    assert not changed and same == updated
    with pytest.raises(RuntimeError, match="unexpected predecessor"):
        replace_function("def f(x):\n    return None\n", "f", old, new)


def test_reuses_existing_recursive_engine_not_saved_proofs():
    source = (Path(__file__).parent / "search_shared_group_goal.py.txt").read_text(encoding="utf8")
    assert "completed_internal_proofs=()" in source
    assert "ordered_completed_proofs=earlier" in source
    assert "target_order=order" in source


def test_no_new_given_or_group_specific_answers():
    source = (Path(__file__).parent / "search_shared_group_goal.py.txt").read_text(encoding="utf8")
    assert "ProofRule.GIVEN" not in source
    assert "\\pi_5^4" not in source
