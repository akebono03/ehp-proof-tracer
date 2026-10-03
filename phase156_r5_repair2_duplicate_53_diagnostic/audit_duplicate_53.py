from __future__ import annotations

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _is_toda_group_proof_narrative_reference_statement_candidate,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  select_toda_group_proof_narrative_reference_statement_steps,
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


def _candidate_steps(
  entry,
) -> tuple:
  result = []
  seen = set()

  for proof_step in entry.proof_steps:
    rendered = _render_generic_narrative_step(
      proof_step
    )

    if not (
      _is_toda_group_proof_narrative_reference_statement_candidate(
        proof_step,
        rendered,
      )
    ):
      continue

    if rendered in seen:
      continue

    seen.add(
      rendered
    )
    result.append(
      proof_step
    )

  return tuple(
    result
  )


def _rule_name(
  proof_step,
) -> str:
  inference_rule = getattr(
    proof_step,
    "inference_rule",
    None,
  )
  if inference_rule is None:
    return ""

  return str(
    getattr(
      inference_rule,
      "name",
      "",
    )
  )


def main() -> int:
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
    max_depth=2,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )

  matching = tuple(
    entry
    for entry in entries
    if entry.reference.locator
    == "(5.3)"
  )

  print(
    "=" * 78
  )
  print(
    "Phase156-R5 repair2 duplicate (5.3) diagnostic"
  )
  print(
    "=" * 78
  )
  print(
    "matching entries:",
    len(
      matching
    ),
  )
  print()

  for index, entry in enumerate(
    matching,
    start=1,
  ):
    reference = entry.reference

    print(
      "-" * 78
    )
    print(
      "ENTRY",
      index,
    )
    print(
      "number:",
      entry.number,
    )
    print(
      "label:",
      reference.label,
    )
    print(
      "locator:",
      reference.locator,
    )
    print(
      "author:",
      reference.author,
    )
    print(
      "title:",
      reference.title,
    )
    print(
      "year:",
      reference.year,
    )
    print(
      "proof_steps:",
      len(
        entry.proof_steps
      ),
    )
    print()

    candidates = _candidate_steps(
      entry
    )
    selected = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        candidates,
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    for step_index, proof_step in enumerate(
      entry.proof_steps,
      start=1,
    ):
      extracted = (
        extract_toda_group_proof_step_literature_reference(
          proof_step
        )
      )
      print(
        "  STEP",
        step_index,
      )
      print(
        "    rule_name:",
        _rule_name(
          proof_step
        ),
      )
      print(
        "    rendered:",
        _render_generic_narrative_step(
          proof_step
        ),
      )
      print(
        "    selected:",
        proof_step in selected,
      )
      print(
        "    extracted_label:",
        (
          ""
          if extracted is None
          else extracted.label
        ),
      )
      print(
        "    extracted_locator:",
        (
          ""
          if extracted is None
          else extracted.locator
        ),
      )
      print(
        "    premise_count:",
        len(
          proof_step.premises
        ),
      )
      print()

  print(
    "=" * 78
  )

  if len(
    matching
  ) != 2:
    print(
      "FAIL: expected exactly two (5.3) entries in the current repair2 state."
    )
    return 1

  print(
    "PASS: reproduced exactly two (5.3) entries."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
