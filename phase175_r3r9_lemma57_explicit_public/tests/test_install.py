"""Review the whole-function replacement and its exact EOL handling."""
from __future__ import annotations

import ast

import pytest

from phase175_r3r9_lemma57_explicit_public import install


def test_only_one_routing_import_changes_in_complete_function() -> None:
    old = (install.PACKAGE / "search_shared_group_goal_BEFORE.py.txt").read_text(
        encoding="utf-8",
    )
    new = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    assert old.count(install.OLD_ROUTE) == 1
    assert new == old.replace(install.OLD_ROUTE, install.NEW_ROUTE, 1)
    before = ast.parse(old)
    after = ast.parse(new)
    assert len(before.body) == len(after.body) == 1
    assert isinstance(before.body[0], ast.FunctionDef)
    assert isinstance(after.body[0], ast.FunctionDef)
    assert ast.dump(before.body[0].args) == ast.dump(after.body[0].args)
    assert not any(isinstance(x, (ast.Global, ast.Nonlocal)) for x in after.body[0].body)


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_rewrite_full_function_and_preserve_newlines(newline: str) -> None:
    old = (install.PACKAGE / "search_shared_group_goal_BEFORE.py.txt").read_text(
        encoding="utf-8",
    )
    new = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    wrapped = "# untouched prefix\n" + old + "\n# untouched suffix\n"
    replaced = install.replace_function_bytes(
        wrapped.replace("\n", newline).encode("utf-8"),
    )
    expected = ("# untouched prefix\n" + new + "\n# untouched suffix\n")
    assert replaced == expected.replace("\n", newline).encode("utf-8")


def test_unreviewed_function_rejected() -> None:
    function = (install.PACKAGE / "search_shared_group_goal_BEFORE.py.txt").read_text(
        encoding="utf-8",
    )
    modified = function.replace("    if n == 4 and k == 3", "    if n == 5 and k == 3", 1)
    with pytest.raises(RuntimeError, match="SOURCE_FUNCTION_CHANGED_SINCE_REVIEW"):
        install.replace_function_bytes(modified.encode("utf-8"))


def test_missing_route_rejected() -> None:
    function = (install.PACKAGE / "search_shared_group_goal_BEFORE.py.txt").read_text(
        encoding="utf-8",
    )
    modified = function.replace(install.OLD_ROUTE, "", 1)
    with pytest.raises(RuntimeError):
        install.replace_function_bytes(modified.encode("utf-8"))
