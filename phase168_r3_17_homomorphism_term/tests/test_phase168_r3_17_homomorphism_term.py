from pathlib import Path

from web_group_proof import build_standard_web_group_proof_view


def test_homomorphism_guard_uses_actual_narrative_term():
    source = Path('toda_group_proof_narrative_renderer.py').read_text(encoding='utf-8-sig')
    assert 'if "準同型定理" not in "\\n\\n".join(paragraphs):' in source
    assert 'if "第一同型定理" not in "\\n\\n".join(paragraphs):' not in source


def test_pi43_homomorphism_theorem_paragraph_not_duplicated():
    view = build_standard_web_group_proof_view(3, 1, mode='narrative')
    rows = tuple(' '.join((line.prefix, line.statement_latex or '', line.suffix)) for line in view.rendered_lines)
    homomorphism_rows = tuple(row for row in rows if '準同型定理' in row)
    assert len(homomorphism_rows) == 1, homomorphism_rows
    assert all('第一同型定理' not in row for row in rows)
    assert any(r'\pi_{4}^{3}' in row for row in rows)


def test_pi32_conclusion_remains_present():
    view = build_standard_web_group_proof_view(2, 1, mode='narrative')
    assert any(r'\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}' == line.statement_latex for line in view.rendered_lines)
