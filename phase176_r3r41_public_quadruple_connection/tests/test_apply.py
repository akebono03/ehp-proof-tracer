"""Regression tests for the two legitimate Prop. 2.7 imports."""
from __future__ import annotations

import difflib

import pytest

from phase176_r3r41_public_quadruple_connection.apply import (
    DISPATCH, DISPATCH_ANCHOR, PATCHED_DISPATCH_ANCHOR, SETUP, SETUP_ANCHOR,
    updated_source,
)


BASELINE = '''def build_shared_typed_bridge():
    if True:
        from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
            register_positioned_prop27,
        )
    return register_positioned_prop27


def shared_expansion_provider(bridge, prior_conclusions=()):
    available = ()
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")

    def expand(goal):
        options = []
        from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
            expand_public_cited_prop27_goal,
        )
        options.extend(public_right_hopf_transport(goal))
        return tuple(options)
    return expand


def following_function():
    return None
'''


def test_duplicate_module_import_is_legitimate_and_eight_lines_only():
    assert BASELINE.count(DISPATCH_ANCHOR.splitlines()[1]) == 2
    changed = updated_source(BASELINE)
    assert changed.replace(SETUP, '').replace(DISPATCH, '') == BASELINE
    assert PATCHED_DISPATCH_ANCHOR in changed
    delta = list(difflib.ndiff(BASELINE.splitlines(), changed.splitlines()))
    assert len([line for line in delta if line.startswith('+ ')]) == 8
    assert not any(line.startswith('- ') for line in delta)
    assert updated_source(changed) == changed


def test_same_setup_text_outside_target_function_does_not_conflict():
    extra = ('\ndef unrelated(prior_conclusions):\n' + SETUP_ANCHOR
             + '        raise TypeError("other function")\n')
    original = BASELINE + extra
    changed = updated_source(original)
    assert changed.endswith(extra)
    assert changed.replace(SETUP, '').replace(DISPATCH, '') == original


def test_missing_or_wrong_inner_dispatch_is_rejected():
    wrong = BASELINE.replace(DISPATCH_ANCHOR, DISPATCH_ANCHOR.replace(
        'expand_public_cited_prop27_goal', 'register_positioned_prop27'))
    with pytest.raises(ValueError, match='SHARED_DISPATCH_ANCHOR_NOT_UNIQUE'):
        updated_source(wrong)
    duplicate = BASELINE.replace(DISPATCH_ANCHOR, DISPATCH_ANCHOR +
        '        )\n' + DISPATCH_ANCHOR)
    with pytest.raises(ValueError, match='SHARED_DISPATCH_ANCHOR_NOT_UNIQUE'):
        updated_source(duplicate)


def test_partial_or_moved_patch_is_rejected():
    changed = updated_source(BASELINE)
    with pytest.raises(ValueError, match='PARTIAL_OR_CHANGED'):
        updated_source(changed.replace(DISPATCH, ''))
    moved = changed.replace(DISPATCH, '').replace(
        '        return tuple(options)\n', DISPATCH + '        return tuple(options)\n')
    with pytest.raises(ValueError, match='DUPLICATE_OR_MOVED'):
        updated_source(moved)


def test_missing_r3r39_or_crlf_is_rejected():
    with pytest.raises(ValueError, match='R3R39_HOOK_MISSING'):
        updated_source(BASELINE.replace('        options.extend(public_right_hopf_transport(goal))\n', ''))
    with pytest.raises(ValueError, match='EXPECTED_REPAIRED_LF_SOURCE'):
        updated_source(BASELINE.replace('\n', '\r\n'))
