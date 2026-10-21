from expression import HomotopyElement, IteratedSuspension
from toda_human_readable_renderer import render_toda_expression_latex
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from toda_human_readable_renderer import render_toda_public_group_relation_latex


def test_one_suspension_has_no_exponent():
    nu_prime = HomotopyElement('ν′', 3, source=6, target=3)
    assert render_toda_expression_latex(IteratedSuspension(nu_prime, 1)) == r"E\nu'"


def test_other_suspension_exponents_unchanged():
    nu_prime = HomotopyElement('ν′', 3, source=6, target=3)
    assert render_toda_expression_latex(IteratedSuspension(nu_prime, 2)) == r"E^{2}\nu'"


def test_pi74_and_pi158_display_no_e_one():
    for n, k in ((4, 3), (8, 7)):
        candidates = database_structured_group_goal_candidates(n=n, k=k)
        assert len(candidates) == 1
        latex = render_toda_public_group_relation_latex(candidates[0])
        assert latex is not None
        assert 'E^{1}' not in latex
        assert 'E' in latex
