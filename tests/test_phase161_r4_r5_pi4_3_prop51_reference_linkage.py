from toda_calculation_facade import (
  build_standard_toda_report,
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
from toda_prop56_zero_bootstrap import (
  _build_pi4_3_prop51_specialization_link_step,
  _build_prop51_step,
)
from toda_upstream_bootstrap import (
  _build_phase50_result,
)


def _phase161_r4_r5_pi4_2_data():
  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  return (
    replay,
    rendered,
  )


def test_phase161_r4_r5_pi4_3_prop51_link_is_structural():
  phase50 = _build_phase50_result()
  pi4_3_step = phase50[
    "final_group_step"
  ]
  prop51_step = _build_prop51_step()

  linked = (
    _build_pi4_3_prop51_specialization_link_step(
      pi4_3_step,
      prop51_step,
    )
  )

  assert linked.conclusion == pi4_3_step.conclusion
  assert linked.inference_rule is not None
  assert (
    linked.inference_rule.name
    == (
      "pi_4^3 Proposition 5.1 "
      "specialization linkage"
    )
  )
  assert (
    linked.inference_rule.literature_reference
    is None
  )

  assert len(
    linked.premises
  ) == 2

  general_step = linked.premises[
    1
  ]

  assert (
    general_step.conclusion
    == (
      prop51_step
      .conclusion
      .higher_eta_group_relation
    )
  )
  assert general_step.inference_rule is not None
  assert (
    general_step
    .inference_rule
    .literature_reference
    is not None
  )
  assert (
    general_step
    .inference_rule
    .literature_reference
    .locator
    == "Proposition 5.1"
  )


def test_phase161_r4_r5_pi4_2_replay_contains_general_prop51_component():
  replay, _ = (
    _phase161_r4_r5_pi4_2_data()
  )

  proof_steps = tuple(
    replay_step.proof_step
    for replay_step in replay.steps
  )

  link_step = next(
    step
    for step in proof_steps
    if (
      step.inference_rule
      is not None
      and step.inference_rule.name
      == (
        "pi_4^3 Proposition 5.1 "
        "specialization linkage"
      )
    )
  )

  general_step = next(
    step
    for step in link_step.premises
    if (
      step.inference_rule
      is not None
      and step.inference_rule.name
      == (
        "Toda Proposition 5.1 "
        "higher eta group relation"
      )
    )
  )

  assert (
    general_step
    .inference_rule
    .literature_reference
    .locator
    == "Proposition 5.1"
  )


def test_phase161_r4_r5_pi4_2_public_reference_is_general_prop51():
  _, rendered = (
    _phase161_r4_r5_pi4_2_data()
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "Proposition 5.1" in reference
  assert "(5.2)" in reference

  assert (
    r"\pi_{n + 1}^{n}"
    in reference
    or r"\pi_{n+1}^{n}"
    in reference
  )
  assert (
    r"\mathbb{Z}/2\{\eta_{n}\}"
    in reference
  )

  assert (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}"
    not in reference
  )

  assert (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}"
    in body
  )

  prop51_number = next(
    number
    for number in range(
      1,
      4,
    )
    if (
      f"**[R{number}] Proposition 5.1.**"
      in reference
    )
  )

  pi4_3_paragraph = next(
    paragraph
    for paragraph in body.split(
      "\n\n"
    )
    if (
      r"\pi_{4}^{3} = "
      r"\mathbb{Z}/2\{\eta_{3}\}"
      in paragraph
    )
  )

  assert (
    f"[R{prop51_number}]"
    in pi4_3_paragraph
  )

  assert (
    r"\pi_{4}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
    in body
  )
  assert "□" in body
