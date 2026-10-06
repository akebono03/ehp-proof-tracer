from low_dimensional_facts import (
  e_pi_1_1_to_pi_2_2_isomorphism_fact,
  pi_2_1_zero_fact,
  pi_3_3_free_cyclic_fact,
)
from proof import ProofStep
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
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)


def _phase159_r1_6b_pi3_2_presentation():
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


def _phase159_r1_6b_recursive_steps(
  root_step,
):
  steps = []
  seen_step_ids = set()

  def visit(
    proof_step,
  ):
    step_id = id(
      proof_step
    )

    if step_id in seen_step_ids:
      return

    seen_step_ids.add(
      step_id
    )
    steps.append(
      proof_step
    )

    for premise in proof_step.premises:
      if isinstance(
        premise,
        ProofStep,
      ):
        visit(
          premise
        )

  visit(
    root_step
  )

  return tuple(
    steps
  )


def test_phase159_r1_6b_pi3_2_low_dimensional_facts_are_toda_51_fixed_statements():
  presentation = (
    _phase159_r1_6b_pi3_2_presentation()
  )
  steps = (
    _phase159_r1_6b_recursive_steps(
      presentation.root_step
    )
  )

  expected = {
    pi_2_1_zero_fact():
      "circle_higher_homotopy_zero",
    pi_3_3_free_cyclic_fact():
      "diagonal_identity_group",
    e_pi_1_1_to_pi_2_2_isomorphism_fact():
      "diagonal_suspension_isomorphism",
  }

  found = {}

  for proof_step in steps:
    if proof_step.conclusion not in expected:
      continue

    boundary = (
      classify_toda_literature_statement_step(
        proof_step
      )
    )

    assert boundary is not None
    assert (
      boundary.classification
      is TodaLiteratureStatementClassification.FIXED_STATEMENT
    )
    assert (
      boundary.reference_locator
      == "(5.1)"
    )

    found[
      proof_step.conclusion
    ] = boundary.component_key

  assert found == expected


def test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry():
  presentation = (
    _phase159_r1_6b_pi3_2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  reference_section = (
    rendered.split(
      "## 使用する結果\n\n",
      1,
    )[1].split(
      "\n---\n",
      1,
    )[0]
  )

  assert (
    reference_section.count(
      "**[R1] (5.1).**"
    )
    == 1
  )
  assert "[F1]" not in reference_section
  assert "[F2]" not in reference_section
  assert "[F3]" not in reference_section

  assert (
    r"$\pi_{2}^{1} = 0$."
    in reference_section
  )
  assert (
    r"$\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
    in reference_section
  )
  assert (
    r"$E: \pi_{1}^{1} \to "
    r"\pi_{2}^{2}$ は同型."
    in reference_section
  )

  assert (
    r"\pi_{3}^{2} = "
    r"\mathbb{Z}\{\eta_{2}\}"
    not in reference_section
  )
  assert (
    "Proposition 5.1"
    not in reference_section
  )


def test_phase159_r1_6b_pi3_2_number_tags_include_map_property_statement():
  presentation = (
    _phase159_r1_6b_pi3_2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3} "
    r"\text{ は単射}. \tag{1}$"
    in rendered
  )
  assert (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3} "
    r"\text{ は全射}. \tag{2}$"
    in rendered
  )

  assert (
    r"\tag{1}$ は単射."
    not in rendered
  )
  assert (
    r"\tag{2}$ は全射."
    not in rendered
  )

  assert (
    "(1), (2) より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
    in rendered
  )


def test_phase159_r1_6b_pi3_2_has_no_foundational_reference_labels():
  presentation = (
    _phase159_r1_6b_pi3_2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert "[F1]" not in rendered
  assert "[F2]" not in rendered
  assert "[F3]" not in rendered
