from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(0, str(REPOSITORY_ROOT))

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
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

TARGET_LOCATORS = (
  "Proposition 5.6",
  "(5.3)",
  "Proposition 5.3",
  "Proposition 5.1",
  "Proposition 2.2",
)


def print_target_nodes(label, presentation) -> None:
  print("")
  print("=" * 78)
  print(label)
  print("=" * 78)

  found = False

  for index, node in enumerate(presentation.nodes):
    step = node.proof_step
    reference = extract_toda_group_proof_step_literature_reference(step)

    if (
      reference is None
      or reference.locator not in TARGET_LOCATORS
    ):
      continue

    found = True
    print(
      f"node {index}: "
      f"{reference.locator} | "
      f"type={type(step.conclusion).__name__} | "
      f"rule="
      + (
        "None"
        if step.inference_rule is None
        else step.inference_rule.name
      )
      + f" | premises={len(step.premises)}"
    )

  if not found:
    print("(none)")


def print_entries(label, entries, statement_lines=None) -> None:
  print("")
  print("=" * 78)
  print(label)
  print("=" * 78)

  found = False

  for entry in entries:
    if entry.reference.locator not in TARGET_LOCATORS:
      continue

    found = True
    print(
      f"[{entry.number}] "
      f"{entry.reference.locator} "
      f"steps={len(entry.proof_steps)}"
    )

    if statement_lines is not None:
      lines = statement_lines.get(entry.number, ())
      print(f"  statement_lines={len(lines)}")

      for line in lines:
        print("   ", line)

    for step in entry.proof_steps:
      boundary = classify_toda_literature_statement_step(step)
      print(
        "  - "
        + type(step.conclusion).__name__
        + " | "
        + (
          "None"
          if step.inference_rule is None
          else step.inference_rule.name
        )
        + " | boundary="
        + repr(boundary)
      )

  if not found:
    print("(none)")


def print_dependency_tree(presentation, locator, max_depth=4) -> None:
  print("")
  print("=" * 78)
  print("DEPENDENCY TREE FOR ", locator, sep="")
  print("=" * 78)

  roots = []

  for node in presentation.nodes:
    step = node.proof_step
    reference = extract_toda_group_proof_step_literature_reference(step)

    if (
      reference is not None
      and reference.locator == locator
    ):
      roots.append(step)

  if not roots:
    print("(no matching nodes)")
    return

  seen = set()

  def walk(step, depth):
    prefix = "  " * depth
    reference = extract_toda_group_proof_step_literature_reference(step)

    print(
      prefix
      + "- "
      + type(step.conclusion).__name__
      + " | ref="
      + (
        "None"
        if reference is None
        else str(reference.locator)
      )
      + " | rule="
      + (
        "None"
        if step.inference_rule is None
        else step.inference_rule.name
      )
    )

    if depth >= max_depth:
      return

    key = id(step)

    if key in seen:
      print(prefix + "  (already visited)")
      return

    seen.add(key)

    for premise in step.premises:
      walk(premise, depth + 1)

  for root in roots:
    walk(root, 0)


def main() -> int:
  print("Repository root:", REPOSITORY_ROOT)

  report = build_standard_toda_report(n=3, k=3)
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
  base_presentation = build_toda_group_proof_presentation(replay)
  closure_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      base_presentation
    )
  )

  print("base nodes:", len(base_presentation.nodes))
  print("base edges:", len(base_presentation.edges))
  print("closure nodes:", len(closure_presentation.nodes))
  print("closure edges:", len(closure_presentation.edges))
  print("closure max_depth:", closure_presentation.max_depth)

  print_target_nodes(
    "TARGET NODES BEFORE SEMANTIC CLOSURE",
    base_presentation,
  )
  print_target_nodes(
    "TARGET NODES AFTER SEMANTIC CLOSURE",
    closure_presentation,
  )

  raw_entries = build_toda_group_proof_narrative_reference_entries(
    closure_presentation
  )
  print_entries(
    "STAGE A: RAW REFERENCES AFTER SEMANTIC CLOSURE",
    raw_entries,
  )

  boundary_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      raw_entries,
      closure_presentation.root_step,
    )
  )
  print_entries(
    "STAGE B: AFTER FIXED-STATEMENT BOUNDARY",
    boundary_entries,
  )

  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      closure_presentation,
      boundary_entries,
    )
  )
  print_entries(
    "STAGE C: STATEMENT LINES",
    boundary_entries,
    statement_lines,
  )

  (
    excluded_entries,
    excluded_lines,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      boundary_entries,
      statement_lines,
      closure_presentation.root_step,
    )
  )
  print_entries(
    "STAGE D: AFTER ROOT REFERENCE EXCLUSION",
    excluded_entries,
    excluded_lines,
  )

  print("")
  print("=" * 78)
  print("SUMMARY")
  print("=" * 78)

  for locator in TARGET_LOCATORS:
    def has(entries):
      return any(
        entry.reference.locator == locator
        for entry in entries
      )

    print(
      locator,
      ": raw=",
      "YES" if has(raw_entries) else "NO",
      ", boundary=",
      "YES" if has(boundary_entries) else "NO",
      ", root_excluded=",
      "YES" if has(excluded_entries) else "NO",
      sep="",
    )

  print_dependency_tree(
    closure_presentation,
    "Proposition 5.3",
    max_depth=4,
  )
  print_dependency_tree(
    closure_presentation,
    "Proposition 2.2",
    max_depth=4,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
