from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


PI4_3_CONCLUSION = (
  r"\pi_{4}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\}"
)


def _render_phase159_pi4_3_public_narrative() -> str:
  (
    presentation,
    _,
    _,
    _,
  ) = _method_evidence_data(
    3,
    1,
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_pi4_3_redundant_group_structure_does_not_override_provenance_suppression():
  rendered = (
    _render_phase159_pi4_3_public_narrative()
  )
  proof_marker = "\n## 証明\n\n"

  assert proof_marker in rendered

  proof_body = rendered.split(
    proof_marker,
    1,
  )[1]

  assert proof_body.count(
    PI4_3_CONCLUSION
  ) == 1
  assert (
    "以上より, "
    + "$"
    + PI4_3_CONCLUSION
    + "$."
  ) in proof_body


def test_phase159_pi4_3_nonredundant_derivation_evidence_remains_visible():
  rendered = (
    _render_phase159_pi4_3_public_narrative()
  )
  proof_marker = "\n## 証明\n\n"

  assert proof_marker in rendered

  proof_body = rendered.split(
    proof_marker,
    1,
  )[1]

  assert (
    r"\pi_{3}^{2} = "
    r"\mathbb{Z}\{\eta_{2}\}"
  ) in proof_body
  assert r"\ker E" in proof_body
  assert (
    r"E: \pi_{3}^{2} \to \pi_{4}^{3}"
    in proof_body
  )
