from phase156_r5_final_cross_group_reference_minimal_display_audit.audit_phase156_r5_final import (
  _body_markers,
  _public_headers,
)


def test_phase156_r5_final_header_without_marker_is_allowed():
  rendered = "\n".join(
    (
      "**[R1] Proposition 5.6.**",
      "$A = B$",
      "",
      "# Group proof narrative",
      "",
      "本文では graph-backed usage により利用する.",
    )
  )

  headers = _public_headers(
    rendered
  )
  markers = _body_markers(
    rendered
  )

  assert tuple(
    number
    for _line_index, number, _title in headers
  ) == (
    1,
  )
  assert markers == ()


def test_phase156_r5_final_header_line_is_not_body_marker_usage():
  rendered = "\n".join(
    (
      "**[R1] Proposition 5.6.**",
      "$A = B$",
    )
  )

  assert _body_markers(
    rendered
  ) == ()


def test_phase156_r5_final_real_body_marker_is_detected():
  rendered = "\n".join(
    (
      "**[R1] Proposition 5.6.**",
      "$A = B$",
      "",
      "## 証明",
      "",
      "[R1]を用いる.",
    )
  )

  assert _body_markers(
    rendered
  ) == (
    1,
  )
