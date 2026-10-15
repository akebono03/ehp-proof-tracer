from __future__ import annotations

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
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

  for depth in (
    2,
    3,
  ):
    replay = build_toda_group_result_proof_replay(
      group_result,
      max_depth=depth,
    )
    raw = build_toda_group_proof_presentation(
      replay
    )
    presentation = (
      build_toda_group_proof_narrative_semantic_closure_presentation(
        raw
      )
    )
    entries = build_toda_group_proof_narrative_reference_entries(
      presentation
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
      "DEPTH",
      depth,
    )
    print(
      "(5.3) entries:",
      len(
        matching
      ),
    )
    print(
      "=" * 78
    )

    for entry_index, entry in enumerate(
      matching,
      start=1,
    ):
      print(
        "ENTRY",
        entry_index,
      )
      print(
        "number:",
        entry.number,
      )
      print(
        "label:",
        entry.reference.label,
      )
      print(
        "locator:",
        entry.reference.locator,
      )
      print(
        "author:",
        entry.reference.author,
      )
      print(
        "title:",
        entry.reference.title,
      )
      print(
        "year:",
        entry.reference.year,
      )
      print(
        "proof_steps:",
        len(
          entry.proof_steps
        ),
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
    "PASS: diagnostic completed."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
