"""Regression tests for the R23 installer, independent of the proof engine."""
import ast
import subprocess
from types import SimpleNamespace

import pytest

from phase178_r23_common_renderer_elision.installer import (
    ISO_PROJECTION, check_git_diff, proposed_common,
)


COMMON_FIXTURE = (
    "def fixture(model, index, refs, body):\n"
    "    match = match_composition_branch(model, index)\n"
    "    tag = ', '.join(f'[R{n}]' for n in refs) + 'より, '\n"
    "    replacement = tag + body\n"
    "    return replacement\n"
)


def git_at(folder, *args):
    return subprocess.check_output(['git', *args], cwd=folder, stderr=subprocess.PIPE)


@pytest.mark.parametrize('ending', ['\n', '\r\n'])
def test_common_writer_has_single_eof_newline_and_clean_diff(tmp_path, ending):
    git_at(tmp_path, 'init', '-q')
    git_at(tmp_path, 'config', 'user.name', 'R23 regression')
    git_at(tmp_path, 'config', 'user.email', 'r23@example.invalid')
    git_at(tmp_path, 'config', 'core.autocrlf', 'false')
    # Use a repository with explicit EOL handling, independent of host Git config.
    git_at(tmp_path, 'config', 'core.whitespace', 'blank-at-eof,blank-at-eol,space-before-tab,cr-at-eol')
    path = tmp_path / 'projection.py'
    path.write_bytes(COMMON_FIXTURE.replace('\n', ending).encode('utf-8'))
    git_at(tmp_path, 'add', 'projection.py')
    git_at(tmp_path, 'commit', '-qm', 'base')
    updated = proposed_common(COMMON_FIXTURE)
    assert updated.endswith('\n') and not updated.endswith('\n\n')
    assert updated.endswith(ISO_PROJECTION.rstrip('\n') + '\n')
    ast.parse(updated)
    path.write_bytes(updated.replace('\n', ending).encode('utf-8'))
    assert git_at(tmp_path, 'diff', '--check') == b''
    check_git_diff(SimpleNamespace(git=lambda *args: git_at(tmp_path, *args)))


def test_diff_check_reports_original_diagnostic(capsys):
    def fail(*args):
        assert args == ('diff', '--check')
        raise subprocess.CalledProcessError(
            2, ['git', *args], output=b'projection.py:54: new blank line at EOF.\n',
        )
    with pytest.raises(RuntimeError, match='new blank line at EOF'):
        check_git_diff(SimpleNamespace(git=fail))
    assert 'PHASE178_R23_DIFF_CHECK_OUTPUT=projection.py:54: new blank line at EOF.' in capsys.readouterr().out
