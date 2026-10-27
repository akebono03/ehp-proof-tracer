"""R10EB: one display projector for verified typed stable-family powers."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from phase168_r3_27_typed_statement_projection import element_tex
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase169_r10eb_typed_composition_power.display import (
    typed_stable_composition_power_latex,
)
from phase169_r10eb_typed_composition_power.patch import (
    PUBLIC_ANCHOR, NARRATIVE_ANCHOR, transform,
)
from toda_human_readable_renderer import (
    render_toda_expression_latex,
    render_toda_public_group_generator_latex,
)


def _element(family_id: int, n: int) -> HomotopyElement:
    family, = (x for x in read_registered_stable_families()
               if x.family_id == family_id)
    return HomotopyElement(
        name=family.name_at(n), dimension=n,
        source=n + family.stem, target=n,
        generator=GeneratorSymbol(family=family.symbol_family, index=n),
    )


def _compose(*factors: HomotopyElement) -> Composition:
    assert len(factors) >= 2
    result = factors[-1]
    for element in reversed(factors[:-1]):
        result = Composition(element, result)
    assert isinstance(result, Composition)
    return result


@pytest.mark.parametrize("family_id,start,r,expected", [
    (4, 30, 3, r"\nu_{30}^{3}"),
    (9, 11, 4, r"\sigma_{11}^{4}"),
    (2, 12, 3, r"\eta_{12}^{3}"),
    (10, 13, 2, r"\varepsilon_{13}^{2}"),
    (11, 12, 2, r"\bar{\nu}_{12}^{2}"),
    (12, 13, 3, r"\mu_{13}^{3}"),
])
def test_r10eb_registered_family_stem_controls_consecutive_power(
    family_id: int, start: int, r: int, expected: str,
):
    family, = (x for x in read_registered_stable_families()
               if x.family_id == family_id)
    value = _compose(*(_element(family_id, start + i * family.stem)
                       for i in range(r)))
    assert typed_stable_composition_power_latex(value) == expected
    assert element_tex(value) == expected
    assert render_toda_expression_latex(value) == expected
    assert render_toda_public_group_generator_latex(value) == expected


def test_r10eb_rejects_nonconsecutive_or_mixed_family_and_bad_type():
    wrong_jump = _compose(_element(4, 11), _element(4, 17))
    wrong_family = _compose(_element(4, 11), _element(2, 14))
    wrong_dimension = _compose(
        _element(4, 11), replace(_element(4, 14), source=18),
    )
    wrong_name = _compose(
        _element(4, 11), replace(_element(4, 14), name="anonymous"),
    )
    decorated = _compose(
        _element(4, 11),
        replace(_element(4, 14), generator=GeneratorSymbol(
            family="ν", index=14, decoration="prime",
        )),
    )
    for value in (wrong_jump, wrong_family, wrong_dimension,
                  wrong_name, decorated):
        assert typed_stable_composition_power_latex(value) is None


def test_r10eb_rejects_same_dimension_identity_and_noncomposition():
    identity = _compose(_element(1, 5), _element(1, 5))
    assert typed_stable_composition_power_latex(identity) is None
    assert typed_stable_composition_power_latex(_element(4, 11)) is None


def test_r10eb_nested_left_associative_composition():
    value = Composition(
        Composition(_element(4, 11), _element(4, 14)), _element(4, 17),
    )
    assert typed_stable_composition_power_latex(value) == r"\nu_{11}^{3}"


def test_r10eb_existing_eta_square_and_nu_square_unchanged():
    eta = _compose(_element(2, 12), _element(2, 13))
    nu = _compose(_element(4, 12), _element(4, 15))
    assert element_tex(eta) == r"\eta_{12}^{2}"
    assert render_toda_public_group_generator_latex(nu) == r"\nu_{12}^{2}"


def test_r10eb_synthetic_patch_guards_no_double_application():
    narrative = (
        "def element_tex(value):\n"
        + NARRATIVE_ANCHOR
        + ":\n        return None\n    return None\n"
    )
    public = (
        "def render_toda_expression_latex(expression):\n"
        + PUBLIC_ANCHOR + "\n"
        + "    return 'fallback'\n"
    )
    for path, fixture in (
        ("phase168_r3_27_typed_statement_projection.py", narrative),
        ("toda_human_readable_renderer.py", public),
    ):
        updated, full_function = transform(path, fixture)
        assert "typed_stable_composition_power_latex" in full_function
        with pytest.raises(RuntimeError, match="anchor changed"):
            transform(path, updated)
