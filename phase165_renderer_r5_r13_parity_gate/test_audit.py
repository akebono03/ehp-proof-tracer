"""Focused tests for the R5-R13 audit; no application fixtures."""
from pathlib import Path

from audit import classify_exception, defined, imported, load_tree, report, run_renderer


def test_imported_symbol_detection(tmp_path: Path):
    path = tmp_path / 'a.py'
    path.write_text('from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n', encoding='utf-8')
    tree = load_tree(path)
    assert imported(tree, 'phase162_ehp_leaf_inputs', '_phase162_ehp_leaves')
    assert not imported(tree, 'other', '_phase162_ehp_leaves')


def test_bom_is_supported(tmp_path: Path):
    path = tmp_path / 'a.py'
    path.write_bytes(b'\xef\xbb\xbfdef f():\n    return 1\n')
    assert defined(load_tree(path), 'f')


def test_defined_functions():
    import ast
    tree = ast.parse('def first():\n    pass\n')
    assert defined(tree, 'first')
    assert not defined(tree, 'other')


def test_runtime_renderer_produces_sections():
    result = run_renderer(lambda: '## 証明対象\n\n## 証明\n')
    assert result['status'] == 'RENDERED'
    assert result['sections'] == ['## 証明対象', '## 証明']


def test_runtime_renderer_reports_failures_without_success():
    def fail():
        raise IndexError('tuple index out of range')
    result = run_renderer(fail)
    assert result['status'] == 'ERROR'
    assert result['type'] == 'IndexError'


def test_runtime_renderer_rejects_non_string():
    assert run_renderer(lambda: None)['status'] == 'NON_STRING'


def test_exception_classification():
    result = classify_exception(ValueError('invalid'))
    assert result['status'] == 'ERROR'
    assert result['type'] == 'ValueError'


def test_report_handles_blocked_precondition():
    text = report({'status': 'PRECONDITION_FAILED', 'guards': {'missing': False}, 'runtime': None})
    assert 'FAIL' in text
    assert '自動置換しない' in text


def test_report_handles_comparable_output():
    result = {'status': 'REVIEW_REQUIRED', 'guards': {'valid': True}, 'runtime': {
        'legacy': {'status': 'RENDERED', 'length': 5, 'sections': ['## 証明']},
        'canonical': {'status': 'ERROR', 'type': 'ValueError', 'message': 'bad'},
        'decision': 'BLOCKED_RUNTIME_INPUTS_NO_AUTOMATIC_REPLACEMENT'}}
    assert 'ValueError' in report(result)
