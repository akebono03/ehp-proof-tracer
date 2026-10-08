from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _phase153_r6_render_reference_statement,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
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
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)


def _rule_name(
  step,
) -> str:
  if step.inference_rule is None:
    return step.rule.value

  return step.inference_rule.name


def _describe_step(
  step,
) -> str:
  reference = (
    extract_toda_group_proof_step_literature_reference(
      step
    )
  )
  boundary = (
    classify_toda_literature_statement_step(
      step
    )
  )

  return (
    f"rule={_rule_name(step)!r}\n"
    f"  reference="
    f"{None if reference is None else (reference.label, reference.locator)!r}\n"
    f"  boundary="
    f"{None if boundary is None else (boundary.classification.value, boundary.reference_locator, boundary.component_key)!r}\n"
    f"  rendered={_render_generic_narrative_step(step)!r}"
  )


def main():
  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
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

  print(
    "=" * 78
  )
  print(
    "Phase 161-R4-R5 repair15 Proposition 5.1 selection audit"
  )
  print(
    "=" * 78
  )

  print()
  print(
    "[1] Proposition 5.1 entries BEFORE fixed-boundary filter"
  )

  for entry in entries:
    if entry.reference.locator != "Proposition 5.1":
      continue

    print(
      f"entry R{entry.number} "
      f"label={entry.reference.label!r} "
      f"locator={entry.reference.locator!r}"
    )

    for step in entry.proof_steps:
      print(
        _describe_step(
          step
        )
      )

  filtered = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      entries,
      presentation.root_step,
    )
  )

  print()
  print(
    "[2] Proposition 5.1 entries AFTER fixed-boundary filter"
  )

  for entry in filtered:
    if entry.reference.locator != "Proposition 5.1":
      continue

    print(
      f"entry R{entry.number} "
      f"label={entry.reference.label!r} "
      f"locator={entry.reference.locator!r}"
    )

    candidates = []

    for step in entry.proof_steps:
      print(
        _describe_step(
          step
        )
      )

      rendered = _render_generic_narrative_step(
        step
      )

      if rendered:
        candidates.append(
          step
        )

    selected = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidates
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    print(
      "  selected rules:",
      tuple(
        _rule_name(
          step
        )
        for step in selected
      ),
    )

    print(
      "  selected rendered:"
    )

    for step in selected:
      rendered = _render_generic_narrative_step(
        step
      )
      specialized = (
        _phase153_r6_render_reference_statement(
          presentation,
          entry,
          step,
          rendered,
        )
      )

      print(
        "   ",
        {
          "rule": _rule_name(
            step
          ),
          "raw": rendered,
          "specialized": specialized,
        },
      )

  lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      filtered,
    )
  )

  print()
  print(
    "[3] Final statement lines after selection"
  )

  for entry in filtered:
    if entry.reference.locator != "Proposition 5.1":
      continue

    print(
      f"R{entry.number}:",
      lines.get(
        entry.number
      ),
    )

  print()
  print(
    "Audit completed. Production changes: NONE"
  )


if __name__ == "__main__":
  main()
