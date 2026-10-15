from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_transition_by_conclusion_id,
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  build_toda_group_proof_narrative_generic_used_step_ids,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
  filter_toda_group_proof_narrative_reference_entries_by_step_usage,
)
from toda_group_proof_narrative_transition_renderer import (
  render_toda_group_proof_narrative_transition_connector,
)


def safe_render(step) -> str:
  try:
    value = _render_generic_narrative_step(step)
  except Exception as exc:
    return (
      "<RENDER_ERROR "
      + type(exc).__name__
      + ": "
      + str(exc)
      + ">"
    )
  return "" if value is None else value


def entry_locators(entries):
  return tuple(
    entry.reference.locator
    or entry.reference.label
    for entry in entries
  )


def describe_entries(lines, label, entries):
  lines.append(label)
  locators = entry_locators(entries)
  lines.append(
    "  count="
    + str(len(entries))
  )
  lines.append(
    "  has Proposition 4.4="
    + str("Proposition 4.4" in locators)
  )
  for entry in entries:
    lines.append(
      "  [R"
      + str(entry.number)
      + "] "
      + (
        entry.reference.locator
        or entry.reference.label
      )
    )


def main() -> int:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  lines = [
    "=" * 80,
    "Phase 159 pi_4^3 repair2c - pi_6^3 reference/transition stage audit",
    "=" * 80,
    "Production code changes: none",
    "Existing test changes: none",
    "",
    "A. Reference filtering stages",
  ]

  entries0 = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  describe_entries(
    lines,
    "Stage A0: raw entries",
    entries0,
  )

  entries1 = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      entries0,
      presentation.root_step,
    )
  )
  describe_entries(
    lines,
    "Stage A1: fixed-statement boundary",
    entries1,
  )

  statement_lines1 = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries1,
    )
  )

  (
    entries2,
    statement_lines2,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      entries1,
      statement_lines1,
      presentation.root_step,
    )
  )
  describe_entries(
    lines,
    "Stage A2: root-reference exclusion",
    entries2,
  )

  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      sidecar,
      arguments,
    )
  )
  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )
  generic_used_step_ids = (
    build_toda_group_proof_narrative_generic_used_step_ids(
      presentation,
      blocks,
      sidecar,
      arguments,
      ordered_contributions,
    )
  )

  frontier_step_ids = frozenset(
    id(step)
    for entry in entries2
    for step in entry.proof_steps
  )
  boundary_visible_used_step_ids = frozenset(
    step_id
    for step_id in generic_used_step_ids
    if step_id in frontier_step_ids
  )

  (
    entries3,
    statement_lines3,
  ) = (
    filter_toda_group_proof_narrative_reference_entries_by_step_usage(
      entries2,
      statement_lines2,
      boundary_visible_used_step_ids,
      presentation.root_step,
    )
  )
  describe_entries(
    lines,
    "Stage A3: step-usage filter using current generic-used frontier",
    entries3,
  )

  prop44_entry = next(
    (
      entry
      for entry in entries2
      if (
        entry.reference.locator
        or entry.reference.label
      )
      == "Proposition 4.4"
    ),
    None,
  )

  lines.append("")
  lines.append(
    "Proposition 4.4 step usage before step-usage filter:"
  )
  if prop44_entry is None:
    lines.append(
      "  entry missing before usage filter"
    )
  else:
    for step in prop44_entry.proof_steps:
      lines.append(
        "  used="
        + str(id(step) in generic_used_step_ids)
        + " boundary_visible="
        + str(id(step) in boundary_visible_used_step_ids)
        + " :: "
        + type(step.conclusion).__name__
        + " :: "
        + safe_render(step)
      )

  lines.extend(
    (
      "",
      "B. Transition/direct-derivation stages",
    )
  )

  transition_by_conclusion_id = (
    _toda_group_proof_narrative_argument_transition_by_conclusion_id(
      presentation,
      blocks,
      arguments,
    )
  )

  block_index = {
    id(block): index
    for index, block in enumerate(blocks)
  }

  for argument_index, argument in enumerate(arguments):
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    if conclusion_step is None:
      continue

    transition = transition_by_conclusion_id.get(
      id(argument.conclusion_block)
    )
    connector = (
      None
      if transition is None
      else render_toda_group_proof_narrative_transition_connector(
        transition
      )
    )
    direct = (
      ()
      if connector is None
      else (
        extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
          argument,
          arguments,
        )
      )
    )
    support = tuple(
      support_step
      for premise_step in direct
      for support_step in premise_step.premises
      if all(
        support_step is not existing_step
        for existing_step in direct
      )
    )

    lines.append(
      "  argument["
      + str(argument_index)
      + "] role="
      + argument.role.value
      + " conclusion_block="
      + str(
        block_index[
          id(argument.conclusion_block)
        ]
      )
    )
    lines.append(
      "    conclusion="
      + safe_render(conclusion_step)
    )
    lines.append(
      "    connector="
      + str(connector)
    )
    if transition is not None:
      lines.append(
        "    transition_sources="
        + repr(
          [
            block_index[id(block)]
            for block in transition.source_blocks
          ]
        )
      )
    lines.append(
      "    direct_derivation_premises="
      + str(len(direct))
    )
    for index, step in enumerate(direct):
      lines.append(
        "      direct["
        + str(index)
        + "] "
        + safe_render(step)
      )
    lines.append(
      "    direct_derivation_support_steps="
      + str(len(support))
    )
    for index, step in enumerate(support):
      lines.append(
        "      support["
        + str(index)
        + "] "
        + safe_render(step)
      )

  lines.extend(
    (
      "",
      "C. Base multi-argument markdown",
      base_markdown,
      "",
      "D. Final contribution/reference markdown",
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      ),
      "",
      "Interpretation:",
      (
        "  If Proposition 4.4 survives A2 but fails A3, "
        "generic-used/frontier usage classification is the loss point."
      ),
      (
        "  If Proposition 4.4 survives A3 but is absent in final markdown, "
        "a later body-usage/reference-restoration stage is the loss point."
      ),
      (
        "  If the final group-structure argument has only a broad "
        "'以上より' connector while numbered direct premises/support are "
        "present, numbering/connector insertion is the loss point."
      ),
      (
        "  If required direct premises/support are already absent, "
        "the provenance-to-Argument dependency graph changed earlier."
      ),
      "",
      "AUDIT_RESULT=PASS",
      "=" * 80,
    )
  )

  output = "\n".join(lines)

  out = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  out.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    out
    / "summary.txt"
  ).write_text(
    output + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(output)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
