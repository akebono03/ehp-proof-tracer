import pytest

from test_phase68_pi9_5_nu5_eta8 import (
  build_phase68_6_data,
)
from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
  get_single_candidate,
)
from toda_end_to_end_presentation import (
  build_toda_end_to_end_candidate_presentation,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
  render_toda_proof_step_mathematical_markdown,
  render_toda_readable_proof_narrative_markdown,
)
from toda_proof_presentation import (
  build_toda_proof_step_presentation,
)


def build_phase96_10_actual_pi9_5():
  data = build_phase95_20_data()

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
      data[
        "repository"
      ].entries(),
    )
  )

  phase68_6 = (
    data[
      "phase68"
    ][
      "phase68_6"
    ]
  )

  return {
    "data": data,
    "candidate": candidate,
    "presentation": presentation,
    "phase68_6": phase68_6,
  }


def test_phase96_10_renders_actual_pi9_5_final_group_relation():
  actual = (
    build_phase96_10_actual_pi9_5()
  )

  final_step = (
    actual[
      "candidate"
    ]
    .group_result
    .proof_step
  )

  assert (
    render_toda_proof_statement_latex(
      final_step.conclusion
    )
    == (
      r"\pi_{9}^{5} = "
      r"\mathbb{Z}/2\{\nu_{5}\eta_{8}\}"
    )
  )


def test_phase96_10_renders_actual_delta_injective_statement():
  actual = (
    build_phase96_10_actual_pi9_5()
  )

  statement = (
    actual[
      "phase68_6"
    ][
      "delta_injective_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"\Delta: "
      r"\pi_{9}^{9} \to \pi_{7}^{4} "
      r"\text{ is injective}"
    )
  )


def test_phase96_10_renders_actual_hopf_zero_statement():
  actual = (
    build_phase96_10_actual_pi9_5()
  )

  statement = (
    actual[
      "phase68_6"
    ][
      "hopf_zero_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"H: "
      r"\pi_{9}^{5} \to \pi_{9}^{9} "
      r"\text{ is the zero map}"
    )
  )


def test_phase96_10_renders_actual_suspension_surjective_statement():
  actual = (
    build_phase96_10_actual_pi9_5()
  )

  statement = (
    actual[
      "phase68_6"
    ][
      "suspension_surjective_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"E: "
      r"\pi_{8}^{4} \to \pi_{9}^{5} "
      r"\text{ is surjective}"
    )
  )


def test_phase96_10_renders_actual_h_delta_exactness_statement():
  actual = (
    build_phase96_10_actual_pi9_5()
  )

  statement = (
    actual[
      "phase68_6"
    ][
      "h_delta_exactness_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert (
    rendered
    == (
      r"\pi_{9}^{5} "
      r"\xrightarrow{H} "
      r"\pi_{9}^{9} "
      r"\xrightarrow{Δ} "
      r"\pi_{7}^{4} "
      r"\text{ is exact}"
    )
  )


def test_phase96_10_renders_actual_nu5_definition():
  actual = (
    build_phase96_10_actual_pi9_5()
  )

  statement = (
    actual[
      "phase68_6"
    ][
      "nu5_definition_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"\nu_{5} "
      r"\text{ is the defined }"
      r"\nu\text{-family element}"
    )
  )


def test_phase96_10_proof_step_markdown_uses_mathematical_statement_when_supported():
  actual = (
    build_phase96_10_actual_pi9_5()
  )

  step = (
    actual[
      "phase68_6"
    ][
      "hopf_zero_step"
    ]
  )

  rendered = (
    render_toda_proof_step_mathematical_markdown(
      build_toda_proof_step_presentation(
        step
      )
    )
  )

  assert (
    "**map property**"
    in rendered
  )
  assert (
    r"H: \pi_{9}^{5} \to "
    r"\pi_{9}^{9} "
    r"\text{ is the zero map}"
    in rendered
  )
  assert (
    "TodaHopfInvariantZeroStatement"
    not in rendered
  )


def test_phase96_10_unknown_aggregate_statement_keeps_safe_type_fallback():
  actual = (
    build_phase96_10_actual_pi9_5()
  )

  aggregate_step = (
    actual[
      "data"
    ][
      "phase65"
    ][
      "integration_step"
    ]
  )

  presentation = (
    build_toda_proof_step_presentation(
      aggregate_step
    )
  )

  rendered = (
    render_toda_proof_step_mathematical_markdown(
      presentation
    )
  )

  assert (
    "TodaProp56FiniteDimensionalStatement"
    in rendered
  )


def test_phase96_10_actual_pi9_5_narrative_is_dependency_first_and_mathematical():
  actual = (
    build_phase96_10_actual_pi9_5()
  )

  rendered = (
    render_toda_readable_proof_narrative_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert (
    "## Readable proof narrative"
    in rendered
  )

  delta_injective = (
    r"\Delta: \pi_{9}^{9} \to "
    r"\pi_{7}^{4} "
    r"\text{ is injective}"
  )
  hopf_zero = (
    r"H: \pi_{9}^{5} \to "
    r"\pi_{9}^{9} "
    r"\text{ is the zero map}"
  )
  suspension_surjective = (
    r"E: \pi_{8}^{4} \to "
    r"\pi_{9}^{5} "
    r"\text{ is surjective}"
  )
  final_group = (
    r"\pi_{9}^{5} = "
    r"\mathbb{Z}/2\{\nu_{5}\eta_{8}\}"
  )

  assert delta_injective in rendered
  assert hopf_zero in rendered
  assert suspension_surjective in rendered
  assert final_group in rendered

  assert (
    rendered.index(
      delta_injective
    )
    < rendered.index(
      hopf_zero
    )
  )

  assert (
    rendered.index(
      hopf_zero
    )
    < rendered.index(
      suspension_surjective
    )
  )

  assert (
    rendered.index(
      suspension_surjective
    )
    < rendered.index(
      final_group
    )
  )


def test_phase96_10_narrative_keeps_unknown_statements_without_inventing_math():
  actual = (
    build_phase96_10_actual_pi9_5()
  )

  rendered = (
    render_toda_readable_proof_narrative_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert (
    "`TodaProp56FiniteDimensionalStatement`"
    in rendered
  )


def test_phase96_10_narrative_is_pure_and_repository_non_mutating():
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
    render_toda_readable_proof_narrative_markdown(
      presentation
    )
  )

  second = (
    render_toda_readable_proof_narrative_markdown(
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


def test_phase96_10_statement_renderer_returns_none_for_unknown_statement():
  data = build_phase68_6_data()

  unknown_statement = (
    data[
      "prop56_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      unknown_statement
    )
    is None
  )


def test_phase96_10_narrative_renderer_rejects_non_presentation():
  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "TodaEndToEndCandidatePresentation"
    ),
  ):
    render_toda_readable_proof_narrative_markdown(
      "not-a-presentation"
    )
