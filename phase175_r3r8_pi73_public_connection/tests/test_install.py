"""Installer must not alter other functions, APIs or unexpected Git states."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r3r8_pi73_public_connection import install


def test_complete_function_template_compiles_without_elision() -> None:
    full = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    assert full.count(install.PUBLIC_INSERTION) == 1
    compile(full, "search_shared_group_goal_FULL.py.txt", "exec")
    original = full.replace(install.PUBLIC_INSERTION, "")
    assert install.ANCHOR in original
    assert original.replace(
        install.ANCHOR, install.PUBLIC_INSERTION + install.ANCHOR, 1,
    ) == full
    parsed = ast.parse(full)
    assert len(parsed.body) == 1
    assert isinstance(parsed.body[0], ast.FunctionDef)
    assert parsed.body[0].name == "search_shared_group_goal"


def test_full_function_preserves_existing_public_api() -> None:
    full = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    node = ast.parse(full).body[0]
    expected = {
        "n", "k", "group_structure", "bridge", "expansion_provider",
        "citing_assertion_id", "verified_assertion_ids",
        "completed_internal_proofs", "proof_use_order",
        "ordered_completed_proofs", "target_order", "proof_order_catalog",
        "recursive_proof_order_catalog", "context_sink",
    }
    assert set(arg.arg for arg in node.args.kwonlyargs) == expected
    assert len(node.args.posonlyargs) == 0


def test_find_function_requires_exactly_one_top_level_definition() -> None:
    source = "def search_shared_group_goal():\n    return 1\n"
    assert install.find_function(source) == (0, len(source))
    with pytest.raises(RuntimeError, match="FUNCTION_NOT_UNIQUE"):
        install.find_function(source + "\n" + source)
    with pytest.raises(RuntimeError, match="FUNCTION_NOT_UNIQUE"):
        install.find_function("def other():\n    pass\n")


def test_git_command_whitelist_is_read_only(tmp_path: Path) -> None:
    for denied in ("add", "reset", "checkout", "commit", "clean", "push"):
        with pytest.raises(ValueError, match="read-only"):
            install.git(tmp_path, denied, "something")


def test_patch_has_no_import_change_or_other_api_change() -> None:
    template = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    before = ast.parse(template.replace(install.PUBLIC_INSERTION, "")).body[0]
    after = ast.parse(template).body[0]
    assert ast.dump(before.args) == ast.dump(after.args)
    assert len(after.body) == len(before.body) + 1
    assert not any(isinstance(node, (ast.Global, ast.Nonlocal)) for node in after.body)
