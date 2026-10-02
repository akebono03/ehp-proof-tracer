from __future__ import annotations

import ast

import repair_phase155_r2c_r2 as repair


def test_r2_repairs_exactly_two_functions():
    assert len(
        repair.REPLACEMENTS
    ) == 2


def test_r2_repair_targets_phase132_and_phase153():
    nodeids = set(
        repair.REPLACEMENTS
    )

    assert any(
        "test_phase132_6_sigma9_narrative_uses_fixed_japanese_leads"
        in nodeid
        for nodeid
        in nodeids
    )
    assert any(
        "test_phase153_r12_pi11_4_body_uses_renumbered_external_references"
        in nodeid
        for nodeid
        in nodeids
    )


def test_all_replacement_functions_parse():
    for source in (
        repair.REPLACEMENTS.values()
    ):
        ast.parse(
            source
        )


def test_phase132_replacement_does_not_ban_all_japanese_periods():
    source = next(
        source
        for nodeid, source
        in repair.REPLACEMENTS.items()
        if "phase132_6" in nodeid
    )

    assert (
        'assert "。" not in rendered'
        not in source
    )
    assert (
        'assert "まず、" not in rendered'
        in source
    )
    assert (
        'assert "まず, " in rendered'
        in source
    )


def test_phase153_replacement_uses_current_r2_semantics():
    source = next(
        source
        for nodeid, source
        in repair.REPLACEMENTS.items()
        if "phase153_r12" in nodeid
    )

    assert (
        "[R1]を用いる."
        in source
    )
    assert (
        "[R2]より, "
        in source
    )
    assert (
        '[R2]を用いる.'
        not in source
    )


def test_replace_function_preserves_other_function():
    original = (
        "def test_a():\n"
        "  assert False\n\n"
        "def test_b():\n"
        "  assert True\n"
    )

    changed = (
        repair._replace_function(
            original,
            "test_a",
            (
                "def test_a():\n"
                "  assert True"
            ),
        )
    )

    assert (
        "def test_b():\n"
        "  assert True"
        in changed
    )
    ast.parse(
        changed
    )
