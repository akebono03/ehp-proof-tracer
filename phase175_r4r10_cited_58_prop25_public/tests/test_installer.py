"""AST / EOL / drift contracts for minimal full-function installation."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r10_cited_58_prop25_public import installer


def fixture_source() -> str:
    return (
        'def build_shared_typed_bridge():\n'
        '    if True:\n'
        + installer.BRIDGE_ANCHOR
        + '    return 1\n\n'
        'def shared_expansion_provider(bridge):\n'
        + installer.PROVIDER_ANCHOR
        + '    return bridge\n\n'
        'def unrelated():\n    return "unchanged"\n'
    )


def test_complete_bridge_replacement_keeps_other_functions() -> None:
    original = fixture_source()
    result, complete = installer.replace_full_function(
        original, installer.BRIDGE_FUNCTION,
        installer.BRIDGE_ANCHOR, installer.BRIDGE_ADDITION,
    )
    ast.parse(result)
    assert complete.startswith('def build_shared_typed_bridge():')
    assert complete.count('build_cited_58_prop25_sources()') == 1
    assert 'def unrelated():\n    return "unchanged"' in result


def test_complete_provider_replacement_keeps_other_functions() -> None:
    original = fixture_source()
    result, complete = installer.replace_full_function(
        original, installer.PROVIDER_FUNCTION,
        installer.PROVIDER_ANCHOR, installer.PROVIDER_ADDITION,
    )
    ast.parse(result)
    assert complete.startswith('def shared_expansion_provider(bridge):')
    assert complete.count('build_cited_58_prop25_provider(bridge)') == 1
    assert installer.BRIDGE_ADDITION not in result


def test_two_function_install_is_idempotent() -> None:
    first, _ = installer.replace_full_function(
        fixture_source(), installer.BRIDGE_FUNCTION,
        installer.BRIDGE_ANCHOR, installer.BRIDGE_ADDITION,
    )
    first, _ = installer.replace_full_function(
        first, installer.PROVIDER_FUNCTION,
        installer.PROVIDER_ANCHOR, installer.PROVIDER_ADDITION,
    )
    second, _ = installer.replace_full_function(
        first, installer.BRIDGE_FUNCTION,
        installer.BRIDGE_ANCHOR, installer.BRIDGE_ADDITION,
    )
    second, _ = installer.replace_full_function(
        second, installer.PROVIDER_FUNCTION,
        installer.PROVIDER_ANCHOR, installer.PROVIDER_ADDITION,
    )
    assert first == second
    assert second.count('build_cited_58_prop25_sources()') == 1
    assert second.count('build_cited_58_prop25_provider(bridge)') == 1


@pytest.mark.parametrize('change', ('deleted', 'twice', 'invalid'))
def test_unreviewed_function_rejected(change: str) -> None:
    source = fixture_source()
    if change == 'deleted':
        source = source.replace(installer.BRIDGE_ANCHOR, '        pass\n')
    elif change == 'twice':
        source = source.replace(installer.BRIDGE_ANCHOR, installer.BRIDGE_ANCHOR * 2)
    else:
        source = source.replace('def build_shared_typed_bridge():', 'def build_shared_typed_bridge(')
    with pytest.raises((RuntimeError, SyntaxError)):
        installer.replace_full_function(
            source, installer.BRIDGE_FUNCTION,
            installer.BRIDGE_ANCHOR, installer.BRIDGE_ADDITION,
        )


def test_plan_rejects_unreviewed_committed_blob(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / installer.TARGET).write_text(fixture_source(), encoding='utf-8')
    monkeypatch.setattr(installer, 'git', lambda root, *args: '0' * 40)
    with pytest.raises(RuntimeError, match='UNREVIEWED_PRODUCTION_COMMIT'):
        installer.plan(tmp_path)


def test_plan_requires_exactly_reviewed_source(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / installer.TARGET).write_text(fixture_source(), encoding='utf-8')
    monkeypatch.setattr(installer, 'git', lambda root, *args: installer.EXPECTED_COMMITTED_BLOB)
    with pytest.raises(RuntimeError, match='UNREVIEWED_LOCAL_PRODUCTION_CHANGE'):
        installer.plan(tmp_path)


def test_plan_accepts_windows_crlf_checkout_of_reviewed_blob(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_lf = fixture_source().encode('utf-8')
    reviewed_blob = installer.git_blob_sha(original_lf)
    monkeypatch.setattr(installer, 'EXPECTED_COMMITTED_BLOB', reviewed_blob)
    monkeypatch.setattr(installer, 'git', lambda root, *args: reviewed_blob)
    (tmp_path / installer.TARGET).write_bytes(original_lf.replace(b'\n', b'\r\n'))
    path, before, after, functions = installer.plan(tmp_path)
    assert path == tmp_path / installer.TARGET
    assert b'\r\n' in before and b'\r\n' in after
    assert b'\n' not in after.replace(b'\r\n', b'')
    assert after != before
    assert len(functions) == 2


def test_dry_run_exports_whole_functions_without_mutating_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = fixture_source().encode('utf-8')
    reviewed_blob = installer.git_blob_sha(original)
    monkeypatch.setattr(installer, 'EXPECTED_COMMITTED_BLOB', reviewed_blob)
    monkeypatch.setattr(installer, 'git', lambda root, *args: reviewed_blob)
    target = tmp_path / installer.TARGET
    target.write_bytes(original)
    report = installer.install(tmp_path, dry_run=True, output=tmp_path / 'output')
    assert target.read_bytes() == original
    assert report['patch_required'] is True
    assert report['patch_applied'] is False
    assert (tmp_path / 'output' / 'build_shared_typed_bridge_FULL_AFTER.py').is_file()
    assert (tmp_path / 'output' / 'shared_expansion_provider_FULL_AFTER.py').is_file()
    assert (tmp_path / 'output' / 'phase165_r52_r9_shared_math_FULL_AFTER.py').is_file()
