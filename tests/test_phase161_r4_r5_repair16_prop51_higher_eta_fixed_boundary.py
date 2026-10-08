from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)


def _phase161_r4_r5_repair16_data():
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )

  return (
    raw,
    presentation,
  )


def test_phase161_r4_r5_repair16_higher_eta_step_is_fixed_prop51_component():
  _, presentation = (
    _phase161_r4_r5_repair16_data()
  )

  higher_eta_step = next(
    node.proof_step
    for node in presentation.nodes
    if (
      node.proof_step.inference_rule is not None
      and node.proof_step.inference_rule.name
      == "Toda Proposition 5.1 higher eta group relation"
    )
  )

  boundary = classify_toda_literature_statement_step(
    higher_eta_step
  )

  assert boundary is not None
  assert (
    boundary.classification
    is TodaLiteratureStatementClassification.FIXED_STATEMENT
  )
  assert (
    boundary.reference_locator
    == "Proposition 5.1"
  )
  assert (
    boundary.component_key
    == "higher_eta_group_relation"
  )


def test_phase161_r4_r5_repair16_public_reference_keeps_general_prop51():
  raw, _ = (
    _phase161_r4_r5_repair16_data()
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "**[R1] (5.2).**" in reference
  assert "**[R2] Proposition 5.1.**" in reference

  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    in reference
  )
  assert (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}"
    not in reference
  )

  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    not in body
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

  assert "[R2]" in pi4_3_paragraph


def test_phase161_r4_r5_repair16_keeps_pi4_2_specialization_contract():
  raw, _ = (
    _phase161_r4_r5_repair16_data()
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "Proposition 4.4" not in reference
  assert "$i=4$" in body
  assert (
    r"\eta_{2}\circ -: "
    r"\pi_{4}^{3} \to \pi_{4}^{2}"
    in body
  )
  assert (
    r"\eta_{3} \mapsto "
    r"\eta_{2}\eta_{3}"
    in body
  )
  assert (
    r"\pi_{4}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
    in body
  )
  assert "□" in body
