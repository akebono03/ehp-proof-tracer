from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = PACKAGE_DIR.parent

if str(
  REPOSITORY_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  prune_toda_group_proof_narrative_root_zero_direct_premise_references,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
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


def _presentation():
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
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def _describe_entry(
  entry,
) -> list[str]:
  lines = [
    (
      f"[R{entry.number}] "
      f"locator={entry.reference.locator!r} "
      f"label={entry.reference.label!r}"
    ),
  ]

  for index, proof_step in enumerate(
    entry.proof_steps,
    start=1,
  ):
    boundary = (
      classify_toda_literature_statement_step(
        proof_step
      )
    )
    inference_rule = (
      proof_step.inference_rule
    )
    lines.append(
      (
        f"  step[{index}] "
        f"rule="
        f"{None if inference_rule is None else inference_rule.name!r}"
      )
    )
    lines.append(
      (
        f"    conclusion_type="
        f"{type(proof_step.conclusion).__name__}"
      )
    )

    if boundary is None:
      lines.append(
        "    boundary=None"
      )
      continue

    lines.append(
      (
        "    boundary="
        f"classification={boundary.classification.value!r}, "
        f"locator={boundary.reference_locator!r}, "
        f"component={boundary.component_key!r}"
      )
    )

  return lines


def main() -> None:
  presentation = _presentation()
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  raw_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  fixed_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      raw_entries,
      presentation.root_step,
    )
  )
  fixed_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      fixed_entries,
    )
  )
  (
    repair4_entries,
    repair4_lines,
  ) = (
    prune_toda_group_proof_narrative_root_zero_direct_premise_references(
      presentation,
      fixed_entries,
      fixed_lines,
    )
  )

  output = []
  output.append(
    "=== FINAL PUBLIC NARRATIVE ==="
  )
  output.append(
    rendered
  )
  output.append("")
  output.append(
    "=== FINAL REFERENCE HEADINGS ==="
  )

  for line in rendered.splitlines():
    if line.startswith(
      "**[R"
    ):
      output.append(
        line
      )

  output.append("")
  output.append(
    "=== FINAL LINES CONTAINING 5.3 OR NU-PRIME ==="
  )

  for line in rendered.splitlines():
    if (
      "5.3" in line
      or r"\nu'" in line
    ):
      output.append(
        line
      )

  output.append("")
  output.append(
    "=== RAW REFERENCE ENTRIES ==="
  )

  for entry in raw_entries:
    output.extend(
      _describe_entry(
        entry
      )
    )

  output.append("")
  output.append(
    "=== FIXED-BOUNDARY REFERENCE ENTRIES ==="
  )

  for entry in fixed_entries:
    output.extend(
      _describe_entry(
        entry
      )
    )
    output.append(
      (
        "  rendered_lines="
        f"{fixed_lines.get(entry.number, ())!r}"
      )
    )

  output.append("")
  output.append(
    "=== AFTER REPAIR4 PRUNER DIRECT CALL ==="
  )

  for entry in repair4_entries:
    output.extend(
      _describe_entry(
        entry
      )
    )
    output.append(
      (
        "  rendered_lines="
        f"{repair4_lines.get(entry.number, ())!r}"
      )
    )

  output.append("")
  output.append(
    "=== REPAIR4 PI6 NO-OP CHECK ==="
  )
  output.append(
    (
      "entries_equal="
      f"{repair4_entries == fixed_entries}"
    )
  )
  output.append(
    (
      "lines_equal="
      f"{repair4_lines == fixed_lines}"
    )
  )

  text = "\n".join(
    output
  )

  audit_output_dir = (
    PACKAGE_DIR
    / "audit_output"
  )
  audit_output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  output_path = (
    audit_output_dir
    / "pi6_reference_diagnosis.txt"
  )
  output_path.write_text(
    text,
    encoding="utf-8",
  )

  print(
    text
  )
  print()
  print(
    "Audit output:",
    output_path,
  )


if __name__ == "__main__":
  main()
