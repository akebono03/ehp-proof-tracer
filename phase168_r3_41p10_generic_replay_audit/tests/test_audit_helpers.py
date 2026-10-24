"""Pure audit helper tests: do not require EHP runtime execution."""
from phase168_r3_41p10_generic_replay_audit.audit import (
    normalized_newlines, render_summary,
)


def test_normalized_newlines():
    assert normalized_newlines('a\r\nb\rc\n') == 'a\nb\nc\n'


def test_render_summary_has_full_suite_disclaimer():
    rendered = render_summary({'cases': {}, 'counterfeits': {}, 'status': 'PASS'})
    assert 'FULL_PYTEST_NOT_RUN' in rendered
    assert 'GIVEN' in rendered


def test_render_summary_keeps_failure():
    report = {'status': 'ERROR', 'error': 'provisional failure', 'cases': {}, 'counterfeits': {}}
    rendered = render_summary(report)
    assert 'provisional failure' in rendered
    assert 'AUDIT_STATUS**: ERROR' in rendered
