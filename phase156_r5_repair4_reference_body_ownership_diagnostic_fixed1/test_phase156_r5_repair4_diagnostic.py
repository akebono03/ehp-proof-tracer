from phase156_r5_repair4_reference_body_ownership_diagnostic_fixed1.diagnose_phase156_r5_repair4 import (
  TARGETS,
  _body_contexts,
  _group_label,
  _proof_body_start_index,
)


def test_phase156_r5_repair4_targets_exact_four_groups():
  assert TARGETS == (
    (
      3,
      3,
    ),
    (
      4,
      6,
    ),
    (
      5,
      7,
    ),
    (
      9,
      7,
    ),
  )


def test_phase156_r5_repair4_group_label():
  assert _group_label(
    3,
    3,
  ) == "pi_6^3"
  assert _group_label(
    9,
    7,
  ) == "pi_16^9"


def test_phase156_r5_repair4_body_start_prefers_proof_heading():
  rendered = "\n".join(
    (
      "**[R1] Proposition 5.6.**",
      "$A = B$",
      "",
      "# Group proof narrative",
      "",
      "## 使用する結果",
      "",
      "**[R1] Proposition 5.6.**",
      "",
      "## 証明",
      "",
      "$A = B$",
    )
  )

  lines = rendered.splitlines()

  assert _proof_body_start_index(
    rendered
  ) == (
    lines.index(
      "## 証明"
    )
    + 1
  )


def test_phase156_r5_repair4_body_start_uses_group_heading_for_raw_generic_route():
  rendered = "\n".join(
    (
      "**[R1] Proposition 5.6.**",
      "$A = B$",
      "",
      "# Group proof narrative",
      "",
      "$A = B$",
    )
  )

  lines = rendered.splitlines()

  assert _proof_body_start_index(
    rendered
  ) == (
    lines.index(
      "# Group proof narrative"
    )
    + 1
  )


def test_phase156_r5_repair4_reference_prefix_is_not_counted_as_body_occurrence():
  rendered = "\n".join(
    (
      "**[R1] Proposition 5.6.**",
      "$A = B$",
      "",
      "# Group proof narrative",
      "",
      "まず, 別の事実を用いる.",
    )
  )

  assert _body_contexts(
    rendered,
    "$A = B$",
  ) == ()
