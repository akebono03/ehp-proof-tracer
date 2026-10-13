"""Targeted presentation-only regression tests for R52-R6."""
from pathlib import Path

from web_app import create_app


def test_group_only_layout_preserves_group_query_and_proof_markup():
    response = create_app().test_client().get("/")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'id="phase165-group-proof-only-layout"' in html
    assert 'main > nav,' in html
    assert 'section:not(#group-query)' in html
    assert '[aria-labelledby="result-heading"]' in html
    assert '[aria-labelledby="group-proof-heading"]' in html
    assert 'id="group-query"' in html
    assert 'name="form_kind"' in html
    assert 'value="group"' in html
    assert 'id="group-proof-progress-query"' in html
    assert 'value="group_proof_progress"' in html
    assert 'id="generator-proof-query"' in html


def test_group_only_layout_does_not_change_application_logic():
    root = Path(__file__).resolve().parent
    assert (root / 'phase165_r52_r5_auto_search.py').is_file()
    response = create_app().test_client().get('/')
    assert response.status_code == 200
    assert b'<h1>EHP Proof Tracer</h1>' in response.data
    # All original forms remain in the DOM for compatibility; CSS only hides them.
    assert b'Generator exploration' in response.data
    assert b'Operation query' in response.data


def test_group_only_layout_does_not_modify_math_renderer():
    root = Path(__file__).resolve().parent
    template = (root / 'templates' / 'index.html').read_text(encoding='utf-8-sig')
    assert 'web_math.js' in template
    assert 'group-proof-rendered-lines' in template
    assert 'group-proof-conclusion' in template
