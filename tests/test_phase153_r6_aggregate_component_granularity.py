from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _presentation(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase153_r6_repair_pi6_2_prop56_renders_only_consumed_component():
  presentation = _presentation(
    2,
    4,
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  lines_by_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )
  entry = next(
    entry
    for entry in entries
    if (
      entry.reference.locator
      == "Proposition 5.6"
    )
  )
  lines = lines_by_number[
    entry.number
  ]

  assert len(
    lines
  ) == 1
  assert (
    r"\pi_{6}^{3}"
    in lines[0]
  )
  assert (
    r"\pi_{5}^{2}"
    not in lines[0]
  )
  assert (
    r"\pi_{7}^{4}"
    not in lines[0]
  )
  assert (
    r"\pi_{8}^{5}"
    not in lines[0]
  )
  assert (
    r"\pi_{n + 3}^{n}"
    not in lines[0]
  )
