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
  TodaGroupProofNarrativeContributionPlacement,
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


def _provider_anchor_index(
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  provider_keys: tuple[
    tuple[str, int],
    ...,
  ],
) -> int | None:
  block_by_id = {
    id(block): block
    for block in blocks
  }
  anchor_indices = []

  for provider_kind, provider_id in provider_keys:
    if provider_kind != "block":
      continue

    block = block_by_id.get(
      provider_id
    )
    if block is None:
      continue

    for proof_step in block.steps:
      line = _render_generic_narrative_step(
        proof_step
      )
      if not line:
        continue

      line_index = markdown.find(
        line
      )
      if line_index < 0:
        continue

      anchor_indices.append(
        line_index + len(line)
      )

  if not anchor_indices:
    return None

  return max(
    anchor_indices
  )


def _contribution_insertion_indices(
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> tuple[
  tuple[
    int | None,
    ...,
  ],
  ...,
]:
  result = []

  for argument_index, contributions in enumerate(
    ordered_contributions
  ):
    if not contributions:
      result.append(())
      continue

    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        arguments[
          argument_index
        ]
      )
    )
    if conclusion_step is None:
      result.append(
        tuple(
          None
          for _ in contributions
        )
      )
      continue

    conclusion_line = (
      _render_generic_narrative_step(
        conclusion_step
      )
    )
    conclusion_index = markdown.find(
      conclusion_line
    )
    if conclusion_index < 0:
      result.append(
        tuple(
          None
          for _ in contributions
        )
      )
      continue

    indices = [
      None
      for _ in contributions
    ]

    for contribution_index, contribution in enumerate(
      contributions
    ):
      if (
        contribution.placement
        is TodaGroupProofNarrativeContributionPlacement
        .AT_PROVIDER_ANCHOR
      ):
        anchor_index = _provider_anchor_index(
          markdown,
          blocks,
          contribution.provider_keys,
        )
        indices[
          contribution_index
        ] = (
          conclusion_index
          if anchor_index is None
          else anchor_index
        )
        continue

      if (
        contribution.placement
        is TodaGroupProofNarrativeContributionPlacement
        .BEFORE_ARGUMENT_CONCLUSION
      ):
        indices[
          contribution_index
        ] = conclusion_index

    for contribution_index in range(
      len(contributions) - 1,
      -1,
      -1,
    ):
      contribution = contributions[
        contribution_index
      ]
      if (
        contribution.placement
        is not TodaGroupProofNarrativeContributionPlacement
        .BEFORE_DEPENDENT_CONTRIBUTION
      ):
        continue

      dependent_index = next(
        (
          indices[index]
          for index in range(
            contribution_index + 1,
            len(contributions),
          )
          if indices[index] is not None
        ),
        conclusion_index,
      )
      indices[
        contribution_index
      ] = dependent_index

    result.append(
      tuple(
        indices
      )
    )

  return tuple(
    result
  )


def _insert_toda_group_proof_narrative_argument_contributions(
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> str:
  insertion_indices = (
    _contribution_insertion_indices(
      markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  insertions_by_index = {}

  for argument_index, contributions in enumerate(
    ordered_contributions
  ):
    for contribution_index, contribution in enumerate(
      contributions
    ):
      contribution_line = (
        _render_generic_narrative_step(
          contribution.proof_step
        )
      )
      if not contribution_line:
        continue
      if contribution_line in markdown:
        continue

      insertion_index = insertion_indices[
        argument_index
      ][
        contribution_index
      ]
      if insertion_index is None:
        continue

      insertions_by_index.setdefault(
        insertion_index,
        [],
      ).append(
        contribution_line
      )

  rendered = markdown

  for insertion_index in sorted(
    insertions_by_index,
    reverse=True,
  ):
    contribution_lines = insertions_by_index[
      insertion_index
    ]
    insertion = (
      "\n\n"
      + "\n\n".join(
        contribution_lines
      )
    )

    if (
      insertion_index < len(markdown)
      and not markdown[
        insertion_index:
      ].startswith(
        "\n\n"
      )
    ):
      insertion += "\n\n"

    rendered = (
      rendered[
        :insertion_index
      ]
      + insertion
      + rendered[
        insertion_index:
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
    blocks,
    arguments,
    ordered_contributions,
  )
