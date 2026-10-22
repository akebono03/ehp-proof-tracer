from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE = Path(__file__).resolve().parents[1] / 'apply.py'
spec = importlib.util.spec_from_file_location('phase168_r2_7_patch', MODULE)
assert spec is not None and spec.loader is not None
patch_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch_module)


def _sample(newline: str) -> bytes:
    content = (
        'def screen_shared_proof_context():\n'
        '    from dataclasses import is_dataclass\n'
        '    for assertion in []:\n'
        '        if not is_dataclass(assertion.content) or isinstance(assertion.content, type):\n'
        '            continue\n'
        '        if type(assertion.content) is type(goal) and assertion.content == goal:\n'
        '            continue\n'
    )
    return content.replace('\n', newline).encode('utf-8')


def test_patch_lf_and_idempotence():
    changed, applied = patch_module.modify_source(_sample('\n'))
    assert applied
    assert b'TodaFixedStatementComponent' in changed
    again, twice = patch_module.modify_source(changed)
    assert not twice and again == changed


def test_patch_crlf_preserves_endings():
    changed, applied = patch_module.modify_source(_sample('\r\n'))
    assert applied
    assert changed.count(b'\r\n') == changed.count(b'\n')
    assert b'"TodaFixedStatementComponent":\r\n' in changed


def test_patch_rejects_unknown_target():
    original = _sample('\n').replace(b'is_dataclass(assertion.content)', b'bool(assertion.content)')
    try:
        patch_module.modify_source(original)
    except ValueError as error:
        assert 'GUARD_MISMATCH' in str(error)
    else:
        raise AssertionError('unexpected acceptance')
