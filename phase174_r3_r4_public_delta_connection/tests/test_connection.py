"""Guard minimal public-provider wiring and citation-certified Delta proof."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r4_public_delta_connection.patch import (
    NEW_CONTEXT, OLD_CONTEXT, ensure_expected_input,
    extract_full_function, git_blob_sha, replace_provider_call,
)


def _fixture() -> bytes:
    return (
        'from __future__ import annotations\n\n'
        'def shared_expansion_provider(bridge):\n'
        '    def expand(goal):\n'
        + OLD_CONTEXT
        + '        return tuple(options)\n'
        + '    return expand\n'
    ).encode("utf-8")


def test_r3r4_exactly_one_local_import_and_proposal():
    source = _fixture()
    changed = replace_provider_call(source)
    assert source != changed
    assert changed.count(NEW_CONTEXT.encode("utf-8")) == 1
    assert changed.count(b'from phase174_r3_r3_injective_delta_zero.rule import') == 1
    assert ast.parse(changed)


def test_r3r4_already_connected_is_idempotent():
    changed = replace_provider_call(_fixture())
    assert replace_provider_call(changed) == changed
    assert ensure_expected_input(changed, _fixture(), changed) == 'ALREADY_INSTALLED'


def test_r3r4_unrelated_edits_refused():
    source = _fixture()
    new = replace_provider_call(source)
    assert ensure_expected_input(source, source, new) == 'ORIGINAL_REVIEWED'
    with pytest.raises(ValueError, match='user-modified'):
        ensure_expected_input(source + b'# unrelated\n', source, new)


def test_r3r4_unknown_anchor_rejected():
    with pytest.raises(ValueError, match='insertion point'):
        replace_provider_call(b'def shared_expansion_provider():\n    return ()\n')


def test_r3r4_function_entire_unit_can_be_exported():
    changed = replace_provider_call(_fixture())
    full = extract_full_function(changed)
    assert full.startswith('def shared_expansion_provider(bridge):\n')
    assert 'from phase174_r3_r3_injective_delta_zero.rule import' in full
    assert full.rstrip().endswith('return expand')


def test_r3r4_real_production_file_has_only_reviewed_wiring():
    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared
    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')
    current = Path('phase165_r52_r9_shared_math.py').read_bytes()
    r3r4 = replace_provider_call(old)
    assert current in (r3r4, insert_shared(r3r4))
    assert git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'
    assert current.count(b'options.extend(expand_delta_zero_from_injection(goal))') == 1


def test_r3r4_public_citation_screened_delta_is_inference():
    from phase174_r3_r4_public_delta_connection.audit import inspect_public_provider
    result = inspect_public_provider()
    assert result['delta_zero_publicly_reconstructed'] is True
    assert result['premises_both_inferred'] is True
    assert result['source_ancestry_checked'] is True
    assert result['named_group_goal_complete'] is False
    assert result['new_given'] == 0
