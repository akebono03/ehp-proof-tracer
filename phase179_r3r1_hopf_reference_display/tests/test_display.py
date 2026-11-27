"""The shared source projection keeps the source's ordinary sphere notation."""
from phase168_r3_37c_reference_projection import project_reference_bodies
from phase174_r3_r6_r2_prop44_lemma54.source import (
    PRELUDE_ASSERTION_ID, build_cited_preprop44_splitting,
)


def test_hopf_splitting_reference_preserves_sphere_notation_and_line_breaks():
    bridge = build_cited_preprop44_splitting()
    body, = project_reference_bodies(bridge.registry, (PRELUDE_ASSERTION_ID,))
    assert body.splitlines() == [
        r'$n=2,4,8$ のとき,',
        r'Hopf fibration $h:S^{2n-1}\to S^n$ が存在し,',
        r'$E+h_*:\pi_{i-1}(S^{n-1})\oplus\pi_i(S^{2n-1})\xrightarrow{\cong}\pi_i(S^n)$',
        r'は任意の $i$ で同型である (Steenrod 1951 を引用).',
    ]
    assert r'\pi_{i-1}^{n-1}' not in body
    assert 'H(h)' not in body
