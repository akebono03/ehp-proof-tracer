import pytest

from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
  get_single_candidate,
)
from toda_end_to_end_presentation import (
  build_toda_end_to_end_candidate_presentation,
)
from toda_full_proof_report_renderer import (
  render_toda_full_proof_report_markdown,
)


REPRESENTATIVE_KEYS = (
  "pi7_4",
  "pi9_5",
  "pi10_4",
  "pi11_5",
  "pi9_2",
  "pi12_5",
)


def build_phase96_11_presentation(
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


def test_phase96_11_actual_pi9_5_full_report_contains_all_major_sections():
  actual = (
    build_phase96_11_presentation(
      "pi9_5"
    )
  )

  rendered = (
    render_toda_full_proof_report_markdown(
      actual[
        "presentation"
      ]
    )
  )

  expected_headings = (
    "# $\\pi_{9}^{5}$",
    "## Result",
    "## Source",
    "## EHP sequence",
    "## Exactness",
    "## Proof flow",
    "## Readable proof narrative",
  )

  assert all(
    heading in rendered
    for heading in expected_headings
  )


def test_phase96_11_actual_pi9_5_section_order_is_stable():
  actual = (
    build_phase96_11_presentation(
      "pi9_5"
    )
  )

  rendered = (
    render_toda_full_proof_report_markdown(
      actual[
        "presentation"
      ]
    )
  )

  headings = (
    "## Result",
    "## Source",
    "## EHP sequence",
    "## Exactness",
    "## Proof flow",
    "## Readable proof narrative",
  )

  positions = tuple(
    rendered.index(
      heading
    )
    for heading in headings
  )

  assert positions == tuple(
    sorted(
      positions
    )
  )


def test_phase96_11_actual_pi9_5_full_report_contains_group_result():
  actual = (
    build_phase96_11_presentation(
      "pi9_5"
    )
  )

  rendered = (
    render_toda_full_proof_report_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert (
    r"\pi_{9}^{5} \cong "
    r"\mathbb{Z}/2\{\nu_{5}\eta_{8}\}"
    in rendered
  )


def test_phase96_11_actual_pi9_5_full_report_contains_source_metadata():
  actual = (
    build_phase96_11_presentation(
      "pi9_5"
    )
  )

  rendered = (
    render_toda_full_proof_report_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert "- Phase: 68" in rendered
  assert (
    "- Theorem: Toda Proposition 5.8"
    in rendered
  )
  assert (
    "- Branch: `pi9_5_group_relation`"
    in rendered
  )


def test_phase96_11_actual_pi9_5_full_report_contains_ehp_sequence():
  actual = (
    build_phase96_11_presentation(
      "pi9_5"
    )
  )

  rendered = (
    render_toda_full_proof_report_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert (
    r"\pi_{10}^{9} "
    r"\xrightarrow{\Delta} "
    r"\pi_{8}^{4} "
    r"\xrightarrow{E} "
    r"\pi_{9}^{5} "
    r"\xrightarrow{H} "
    r"\pi_{9}^{9} "
    r"\xrightarrow{\Delta} "
    r"\pi_{7}^{4}"
    in rendered
  )


def test_phase96_11_actual_pi9_5_full_report_contains_mathematical_narrative_steps():
  actual = (
    build_phase96_11_presentation(
      "pi9_5"
    )
  )

  rendered = (
    render_toda_full_proof_report_markdown(
      actual[
        "presentation"
      ]
    )
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
    < rendered.rindex(
      final_group
    )
  )


def test_phase96_11_actual_pi9_5_unknown_statements_remain_safe_fallbacks():
  actual = (
    build_phase96_11_presentation(
      "pi9_5"
    )
  )

  rendered = (
    render_toda_full_proof_report_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert (
    "`TodaProp56FiniteDimensionalStatement`"
    in rendered
  )


def test_phase96_11_pi7_4_full_report_preserves_direct_sum_result():
  actual = (
    build_phase96_11_presentation(
      "pi7_4"
    )
  )

  rendered = (
    render_toda_full_proof_report_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert (
    r"\pi_{7}^{4} \cong "
    r"\mathbb{Z}\{\nu_{4}\}"
    r" \oplus "
    r"\mathbb{Z}/4\{E\nu'\}"
    in rendered
  )

  assert (
    "## Readable proof narrative"
    in rendered
  )


def test_phase96_11_pi9_2_full_report_handles_zero_group_without_forcing_ehp():
  actual = (
    build_phase96_11_presentation(
      "pi9_2"
    )
  )

  presentation = actual[
    "presentation"
  ]

  rendered = (
    render_toda_full_proof_report_markdown(
      presentation
    )
  )

  assert (
    r"\pi_{9}^{2} \cong 0"
    in rendered
  )

  if presentation.ehp is None:
    assert (
      "## EHP sequence"
      not in rendered
    )
    assert (
      "No EHP exactness presentation is attached."
      in rendered
    )


def test_phase96_11_all_representative_targets_render_with_one_unified_entry_point():
  data = build_phase95_20_data()

  repository_entries = (
    data[
      "repository"
    ].entries()
  )

  for key in REPRESENTATIVE_KEYS:
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
        repository_entries,
      )
    )

    rendered = (
      render_toda_full_proof_report_markdown(
        presentation
      )
    )

    assert rendered.startswith(
      "# $\\pi_"
    )
    assert "## Result" in rendered
    assert "## Source" in rendered
    assert "## Proof flow" in rendered
    assert (
      "## Readable proof narrative"
      in rendered
    )


def test_phase96_11_full_report_renderer_is_deterministic_and_repository_non_mutating():
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
    render_toda_full_proof_report_markdown(
      presentation
    )
  )

  second = (
    render_toda_full_proof_report_markdown(
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


def test_phase96_11_full_report_renderer_rejects_non_presentation():
  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "TodaEndToEndCandidatePresentation"
    ),
  ):
    render_toda_full_proof_report_markdown(
      "not-a-presentation"
    )
