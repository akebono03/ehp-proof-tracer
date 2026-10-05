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


def _pi6_3_rendered() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[
      0
    ]
    .source_candidate
    .group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _r1_part() -> str:
  rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "まず",
    1,
  )[
    0
  ]

  return reference_part.split(
    "**[R2]",
    1,
  )[
    0
  ]


def test_phase157_r5_r7_equation53_definition_precedes_consequences():
  r1_part = _r1_part()

  definition_index = r1_part.find(
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
  )
  membership_index = r1_part.find(
    r"\nu' \in \pi_{6}^{3}"
  )
  double_index = r1_part.find(
    r"2\nu' = \eta_{3}\eta_{4}\eta_{5}"
  )

  assert definition_index >= 0
  assert membership_index >= 0
  assert double_index >= 0
  assert (
    definition_index
    < membership_index
    < double_index
  )


def test_phase157_r5_r7_equation53_definition_uses_to_suru_connector():
  r1_part = _r1_part()

  assert (
    (
      r"$\nu' \in "
      r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$"
      " とすると,"
    )
    in r1_part
  )


def test_phase157_r5_r7_equation53_consequences_use_comma_then_period():
  r1_part = _r1_part()

  assert (
    r"$\nu' \in \pi_{6}^{3}$,"
    in r1_part
  )
  assert (
    (
      r"$2\nu' = "
      r"\eta_{3}\eta_{4}\eta_{5}$."
    )
    in r1_part
  )
