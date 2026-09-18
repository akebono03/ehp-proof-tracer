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
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


REPRESENTATIVE_KEYS = (
  "pi7_4",
  "pi9_5",
  "pi10_4",
  "pi11_5",
  "pi9_2",
  "pi12_5",
)


def build_phase96_12_report(
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
    "report": (
      render_toda_full_proof_report_markdown(
        presentation
      )
    ),
  }


def test_phase96_12_actual_pi9_5_exactness_uses_consistent_latex_delta():
  actual = (
    build_phase96_12_report(
      "pi9_5"
    )
  )

  statement = (
    actual[
      "data"
    ][
      "phase68"
    ][
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
    r"\xrightarrow{\Delta}"
    in rendered
  )

  assert (
    r"\xrightarrow{Δ}"
    not in rendered
  )


def test_phase96_12_actual_pi9_5_full_report_has_no_raw_delta_arrow_markup():
  actual = (
    build_phase96_12_report(
      "pi9_5"
    )
  )

  assert (
    r"\xrightarrow{\Delta}"
    in actual[
      "report"
    ]
  )

  assert (
    r"\xrightarrow{Δ}"
    not in actual[
      "report"
    ]
  )


def test_phase96_12_map_property_narrative_does_not_overstate_exactness_dependency():
  actual = (
    build_phase96_12_report(
      "pi9_5"
    )
  )

  report = actual[
    "report"
  ]

  delta_injective = (
    r"$\Delta: \pi_{9}^{9} \to "
    r"\pi_{7}^{4} "
    r"\text{ is injective}$"
  )

  matching_lines = tuple(
    line
    for line in report.splitlines()
    if delta_injective in line
  )

  assert len(
    matching_lines
  ) == 1

  assert (
    "From the preceding statements:"
    in matching_lines[
      0
    ]
  )

  assert (
    "preceding exactness and map information"
    not in matching_lines[
      0
    ]
  )


def test_phase96_12_actual_pi9_5_full_report_has_each_major_section_once():
  actual = (
    build_phase96_12_report(
      "pi9_5"
    )
  )

  report = actual[
    "report"
  ]

  headings = (
    "## Result",
    "## Source",
    "## EHP sequence",
    "## Exactness",
    "## Proof flow",
    "## Readable proof narrative",
  )

  assert all(
    report.count(
      heading
    ) == 1
    for heading in headings
  )


def test_phase96_12_technical_flow_and_readable_narrative_remain_distinct_sections():
  actual = (
    build_phase96_12_report(
      "pi9_5"
    )
  )

  report = actual[
    "report"
  ]

  technical_position = (
    report.index(
      "## Proof flow"
    )
  )

  narrative_position = (
    report.index(
      "## Readable proof narrative"
    )
  )

  assert (
    technical_position
    < narrative_position
  )

  assert (
    "**map property**"
    in report[
      technical_position:
      narrative_position
    ]
  )

  assert (
    r"\text{ is the zero map}"
    in report[
      narrative_position:
    ]
  )


def test_phase96_12_unknown_statement_fallback_is_explicit_and_safe():
  actual = (
    build_phase96_12_report(
      "pi9_5"
    )
  )

  report = actual[
    "report"
  ]

  assert (
    "`TodaProp56FiniteDimensionalStatement`"
    in report
  )

  assert (
    "object at 0x"
    not in report
  )


def test_phase96_12_all_representative_targets_render_without_python_object_repr():
  for key in REPRESENTATIVE_KEYS:
    actual = (
      build_phase96_12_report(
        key
      )
    )

    report = actual[
      "report"
    ]

    assert report.startswith(
      "# $\\pi_"
    )

    assert report.endswith(
      "\n"
    )

    assert (
      "object at 0x"
      not in report
    )


def test_phase96_12_representative_report_rendering_is_deterministic_and_non_mutating():
  data = build_phase95_20_data()

  before = (
    data[
      "repository"
    ].entries()
  )

  reports = []

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

    assert first == second

    reports.append(
      first
    )

  after = (
    data[
      "repository"
    ].entries()
  )

  assert len(
    reports
  ) == len(
    REPRESENTATIVE_KEYS
  )

  assert after == before

  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )
