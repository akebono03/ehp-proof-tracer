from pathlib import Path
import ast


def test_audit_code_parses():
    filename = Path(__file__).resolve().parents[1] / 'audit.py'
    ast.parse(filename.read_text(encoding='utf-8'))


def test_audit_is_read_only():
    filename = Path(__file__).resolve().parents[1] / 'audit.py'
    source = filename.read_text(encoding='utf-8')
    assert 'render_model_backed_narrative_markdown(result, model)' in source
    assert 'model.step_citation_numbers' in source
    assert "OUT / 'renderer_integrity_audit.json'" in source
    assert 'patch.object' not in source
