from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_labels,
  _generic_narrative_sentence_lead,
  _render_generic_narrative_proof_block,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
)
from toda_group_proof_narrative_exactness_contribution_ownership import (
  filter_toda_group_proof_narrative_exactness_body_contributions,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  TodaGroupProofNarrativeExactnessDisplayContributionKind,
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


def _toda_group_proof_narrative_exactness_contribution_key(
  contribution,
) -> tuple[
  object,
  int,
  str,
]:
  return (
    contribution.kind,
    id(
      contribution.proof_step
    ),
    contribution.latex,
  )


def _render_toda_group_proof_narrative_argument_exactness_body_block(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  block_index: int,
  primary_component: (
    TodaGroupProofNarrativeExactnessMethodComponent
    | None
  ),
  excluded_exactness_contribution_keys: (
    frozenset[
      tuple[
        object,
        int,
        str,
      ]
    ]
    | None
  ) = None,
) -> tuple[
  str,
  ...,
]:
  block = blocks[
    block_index
  ]
  contributions = (
    extract_toda_group_proof_narrative_exactness_display_contributions(
      presentation,
      block,
    )
  )
  body_contributions = (
    filter_toda_group_proof_narrative_exactness_body_contributions(
      block,
      contributions,
      primary_component,
    )
  )

  if excluded_exactness_contribution_keys is not None:
    body_contributions = tuple(
      contribution
      for contribution in body_contributions
      if (
        _toda_group_proof_narrative_exactness_contribution_key(
          contribution
        )
        not in excluded_exactness_contribution_keys
      )
    )

  if not body_contributions:
    return ()

  lines = []
  window_contributions = tuple(
    contribution
    for contribution in body_contributions
    if (
      contribution.kind
      is TodaGroupProofNarrativeExactnessDisplayContributionKind
      .EXACTNESS_WINDOW
    )
  )

  if window_contributions:
    sentence_lead = (
      _generic_narrative_sentence_lead(
        block.role,
        (),
      )
    )

    if sentence_lead:
      lines.append(
        sentence_lead
      )
      lines.append(
        ""
      )

  for contribution in body_contributions:
    if (
      contribution.kind
      is TodaGroupProofNarrativeExactnessDisplayContributionKind
      .EXACTNESS_WINDOW
    ):
      exactness_latex = (
        contribution.latex
      )
      english_suffix = (
        r" \text{ is exact}"
      )

      if exactness_latex.endswith(
        english_suffix
      ):
        exactness_latex = (
          exactness_latex[
            :-len(
              english_suffix
            )
          ]
        )

      lines.append(
        "$"
        + exactness_latex
        + "$ は完全である."
      )
      lines.append(
        ""
      )
      continue

    if (
      contribution.kind
      is TodaGroupProofNarrativeExactnessDisplayContributionKind
      .DERIVED_SHORT_EXACT_SEQUENCE
    ):
      lines.append(
        "この完全性と両端の写像の性質より, "
        "次の短完全列を得る."
      )
      lines.append(
        ""
      )
      lines.append(
        "$"
        + contribution.latex
        + "$"
      )
      lines.append(
        ""
      )
      continue

    raise ValueError(
      "unsupported EXACTNESS display contribution kind"
    )

  return tuple(
    lines
  )


def render_toda_group_proof_narrative_argument_body_markdown(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  local_body_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  primary_component: (
    TodaGroupProofNarrativeExactnessMethodComponent
    | None
  ),
  excluded_non_exact_block_ids: (
    frozenset[
      int
    ]
    | None
  ) = None,
  excluded_exactness_contribution_keys: (
    frozenset[
      tuple[
        object,
        int,
        str,
      ]
    ]
    | None
  ) = None,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    blocks,
    tuple,
  ):
    raise TypeError(
      "blocks must be a tuple"
    )

  for block in blocks:
    if not isinstance(
      block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "blocks must contain only "
        "TodaGroupProofNarrativeBlock objects"
      )

  if not isinstance(
    local_body_blocks,
    tuple,
  ):
    raise TypeError(
      "local_body_blocks must be a tuple"
    )

  if (
    excluded_non_exact_block_ids is not None
    and not isinstance(
      excluded_non_exact_block_ids,
      frozenset,
    )
  ):
    raise TypeError(
      "excluded_non_exact_block_ids must be "
      "a frozenset or None"
    )

  if (
    excluded_exactness_contribution_keys is not None
    and not isinstance(
      excluded_exactness_contribution_keys,
      frozenset,
    )
  ):
    raise TypeError(
      "excluded_exactness_contribution_keys must be "
      "a frozenset or None"
    )

  block_index_by_identity = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }

  seen_local_block_ids = set()

  for block in local_body_blocks:
    if not isinstance(
      block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "local_body_blocks must contain only "
        "TodaGroupProofNarrativeBlock objects"
      )

    block_id = id(
      block
    )

    if block_id not in block_index_by_identity:
      raise ValueError(
        "local_body_blocks must contain only "
        "blocks from blocks"
      )

    if block_id in seen_local_block_ids:
      raise ValueError(
        "local_body_blocks must not contain "
        "duplicate blocks"
      )

    seen_local_block_ids.add(
      block_id
    )

  if (
    primary_component is not None
    and not isinstance(
      primary_component,
      TodaGroupProofNarrativeExactnessMethodComponent,
    )
  ):
    raise TypeError(
      "primary_component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent "
      "or None"
    )

  lines = []

  for block in local_body_blocks:
    block_index = block_index_by_identity[
      id(
        block
      )
    ]

    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    ):
      lines.extend(
        _render_toda_group_proof_narrative_argument_exactness_body_block(
          presentation,
          blocks,
          block_index,
          primary_component,
          excluded_exactness_contribution_keys,
        )
      )
      continue

    if (
      excluded_non_exact_block_ids is not None
      and id(
        block
      ) in excluded_non_exact_block_ids
    ):
      continue

    lines.extend(
      _render_generic_narrative_proof_block(
        presentation,
        blocks,
        block_index,
        show_dependency_labels=False,
      )
    )

  return "\n".join(
    lines
  ).rstrip()
