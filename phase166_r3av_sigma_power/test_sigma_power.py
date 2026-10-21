from expression import Composition, GeneratorSymbol, HomotopyElement
from toda_human_readable_renderer import render_toda_expression_latex


def sigma(n):
    return HomotopyElement(name=f"σ{n}", dimension=n, source=n+7, target=n, generator=GeneratorSymbol(family="σ", index=n))


def compose(*factors):
    value = factors[-1]
    for factor in reversed(factors[:-1]):
        value = Composition(factor, value)
    return value


def test_sigma_fourfold_consecutive_display():
    value = compose(sigma(11), sigma(18), sigma(25), sigma(32))
    assert render_toda_expression_latex(value) == r"\sigma_{11}^{4}"


def test_sigma_nonconsecutive_does_not_compress():
    value = compose(sigma(11), sigma(25))
    assert render_toda_expression_latex(value) == r"\sigma_{11}\sigma_{25}"


def test_sigma_mixed_families_do_not_compress():
    eta = HomotopyElement(name="η18", dimension=18, source=19, target=18, generator=GeneratorSymbol(family="η", index=18))
    value = compose(sigma(11), eta)
    assert render_toda_expression_latex(value) == r"\sigma_{11}\eta_{18}"
