from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
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


def _phase153_r3_11_presentations():
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


def _phase153_r3_11_public_body(
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
        proof_index + 1:
      ]
    )

  if rendered.startswith(
    canonical_reference_section
  ):
    return rendered[
      len(
        canonical_reference_section
      ):
    ].lstrip()

  return rendered


def test_phase153_r3_11_replaces_embedded_unmarked_selected_statement_with_reference_marker():
  statement = "$E: A \\xrightarrow{\\cong} B$"
  body = (
    "この結果として、"
    + statement
    + "を得る。"
  )

  suppressed = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert statement not in suppressed
  assert suppressed == "この結果として、[R2]を得る。"


def test_phase153_r3_11_preserves_surrounding_prose_when_replacing_embedded_statement():
  statement = "$E: A \\xrightarrow{\\cong} B$"
  body = (
    "まず、"
    + statement
    + "を確認し、次の計算へ進む。"
  )

  suppressed = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert suppressed == (
    "まず、[R2]を確認し、次の計算へ進む。"
  )


def test_phase153_r3_11_keeps_nonidentical_body_statement():
  selected = "$E: A \\xrightarrow{\\cong} B$"
  different = "$E^2: A \\xrightarrow{\\cong} B$"
  body = (
    "この結果として、"
    + different
    + "を得る。"
  )

  suppressed = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          selected,
        ),
      },
    )
  )

  assert suppressed == body


def test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates():
  duplicates = []

  for (
    n,
    k,
    raw_presentation,
    presentation,
  ) in _phase153_r3_11_presentations():
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
    body = (
      _phase153_r3_11_public_body(
        rendered,
        canonical_reference_section,
      )
    )

    for reference_number, statement_lines in (
      selected_by_number.items()
    ):
      for statement_line in statement_lines:
        if statement_line not in body:
          continue

        duplicates.append(
          (
            n,
            k,
            reference_number,
            statement_line,
          )
        )

  assert duplicates == []
