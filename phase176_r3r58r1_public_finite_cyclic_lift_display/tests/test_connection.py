"""Strict inverse checks and actual public Web integration."""
import pytest

from phase176_r3r58r1_public_finite_cyclic_lift_display.apply import (
    ROOT, PINS, previous_source, updated_source, planned_changes, r57_stage_changes,
)
from phase176_r3r58r1_public_finite_cyclic_lift_display.audit import observe


def test_exact_replacements_and_unknown_bytes():
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        assert updated_source(path, raw) == raw
        previous = previous_source(path, raw)
        assert previous != raw
        for eol in (b'\n', b'\r\n'):
            base = previous.replace(b'\r\n', b'\n').replace(b'\n', eol)
            new = updated_source(path, base)
            assert previous_source(path, new) == base
            assert updated_source(path, new) == new
        with pytest.raises(ValueError):
            updated_source(path, raw + b'\n# unknown edit\n')


def test_prior_stage_is_preserved():
    assert all(raw == new for raw, new in planned_changes().values())
    assert all(raw == new for raw, new in r57_stage_changes().values())


def test_public_finite_cyclic_lift_on_verified_model():
    report = observe()
    assert report['gate'] == 'PASS_R3R58R1_PUBLIC_FINITE_CYCLIC_LIFT_DISPLAY_CONNECTED'
    assert report['body_rows_before'] == 18 and report['body_rows_after'] == 21
    assert report['root_display_count'] == 1
    assert report['references_without_explicit_body_use'] == []
    assert report['model_unchanged'] and report['partial_render_unchanged']
