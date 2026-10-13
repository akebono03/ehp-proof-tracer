from web_group_proof import build_standard_web_group_proof_view


def test_r50_final_exactness_is_only_displayed_once():
    view = build_standard_web_group_proof_view(
        n=2, k=1, max_depth=2, mode='narrative'
    )
    text = '\n'.join(
        line.prefix + (line.statement_latex or '') + line.suffix
        for line in view.rendered_lines
    )
    references = text.split('使用する結果', 1)[1].split('証明', 1)[0]
    proof = text.split('証明\n', 1)[1]
    assert '(5.1)' in references
    assert 'Proposition 5.1' in references
    assert 'Proposition 4.2' in references
    assert '[R3]' in proof
    assert proof.count('は完全である') == 0
    assert r'\operatorname{Im}' in proof
    assert r'\ker E=0' in proof
    assert proof.count('は零写像') == 1
    assert proof.index('は単射') < proof.index('は全射') < proof.index('単射性と全射性より')
