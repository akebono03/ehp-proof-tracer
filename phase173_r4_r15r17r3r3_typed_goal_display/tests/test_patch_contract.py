"""Isolated tests for exact, repeat-safe source transformation."""
from __future__ import annotations

import ast

import pytest

from phase173_r4_r15r17r3r3_typed_goal_display.patch import (
    ANCHOR, FUNCTION_ANCHOR, HELPER, REPLACEMENT, transform,
)


def original_fixture() -> str:
    return FUNCTION_ANCHOR + '    result, model,\n) -> str:\n    if True:\n' + ANCHOR


def test_replacement_is_single_and_entirely_within_common_renderer() -> None:
    transformed = transform(original_fixture())
    ast.parse(transformed)
    assert transformed.count('def project_typed_open_goal_displays(') == 1
    assert transformed.count(FUNCTION_ANCHOR) == 1
    assert transformed.count(REPLACEMENT) == 1
    assert 'for goal in model.open_goals:' not in transformed


def test_reapplication_and_missing_anchor_fail_closed() -> None:
    transformed = transform(original_fixture())
    with pytest.raises(RuntimeError, match='anchor|already installed'):
        transform(transformed)
    with pytest.raises(RuntimeError, match='anchor|already installed'):
        transform('def render_model_backed_narrative_markdown():\n    pass\n')


def test_unreviewed_duplicate_anchor_is_rejected() -> None:
    source = original_fixture() + ANCHOR
    with pytest.raises(RuntimeError, match='open Goal'):
        transform(source)


def test_patch_adds_no_dimension_or_family_branches() -> None:
    new = ast.parse(HELPER)
    for node in ast.walk(new):
        if not isinstance(node, ast.Compare):
            continue
        targets = (node.left, *node.comparators)
        names = {child.id for item in targets for child in ast.walk(item)
                 if isinstance(child, ast.Name)}
        assert not names.intersection({'n', 'k'})
