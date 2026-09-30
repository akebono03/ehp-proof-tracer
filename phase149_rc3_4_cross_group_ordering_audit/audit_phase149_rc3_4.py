from pathlib import Path

from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_body_renderer import (
  _render_toda_group_proof_narrative_argument_exactness_body_block,
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_contribution_ownership import (
  filter_toda_group_proof_narrative_exactness_body_contributions,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_exactness_exposure import (
  TodaGroupProofNarrativeExactnessExposureClass,
  classify_toda_group_proof_narrative_exactness_component_exposure,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


CASES = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _exposure_by_block_id(
  presentation,
  blocks,
  argument,
  components,
):
  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
  )
  result = {}

  for component in components:
    exposure = (
      classify_toda_group_proof_narrative_exactness_component_exposure(
        relevant_groups,
        components,
        component,
      )
    )

    for evidence_block in component.evidence_blocks:
      block_id = id(
        evidence_block
      )
      existing = result.get(
        block_id
      )

      if (
        existing is not None
        and existing is not exposure
      ):
        result[
          block_id
        ] = (
          TodaGroupProofNarrativeExactnessExposureClass
          .AMBIGUOUS_RELEVANT
        )
        continue

      result[
        block_id
      ] = exposure

  return result


def _argument_record(
  presentation,
  blocks,
  sidecar,
  arguments,
  argument_index,
):
  argument = arguments[
    argument_index
  ]
  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )
  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )
  exposure_by_block_id = (
    _exposure_by_block_id(
      presentation,
      blocks,
      argument,
      components,
    )
  )
  primary_component = (
    select_toda_group_proof_narrative_argument_primary_exactness_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )
  local_body = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
  )
  local_ids = {
    id(
      block
    )
    for block in local_body
  }
  evidence_ids = {
    id(
      block
    )
    for block in evidence
  }
  merged_body = tuple(
    block
    for block in blocks
    if (
      id(
        block
      ) in local_ids
      or id(
        block
      ) in evidence_ids
    )
  )
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )
  body = (
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      merged_body,
      primary_component,
      exactness_exposure_by_block_id=exposure_by_block_id,
      connector_before_block_id=(
        None
        if conclusion_step is None
        else id(
          argument.conclusion_block
        )
      ),
      connector_text=(
        None
        if conclusion_step is None
        else "したがって,"
      ),
      conclusion_step=conclusion_step,
    )
  )

  owned_primary_latex = []
  owned_primary_block_indices = []

  for block_index, block in enumerate(
    blocks
  ):
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    ):
      continue

    if (
      exposure_by_block_id.get(
        id(
          block
        )
      )
      is not TodaGroupProofNarrativeExactnessExposureClass
      .OWNED_PRIMARY
    ):
      continue

    contributions = (
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      )
    )
    visible = (
      filter_toda_group_proof_narrative_exactness_body_contributions(
        block,
        contributions,
        primary_component,
        TodaGroupProofNarrativeExactnessExposureClass
        .OWNED_PRIMARY,
      )
    )

    if not visible:
      continue

    owned_primary_block_indices.append(
      block_index
    )
    owned_primary_latex.extend(
      contribution.latex
      for contribution in visible
    )

  conclusion_text = (
    None
    if conclusion_step is None
    else _render_generic_narrative_step(
      conclusion_step
    )
  )
  conclusion_position = (
    None
    if conclusion_text is None
    else body.find(
      conclusion_text
    )
  )
  evidence_positions = tuple(
    (
      latex,
      body.find(
        latex
      ),
    )
    for latex in owned_primary_latex
  )
  visible_positions = tuple(
    position
    for _latex, position in evidence_positions
    if position >= 0
  )
  ordering_ok = (
    True
    if not visible_positions
    else (
      conclusion_position is not None
      and conclusion_position >= 0
      and all(
        position < conclusion_position
        for position in visible_positions
      )
    )
  )

  return {
    "role": argument.role.value,
    "conclusion_block_index": blocks.index(
      argument.conclusion_block
    ),
    "conclusion_text": conclusion_text,
    "conclusion_position": conclusion_position,
    "owned_primary_block_indices": tuple(
      owned_primary_block_indices
    ),
    "owned_primary_latex": tuple(
      owned_primary_latex
    ),
    "evidence_positions": evidence_positions,
    "ordering_ok": ordering_ok,
    "body": body,
  }


def main():
  output_dir = Path(
    "phase149_rc3_4_cross_group_ordering_audit"
  ) / "audit_output"
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  failures = []
  summary_lines = []

  for label, n, k in CASES:
    (
      presentation,
      blocks,
      sidecar,
      arguments,
    ) = _method_evidence_data(
      n,
      k,
    )
    final_rendered = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )

    records = tuple(
      _argument_record(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
      for argument_index in range(
        len(
          arguments
        )
      )
    )

    case_lines = [
      "=" * 78,
      label,
      "=" * 78,
      f"blocks={len(blocks)}",
      f"arguments={len(arguments)}",
      "",
      "ARGUMENT ORDERING RECORDS",
    ]

    for index, record in enumerate(
      records
    ):
      case_lines.extend(
        (
          "-" * 78,
          f"argument_index={index}",
          f"role={record['role']}",
          (
            "conclusion_block_index="
            f"{record['conclusion_block_index']}"
          ),
          (
            "conclusion_position="
            f"{record['conclusion_position']}"
          ),
          (
            "owned_primary_block_indices="
            f"{record['owned_primary_block_indices']}"
          ),
          (
            "evidence_positions="
            f"{record['evidence_positions']}"
          ),
          f"ordering_ok={record['ordering_ok']}",
          "",
          "BODY",
          record["body"],
          "",
        )
      )

      if not record[
        "ordering_ok"
      ]:
        failures.append(
          (
            label,
            index,
            record[
              "role"
            ],
          )
        )

    case_lines.extend(
      (
        "=" * 78,
        "FINAL NARRATIVE",
        "=" * 78,
        final_rendered,
        "",
      )
    )

    case_path = output_dir / (
      label.replace(
        "^",
        "_",
      )
      + ".txt"
    )
    case_path.write_text(
      "\n".join(
        case_lines
      ),
      encoding="utf-8",
    )

    owned_count = sum(
      len(
        record[
          "owned_primary_latex"
        ]
      )
      for record in records
    )
    case_ok = all(
      record[
        "ordering_ok"
      ]
      for record in records
    )
    summary_lines.append(
      (
        f"{label}: "
        f"owned_primary_visible={owned_count}, "
        f"ordering_ok={case_ok}"
      )
    )

  summary_lines.extend(
    (
      "",
      f"failures={failures}",
      (
        "AUDIT_RESULT=PASS"
        if not failures
        else "AUDIT_RESULT=FAIL"
      ),
    )
  )

  summary = "\n".join(
    summary_lines
  )
  print(
    summary
  )
  (
    output_dir
    / "summary.txt"
  ).write_text(
    summary + "\n",
    encoding="utf-8",
  )

  if failures:
    raise SystemExit(
      1
    )


if __name__ == "__main__":
  main()
