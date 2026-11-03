"""Focused full-function installation guards, independent of the EHP runtime."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r11_zero_public_connection import install


def _function() -> str:
    return Path(install.__file__).with_name(
        "search_group_from_registered_goal_FULL.py.txt"
    ).read_text(encoding="utf-8")


def _old_function() -> str:
    updated = _function()
    hook = '''        from phase173_r4_r11_zero_public_connection.route import (
            prepare_zero_toda56_public_connection,
        )
        zero_connection = prepare_zero_toda56_public_connection(
            bridge=bridge, goal=candidate,
        )
        if zero_connection is None:
            screened = screen_independent_sources_for_derived_goal(
                bridge, goal=candidate,
            )
            provider = shared_expansion_provider(
                screened, proof_target=candidate,
            )
        else:
            screened, provider = zero_connection
'''
    old = '''        screened = screen_independent_sources_for_derived_goal(
            bridge, goal=candidate,
        )
        if context_sink is not None:
            context_sink(screened)
        provider = shared_expansion_provider(
            screened, proof_target=candidate,
        )
'''
    assert updated.count(hook) == 1
    return updated.replace(hook + '        if context_sink is not None:\n            context_sink(screened)\n', old)


def test_full_function_is_single_complete_ast() -> None:
    tree = ast.parse(_function())
    assert len(tree.body) == 1
    assert isinstance(tree.body[0], ast.FunctionDef)
    assert tree.body[0].name == "search_group_from_registered_goal"
    assert not any(isinstance(node, ast.Constant) and node.value is Ellipsis
                   for node in ast.walk(tree))


@pytest.mark.parametrize("newline", ("\n", "\r\n"))
def test_full_function_patch_preserves_newline(newline: str) -> None:
    fixture = (_old_function() + '\nOTHER_SENTINEL = 1\n').replace('\n', newline).encode()
    expected = (_function() + '\nOTHER_SENTINEL = 1\n').replace('\n', newline).encode()
    assert install.patched_source(fixture, _function()) == expected


def test_patch_fails_on_unreviewed_zero_branch() -> None:
    wrong = _old_function().replace("if proof_order_catalog is None:", "if proof_order_catalog is not None:")
    with pytest.raises(RuntimeError, match="only the zero branch"):
        install.patched_source(wrong.encode(), _function())
