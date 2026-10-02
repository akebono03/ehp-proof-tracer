from __future__ import annotations

import ast

import repair_phase155_r2c as repair


def test_replace_function_replaces_complete_function():
    source = (
        "import os\n\n"
        "def test_x():\n"
        "  assert 'old'\n\n"
        "def test_y():\n"
        "  assert True\n"
    )
    replacement = (
        "def test_x():\n"
        "  assert 'new'"
    )

    changed = repair._replace_function(
        source,
        "test_x",
        replacement,
    )

    assert "assert 'old'" not in changed
    assert "assert 'new'" in changed
    assert "def test_y():" in changed
    ast.parse(changed)


def test_punctuation_normalization_is_function_scoped():
    source = (
        "def test_x():\n"
        "  assert 'まず、結論。'\n\n"
        "def test_y():\n"
        "  assert 'まず、維持。'\n"
    )

    changed = (
        repair._normalize_ascii_punctuation_in_function(
            source,
            "test_x",
        )
    )

    assert "まず, 結論." in changed
    assert "まず、維持。" in changed
    ast.parse(changed)


def test_confirmed_stale_set_has_45_tests():
    all_nodeids = (
        set(
            repair.PUNCTUATION_NODEIDS
        )
        | set(
            repair.SPECIAL_REPLACEMENTS
        )
    )
    assert len(all_nodeids) == 45


def test_special_and_punctuation_sets_do_not_overlap():
    assert not (
        set(
            repair.PUNCTUATION_NODEIDS
        )
        & set(
            repair.SPECIAL_REPLACEMENTS
        )
    )


def test_special_replacement_sources_parse():
    for source in (
        repair.SPECIAL_REPLACEMENTS.values()
    ):
        ast.parse(source)


def test_special_replacements_cover_current_contract_exceptions():
    nodeids = set(
        repair.SPECIAL_REPLACEMENTS
    )
    assert any(
        "phase132_6" in nodeid
        for nodeid in nodeids
    )
    assert any(
        "phase143_42" in nodeid
        for nodeid in nodeids
    )
    assert any(
        "phase144_6" in nodeid
        for nodeid in nodeids
    )
    assert any(
        "phase153_r2" in nodeid
        for nodeid in nodeids
    )
