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


def test_phase153_r3_10_all_selected_statements_are_publicly_visible():
  missing = []

  for (
    n,
    k,
    raw_presentation,
    presentation,
  ) in _phase153_r3_10_presentations():
    entries = (
      build_toda_group_proof_narrative_reference_entries(
        presentation
      )
    )

    if not entries:
      continue

    selected_by_number = (
      _toda_group_proof_narrative_reference_statement_lines_by_number(
        presentation,
        entries,
      )
    )
    canonical_reference_section = (
      render_toda_group_proof_narrative_reference_entries_markdown(
        entries,
        selected_by_number,
      )
    )
    rendered = (
      render_toda_group_proof_narrative_markdown(
        raw_presentation
      )
    )
    public_reference_section = (
      _phase153_r3_10_public_reference_section(
        rendered,
        canonical_reference_section,
      )
    )

    assert public_reference_section, (
      n,
      k,
      rendered,
    )

    for entry in entries:
      for statement_line in selected_by_number.get(
        entry.number,
        (),
      ):
        if statement_line in public_reference_section:
          continue

        missing.append(
          (
            n,
            k,
            entry.number,
            entry.reference.locator
            or entry.reference.label,
            statement_line,
          )
        )

  assert missing == []


def test_phase153_r3_10_public_reference_markers_cover_structured_entries():
  missing_markers = []

  for (
    n,
    k,
    raw_presentation,
    presentation,
  ) in _phase153_r3_10_presentations():
    entries = (
      build_toda_group_proof_narrative_reference_entries(
        presentation
      )
    )

    if not entries:
      continue

    selected_by_number = (
      _toda_group_proof_narrative_reference_statement_lines_by_number(
        presentation,
        entries,
      )
    )
    canonical_reference_section = (
      render_toda_group_proof_narrative_reference_entries_markdown(
        entries,
        selected_by_number,
      )
    )
    rendered = (
      render_toda_group_proof_narrative_markdown(
        raw_presentation
      )
    )
    public_reference_section = (
      _phase153_r3_10_public_reference_section(
        rendered,
        canonical_reference_section,
      )
    )

    assert public_reference_section, (
      n,
      k,
      rendered,
    )

    for entry in entries:
      marker = (
        "[R"
        + str(
          entry.number
        )
        + "]"
      )

      if marker in public_reference_section:
        continue

      missing_markers.append(
        (
          n,
          k,
          entry.number,
          entry.reference.locator
          or entry.reference.label,
        )
      )

  assert missing_markers == []
