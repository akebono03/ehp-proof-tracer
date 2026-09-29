from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_group_structure_semantics import (
  extract_toda_group_structure_narrative_redundant_direct_premise_step_ids,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _render(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def test_phase143_59b_pi15_8_finds_redundant_direct_premise():
  (
    _,
    _,
    _,
    arguments,
  ) = _method_evidence_data(
    8,
    7,
  )

  conclusion_steps = tuple(
    step
    for argument in arguments
    for step in (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      ),
    )
    if step is not None
  )
  conclusion_step = next(
    step
    for step in conclusion_steps
    if (
      hasattr(
        step.conclusion,
        "lhs",
      )
      and step.conclusion.lhs.group_dimension == 15
      and step.conclusion.lhs.sphere_dimension == 8
    )
  )

  redundant_ids = (
    extract_toda_group_structure_narrative_redundant_direct_premise_step_ids(
      conclusion_step
    )
  )

  assert len(
    redundant_ids
  ) == 1
  assert id(
    conclusion_step.premises[
      0
    ]
  ) in redundant_ids


def test_phase143_59b_pi15_8_suppresses_transported_duplicate():
  rendered = _render(
    8,
    7,
  )

  assert (
    r"$\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
    not in rendered
  )


def test_phase143_59b_pi15_8_keeps_final_group_conclusion():
  rendered = _render(
    8,
    7,
  )

  assert (
    "以上より、\n\n"
    r"$\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}$"
    in rendered
  )


def test_phase143_59b_pi15_8_keeps_supporting_short_exact_sequence():
  rendered = _render(
    8,
    7,
  )

  assert (
    r"$0\longrightarrow \pi_{13}^{6}"
    r"\xrightarrow{E} \pi_{14}^{7}"
    r"\xrightarrow{H} \pi_{14}^{13}"
    r"\longrightarrow 0$"
    in rendered
  )


def test_phase143_59b_pi6_3_narrative_remains_available():
  rendered = _render(
    3,
    3,
  )

  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in rendered
  )
  assert "これらより、" in rendered


def test_phase143_59b_pi8_5_narrative_remains_available():
  rendered = _render(
    5,
    3,
  )

  assert (
    r"$\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$"
    in rendered
  )


def test_phase143_59b_pi16_9_narrative_remains_available():
  rendered = _render(
    9,
    7,
  )

  assert (
    r"$\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}$"
    in rendered
  )
