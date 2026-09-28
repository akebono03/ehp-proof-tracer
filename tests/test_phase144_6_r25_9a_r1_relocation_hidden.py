from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)


PI5_3_TEXT = (
  r"\pi_{5}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\eta_{4}\}"
)


def test_phase144_6_r25_9a_r1_hidden_support_is_not_reintroduced():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  assert PI5_3_TEXT not in rendered
  assert r"$\nu'$ を定める." in rendered
  assert r"2\nu' = \eta_{3}^{3}" in rendered
  assert "(1) と (2) より、" in rendered
  assert r"H\left(\nu'\right) = \eta_{5}" in rendered
  assert "(4) と (5) より、" in rendered
  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in rendered
  )
