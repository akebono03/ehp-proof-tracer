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

import toda_group_proof_narrative_argument_multi_renderer as multi_renderer
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_equation_numbering import (
  _numbered_step_line,
  number_toda_group_proof_narrative_equations,
)
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
)


def _numbering_steps(
  presentation,
  blocks,
):
  transitions = (
    extract_toda_group_proof_narrative_step_transitions(
      presentation,
      blocks,
    )
  )
  sources_by_target = {}

  for transition in transitions:
    target_id = id(
      transition.target_step
    )
    current = sources_by_target.get(
      target_id,
      (),
    )

    if any(
      step is transition.source_step
      for step in current
    ):
      continue

    sources_by_target[
      target_id
    ] = (
      *current,
      transition.source_step,
    )

  ordered_steps = []
  seen_ids = set()

  for block in blocks:
    for target_step in block.steps:
      source_steps = sources_by_target.get(
        id(
          target_step
        ),
        (),
      )

      for source_step in source_steps:
        source_id = id(
          source_step
        )

        if source_id in seen_ids:
          continue

        ordered_steps.append(
          source_step
        )
        seen_ids.add(
          source_id
        )

      if (
        source_steps
        and id(
          target_step
        ) not in seen_ids
      ):
        ordered_steps.append(
          target_step
        )
        seen_ids.add(
          id(
            target_step
          )
        )

  return tuple(
    ordered_steps
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

  captured = {}

  original_numbering = (
    multi_renderer
    .number_toda_group_proof_narrative_equations
  )

  def capture_numbering(
    markdown,
    captured_presentation,
    captured_blocks,
  ):
    captured[
      "raw"
    ] = markdown

    direct = (
      number_toda_group_proof_narrative_equations(
        markdown,
        captured_presentation,
        captured_blocks,
      )
    )
    captured[
      "direct"
    ] = direct

    return direct

  multi_renderer.number_toda_group_proof_narrative_equations = (
    capture_numbering
  )

  try:
    final = (
      multi_renderer
      .render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )
  finally:
    multi_renderer.number_toda_group_proof_narrative_equations = (
      original_numbering
    )

  raw = captured[
    "raw"
  ]
  direct = captured[
    "direct"
  ]
  steps = _numbering_steps(
    presentation,
    blocks,
  )

  lines = [
    "=" * 100,
    "Phase 158-R5-5b repair1f - equation line identity diagnosis",
    "=" * 100,
    "",
    "A. DIRECT NUMBERING CONSISTENCY",
    "-" * 100,
    "direct_equals_final="
    + str(
      direct == final
    ),
    "raw_equals_direct="
    + str(
      raw == direct
    ),
    "",
    "B. NUMBERING STEP / LINE MATCHES",
    "-" * 100,
  ]

  raw_lines = raw.splitlines()

  for number, proof_step in enumerate(
    steps,
    start=1,
  ):
    plain = (
      _render_generic_narrative_step(
        proof_step
      )
    )
    tagged = (
      _numbered_step_line(
        proof_step,
        number,
      )
    )
    matching_raw_indices = tuple(
      index
      for index, line in enumerate(
        raw_lines
      )
      if line == plain
    )

    lines.append(
      (
        f"N{number} "
        f"id={id(proof_step)} "
        f"plain_occurrences={matching_raw_indices} "
        f"tag_changes_line={tagged != plain}"
      )
    )
    lines.append(
      "  plain="
      + plain
    )
    lines.append(
      "  tagged="
      + tagged
    )

  lines.extend(
    (
      "",
      "C. RAW LINES THAT MATCH MULTIPLE NUMBERING STEPS",
      "-" * 100,
    )
  )

  plain_to_numbers = {}

  for number, proof_step in enumerate(
    steps,
    start=1,
  ):
    plain = (
      _render_generic_narrative_step(
        proof_step
      )
    )
    plain_to_numbers.setdefault(
      plain,
      [],
    ).append(
      number
    )

  for plain, numbers in plain_to_numbers.items():
    if len(
      numbers
    ) < 2:
      continue

    lines.append(
      (
        "numbers="
        + repr(
          tuple(
            numbers
          )
        )
        + " occurrences="
        + repr(
          tuple(
            index
            for index, line in enumerate(
              raw_lines
            )
            if line == plain
          )
        )
      )
    )
    lines.append(
      "  "
      + plain
    )

  lines.extend(
    (
      "",
      "D. TAG INVENTORY AFTER DIRECT NUMBERING",
      "-" * 100,
    )
  )

  for number in range(
    1,
    len(
      steps
    )
    + 1,
  ):
    tag = (
      r"\tag{"
      + str(
        number
      )
      + "}"
    )
    lines.append(
      (
        f"N{number}: "
        f"{tag in direct}"
      )
    )

  lines.extend(
    (
      "",
      "E. DIRECT NUMBERED MARKDOWN",
      "-" * 100,
      direct,
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
    / "pi6_3_equation_line_identity.txt"
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
