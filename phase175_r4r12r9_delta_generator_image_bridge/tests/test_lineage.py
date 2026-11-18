"""Review-only regression tests for the R9R1 merge HEAD acceptance."""
from pathlib import Path

import pytest

from phase175_r4r12r9_delta_generator_image_bridge import audit


def simulated_git(head: str, *, count: str = '1', paths: str = '', ancestor: str | None = None):
    def command(root: Path, *args: str) -> str:
        key = tuple(args)
        if key == ('rev-parse', '--show-toplevel'):
            return str(root)
        if key == ('branch', '--show-current'):
            return 'develop'
        if key == ('rev-parse', 'HEAD'):
            return head
        if key == ('rev-list', '--count', audit.PRIOR_COMMIT + '..' + head):
            return count
        if key == ('diff', '--name-only', audit.PRIOR_COMMIT, head):
            return paths
        if key == ('merge-base', audit.PRIOR_COMMIT, head):
            return audit.PRIOR_COMMIT if ancestor is None else ancestor
        if key in (('diff', '--name-only'), ('diff', '--cached', '--name-only')):
            return ''
        raise AssertionError('Unrecognized Git command: ' + repr(key))
    return command


def test_reviewed_merge_with_zero_changed_paths_is_allowed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, 'git', simulated_git(audit.REVIEWED_MERGE_COMMIT))
    state = audit.verify(tmp_path)
    assert state['head'] == audit.REVIEWED_MERGE_COMMIT
    assert state['dirty'] == []


def test_unreviewed_head_rejected(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, 'git', simulated_git('f' * 40))
    with pytest.raises(RuntimeError, match='R9_HEAD_NEEDS_REVIEW'):
        audit.verify(tmp_path)


def test_reviewed_merge_with_file_changes_is_rejected(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, 'git', simulated_git(audit.REVIEWED_MERGE_COMMIT, paths='proof.py'))
    with pytest.raises(RuntimeError, match='R9_UNREVIEWED_MERGE_FILES'):
        audit.verify(tmp_path)


def test_reviewed_merge_with_wrong_commit_count_rejected(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, 'git', simulated_git(audit.REVIEWED_MERGE_COMMIT, count='2'))
    with pytest.raises(RuntimeError, match='R9_UNREVIEWED_MERGE_COUNT'):
        audit.verify(tmp_path)


def test_reviewed_merge_with_wrong_ancestry_rejected(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, 'git', simulated_git(audit.REVIEWED_MERGE_COMMIT, ancestor='a'*40))
    with pytest.raises(RuntimeError, match='R9_UNREVIEWED_MERGE_ANCESTRY'):
        audit.verify(tmp_path)


def test_original_reviewed_head_remains_allowed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, 'git', simulated_git(audit.PRIOR_COMMIT))
    assert audit.verify(tmp_path)['head'] == audit.PRIOR_COMMIT
