from web_group_proof import build_standard_web_group_proof_view


def _view(n, k=1):
    view = build_standard_web_group_proof_view(n, k, max_depth=2, mode='narrative')
    return tuple((line.prefix, line.statement_latex or '', line.suffix) for line in view.rendered_lines)


def test_r46_general_form_reference_only_and_specialized_proof():
    rows = _view(3)
    proof_index = next(i for i, (prefix, _, _) in enumerate(rows) if prefix == '証明')
    reference, proof = rows[:proof_index], rows[proof_index+1:]
    assert any(r'\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}' in math for _, math, _ in reference)
    assert not any(math == r'\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}' for _, math, _ in proof)
    target = r'\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}'
    matched = [(prefix, math) for prefix, math, _ in proof if math == target]
    assert len(matched) == 1
    assert matched[0][0].replace(' ', '') == '[R1]より,'
    assert len(rows) == 24


def test_r46_pi32_unchanged():
    rows = _view(2)
    assert len(rows) == 25
    for n in (1, 2, 3):
        target = rf'\pi_{{{n}}}^{{{n}}} = \mathbb{{Z}}\{{\iota_{{{n}}}\}}'
        assert any(math == target and prefix.replace(' ', '') == '[R1]より,' for prefix, math, _ in rows)


def test_r46_pi43_ehp_and_conclusion_unchanged():
    content = '\n'.join(''.join(row) for row in _view(3))
    assert r'\operatorname{Im}\Delta' in content
    assert r'\ker E' in content
    assert '準同型定理' in content
    assert r'\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}' in content


def test_r46_other_stems_unmodified():
    for n in (4, 5, 6):
        assert len(_view(n)) == 15
