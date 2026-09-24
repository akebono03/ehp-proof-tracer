import pytest

from toda_group_proof_narrative_renderer import (
  _phase134_30_completed_boundary_lines,
  _phase134_30_display_math_lines,
  _phase134_30_final_conclusion_lines,
)


def test_phase134_30_display_math_lines_without_tag(
):
  assert (
    _phase134_30_display_math_lines(
      "FORMULA"
    )
    == [
      "",
      r"\[",
      "FORMULA",
      r"\]",
      "",
    ]
  )


def test_phase134_30_display_math_lines_with_tag(
):
  assert (
    _phase134_30_display_math_lines(
      "FORMULA",
      3,
    )
    == [
      "",
      r"\[",
      r"FORMULA\tag{3}",
      r"\]",
      "",
    ]
  )


def test_phase134_30_completed_boundary_lines_preserves_optional_closing(
):
  assert (
    _phase134_30_completed_boundary_lines(
      "BOUNDARY",
      3,
    )
    == [
      "既に,",
      "",
      r"\[",
      r"BOUNDARY\tag{3}",
      r"\]",
      "",
    ]
  )

  assert (
    _phase134_30_completed_boundary_lines(
      "BOUNDARY",
      closing_text="である.",
    )
    == [
      "既に,",
      "",
      r"\[",
      "BOUNDARY",
      r"\]",
      "",
      "である.",
      "",
    ]
  )


def test_phase134_30_final_conclusion_lines(
):
  assert (
    _phase134_30_final_conclusion_lines(
      "TARGET",
      8,
    )
    == [
      "したがって,",
      "",
      r"\[",
      r"TARGET\tag{8}",
      r"\]",
      "",
      "を得る.",
      "",
    ]
  )


def test_phase134_30_display_math_lines_rejects_invalid_tag(
):
  with pytest.raises(
    TypeError,
    match="tag must be an int or None",
  ):
    _phase134_30_display_math_lines(
      "FORMULA",
      "3",
    )
