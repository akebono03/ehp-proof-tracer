from pathlib import Path

import pytest

from phase176_r3r39_public_equality_transport.apply import (
    INSERT_AFTER_AVAILABLE, INSERT_AFTER_HOPF,
)
from phase176_r3r39r3_fixed_baseline_repair.repair import (
    TARGET, expected_bytes, git, inspect, representation,
)


def baseline() -> bytes:
    return ('def f(prior_conclusions, goal, available):\n'
            + INSERT_AFTER_AVAILABLE + '        pass\n'
            + '    if True:\n'
            + '        options.extend(expand_composite_suspension_equality(goal))\n'
            + INSERT_AFTER_HOPF).encode()


def repo(path: Path, autocrlf: str) -> bytes:
    expected = expected_bytes(baseline())
    git(path, 'init', '-q')
    git(path, 'config', 'user.name', 'Test')
    git(path, 'config', 'user.email', 'test@example.invalid')
    git(path, 'config', 'core.autocrlf', 'false')
    (path / TARGET).write_bytes(expected.replace(b'\n', b'\r\n'))
    git(path, 'add', '--', TARGET)
    git(path, 'commit', '-qm', 'CRLF commit')
    git(path, 'config', 'core.autocrlf', autocrlf)
    return expected


@pytest.mark.parametrize('autocrlf', ['false', 'true', 'input'])
def test_committed_crlf_repair(tmp_path, autocrlf):
    expected = repo(tmp_path, autocrlf)
    before = git(tmp_path, 'rev-parse', 'HEAD')
    dry = inspect(tmp_path, baseline(), dry_run=True)
    assert dry['WORKTREE_AFTER'] == 'CRLF'
    result = inspect(tmp_path, baseline(), dry_run=False)
    assert result['HEAD'] == 'CRLF'
    assert result['WORKTREE_AFTER'] == 'LF'
    assert (tmp_path / TARGET).read_bytes() == expected
    assert git(tmp_path, 'rev-parse', 'HEAD') == before
    assert git(tmp_path, 'show', ':' + TARGET) != expected
    git(tmp_path, 'add', '--', TARGET)
    assert git(tmp_path, 'show', ':' + TARGET) == expected
    git(tmp_path, 'commit', '-qm', 'LF repair')
    assert inspect(tmp_path, baseline(), dry_run=False)['COMMIT_REQUIRED'] == 'False'


def test_unrelated_worktree_refused(tmp_path):
    expected = repo(tmp_path, 'false')
    wrong = expected + b'# unrelated\n'
    (tmp_path / TARGET).write_bytes(wrong)
    with pytest.raises(ValueError, match='UNRELATED_OR_INCOMPLETE'):
        inspect(tmp_path, baseline(), dry_run=False)
    assert (tmp_path / TARGET).read_bytes() == wrong


def test_missing_patch_refused():
    with pytest.raises(ValueError, match='UNRELATED_OR_INCOMPLETE'):
        representation(baseline(), expected_bytes(baseline()))


def test_mixed_eol_refused():
    expected = expected_bytes(baseline())
    with pytest.raises(ValueError, match='UNRELATED_OR_INCOMPLETE'):
        representation(expected.replace(b'\n', b'\r\n', 1), expected)
