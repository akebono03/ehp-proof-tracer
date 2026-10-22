from phase167_r4_5_latex_audit.audit import validate_latex


def test_balanced_latex_examples():
    assert validate_latex(r"\pi_{4}^{3}\cong \mathbb{Z}/2\{\eta_3\}") == []
    assert validate_latex(r"\left(\frac{a}{b}\right)") == []


def test_unbalanced_latex_is_detected():
    assert validate_latex(r"\frac{a}{b") != []
    assert validate_latex(r"\left(a") != []
