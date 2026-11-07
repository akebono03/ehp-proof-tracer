"""R18R1 mixed-EOL Git-object guard and reviewed lineage contracts."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r7_r18r1_git_mixed_eol_guard.patch import (
    AFTER_SHA256,
    BEFORE_SHA256,
    REPLACEMENT,
    REVIEWED_R17_HEAD,
    REVIEWED_R18_HEAD,
    digest,
    exact_replacement,
)


def _reviewed_module():
    namespace = {'__name__': 'phase174_r3_r7_r18r1_test_target', '__file__': str(REPLACEMENT)}
    exec(compile(exact_replacement(), str(REPLACEMENT), 'exec'), namespace)
    return namespace


def _committed():
    return (
        'phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py',
        'web_group_proof_common.py',
        'phase174_r3_r7_r17_typed_map_open_goal/patch.py',
    )


def test_full_replacement_integrity_and_syntax() -> None:
    data = exact_replacement()
    assert digest(data) == AFTER_SHA256
    assert BEFORE_SHA256 != AFTER_SHA256
    ast.parse(data.decode('utf-8'))
    assert b'git reset' not in data


def test_exact_mixed_eol_blob_is_accepted() -> None:
    module = _reviewed_module()
    data = b'one\r\ntwo\nthree\r\n'
    expected = module['git_blob_sha'](data)
    assert module['matches_reviewed_checkout'](data, expected, data)
    assert not module['matches_git_blob'](data, expected)


def test_uniform_checkout_forms_accepted_only_from_pinned_blob() -> None:
    module = _reviewed_module()
    committed = b'one\r\ntwo\nthree\r\n'
    expected = module['git_blob_sha'](committed)
    assert module['matches_reviewed_checkout'](b'one\ntwo\nthree\n', expected, committed)
    assert module['matches_reviewed_checkout'](b'one\r\ntwo\r\nthree\r\n', expected, committed)


@pytest.mark.parametrize('file', (
    b'one\r\ntwo\nthree\n',
    b'one\ntwo\nthree corrupted\n',
    b'one\r\ntwo\nthree\r\n\n',
))
def test_changed_or_unreviewed_checkout_rejected(file: bytes) -> None:
    module = _reviewed_module()
    committed = b'one\r\ntwo\nthree\r\n'
    expected = module['git_blob_sha'](committed)
    assert not module['matches_reviewed_checkout'](file, expected, committed)


def test_wrong_stored_blob_pin_rejected() -> None:
    module = _reviewed_module()
    committed = b'one\r\ntwo\nthree\r\n'
    assert not module['matches_reviewed_checkout'](committed, 'a' * 40, committed)


def test_reviwed_original_lineage_supported() -> None:
    module = _reviewed_module()
    assert module['checked_lineage'](REVIEWED_R17_HEAD, REVIEWED_R17_HEAD, (), _committed()) == 'R17_MERGED_CLEAN'


def test_r18_merged_clean_and_own_audit_edit_supported() -> None:
    module = _reviewed_module()
    marker = 'phase174_r3_r7_r18_delta_image_surjectivity/audit.py'
    assert module['checked_lineage'](REVIEWED_R18_HEAD, REVIEWED_R18_HEAD, (), _committed()) == 'R18_MERGED_CLEAN'
    assert module['checked_lineage'](REVIEWED_R18_HEAD, REVIEWED_R18_HEAD, (marker,), _committed()) == 'R18_MERGED_REVIEWED_GUARD_FIX'
    assert module['checked_lineage'](REVIEWED_R17_HEAD, REVIEWED_R18_HEAD, (), _committed()) == 'R18_MERGED_REMOTE_R17_LOCAL_CLEAN'


@pytest.mark.parametrize('bad', (
    ('b' * 40, REVIEWED_R18_HEAD, ()),
    (REVIEWED_R18_HEAD, 'a' * 40, ()),
    (REVIEWED_R18_HEAD, REVIEWED_R18_HEAD, ('proof.py',)),
    (REVIEWED_R18_HEAD, REVIEWED_R18_HEAD, ('phase174_r3_r7_r18_delta_image_surjectivity/rule.py',)),
))
def test_unknown_lineages_fail_closed(bad) -> None:
    module = _reviewed_module()
    with pytest.raises(RuntimeError):
        module['checked_lineage'](bad[0], bad[1], bad[2], _committed())


def test_r18_unreviewed_old_committed_paths_rejected() -> None:
    module = _reviewed_module()
    with pytest.raises(RuntimeError, match='unexpected files'):
        module['checked_lineage'](REVIEWED_R18_HEAD, REVIEWED_R18_HEAD, (), _committed() + ('proof.py',))


def test_no_production_search_or_rule_changes() -> None:
    data = exact_replacement().decode('utf-8')
    assert 'def inspect_live_frontier' in data
    assert 'production_provider_changed": False' in data
    assert 'new_group_given": 0' in data
