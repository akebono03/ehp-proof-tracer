from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_body_renderer import (
  _is_toda_group_proof_narrative_rendered_reflexive_equality_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)


FORMS = (
  (
    "eq1_tagged",
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}\tag{1}$",
  ),
  (
    "eq1_plain",
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}$",
  ),
  (
    "eq2_tagged",
    r"$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}\tag{2}$",
  ),
  (
    "eq2_plain",
    r"$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}$",
  ),
  (
    "connector_two",
    "(1) と (2) より,",
  ),
  (
    "connector_one",
    "(1) より,",
  ),
  (
    "eq3_tagged",
    r"$2\nu' = \eta_{3}^{3}\tag{3}$",
  ),
  (
    "eq3_plain",
    r"$2\nu' = \eta_{3}^{3}$",
  ),
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

  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  lines = [
    "=" * 100,
    "Phase 158-R5-5b repair1k - pi6 tag-vs-plain diagnosis",
    "=" * 100,
    "",
    "A. PUBLIC FORMS",
    "-" * 100,
  ]

  for label, text in FORMS:
    indices = tuple(
      index
      for index in range(
        len(
          rendered
        )
      )
      if rendered.startswith(
        text,
        index,
      )
    )
    lines.append(
      f"{label}: count={len(indices)} indices={indices}"
    )
    lines.append(
      "  "
      + text
    )

  lines.extend(
    (
      "",
      "B. CALCULATION BLOCK STEP CLASSIFICATION",
      "-" * 100,
    )
  )

  for block_index, block in enumerate(
    blocks
  ):
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .CALCULATION
    ):
      continue

    lines.append(
      f"B{block_index}"
    )

    for step_index, proof_step in enumerate(
      block.steps
    ):
      rendered_step = (
        _render_generic_narrative_step(
          proof_step
        )
      )
      reflexive = (
        _is_toda_group_proof_narrative_rendered_reflexive_equality_step(
          proof_step
        )
      )

      lines.append(
        (
          f"  S{step_index} "
          f"type={type(proof_step.conclusion).__name__} "
          f"reflexive={reflexive}"
        )
      )
      lines.append(
        "    "
        + rendered_step
      )

  lines.extend(
    (
      "",
      "C. FULL MULTI-ARGUMENT OUTPUT",
      "-" * 100,
      rendered,
      "",
      "=" * 100,
    )
  )

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
    / "pi6_tag_vs_plain.txt"
  ).write_text(
    "\n".join(
      lines
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    "\n".join(
      lines
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
