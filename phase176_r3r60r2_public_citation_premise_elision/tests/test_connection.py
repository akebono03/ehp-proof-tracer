"""Public hook and strict historical-stage contracts."""
import pytest

from phase176_r3r60r2_public_citation_premise_elision.apply import (
    ROOT, PINS, previous_source, updated_source, planned_changes, previous_stage,
)
from phase176_r3r60r2_public_citation_premise_elision.audit import observe


def test_exact_replacements_and_unknown_bytes():
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        assert updated_source(path, raw) == raw
        prior = previous_source(path, raw)
        assert prior != raw
        for eol in (b'\n', b'\r\n'):
            base = prior.replace(b'\r\n', b'\n').replace(b'\n', eol)
            new = updated_source(path, base)
            assert previous_source(path, new) == base
            assert updated_source(path, new) == new
        with pytest.raises(ValueError):
            updated_source(path, raw + b'\n# unknown edit\n')


def test_prior_stage_is_exact_and_restored():
    from phase176_r3r60r1_citation_premise_elision_isolated import projection
    from phase176_r3r60r1_citation_premise_elision_isolated.audit import preflight
    current = {path: (ROOT / path).read_bytes() for path in PINS}
    hook = projection.project_citation_premise_elision
    assert all(raw == new for raw, new in planned_changes().values())
    with previous_stage():
        assert preflight()
        assert all((ROOT / path).read_bytes() == previous_source(path, raw)
                   for path, raw in current.items())
        assert projection.project_citation_premise_elision is not hook
        with previous_stage():
            assert preflight()
        assert projection.project_citation_premise_elision is not hook
    assert projection.project_citation_premise_elision is hook
    assert all((ROOT / path).read_bytes() == raw for path, raw in current.items())


def test_actual_public_elision():
    report = observe()
    assert report['gate'] == 'PASS_R3R60R2_PUBLIC_CITATION_PREMISE_ELISION_CONNECTED'
    assert (report['body_rows_before'], report['body_rows_after']) == (19, 18)
    assert (report['display_reference_count_before'], report['display_reference_count_after']) == (10, 9)
    assert report['citation_count'] == 10
    assert report['plan']['display_number_map'] == {**{i:i for i in range(1,9)},10:9}
    assert report['model_unchanged'] and report['partial_render_unchanged']
    assert report['retained_reference_blocks_unchanged_except_display_numbers']
    assert report['public_adapter_verified'] and report['root_display_count'] == 1
    assert report['references_without_explicit_body_use'] == []
