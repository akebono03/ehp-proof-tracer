"""Installer and full-function contract tests, independent of the EHP runtime."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r8_public_connection import install


def test_full_function_is_standalone_and_not_ellipsis() -> None:
    src = Path(install.__file__).with_name("search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    body = ast.parse(src).body
    assert len(body) == 1
    assert isinstance(body[0], ast.FunctionDef)
    assert body[0].name == "search_shared_group_goal"
    assert not any(isinstance(node, ast.Expr)
                   and isinstance(node.value, ast.Constant)
                   and node.value.value is Ellipsis
                   for node in ast.walk(body[0]))
    assert src.count(install.HOOK) == 1


def test_transform_exact_full_function() -> None:
    src = Path(install.__file__).with_name("search_shared_group_goal_FULL.py.txt").read_text()
    original = src.replace(install.HOOK, "")
    assert install.transform(original.encode("utf-8")).decode("utf-8") == src


def test_crlf_preserved() -> None:
    src = Path(install.__file__).with_name("search_shared_group_goal_FULL.py.txt").read_text()
    original = src.replace(install.HOOK, "").replace("\n", "\r\n").encode()
    result = install.transform(original)
    assert b"\r\n" in result
    assert result.replace(b"\r\n", b"\n").decode() == src


def test_duplicate_hook_rejected() -> None:
    src = Path(install.__file__).with_name("search_shared_group_goal_FULL.py.txt").read_text()
    with pytest.raises(RuntimeError, match="already installed"):
        install.transform(src.encode())


def test_missing_anchor_rejected() -> None:
    with pytest.raises(RuntimeError, match="not unique"):
        install.transform(b"def search_shared_group_goal():\n    return None\n")


def test_source_guards_are_exact() -> None:
    assert install.REVIEWED_HEAD == "72c66346b07cfc5517543627e010fd0db9842274"
    assert install.PREVIOUS_WORKTREE_BLOB == "abdc05c731e5ede1258962705bc577b5307b6f38"
    assert install.TARGET in install.REVIEWED_FILES
    assert install.PREVIOUS_PATCH in install.REVIEWED_FILES
    assert all(len(blob) == 40 for blob in install.REVIEWED_FILES.values())


def test_hook_does_not_modify_prior_pi74_branch() -> None:
    src = Path(install.__file__).with_name("search_shared_group_goal_FULL.py.txt").read_text()
    assert src.index("if n == 4 and k == 3") < src.index("# Phase 173 R4-R8")
    assert src.index("proof_context = prefer_universal_prop42_derivation") < src.index(
        "# Phase 173 R4-R8"
    ) < src.index("if context_sink is not None:")
