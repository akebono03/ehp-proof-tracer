import pytest

from toda_group_proof_narrative_renderer import (
  _phase134_26_narrative_section_header_lines,
  _phase134_26_narrative_start_lines,
)


def test_phase134_26_section_header_lines(
):
  assert (
    _phase134_26_narrative_section_header_lines(
      "使用する結果"
    )
    == [
      "## 使用する結果",
      "",
    ]
  )

  assert (
    _phase134_26_narrative_section_header_lines(
      "証明"
    )
    == [
      "## 証明",
      "",
    ]
  )


def test_phase134_26_start_lines_preserve_target_body(
):
  target_lines = [
    "Toda Proposition 5.6 のうち,",
    "",
    r"\[",
    "TARGET",
    r"\]",
    "",
    "を示す.",
  ]

  assert (
    _phase134_26_narrative_start_lines(
      target_lines
    )
    == [
      "# Group proof narrative",
      "",
      "## 証明対象",
      "",
      *target_lines,
      "",
    ]
  )


def test_phase134_26_section_header_rejects_empty_title(
):
  with pytest.raises(
    ValueError,
    match="section_title must not be empty",
  ):
    _phase134_26_narrative_section_header_lines(
      ""
    )
