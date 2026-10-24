"""Scoped Web Narrative checks; no full repository suite."""
from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections


def test_phase168_r3_39g_reference_diagonal_condition():
    for n, k in ((2, 1), (3, 1)):
        current, _, _ = capture(n, k)
        refs, _ = sections(current)
        assert r'\quad(n\ge 1)' in refs


def test_phase168_r3_39g_pi32_explanation():
    current, _, _ = capture(2, 1)
    _, proof = sections(current)
    assert '完全性より' in proof
    assert r'\operatorname{Im}\Delta=\ker E=0' in proof
    assert '単射性と全射性より' in proof


def test_phase168_r3_39g_pi43_explanation():
    current, _, _ = capture(3, 1)
    _, proof = sections(current)
    assert '完全性より' in proof
    assert 'は全射' in proof
    assert '準同型定理より' in proof


def test_phase168_r3_39g_pi54_order():
    current, _, _ = capture(4, 1)
    _, proof = sections(current)
    source = proof.index(r'\pi_{4}^{3} = \mathbb{Z}/2')
    image = proof.index(r'E(\eta_{3})=\eta_{4}')
    assert source < image
    assert r'E: \pi_{4}^{3}\to \pi_{5}^{4}' in proof
