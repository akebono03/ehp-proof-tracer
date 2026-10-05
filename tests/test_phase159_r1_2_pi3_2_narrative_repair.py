from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaPi32Eta2DefinitionStatement,
)


def _phase159_r1_2_pi3_2_presentation():
  report = build_standard_toda_report(
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def test_phase159_r1_2_pi3_2_definition_uses_semantic_prose():
  presentation = (
    _phase159_r1_2_pi3_2_presentation()
  )
  definition_step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaPi32Eta2DefinitionStatement,
    )
  )

  rendered = _render_generic_narrative_step(
    definition_step
  )

  assert "Toda pi_3^2 define eta_2 as unique Hopf preimage" not in rendered
  assert r"H(\eta_{2}) = \iota_{3}" in rendered
  assert r"\eta_{2} \in \pi_{3}^{2}" in rendered
  assert "を定める." in rendered


def test_phase159_r1_2_pi3_2_public_narrative_restores_injective_before_isomorphism():
  presentation = (
    _phase159_r1_2_pi3_2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  injective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$"
    " は単射である."
  )
  surjective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$"
    " は全射である."
  )
  isomorphism = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$"
    " は同型写像である."
  )

  assert injective in rendered
  assert surjective in rendered
  assert isomorphism in rendered
  assert rendered.index(injective) < rendered.index(isomorphism)
  assert rendered.index(surjective) < rendered.index(isomorphism)
  assert "Toda pi_3^2 define eta_2 as unique Hopf preimage" not in rendered
  assert r"H(\eta_{2}) = \iota_{3}" in rendered
  assert r"\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}" in rendered
  assert rendered.rstrip().endswith("□")
