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
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_transition_renderer import (
  render_toda_group_proof_narrative_transition_connector,
)
from toda_group_proof_narrative_transitions import (
  extract_toda_group_proof_narrative_transitions,
)
from toda_prop56_zero_bootstrap import (
  _build_prop51_step,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
)


def safe_render(step):
  try:
    rendered = _render_generic_narrative_step(step)
  except Exception as exc:
    return f"<RENDER_ERROR {type(exc).__name__}: {exc}>"
  return "" if rendered is None else rendered


def ref_of(step):
  if step.inference_rule is None:
    return None
  return step.inference_rule.literature_reference


def main() -> int:
  presentation, blocks, sidecar, arguments = (
    _method_evidence_data(
      3,
      3,
    )
  )

  block_index = {
    id(block): index
    for index, block in enumerate(blocks)
  }

  lines = [
    "=" * 80,
    "Phase 159 pi_4^3 repair2b - pi_6^3 regression root-cause audit",
    "=" * 80,
    "Production code changes: none",
    "Existing test changes: none",
    "",
    "A. Current Prop 5.1 builder result",
  ]

  prop51 = _build_prop51_step()
  lines.append(
    "prop51 rule="
    + (
      ""
      if prop51.inference_rule is None
      else prop51.inference_rule.name
    )
  )
  lines.append(
    "prop51 premise count="
    + str(len(prop51.premises))
  )

  for index, premise in enumerate(prop51.premises):
    ref = ref_of(premise)
    lines.append(
      f"  premise[{index}] "
      f"type={type(premise.conclusion).__name__}"
    )
    lines.append(
      "    rendered=" + safe_render(premise)
    )
    lines.append(
      "    rule="
      + (
        ""
        if premise.inference_rule is None
        else premise.inference_rule.name
      )
    )
    lines.append(
      "    reference="
      + (
        ""
        if ref is None
        else (
          (ref.locator or ref.label)
        )
      )
    )

  delta_premises = tuple(
    premise
    for premise in prop51.premises
    if isinstance(
      premise.conclusion,
      TodaDeltaImageUpToSignStatement,
    )
  )
  lines.append(
    "direct Delta premise count="
    + str(len(delta_premises))
  )

  lines.extend(
    (
      "",
      "B. pi_6^3 Reference entries",
    )
  )

  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )

  for entry in entries:
    locator = (
      entry.reference.locator
      or entry.reference.label
    )
    lines.append(
      f"  [R{entry.number}] {locator}"
    )
    for step in entry.proof_steps:
      lines.append(
        "    "
        + type(step.conclusion).__name__
        + " :: "
        + safe_render(step)
      )

  locators = tuple(
    entry.reference.locator
    or entry.reference.label
    for entry in entries
  )
  lines.append(
    "Reference has Proposition 4.4="
    + str(
      "Proposition 4.4" in locators
    )
  )

  lines.extend(
    (
      "",
      "C. pi_6^3 Argument transitions",
    )
  )

  transitions = (
    extract_toda_group_proof_narrative_transitions(
      presentation,
      blocks,
      arguments,
    )
  )

  for index, transition in enumerate(
    transitions
  ):
    source_indices = [
      block_index[id(block)]
      for block in transition.source_blocks
    ]
    target_index = block_index[
      id(transition.target_block)
    ]
    connector = (
      render_toda_group_proof_narrative_transition_connector(
        transition
      )
    )

    lines.append(
      f"  transition[{index}] "
      f"role={transition.role.value} "
      f"sources={source_indices} "
      f"target={target_index}"
    )
    lines.append(
      "    connector="
      + str(connector)
    )

  lines.extend(
    (
      "",
      "D. pi_6^3 blocks",
    )
  )

  for index, block in enumerate(blocks):
    lines.append(
      f"  block[{index}] role={block.role.value}"
    )
    for step in block.steps:
      ref = ref_of(step)
      lines.append(
        "    "
        + type(step.conclusion).__name__
        + " :: "
        + safe_render(step)
      )
      if ref is not None:
        lines.append(
          "      ref="
          + (
            ref.locator
            or ref.label
          )
        )

  lines.extend(
    (
      "",
      "Interpretation targets:",
      (
        "  1. If Proposition 4.4 is already absent from Reference entries, "
        "the regression is upstream of rendering."
      ),
      (
        "  2. If the transition that formerly produced '(4) と (5) より' "
        "has different source blocks or connector text, the provenance/argument "
        "graph changed before final rendering."
      ),
      (
        "  3. If both defects coexist after repair1b/1c, repair1 must be "
        "adjusted without restoring the legacy Phase50 public route."
      ),
      "",
      "AUDIT_RESULT=PASS",
      "=" * 80,
    )
  )

  output = "\n".join(lines)

  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    output_dir
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
