"""Isolated guard tests: do not need to import the production repository."""
from __future__ import annotations

import pytest

from phase172_r3r2_r2_test_contract_correction.install import (
    NEW_ASSERTIONS, OLD_ASSERTION, TARGET_TEST_NAME, function_text, normalize,
    transform_test, unique_function,
)


def source() -> bytes:
    return (
        'from __future__ import annotations\n'
        '\n'
        f'def {TARGET_TEST_NAME}(verified_pi63):\n'
        '    references = "[R4] Proposition 2.2. [R5] (5.3)."\n'
        '    body = "proof"\n'
        + OLD_ASSERTION + '\n'
    ).encode('utf-8')


def test_replaces_only_legacy_visibility_assertion():
    result = transform_test(source())
    output = normalize(result)
    assert NEW_ASSERTIONS in output
    assert OLD_ASSERTION not in output
    assert '    body = "proof"' in output
    assert TARGET_TEST_NAME in function_text(result)


def test_works_with_windows_newlines():
    baseline = source().replace(b'\n', b'\r\n')
    result = transform_test(baseline)
    assert b'\r\n' in result
    assert b'\n' not in result.replace(b'\r\n', b'')


def test_rejects_duplicate_and_missing_assertions():
    with pytest.raises(RuntimeError):
        transform_test(source() + OLD_ASSERTION.encode('utf-8') + b'\n')
    with pytest.raises(RuntimeError):
        transform_test(source().replace(OLD_ASSERTION.encode('utf-8'), b'    assert True'))


def test_rejects_reapplying_patch():
    updated = transform_test(source())
    with pytest.raises(RuntimeError):
        transform_test(updated)


def test_rejects_assertion_outside_target_function():
    bad = (
        'def ' + TARGET_TEST_NAME + '(verified_pi63):\n'
        '    assert True\n'
        '\n'
        'def unrelated():\n' + OLD_ASSERTION + '\n'
    ).encode('utf-8')
    with pytest.raises(RuntimeError):
        transform_test(bad)


def test_unique_function_rejects_ambiguous_target():
    body = normalize(source())
    with pytest.raises(RuntimeError):
        unique_function(body + '\n' + body, TARGET_TEST_NAME)
