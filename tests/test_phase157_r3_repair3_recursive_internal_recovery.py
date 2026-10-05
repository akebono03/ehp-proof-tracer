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


def _presentation_pi6_3(
  depth: int,
):
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def _find_recursive_rule(
  root_step,
  rule_name: str,
):
  stack = [
    root_step,
  ]
  visited = set()

  while stack:
    step = stack.pop()
    step_id = id(
      step
    )

    if step_id in visited:
      continue

    visited.add(
      step_id
    )

    if (
      step.inference_rule is not None
      and step.inference_rule.name == rule_name
    ):
      return step

    stack.extend(
      reversed(
        step.premises
      )
    )

  return None


def test_phase157_r3_repair3_recursive_graph_contains_prop53_suspension_isomorphism():
  presentation = _presentation_pi6_3(
    3
  )

  step = _find_recursive_rule(
    presentation.root_step,
    "Toda Proposition 5.3 n=3 suspension isomorphism",
  )

  assert step is not None

  rendered = _render_generic_narrative_step(
    step
  )

  assert (
    r"E: \pi_{4}^{2} \to \pi_{5}^{3}"
    in rendered
  )


def test_phase157_r3_repair3_public_narrative_rehomes_recursive_suspension_step_to_body():
  presentation = _presentation_pi6_3(
    3
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  expected = (
    r"E: \pi_{4}^{2} \to \pi_{5}^{3}"
  )

  assert expected in rendered

  first_body_line = "$2\\eta_{3} = 0$"
  body_index = rendered.find(
    first_body_line
  )
  expected_index = rendered.find(
    expected
  )

  assert body_index >= 0
  assert expected_index > body_index
