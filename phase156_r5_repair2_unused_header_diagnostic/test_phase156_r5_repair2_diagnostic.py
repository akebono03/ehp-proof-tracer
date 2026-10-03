from phase156_r5_repair2_unused_header_diagnostic.diagnose_phase156_r5_repair2 import (
  _body_markers,
  _headers,
  _normalize,
)


def test_phase156_r5_repair2_header_marker_is_not_counted_as_body_usage():
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

  assert _headers(
    rendered
  )[0][1] == 1
  assert _body_markers(
    rendered
  ) == ()


def test_phase156_r5_repair2_real_body_marker_is_counted():
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


def test_phase156_r5_repair2_normalization_ignores_display_wrapper():
  assert _normalize(
    r"\[$A = B$\]"
  ) == _normalize(
    "$A = B$"
  )
