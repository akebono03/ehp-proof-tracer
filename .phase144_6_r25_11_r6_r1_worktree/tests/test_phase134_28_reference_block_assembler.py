import pytest

from toda_group_proof_narrative_renderer import (
  _phase134_28_reference_section_lines,
)


def test_phase134_28_reference_section_lines_numbers_blocks(
):
  rendered = (
    _phase134_28_reference_section_lines(
      (
        (
          "First reference",
          (),
        ),
        (
          "Second reference",
          (),
        ),
      )
    )
  )

  assert rendered == [
    "## 使用する結果",
    "",
    "**[R1] First reference.**",
    "",
    "**[R2] Second reference.**",
    "",
  ]


def test_phase134_28_reference_section_lines_preserves_statement_lines(
):
  rendered = (
    _phase134_28_reference_section_lines(
      (
        (
          "Reference",
          (
            "次の写像は同型である.",
            "",
            r"\[",
            "FORMULA",
            r"\]",
          ),
        ),
      )
    )
  )

  assert rendered == [
    "## 使用する結果",
    "",
    "**[R1] Reference.**",
    "",
    "次の写像は同型である.",
    "",
    r"\[",
    "FORMULA",
    r"\]",
    "",
  ]


def test_phase134_28_reference_section_lines_empty_is_empty(
):
  assert (
    _phase134_28_reference_section_lines(
      ()
    )
    == []
  )


def test_phase134_28_reference_section_lines_rejects_non_tuple(
):
  with pytest.raises(
    TypeError,
    match="reference_blocks must be a tuple",
  ):
    _phase134_28_reference_section_lines(
      []
    )
