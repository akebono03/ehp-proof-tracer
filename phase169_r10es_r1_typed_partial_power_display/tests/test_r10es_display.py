"""R10ES typed composition-run display tests; no new group proof rule."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase169_r10eb_typed_composition_power.display import (
    typed_stable_composition_power_latex,
)
from toda_human_readable_renderer import (
    render_toda_expression_latex,
    render_toda_public_group_generator_latex,
)


def _element(family_id: int, n: int) -> HomotopyElement:
    row, = (row for row in read_registered_stable_families()
            if row.family_id == family_id)
    return HomotopyElement(
        name=row.name_at(n), dimension=n,
        source=n + row.stem, target=n,
        generator=GeneratorSymbol(family=row.symbol_family, index=n),
    )


def _compose(*factors: HomotopyElement, left_associative: bool = False):
    if len(factors) < 2:
        raise ValueError("at least two factors required")
    if left_associative:
        expression = factors[0]
        for factor in factors[1:]:
            expression = Composition(expression, factor)
    else:
        expression = factors[-1]
        for factor in reversed(factors[:-1]):
            expression = Composition(factor, expression)
    return expression


@pytest.mark.parametrize("n", (28, 30))
@pytest.mark.parametrize("left_associative", (False, True))
def test_r10es_nu_square_inside_mixed_composition(n, left_associative):
    value = _compose(
        _element(4, n), _element(4, n + 3), _element(56, n + 6),
        left_associative=left_associative,
    )
    expected = rf"\nu_{{{n}}}^{{2}}\bar{{\kappa}}_{{{n + 6}}}"
    assert typed_stable_composition_power_latex(value) is None
    assert render_toda_expression_latex(value) == expected
    assert render_toda_public_group_generator_latex(value) == expected


def test_r10es_fourfold_run_then_other_factor():
    value = _compose(
        _element(4, 18), _element(4, 21), _element(4, 24),
        _element(4, 27), _element(56, 30),
    )
    assert render_toda_expression_latex(value) == (
        r"\nu_{18}^{4}\bar{\kappa}_{30}"
    )


def test_r10es_mixed_singletons_unchanged():
    value = _compose(_element(9, 18), _element(12, 25))
    assert render_toda_expression_latex(value) == r"\sigma_{18}\mu_{25}"


def test_r10es_spoofed_typed_factor_does_not_compress():
    bad = replace(_element(4, 33), name="unregistered-name")
    value = _compose(_element(4, 30), bad, _element(56, 36))
    assert typed_stable_composition_power_latex(value) is None
    assert r"\nu_{30}^{2}" not in render_toda_expression_latex(value)


def test_r10es_noncomposable_mixed_expression_not_compressed():
    bad = replace(_element(56, 36), target=37)
    value = _compose(_element(4, 30), _element(4, 33), bad)
    assert r"\nu_{30}^{2}" not in render_toda_expression_latex(value)


def test_r10es_one_family_powers_unchanged():
    value = _compose(_element(4, 30), _element(4, 33))
    assert typed_stable_composition_power_latex(value) == r"\nu_{30}^{2}"
    assert render_toda_expression_latex(value) == r"\nu_{30}^{2}"


def test_r10es_full_function_patch_and_sha_guard():
    from phase169_r10es_r1_typed_partial_power_display.patch import (
        FUNCTION, replacement_content, full_function_span,
    )
    source = FUNCTION.read_text(encoding="utf-8")
    compile(source, str(FUNCTION), "exec")
    assert source.startswith("def render_toda_expression_latex(")
    with pytest.raises(RuntimeError, match="SHA1 differs"):
        replacement_content(b"wrong source")
