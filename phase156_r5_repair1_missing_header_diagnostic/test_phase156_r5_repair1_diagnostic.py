from phase156_r5_repair1_missing_header_diagnostic.diagnose_phase156_r5_repair1 import (
  _body_markers,
  _header_numbers,
  _sections,
)


def test_phase156_r5_repair1_extracts_reference_headers():
  lines = (
    "**[R1] Proposition 5.6.**",
    "$A = B$",
    "**[R2] Proposition 5.8.**",
    "$C = D$",
  )

  assert _header_numbers(
    lines
  ) == (
    1,
    2,
  )


def test_phase156_r5_repair1_extracts_body_markers():
  lines = (
    "[R1]を用いる.",
    "[R3] より結論を得る.",
    "[R1], [R2] より.",
  )

  assert _body_markers(
    lines
  ) == (
    1,
    3,
    1,
    2,
  )


def test_phase156_r5_repair1_splits_public_sections():
  rendered = "\n".join(
    (
      "# Group proof narrative",
      "",
      "## 使用する結果",
      "",
      "**[R1] Proposition 5.6.**",
      "",
      "## 証明",
      "",
      "[R1]を用いる.",
    )
  )

  reference_lines, body_lines = (
    _sections(
      rendered
    )
  )

  assert "**[R1] Proposition 5.6.**" in reference_lines
  assert "[R1]を用いる." in body_lines
