from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_group_structure_semantics import (
  extract_toda_group_structure_narrative_redundant_direct_premise_step_ids,
)
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


def _phase159_pi4_3_data():
  return _method_evidence_data(
    3,
    1,
  )


def _phase159_pi4_3_conclusion_step(
  arguments,
):
  matches = tuple(
    conclusion_step
    for argument in arguments
    for conclusion_step in (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      ),
    )
    if (
      conclusion_step is not None
      and conclusion_step.inference_rule is not None
      and conclusion_step.inference_rule.name
      == "Toda pi_4^3 eta_3 generator notation"
    )
  )

  assert len(
    matches
  ) == 1

  return matches[
    0
  ]


def test_phase159_pi4_3_generator_bridge_marks_quotient_premise_redundant():
  (
    _,
    _,
    _,
    arguments,
  ) = _phase159_pi4_3_data()
  conclusion_step = (
    _phase159_pi4_3_conclusion_step(
      arguments
    )
  )
  redundant_ids = (
    extract_toda_group_structure_narrative_redundant_direct_premise_step_ids(
      conclusion_step
    )
  )
  quotient_step = next(
    premise_step
    for premise_step in conclusion_step.premises
    if (
      premise_step.inference_rule is not None
      and premise_step.inference_rule.name
      == "Toda pi_4^3 finite cyclic quotient calculation"
    )
  )
  notation_bridge_step = next(
    premise_step
    for premise_step in conclusion_step.premises
    if (
      premise_step.inference_rule is not None
      and premise_step.inference_rule.name
      == "Toda eta_3 notation suspension bridge"
    )
  )

  assert id(
    quotient_step
  ) in redundant_ids
  assert id(
    notation_bridge_step
  ) not in redundant_ids


def test_phase159_pi4_3_public_proof_emits_group_conclusion_once():
  (
    presentation,
    _,
    _,
    _,
  ) = _phase159_pi4_3_data()
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
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
  assert rendered.rstrip().endswith(
    "□"
  )
