from low_dimensional_facts import (
  e_pi_1_1_to_pi_2_2_isomorphism_fact,
  pi_2_1_zero_fact,
  pi_3_3_free_cyclic_fact,
)
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


def _phase159_r1_6a_pi3_2_presentation():
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


def test_phase159_r1_6a_pi3_2_foundational_premises_keep_identity():
  presentation = (
    _phase159_r1_6a_pi3_2_presentation()
  )

  expected = {
    pi_2_1_zero_fact():
      "sphere.circle.higher_zero",
    pi_3_3_free_cyclic_fact():
      "sphere.identity_group",
    e_pi_1_1_to_pi_2_2_isomorphism_fact():
      (
        "sphere.low_dimensional."
        "suspension_isomorphism"
      ),
  }

  found = {}
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

    if proof_step.conclusion in expected:
      identity = (
        proof_step.foundational_reference
      )

      assert identity is not None

      found[
        proof_step.conclusion
      ] = identity.key

    for premise in proof_step.premises:
      if hasattr(
        premise,
        "conclusion",
      ):
        visit(
          premise
        )

  visit(
    presentation.root_step
  )

  assert found == expected

def test_phase159_r1_6a_pi3_2_root_is_not_foundational_reference():
  presentation = (
    _phase159_r1_6a_pi3_2_presentation()
  )

  assert (
    presentation.root_step
    .foundational_reference
    is None
  )


def test_phase159_r1_6a_pi3_2_public_reference_section_shows_foundational_facts():
  presentation = (
    _phase159_r1_6a_pi3_2_presentation()
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
    "Circle higher homotopy vanishing"
    in reference_section
  )
  assert (
    "Sphere identity group"
    in reference_section
  )
  assert (
    "Low-dimensional suspension isomorphism"
    in reference_section
  )
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


def test_phase159_r1_6a_pi3_2_target_is_not_reintroduced_as_reference():
  presentation = (
    _phase159_r1_6a_pi3_2_presentation()
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
    r"\pi_{3}^{2} = "
    r"\mathbb{Z}\{\eta_{2}\}"
    not in reference_section
  )
  assert (
    "Proposition 5.1"
    not in reference_section
  )
