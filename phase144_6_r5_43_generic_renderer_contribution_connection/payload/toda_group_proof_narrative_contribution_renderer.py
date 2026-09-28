from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


def _insert_toda_group_proof_narrative_argument_contributions(
  markdown: str,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> str:
  rendered = markdown

  for argument_index, contributions in enumerate(
    ordered_contributions
  ):
    if not contributions:
      continue

    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        arguments[
          argument_index
        ]
      )
    )
    if conclusion_step is None:
      continue

    conclusion_line = (
      _render_generic_narrative_step(
        conclusion_step
      )
    )
    conclusion_index = rendered.find(
      conclusion_line
    )
    if conclusion_index < 0:
      continue

    contribution_lines = []
    for contribution in contributions:
      contribution_line = (
        _render_generic_narrative_step(
          contribution.proof_step
        )
      )
      if not contribution_line:
        continue
      if contribution_line in rendered:
        continue
      contribution_lines.append(
        contribution_line
      )

    if not contribution_lines:
      continue

    insertion = (
      "\n\n".join(
        contribution_lines
      )
      + "\n\n"
    )
    rendered = (
      rendered[
        :conclusion_index
      ]
      + insertion
      + rendered[
        conclusion_index:
      ]
    )

  return rendered


def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> str:
  base_markdown = (
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
  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )

  return _insert_toda_group_proof_narrative_argument_contributions(
    base_markdown,
    arguments,
    ordered_contributions,
  )
