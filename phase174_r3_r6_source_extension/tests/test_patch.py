"""Guarded local replacement contracts; no real repository mutation."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r6_source_extension.patch import (
    connect_shared,
    replace_r3r4_test,
    replace_preflight_audit,
)


SHARED_FIXTURE = b'''def build_shared_typed_bridge():
    if True:
        sources = sources + (build_cited_prop22_right_reference(production),)
    registry = UnifiedStatementRegistry()
    return registry

def shared_expansion_provider():
    def expand(goal):
        options.extend(expand_toda48_index_two(goal))
        options.extend(expand_finite_index_two_cyclic_structure(goal))
        options.extend(expand_finite_cyclic_relation(goal))
        return options
    return expand
'''


def test_shared_patch_only_two_full_function_targets_and_idempotent() -> None:
    revised = connect_shared(SHARED_FIXTURE)
    assert connect_shared(revised) == revised
    assert revised.count(b'build_cited_extension_sources()') == 1
    assert revised.count(b'expand_cited_toda55_double(goal, tuple(available))') == 1
    assert ast.parse(revised)


def test_shared_patch_rejects_changed_or_duplicated_anchor() -> None:
    with pytest.raises(ValueError, match='insertion context'):
        connect_shared(SHARED_FIXTURE.replace(b'expand_toda48_index_two', b'unreviewed_rule'))
    with pytest.raises(ValueError, match='insertion context'):
        connect_shared(SHARED_FIXTURE + SHARED_FIXTURE)


def test_crlf_checkout_preserves_line_endings_and_syntax() -> None:
    crlf = SHARED_FIXTURE.replace(b'\n', b'\r\n')
    transformed = connect_shared(crlf)
    assert b'\r\n' in transformed
    assert transformed.replace(b'\r\n', b'').count(b'\n') == 0
    assert ast.parse(transformed)


def test_prior_regression_test_patch_only_accepts_reviewed_chain() -> None:
    source = (
        "from pathlib import Path\n"
        "\n"
        "def test_r3r4_real_production_file_has_only_reviewed_wiring():\n"
        "    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared\n"
        "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    r3r4 = replace_provider_call(old)\n"
        "    assert current in (r3r4, insert_shared(r3r4))\n"
    ).encode('utf-8')
    transformed = replace_r3r4_test(source)
    assert replace_r3r4_test(transformed) == transformed
    assert b'connect_shared(r3r5)' in transformed
    with pytest.raises(ValueError, match='insertion context'):
        replace_r3r4_test(source.replace(b'insert_shared(r3r4)', b'arbitrary(r3r4)'))


def test_preflight_complete_function_replacement_parses() -> None:
    source = (
        'from __future__ import annotations\n'
        'from pathlib import Path\n'
        'from typing import Any\n'
        '\n'
        'def inspect_source_provider(root: Path) -> dict[str, Any]:\n'
        '    return {"state": "COMMITTED"}\n'
        '\n'
        'def unaffected():\n'
        '    return 1\n'
    ).encode('utf-8')
    updated = replace_preflight_audit(source)
    assert b'def unaffected():' in updated
    assert updated.count(b'def inspect_source_provider') == 1
    assert ast.parse(updated)
