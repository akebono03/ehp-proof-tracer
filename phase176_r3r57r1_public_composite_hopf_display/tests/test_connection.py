"""Verify all replacements against their exact previous stage."""
import pytest

from phase176_r3r57r1_public_composite_hopf_display.apply import (
    ROOT, PINS, LAYOUT, previous_source, updated_source, planned_changes,
)
from phase176_r3r56r3_public_cited_source_display import apply as r56


def test_exact_replacements_are_idempotent_and_reject_unknown_bytes():
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        assert updated_source(path, raw) == raw
        base = previous_source(path, raw)
        for eol in (b'\n', b'\r\n'):
            previous = base.replace(b'\r\n', b'\n').replace(b'\n', eol)
            changed = updated_source(path, previous)
            assert previous_source(path, changed) == previous
            assert updated_source(path, changed) == changed
        with pytest.raises(ValueError):
            updated_source(path, raw + b'\n# unknown edit\n')


def test_previous_public_source_connection_is_preserved():
    changes = planned_changes()
    assert all(raw == changed for raw, changed in changes.values())
    prior = previous_source(LAYOUT, changes[LAYOUT][0])
    assert r56.updated_source(LAYOUT, prior) == prior
