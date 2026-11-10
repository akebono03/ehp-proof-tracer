"""R55R1 checks exact source replacement and the real guard's two states."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r55r1_source_guard_type_fix import patch

PACKAGE = Path(__file__).resolve().parents[1]


def _source_bytes(name: str) -> bytes:
    return (PACKAGE / name / 'source_guard.py').read_bytes()


def test_exactly_one_comparison_changed_without_restructuring() -> None:
    before = _source_bytes('baseline')
    after = _source_bytes('replacement')
    assert patch.digest(before) == patch.BEFORE_SHA256
    assert patch.digest(after) == patch.AFTER_SHA256
    assert patch.corrected_source(before) == after
    assert patch.corrected_source(after) == after
    assert patch.BEFORE_EXPRESSION.encode('utf-8') in before
    assert patch.AFTER_EXPRESSION.encode('utf-8') in after
    assert before.replace(
        patch.BEFORE_EXPRESSION.encode('utf-8'),
        patch.AFTER_EXPRESSION.encode('utf-8'), 1,
    ) == after
    ast.parse(after.decode('utf-8'))


def test_windows_crlf_is_preserved_and_replay_is_idempotent() -> None:
    before = _source_bytes('baseline').replace(b'\n', b'\r\n')
    after = patch.corrected_source(before)
    assert patch.digest(after) == patch.AFTER_SHA256
    assert after == _source_bytes('replacement').replace(b'\n', b'\r\n')
    assert patch.corrected_source(after) == after


def test_unreviewed_partial_or_unrelated_changes_are_rejected() -> None:
    with pytest.raises(RuntimeError):
        patch.corrected_source(_source_bytes('baseline').replace(
            patch.BEFORE_EXPRESSION.encode('utf-8'), b'installed=True', 1,
        ))
    with pytest.raises(RuntimeError):
        patch.corrected_source(_source_bytes('baseline').replace(
            b"return {", b"return {'unexpected': 1,", 1,
        ))


def _mock_checkout(monkeypatch, tmp_path: Path, *, installed: bool) -> dict[str, object]:
    """Execute the complete revised guard with a realistic fake Git checkout."""
    import runpy
    guard_globals = runpy.run_path(str(PACKAGE / 'replacement' / 'source_guard.py'))
    original = b'\n'.join((
        b'def render_model_backed_narrative_markdown(result, model):',
        b'    for chain in chains:',
        b'        exactness_numbers = (3,)',
        b'        if exactness_numbers:',
        b'            tags = ", ".join(f"[R{number}]" for number in exactness_numbers)',
        '            lines.append(f"${group_tex(model.target)}$の群構造を決定するために, {tags}を用いて次の完全列を考える.")'.encode('utf-8'),
        b'        else:',
        '            lines.append(f"${group_tex(model.target)}$の群構造を決定するために, 次の完全列を考える.")'.encode('utf-8'),
        b'    return lines', b'',
    ))
    from phase174_r3_r7_r55_common_exactness_intro.patch import replace_lines_preserving_eol
    desired = replace_lines_preserving_eol(original.decode('utf-8')).encode('utf-8')
    target = guard_globals['TARGET']
    extra_name = 'extra.txt'
    tree = tmp_path / 'repo'
    tree.mkdir()
    (tree / target).write_bytes(desired if installed else original)
    (tree / extra_name).write_bytes(b'unchanged\n')
    baseline_blobs = {target: original, extra_name: b'unchanged\n'}
    dummy_sha = {name: guard_globals['sha_blob'](contents)
                 for name, contents in baseline_blobs.items()}
    head = guard_globals['REVIEWED_HEAD']
    changed = (target,) if installed else ()

    def fake_git(*args: str) -> bytes:
        if args == ('rev-parse', '--show-toplevel'):
            return str(tree).encode('utf-8') + b'\n'
        if args == ('branch', '--show-current'):
            return b'develop\n'
        if args == ('rev-parse', 'HEAD'):
            return head.encode('ascii') + b'\n'
        if args == ('ls-remote', 'origin', 'refs/heads/develop'):
            return head.encode('ascii') + b'\trefs/heads/develop\n'
        if args == ('diff', '--cached', '--name-only'):
            return b''
        if args == ('diff', '--name-only'):
            return b''.join(item.encode('utf-8') + b'\n' for item in changed)
        if len(args) == 2 and args[0] == 'show' and args[1].startswith('HEAD:'):
            return baseline_blobs[args[1][5:]]
        raise AssertionError(args)

    # The function keeps its original module globals, which runpy returns as a
    # dictionary only after running the module; override them in place via
    # the underlying function globals (no project production imports patched).
    guard = guard_globals['verify_checkout']
    guard.__globals__['ROOT'] = tree
    guard.__globals__['BLOBS'] = dummy_sha
    guard.__globals__['git'] = fake_git
    return guard()


def test_complete_guard_accepts_uninstalled_baseline(monkeypatch, tmp_path: Path) -> None:
    observed = _mock_checkout(monkeypatch, tmp_path, installed=False)
    assert observed['source_guard'] == 'PASS'
    assert observed['r55_renderer_installed'] is False
    assert observed['tracked_changes'] == ()


def test_complete_guard_accepts_installed_patch(monkeypatch, tmp_path: Path) -> None:
    observed = _mock_checkout(monkeypatch, tmp_path, installed=True)
    assert observed['source_guard'] == 'PASS'
    assert observed['r55_renderer_installed'] is True
    assert observed['tracked_changes'] == ('phase168_r3_5_model_renderer.py',)
