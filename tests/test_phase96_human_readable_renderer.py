import pytest

from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
  get_single_candidate,
)
from toda_end_to_end_presentation import (
  build_toda_end_to_end_candidate_presentation,
)
from toda_human_readable_renderer import (
  render_toda_ehp_sequence_latex,
  render_toda_end_to_end_markdown,
  render_toda_expression_latex,
  render_toda_group_result_latex,
  render_toda_target_latex,
)


def build_phase96_9_presentation(
  key,
):
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      key
    ]
  )

  presentation = (
    build_toda_end_to_end_candidate_presentation(
      candidate,
      data[
        "repository"
      ].entries(),
    )
  )

  return {
    "data": data,
    "candidate": candidate,
    "presentation": presentation,
  }


def test_phase96_9_pi9_5_target_renders_as_latex():
  actual = (
    build_phase96_9_presentation(
      "pi9_5"
    )
  )

  assert (
    render_toda_target_latex(
      actual[
        "presentation"
      ].group.target
    )
    == r"\pi_{9}^{5}"
  )


def test_phase96_9_pi9_5_generator_renders_as_composed_latex_symbol():
  actual = (
    build_phase96_9_presentation(
      "pi9_5"
    )
  )

  generator = (
    actual[
      "presentation"
    ]
    .group
    .generators[
      0
    ]
    .source_generator
  )

  assert (
    render_toda_expression_latex(
      generator
    )
    == r"\nu_{5}\eta_{8}"
  )


def test_phase96_9_pi9_5_group_result_renders_as_latex():
  actual = (
    build_phase96_9_presentation(
      "pi9_5"
    )
  )

  assert (
    render_toda_group_result_latex(
      actual[
        "presentation"
      ].group
    )
    == (
      r"\pi_{9}^{5} \cong "
      r"\mathbb{Z}/2\{\nu_{5}\eta_{8}\}"
    )
  )


def test_phase96_9_pi7_4_direct_sum_renders_as_latex():
  actual = (
    build_phase96_9_presentation(
      "pi7_4"
    )
  )

  assert (
    render_toda_group_result_latex(
      actual[
        "presentation"
      ].group
    )
    == (
      r"\pi_{7}^{4} \cong "
      r"\mathbb{Z}\{\nu_{4}\}"
      r" \oplus "
      r"\mathbb{Z}/4\{E\nu'\}"
    )
  )


def test_phase96_9_pi9_2_zero_group_renders_as_latex():
  actual = (
    build_phase96_9_presentation(
      "pi9_2"
    )
  )

  assert (
    render_toda_group_result_latex(
      actual[
        "presentation"
      ].group
    )
    == r"\pi_{9}^{2} \cong 0"
  )


def test_phase96_9_pi10_4_order_eight_renders_as_latex():
  actual = (
    build_phase96_9_presentation(
      "pi10_4"
    )
  )

  rendered = (
    render_toda_group_result_latex(
      actual[
        "presentation"
      ].group
    )
  )

  assert rendered.startswith(
    r"\pi_{10}^{4} \cong \mathbb{Z}/8\{"
  )
  assert rendered.endswith(
    r"\}"
  )


def test_phase96_9_pi12_5_sigma_triple_prime_renders_as_latex():
  actual = (
    build_phase96_9_presentation(
      "pi12_5"
    )
  )

  rendered = (
    render_toda_group_result_latex(
      actual[
        "presentation"
      ].group
    )
  )

  assert (
    rendered
    == (
      r"\pi_{12}^{5} \cong "
      r"\mathbb{Z}/2\{\sigma'''\}"
    )
  )


def test_phase96_9_actual_pi9_5_ehp_sequence_renders_as_latex():
  actual = (
    build_phase96_9_presentation(
      "pi9_5"
    )
  )

  sequence = (
    actual[
      "presentation"
    ].ehp
  )

  assert (
    sequence
    is not None
  )

  assert (
    render_toda_ehp_sequence_latex(
      sequence
    )
    == (
      r"\pi_{10}^{9} "
      r"\xrightarrow{\Delta} "
      r"\pi_{8}^{4} "
      r"\xrightarrow{E} "
      r"\pi_{9}^{5} "
      r"\xrightarrow{H} "
      r"\pi_{9}^{9} "
      r"\xrightarrow{\Delta} "
      r"\pi_{7}^{4}"
    )
  )


def test_phase96_9_actual_pi9_5_markdown_contains_result_source_and_ehp():
  actual = (
    build_phase96_9_presentation(
      "pi9_5"
    )
  )

  rendered = (
    render_toda_end_to_end_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert "# $\\pi_{9}^{5}$" in rendered
  assert "## Result" in rendered
  assert (
    r"\pi_{9}^{5} \cong "
    r"\mathbb{Z}/2\{\nu_{5}\eta_{8}\}"
    in rendered
  )
  assert "## Source" in rendered
  assert "- Phase: 68" in rendered
  assert (
    "- Theorem: Toda Proposition 5.8"
    in rendered
  )
  assert (
    "- Branch: `pi9_5_group_relation`"
    in rendered
  )
  assert "## EHP sequence" in rendered
  assert (
    r"\xrightarrow{\Delta}"
    in rendered
  )
  assert (
    r"\xrightarrow{E}"
    in rendered
  )
  assert (
    r"\xrightarrow{H}"
    in rendered
  )


def test_phase96_9_actual_pi9_5_markdown_contains_exactness_and_dependency_first_flow():
  actual = (
    build_phase96_9_presentation(
      "pi9_5"
    )
  )

  presentation = actual[
    "presentation"
  ]

  rendered = (
    render_toda_end_to_end_markdown(
      presentation
    )
  )

  assert "## Exactness" in rendered
  assert (
    rendered.count(
      "direct consumers:"
    )
    == 3
  )
  assert "## Proof flow" in rendered

  flow_lines = tuple(
    line
    for line in rendered.splitlines()
    if (
      line
      and line[
        0
      ].isdigit()
      and ". **" in line
    )
  )

  assert len(
    flow_lines
  ) == len(
    presentation
    .proof_flow
    .nodes
  )

  assert (
    type(
      presentation
      .proof_flow
      .root
      .step
      .conclusion
    ).__name__
    in flow_lines[
      -1
    ]
  )


def test_phase96_9_non_ehp_target_omits_ehp_section_and_reports_no_exactness():
  actual = (
    build_phase96_9_presentation(
      "pi9_2"
    )
  )

  presentation = actual[
    "presentation"
  ]

  if presentation.ehp is not None:
    pytest.skip(
      "pi9_2 currently has EHP provenance"
    )

  rendered = (
    render_toda_end_to_end_markdown(
      presentation
    )
  )

  assert (
    "## EHP sequence"
    not in rendered
  )
  assert (
    "No EHP exactness presentation is attached."
    in rendered
  )


def test_phase96_9_renderer_is_pure_and_does_not_mutate_repository():
  data = build_phase95_20_data()

  before = (
    data[
      "repository"
    ].entries()
  )

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  presentation = (
    build_toda_end_to_end_candidate_presentation(
      candidate,
      before,
    )
  )

  first = (
    render_toda_end_to_end_markdown(
      presentation
    )
  )
  second = (
    render_toda_end_to_end_markdown(
      presentation
    )
  )

  after = (
    data[
      "repository"
    ].entries()
  )

  assert first == second
  assert after == before
  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase96_9_markdown_renderer_rejects_non_end_to_end_presentation():
  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "TodaEndToEndCandidatePresentation"
    ),
  ):
    render_toda_end_to_end_markdown(
      "not-a-presentation"
    )


def test_phase96_9_target_renderer_rejects_invalid_type():
  with pytest.raises(
    TypeError,
    match=(
      "target must be a "
      "TodaTargetPresentation"
    ),
  ):
    render_toda_target_latex(
      "not-a-target"
    )
