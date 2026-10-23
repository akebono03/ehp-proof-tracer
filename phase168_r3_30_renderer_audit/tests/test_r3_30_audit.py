from pathlib import Path
from audit import audit_sources, report_markdown


def test_audit_is_read_only_and_includes_key_components():
    report = audit_sources()
    assert report['status'] == 'AUDIT_ONLY'
    assert all(report['sources'][key]['exists'] for key in
               ('renderer', 'narrative_model', 'body_binding', 'exactness', 'typed', 'order'))
    renderer = report['sources']['renderer']
    assert renderer['uses_exactness_projection']
    assert renderer['uses_order_projection']
    assert renderer['uses_typed_projection']
    assert renderer['references_citation_model']
    assert not renderer['reaches_legacy_renderer_by_direct_import']


def test_report_contains_scope_limitations():
    text = report_markdown(audit_sources())
    assert 'Renderer 構造監査' in text
    assert '注意' in text
