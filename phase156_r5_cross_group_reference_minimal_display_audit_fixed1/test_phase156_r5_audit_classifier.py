from phase156_r5_cross_group_reference_minimal_display_audit_fixed1.audit_phase156_r5 import (
  _document_body_reference_markers,
  _document_reference_headers,
  classify_public_reference_structure,
)


def test_phase156_r5_structure_accepts_contiguous_used_headers():
  missing, unused, contiguous = (
    classify_public_reference_structure(
      header_numbers=(
        1,
        2,
      ),
      body_markers=(
        2,
        1,
        2,
      ),
    )
  )

  assert missing == ()
  assert unused == ()
  assert contiguous is True


def test_phase156_r5_structure_detects_missing_header():
  missing, unused, contiguous = (
    classify_public_reference_structure(
      header_numbers=(
        1,
      ),
      body_markers=(
        1,
        2,
      ),
    )
  )

  assert missing == (
    2,
  )
  assert unused == ()
  assert contiguous is True


def test_phase156_r5_structure_detects_unused_header():
  missing, unused, contiguous = (
    classify_public_reference_structure(
      header_numbers=(
        1,
        2,
      ),
      body_markers=(
        1,
      ),
    )
  )

  assert missing == ()
  assert unused == (
    2,
  )
  assert contiguous is True


def test_phase156_r5_structure_detects_non_contiguous_headers():
  missing, unused, contiguous = (
    classify_public_reference_structure(
      header_numbers=(
        1,
        3,
      ),
      body_markers=(
        1,
        3,
      ),
    )
  )

  assert missing == ()
  assert unused == ()
  assert contiguous is False


def test_phase156_r5_document_parser_accepts_generic_reference_prefix_without_section_heading():
  rendered = "\n".join(
    (
      "使用する結果を先にまとめる.",
      "",
      "**[R1] Proposition 5.6.**",
      "$A = B$",
      "",
      "**[R2] Lemma 5.4.**",
      "$C = D$",
      "",
      "# Group proof narrative",
      "",
      "## 証明",
      "",
      "[R1]を用いる.",
      "[R2]より結論を得る.",
    )
  )

  headers = _document_reference_headers(
    rendered
  )
  markers = _document_body_reference_markers(
    rendered
  )

  assert tuple(
    number
    for _line_index, number, _title in headers
  ) == (
    1,
    2,
  )
  assert markers == (
    1,
    2,
  )


def test_phase156_r5_document_parser_does_not_count_header_marker_as_body_usage():
  rendered = "\n".join(
    (
      "**[R1] Proposition 5.6.**",
      "$A = B$",
      "",
      "# Group proof narrative",
      "",
      "## 証明",
      "",
      "結論を得る.",
    )
  )

  assert _document_body_reference_markers(
    rendered
  ) == ()
