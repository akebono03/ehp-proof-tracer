from web_group_proof import build_standard_web_group_proof_view


def test_phase165_r50_general_reference_and_proof_boundary():
    view = build_standard_web_group_proof_view(n=2, k=1, max_depth=2, mode='narrative')
    text = '\n'.join(line.prefix + (line.statement_latex or '') + line.suffix for line in view.rendered_lines)
    references = text.split('使用する結果', 1)[1].split('証明', 1)[0]
    body = text.split('証明', 2)[-1]
    assert '(5.1)' in references
    assert r'\pi_{i}^{1}' in references
    assert r'\pi_{n}^{n}' in references
    assert 'Proposition 5.1' in references
    assert 'Proposition 4.2' in references
    assert r'\pi_{i}^{n+1}' in references
    assert r'\pi_{3}^{3}' in body
    assert 'Im' in body and 'ker' in body
    assert body.index('は単射') < body.index('は全射') < body.index('単射性と全射性より')
    assert body.count('は零写像') == 1
