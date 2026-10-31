"""Safety regression checks for the restored-source guard and its runner."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from phase171_closeout_r2r4_restored_source_guard import repair as g
from phase171_closeout_r2r3_mixed_line_ending_fix import install as r


def _hash(data: bytes) -> str:
    return sha256(data).hexdigest()


def test_all_reviewed_replacements_match_exact_hashes():
    assert _hash((g.HERE / 'reviewed_originals/install.py').read_bytes()) == g.REVIEWED_OLD_INSTALL
    assert _hash((g.HERE / 'replacements/install.py').read_bytes()) == g.REVIEWED_NEW_INSTALL
    for name, expected in g.REVIEWED_PAIRS['R2_BASE'].items():
        assert _hash((g.HERE / 'reviewed_originals' / name).read_bytes()) == expected


def test_r2r4_installer_is_only_r2r3_guard_extension():
    old = (g.HERE / 'reviewed_originals/install.py').read_text(encoding='utf-8')
    new = (g.HERE / 'replacements/install.py').read_text(encoding='utf-8')
    assert 'REVIEWED_R2_BASE_SHA256' not in old
    assert 'REVIEWED_R2_BASE_SHA256' in new
    assert new.count('states.append("R2_BASE")') == 1
    assert new.count('states.append("R2R1")') == 1
    assert old.count('states.append("OLD")') == 1
    assert new.count('states.append("NEW")') == 1
    assert 'if len(set(states)) != 1:' in new


def test_power_shell_runner_uses_explicit_argument_variable():
    runner = (g.HERE / 'run.ps1').read_text(encoding='utf-8')
    assert '& python @PythonArguments' in runner
    assert '"--dry-run"' in runner
    assert '& python @Args' not in runner


def _prepare_guard_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    root = tmp_path / 'repo'
    r2 = root / 'phase171_closeout_r2_documentation_full_output'
    r2r3 = root / 'phase171_closeout_r2r3_mixed_line_ending_fix'
    for name in g.REVIEWED_PAIRS['R2_BASE']:
        path = r2 / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((g.HERE / 'reviewed_originals' / name).read_bytes())
    target = r2r3 / 'install.py'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((g.HERE / 'reviewed_originals/install.py').read_bytes())
    (r2r3 / 'run.ps1').write_text('# reviewed runner\n', encoding='utf-8')
    monkeypatch.setattr(g, 'ROOT', root)
    monkeypatch.setattr(g, 'R2', r2)
    monkeypatch.setattr(g, 'R2R3', r2r3)
    monkeypatch.setattr(g, 'TARGET', target)

    def fake_git(*args):
        if args == ('branch', '--show-current'):
            return 'develop'
        if args in (('rev-parse', 'HEAD'), ('rev-parse', 'origin/develop')):
            return g.REVIEWED_HEAD
        if args in (('diff', '--cached', '--name-only', '--'), ('diff', '--name-only', 'HEAD', '--')):
            return ''
        raise AssertionError(args)

    monkeypatch.setattr(g, 'git', fake_git)
    return r2, target


def test_repaired_guard_accepts_exact_restored_r2_original_pair(tmp_path, monkeypatch):
    r2, target = _prepare_guard_fixture(tmp_path, monkeypatch)
    before, after, already, state = g.preflight()
    assert state == 'R2_BASE'
    assert not already
    assert before == (g.HERE / 'reviewed_originals/install.py').read_bytes()
    target.write_bytes(after)
    _, _, already, state = g.preflight()
    assert already and state == 'R2_BASE'


def test_guard_rejects_mixed_base_and_intermediate_r2_pair(tmp_path, monkeypatch):
    r2, _ = _prepare_guard_fixture(tmp_path, monkeypatch)
    intermediate = r.HERE / 'reviewed_originals' / 'tests' / 'test_document_writer.py'
    (r2 / 'tests' / 'test_document_writer.py').write_bytes(intermediate.read_bytes())
    with pytest.raises(RuntimeError, match='unreviewed or mixed'):
        g.preflight()


def test_guard_rejects_unknown_r2_writer(tmp_path, monkeypatch):
    r2, _ = _prepare_guard_fixture(tmp_path, monkeypatch)
    (r2 / 'update_docs.py').write_text('unexpected edit\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='unreviewed or mixed'):
        g.preflight()


def test_guard_rejects_unreviewed_existing_r2r3_installer(tmp_path, monkeypatch):
    _, target = _prepare_guard_fixture(tmp_path, monkeypatch)
    target.write_text('unreviewed installer\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='unreviewed R2R3 installer'):
        g.preflight()


def test_guard_rejects_unreviewed_git_tracked_change(tmp_path, monkeypatch):
    _prepare_guard_fixture(tmp_path, monkeypatch)
    original = g.git
    def git(*args):
        if args == ('diff', '--name-only', 'HEAD', '--'):
            return 'phase165_r52_r9_shared_math.py'
        return original(*args)
    monkeypatch.setattr(g, 'git', git)
    with pytest.raises(RuntimeError, match='unexpected tracked changes'):
        g.preflight()


def test_patched_r2r3_preflight_accepts_original_restored_r2_source(tmp_path, monkeypatch):
    root = tmp_path / 'repo'
    r2 = root / 'phase171_closeout_r2_documentation_full_output'
    r2r1 = root / 'phase171_closeout_r2r1_committed_head_guard'
    for relative in r.REPLACEMENTS:
        destination = r2 / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((g.HERE / 'reviewed_originals' / relative).read_bytes())
    for name in r.SECTIONS:
        path = r2 / 'sections' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((r.HERE / 'reviewed_sections' / name).read_bytes())
    (r2 / 'run.ps1').write_text('# fixture\n', encoding='utf-8')
    r2r1.mkdir(parents=True)
    (r2r1 / 'run.ps1').write_text('# fixture\n', encoding='utf-8')
    monkeypatch.setattr(r, 'ROOT', root)
    monkeypatch.setattr(r, 'R2', r2)

    def git(*args):
        if args == ('branch', '--show-current'):
            return 'develop'
        if args in (('rev-parse', 'HEAD'), ('rev-parse', 'origin/develop')):
            return r.BASE
        if args == ('merge-base', '--is-ancestor', r.BASE, 'HEAD'):
            return ''
        if args == ('rev-parse', 'HEAD:' + r.R1R1_TEST):
            return r.TEST_BLOB
        if len(args) == 2 and args[0] == 'rev-parse' and args[1].startswith('HEAD:'):
            return r.DOCUMENT_BLOBS[args[1][5:]]
        if args in (('diff', '--cached', '--name-only', '--'), ('diff', '--name-only', 'HEAD', '--')):
            return ''
        raise AssertionError(args)

    monkeypatch.setattr(r, 'git', git)
    original_source = r.preflight()
    assert original_source[2] is False
    assert len(original_source[0]) == 2
    for file, content in original_source[1].items():
        file.write_bytes(content)
    assert r.preflight()[2] is True


def test_r2r3_preflight_preserves_previous_r2r1_acceptance(tmp_path, monkeypatch):
    from phase171_closeout_r2r3_mixed_line_ending_fix.tests.test_install import _fixture
    r2 = _fixture(tmp_path, monkeypatch)
    original = r.preflight()
    assert original[2] is False
    for path, content in original[1].items():
        path.write_bytes(content)
    assert r.preflight()[2] is True


def test_r2r3_preflight_refuses_two_different_reviewed_states(tmp_path, monkeypatch):
    from phase171_closeout_r2r3_mixed_line_ending_fix.tests.test_install import _fixture
    r2 = _fixture(tmp_path, monkeypatch)
    original = (g.HERE / 'reviewed_originals' / 'update_docs.py').read_bytes()
    (r2 / 'update_docs.py').write_bytes(original)
    with pytest.raises(RuntimeError, match='mixed state'):
        r.preflight()
