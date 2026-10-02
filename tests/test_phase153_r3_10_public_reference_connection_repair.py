from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
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


def _phase153_r3_10_presentations():
  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      report = build_standard_toda_report(
        n=n,
        k=k,
      )

      if not report.candidates:
        continue

      group_result = (
        report.candidates[
          0
        ].source_candidate.group_result
      )
      replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=2,
      )
      raw_presentation = (
        build_toda_group_proof_presentation(
          replay
        )
      )
      presentation = (
        build_toda_group_proof_narrative_semantic_closure_presentation(
          raw_presentation
        )
      )

      yield (
        n,
        k,
        raw_presentation,
        presentation,
      )


def _phase153_r3_10_public_reference_section(
  rendered: str,
  canonical_reference_section: str,
) -> str:
  lines = rendered.splitlines()

  if "## 証明" in lines:
    proof_index = lines.index(
      "## 証明"
    )

    return "\n".join(
      lines[
        :proof_index
      ]
    )

  if rendered.startswith(
    canonical_reference_section
  ):
    return canonical_reference_section

  return ""


def test_phase153_r3_10_all_group_reference_population_invariants():
  import re

  violations = []

  for (
    n,
    k,
    raw_presentation,
    _presentation,
  ) in _phase153_r3_10_presentations():
    rendered = (
      render_toda_group_proof_narrative_markdown(
        raw_presentation
      )
    )

    header_numbers = []
    body_marker_numbers = []

    for line in rendered.splitlines():
      header_match = re.match(
        r"^\*\*\[R(\d+)\]",
        line,
      )

      if header_match is not None:
        header_numbers.append(
          int(
            header_match.group(
              1
            )
          )
        )
        continue

      body_marker_numbers.extend(
        int(
          number
        )
        for number in re.findall(
          r"\[R(\d+)\]",
          line,
        )
      )

    if header_numbers:
      expected = list(
        range(
          1,
          len(
            header_numbers
          )
          + 1,
        )
      )

      if header_numbers != expected:
        violations.append(
          (
            n,
            k,
            "non_contiguous_reference_headers",
            tuple(
              header_numbers
            ),
          )
        )

      header_set = set(
        header_numbers
      )

      for marker in body_marker_numbers:
        if marker in header_set:
          continue

        violations.append(
          (
            n,
            k,
            "body_marker_without_header",
            marker,
          )
        )

      continue

    if body_marker_numbers:
      violations.append(
        (
          n,
          k,
          "body_markers_without_reference_headers",
          tuple(
            body_marker_numbers
          ),
        )
      )

  assert violations == []


