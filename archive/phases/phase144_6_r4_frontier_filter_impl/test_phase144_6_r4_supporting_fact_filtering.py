from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)


def _render_phase144_6_r4_pi6_3():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  return render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )


def test_phase144_6_r4_hides_internal_supporting_group_facts():
  rendered = _render_phase144_6_r4_pi6_3()

  assert r"\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}" not in rendered
  assert r"\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\}" not in rendered
  assert r"\pi_{i - 1}^{1} = 0" not in rendered
  assert r"\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}" not in rendered


def test_phase144_6_r4_preserves_definition_frontier():
  rendered = _render_phase144_6_r4_pi6_3()

  assert r"$\nu'$ を定める." in rendered
  assert r"\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}" in rendered
  assert r"2\eta_{3} = 0" in rendered
  assert r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}" in rendered


def test_phase144_6_r4_preserves_argument_frontier_and_transition_chains():
  rendered = _render_phase144_6_r4_pi6_3()

  assert r"\operatorname{ord}\left(\nu'\right) = 4" in rendered
  assert r"2\nu' = \eta_{3}^{3}" in rendered
  assert "(1) と (2) より、" in rendered
  assert r"H\left(\nu'\right) = \eta_{5}" in rendered
  assert "(4) と (5) より、" in rendered
  assert r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}" in rendered


def test_phase144_6_r4_preserves_structured_reference_section():
  rendered = _render_phase144_6_r4_pi6_3()

  assert "**[R1]" in rendered
  assert "**[R2]" in rendered
  assert "Proposition 5.1" in rendered
  assert "Proposition 4.4" in rendered
  assert "Proposition 2.2" not in rendered
