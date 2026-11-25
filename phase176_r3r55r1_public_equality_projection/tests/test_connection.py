"""Exact connection checks; no synthetic accepted proof."""
import ast

import pytest

from phase176_r3r55r1_public_equality_projection.apply import (
    ANCHOR, INSERT, TARGET, baseline_source, function_node, updated_source,
)


def test_exact_public_connection_idempotent_and_other_bytes_preserved():
    raw = TARGET.read_bytes()
    assert updated_source(raw) == raw
    base, _ = baseline_source(raw)
    expected = base.replace(ANCHOR, INSERT + ANCHOR, 1)
    assert expected.count(INSERT) == 1
    for eol in ('\n', '\r\n'):
        original = base.replace('\n', eol).encode('utf-8')
        connected = expected.replace('\n', eol).encode('utf-8')
        assert updated_source(original) == connected
        assert updated_source(connected) == connected
    with pytest.raises(ValueError):
        updated_source(raw + b'\n# unreviewed edit\n')


def test_only_render_function_changed_and_projection_is_local():
    raw = TARGET.read_bytes()
    base, _ = baseline_source(raw)
    changed = base.replace(ANCHOR, INSERT + ANCHOR, 1)
    old, new = ast.parse(base), ast.parse(changed)
    old_other = [ast.dump(n) for n in old.body if n is not None and not (isinstance(n, ast.FunctionDef) and n.name == 'render_model_backed_narrative_markdown')]
    new_other = [ast.dump(n) for n in new.body if n is not None and not (isinstance(n, ast.FunctionDef) and n.name == 'render_model_backed_narrative_markdown')]
    assert old_other == new_other
    assert INSERT.rstrip() in ast.get_source_segment(changed, function_node(changed))
    assert '_r55_observe_projection' not in changed
