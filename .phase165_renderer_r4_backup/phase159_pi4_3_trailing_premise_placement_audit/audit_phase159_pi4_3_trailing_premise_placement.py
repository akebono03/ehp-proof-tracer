from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
  _provider_anchor_index,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)


TARGET_FRAGMENT = (
  r"\pi_{3}^{2} = "
  r"\mathbb{Z}\{\eta_{2}\}"
)


def main() -> int:
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    1,
  )

  base = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  ordered = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base,
    )
  )
  insertion_indices = (
    _contribution_insertion_indices(
      base,
      blocks,
      arguments,
      ordered,
    )
  )

  lines = [
    "# Phase 159 pi4_3 trailing premise placement audit",
    "",
    "## Base markdown",
    "",
    base,
    "",
    "## Arguments and contributions",
    "",
  ]

  for argument_index, argument in enumerate(
    arguments
  ):
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    conclusion_rendered = (
      None
      if conclusion_step is None
      else _render_generic_narrative_step(
        conclusion_step
      )
    )
    local_body = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )

    lines.extend(
      (
        "argument_"
        + str(
          argument_index
        )
        + "_role="
        + str(
          argument.role
        ),
        "argument_"
        + str(
          argument_index
        )
        + "_conclusion="
        + repr(
          conclusion_rendered
        ),
      )
    )

    for local_index, block in enumerate(
      local_body
    ):
      lines.append(
        "  local_block_"
        + str(
          local_index
        )
        + "_role="
        + str(
          block.role
        )
      )

      for step_index, step in enumerate(
        block.steps
      ):
        rendered = (
          _render_generic_narrative_step(
            step
          )
        )
        lines.append(
          "    step_"
          + str(
            step_index
          )
          + "="
          + repr(
            rendered
          )
        )

    for contribution_index, contribution in enumerate(
      ordered[
        argument_index
      ]
    ):
      rendered = (
        _render_generic_narrative_step(
          contribution.proof_step
        )
      )
      insertion_index = insertion_indices[
        argument_index
      ][
        contribution_index
      ]
      provider_anchor_index = (
        _provider_anchor_index(
          base,
          blocks,
          contribution.provider_keys,
        )
      )

      lines.extend(
        (
          "  contribution_"
          + str(
            contribution_index
          )
          + "_rendered="
          + repr(
            rendered
          ),
          "    placement="
          + str(
            contribution.placement
          ),
          "    provider_anchor="
          + str(
            contribution.provider_anchor
          ),
          "    distance_to_conclusion="
          + str(
            contribution.distance_to_conclusion
          ),
          "    provider_keys="
          + repr(
            contribution.provider_keys
          ),
          "    provider_anchor_index="
          + repr(
            provider_anchor_index
          ),
          "    insertion_index="
          + repr(
            insertion_index
          ),
        )
      )

      if TARGET_FRAGMENT in rendered:
        lines.append(
          "    *** TARGET TRAILING PREMISE ***"
        )

  output = "\n".join(
    lines
  )
  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi4_3_trailing_premise_placement_audit.txt"
  )
  output_path.write_text(
    output,
    encoding="utf-8",
  )

  print(
    output
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
