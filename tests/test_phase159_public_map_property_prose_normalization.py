from toda_group_proof_narrative_renderer import (
  _phase159_r1_7c_r4_normalize_public_map_property_prose,
)


def test_phase159_public_map_property_prose_keeps_exactness_injective_once():
  rendered = (
    "## 証明\n\n"
    "以上より, 完全性より, "
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
    "\n\n"
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
    "\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )

  sentence = (
    "完全性より, "
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
  )

  assert normalized.count(
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
  ) == 1
  assert normalized.count(
    sentence
  ) == 1
  assert (
    "以上より, 完全性より,"
    not in normalized
  )


def test_phase159_public_map_property_prose_keeps_exactness_surjective_once():
  rendered = (
    "## 証明\n\n"
    "完全性より, "
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
    "\n\n"
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射である."
    "\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )

  sentence = (
    "完全性より, "
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  )

  assert normalized.count(
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  ) == 1
  assert normalized.count(
    sentence
  ) == 1


def test_phase159_public_map_property_prose_keeps_standalone_without_exactness_reason():
  rendered = (
    "## 証明\n\n"
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である."
    "\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )

  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射."
    in normalized
  )
  assert (
    "は全射である."
    not in normalized
  )
