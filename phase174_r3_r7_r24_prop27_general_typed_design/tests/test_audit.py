"""Focused source and typed-contract tests for R24."""
import pytest

from phase174_r3_r7_r24_prop27_general_typed_design.audit import (
    GENERAL_EQUATION,
    SPECIAL_EQUATION,
    source_contract,
    specialize_prop27_design,
)


def test_n6_signature_and_sign_are_preserved():
    sig = specialize_prop27_design(6)
    assert sig.source_group == (13, 13)
    assert sig.delta_target_group == (11, 6)
    assert sig.hopf_target_group == (11, 11)
    assert sig.source_iota_dimension == 13
    assert sig.target_iota_dimension == 11
    assert sig.absolute_coefficient == 2
    assert sig.sign_is_undetermined is True


@pytest.mark.parametrize("n", [2, 4, 6, 8, 10])
def test_general_even_dimensions(n):
    sig = specialize_prop27_design(n)
    assert sig.delta_target_group == (2 * n - 1, n)
    assert sig.hopf_target_group == (2 * n - 1, 2 * n - 1)


@pytest.mark.parametrize("n", [True, False, 0, 1, 3, 5, -2, 2.0, "6", None])
def test_invalid_parameters_are_rejected(n):
    with pytest.raises(ValueError):
        specialize_prop27_design(n)


def _fixtures():
    chapter_ii = (
        r"H[\,\iota_n,\ \iota_n\,]" + "\n" +
        r"\begin{proposition}\label{prop:2.7}" + "\n" +
        "$n$ が偶数のとき" + "\n" + GENERAL_EQUATION + "\n" +
        r"\end{proposition}"
    )
    chapter_v = SPECIAL_EQUATION + "\n" + r"\iota_{2m-1}"
    legacy = "WhiteheadProduct TodaProp27HopfInvariantUpToSignStatement"
    return chapter_ii, chapter_v, legacy


def test_source_contract_accepts_unmodified_formula():
    result = source_contract(*_fixtures())
    assert result["even_n_condition"] is True
    assert result["chapter_v_sidebar_mismatch"] is True


def test_source_contract_rejects_wrong_index():
    chapter_ii, chapter_v, legacy = _fixtures()
    with pytest.raises(ValueError):
        source_contract(chapter_ii.replace(GENERAL_EQUATION, r"\iota_{2m-1}"), chapter_v, legacy)


def test_source_contract_rejects_missing_evenness():
    chapter_ii, chapter_v, legacy = _fixtures()
    with pytest.raises(ValueError):
        source_contract(chapter_ii.replace("$n$ が偶数のとき", "$n$ が奇数のとき"), chapter_v, legacy)


def test_source_contract_rejects_legacy_whitehead_removal():
    chapter_ii, chapter_v, legacy = _fixtures()
    with pytest.raises(ValueError):
        source_contract(chapter_ii, chapter_v, legacy.replace("WhiteheadProduct", "UnknownProduct"))
