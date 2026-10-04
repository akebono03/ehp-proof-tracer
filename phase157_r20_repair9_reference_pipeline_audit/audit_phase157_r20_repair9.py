from __future__ import annotations

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
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


TARGET_LOCATORS = {
  "Proposition 5.6",
  "(5.3)",
  "Proposition 5.3",
  "Proposition 5.1",
  "Proposition 2.2",
}


def locator_of(entry) -> str | None:
  return entry.reference.locator


def print_entries(label, entries) -> None:
  print("")
  print("=" * 72)
  print(label)
  print("=" * 72)

  if not entries:
    print("(none)")
    return

  for entry in entries:
    locator = locator_of(
      entry
    )
    marker = (
      " <== TARGET"
      if locator in TARGET_LOCATORS
      else ""
    )

    print(
      f"[{entry.number}] {locator}{marker}"
    )

    for index, step in enumerate(
      entry.proof_steps,
      start=1,
    ):
      rule_name = (
        None
        if step.inference_rule is None
        else step.inference_rule.name
      )
      boundary = (
        classify_toda_literature_statement_step(
          step
        )
      )

      print(
        "  step",
        index,
        "id=",
        id(
          step
        ),
      )
      print(
        "    type=",
        type(
          step.conclusion
        ).__name__,
      )
      print(
        "    rule=",
        rule_name,
      )
      print(
        "    boundary=",
        boundary,
      )
      print(
        "    premises=",
        len(
          step.premises
        ),
      )


def print_statement_lines(
  label,
  entries,
  statement_lines,
) -> None:
  print("")
  print("=" * 72)
  print(label)
  print("=" * 72)

  for entry in entries:
    locator = locator_of(
      entry
    )

    if locator not in TARGET_LOCATORS:
      continue

    lines = statement_lines.get(
      entry.number,
      (),
    )

    print(
      f"[{entry.number}] {locator}: "
      f"{len(lines)} line(s)"
    )

    for line in lines:
      print(
        "   ",
        line,
      )


def print_target_nodes(
  presentation,
) -> None:
  print("")
  print("=" * 72)
  print("TARGET REFERENCE NODES IN PRESENTATION")
  print("=" * 72)

  found = False

  for node_index, node in enumerate(
    presentation.nodes
  ):
    step = node.proof_step
    reference = (
      extract_toda_group_proof_step_literature_reference(
        step
      )
    )

    if (
      reference is None
      or reference.locator
      not in TARGET_LOCATORS
    ):
      continue

    found = True
    print(
      "node",
      node_index,
      "locator=",
      reference.locator,
      "id=",
      id(
        step
      ),
      "type=",
      type(
        step.conclusion
      ).__name__,
      "rule=",
      (
        None
        if step.inference_rule is None
        else step.inference_rule.name
      ),
    )

  if not found:
    print(
      "(no target reference nodes)"
    )


def print_prop53_consumers(
  presentation,
) -> None:
  print("")
  print("=" * 72)
  print("PROPOSITION 5.3 CONSUMER EDGES")
  print("=" * 72)

  prop53_steps = []

  for node in presentation.nodes:
    step = node.proof_step
    reference = (
      extract_toda_group_proof_step_literature_reference(
        step
      )
    )

    if (
      reference is not None
      and reference.locator
      == "Proposition 5.3"
    ):
      prop53_steps.append(
        step
      )

  if not prop53_steps:
    print(
      "(no Proposition 5.3 steps in presentation)"
    )
    return

  for prop53_step in prop53_steps:
    print(
      "Prop5.3 step id=",
      id(
        prop53_step
      ),
      "type=",
      type(
        prop53_step.conclusion
      ).__name__,
    )

    matching_edges = tuple(
      edge
      for edge in presentation.edges
      if (
        edge.premise_step
        is prop53_step
        or edge.premise_step.conclusion
        == prop53_step.conclusion
      )
    )

    if not matching_edges:
      print(
        "  (no identity/equal-conclusion consumer edges)"
      )
      continue

    for edge in matching_edges:
      parent = edge.parent_step
      print(
        "  -> parent id=",
        id(
          parent
        ),
        "type=",
        type(
          parent.conclusion
        ).__name__,
        "rule=",
        (
          None
          if parent.inference_rule is None
          else parent.inference_rule.name
        ),
        "premise_index=",
        edge.premise_index,
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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  print(
    "root type:",
    type(
      presentation.root_step.conclusion
    ).__name__,
  )
  print(
    "presentation nodes:",
    len(
      presentation.nodes
    ),
  )
  print(
    "presentation edges:",
    len(
      presentation.edges
    ),
  )

  print_target_nodes(
    presentation
  )
  print_prop53_consumers(
    presentation
  )

  raw_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  print_entries(
    "STAGE 1: raw reference entries",
    raw_entries,
  )

  boundary_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      raw_entries,
      presentation.root_step,
    )
  )
  print_entries(
    "STAGE 2: after fixed-statement boundary filter",
    boundary_entries,
  )

  boundary_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      boundary_entries,
    )
  )
  print_statement_lines(
    "STAGE 3: statement lines after boundary filter",
    boundary_entries,
    boundary_lines,
  )

  (
    root_excluded_entries,
    root_excluded_lines,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      boundary_entries,
      boundary_lines,
      presentation.root_step,
    )
  )

  print_entries(
    "STAGE 4: after root-reference exclusion",
    root_excluded_entries,
  )
  print_statement_lines(
    "STAGE 4b: statement lines after root exclusion",
    root_excluded_entries,
    root_excluded_lines,
  )

  print("")
  print("=" * 72)
  print("TARGET LOCATOR SUMMARY")
  print("=" * 72)

  stages = (
    (
      "raw",
      raw_entries,
    ),
    (
      "boundary",
      boundary_entries,
    ),
    (
      "root_excluded",
      root_excluded_entries,
    ),
  )

  for locator in (
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "Proposition 2.2",
  ):
    states = []

    for stage_name, entries in stages:
      states.append(
        stage_name
        + "="
        + (
          "YES"
          if any(
            entry.reference.locator
            == locator
            for entry in entries
          )
          else "NO"
        )
      )

    print(
      locator,
      ":",
      ", ".join(
        states
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
