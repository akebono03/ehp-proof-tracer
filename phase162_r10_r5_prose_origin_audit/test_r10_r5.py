"""Fast local tests for the read-only R10-R5 audit helpers."""
from audit import ancestor_distances, math_expressions, normalize_math


def test_phase162_r10_r5_math_normalization():
    assert normalize_math(r' H\left(\nu^\prime\right) = \eta_5 ') == normalize_math(r'H(\nu^\prime)=\eta_5')


def test_phase162_r10_r5_inline_math_extraction():
    assert math_expressions(r'[R1]より, $H(\nu)=\eta_5$ が成り立つ.') == (r'H(\nu)=\eta_5',)


def test_phase162_r10_r5_ancestry_counts_identity():
    class Step:
        def __init__(self, *premises):
            self.premises = premises
    leaf = Step()
    left = Step(leaf)
    right = Step(leaf)
    root = Step(left, right)
    distances = ancestor_distances(root)
    assert len(distances) == 4
    assert distances[id(leaf)] == 2
