from expression import HomotopyElement
from toda_human_readable_renderer import render_toda_expression_latex


def test_r3ar_delta_eta_numeric_index():
    expr = HomotopyElement(name='Δ(η41)', dimension=20, source=40, target=20)
    assert render_toda_expression_latex(expr) == r'\Delta(\eta_{41})'


def test_r3ar_double_bar_beta():
    expr = HomotopyElement(name='β̅̅', dimension=20, source=40, target=20)
    assert render_toda_expression_latex(expr) == r'\bar{\bar{\beta}}'


def test_r3ar_single_bar():
    expr = HomotopyElement(name='ν̅', dimension=6, source=14, target=6)
    assert render_toda_expression_latex(expr) == r'\bar{\nu}'


def test_r3ar_existing_prime():
    expr = HomotopyElement(name='ν′', dimension=3, source=6, target=3)
    assert render_toda_expression_latex(expr) == r"\nu'"
