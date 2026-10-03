from phase156_r5_repair4_reference_body_ownership_diagnostic_fixed2.diagnose_phase156_r5_repair4 import (
  TARGETS,
  _body_contexts,
  _group_label,
  _proof_body_text,
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


def test_phase156_r5_repair4_body_text_prefers_proof_heading():
  rendered = "\n".join(
    (
      "**[R1] Proposition 5.6.**",
      "$A = B$",
      "",
      "## 証明",
      "",
      "$C = D$",
    )
  )

  body = _proof_body_text(
    rendered,
    "**[R1] Proposition 5.6.**\n$A = B$",
  )

  assert body == "$C = D$"


def test_phase156_r5_repair4_body_text_removes_raw_generic_reference_prefix():
  reference_section = "\n".join(
    (
      "**[R1] Proposition 5.6.**",
      "$A = B$",
    )
  )
  rendered = (
    reference_section
    + "\n\n"
    + "使用する結果を先にまとめる.\n\n"
    + "まず, $C = D$."
  )

  body = _proof_body_text(
    rendered,
    reference_section,
  )

  assert "$A = B$" not in body
  assert "使用する結果を先にまとめる." in body
  assert "まず, $C = D$." in body


def test_phase156_r5_repair4_reference_prefix_is_not_counted_as_body_occurrence():
  reference_section = "\n".join(
    (
      "**[R1] Proposition 5.6.**",
      "$A = B$",
    )
  )
  rendered = (
    reference_section
    + "\n\n"
    + "まず, 別の事実を用いる."
  )
  body = _proof_body_text(
    rendered,
    reference_section,
  )

  assert _body_contexts(
    body,
    "$A = B$",
  ) == ()
