from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_labels,
  _generic_narrative_sentence_lead,
  _render_generic_narrative_proof_block,
  _render_generic_narrative_step,
)
from proof import (
  ProofStep,
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


def _reorder_toda_group_proof_narrative_block_conclusion_step_last(
  block: TodaGroupProofNarrativeBlock,
  conclusion_step: ProofStep,
) -> TodaGroupProofNarrativeBlock:
  if conclusion_step not in block.steps:
    return block

  reordered_steps = tuple(
    proof_step
    for proof_step in block.steps
    if proof_step is not conclusion_step
  ) + (
    conclusion_step,
  )

  if reordered_steps == block.steps:
    return block

  return TodaGroupProofNarrativeBlock(
    role=block.role,
    steps=reordered_steps,
  )


def _insert_toda_group_proof_narrative_connector_before_conclusion_step(
  block_lines: tuple[
    str,
    ...,
  ],
  conclusion_step: ProofStep,
  connector_text: str,
) -> tuple[
  str,
  ...,
]:
  conclusion_line = (
    _render_generic_narrative_step(
      conclusion_step
    )
  )
  conclusion_index = next(
    (
      index
      for index in range(
        len(
          block_lines
        ) - 1,
        -1,
        -1,
      )
      if block_lines[
        index
      ] == conclusion_line
    ),
    None,
  )

  if conclusion_index is None:
    return block_lines

  return (
    block_lines[
      :conclusion_index
    ]
    + (
      connector_text,
      "",
    )
    + block_lines[
      conclusion_index:
    ]
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
  connector_before_block_id: int | None = None,
  connector_text: str | None = None,
  conclusion_step: ProofStep | None = None,
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

  if (
    connector_before_block_id is not None
    and (
      not isinstance(
        connector_before_block_id,
        int,
      )
      or isinstance(
        connector_before_block_id,
        bool,
      )
    )
  ):
    raise TypeError(
      "connector_before_block_id must be "
      "an int or None"
    )

  if (
    connector_text is not None
    and not isinstance(
      connector_text,
      str,
    )
  ):
    raise TypeError(
      "connector_text must be a str or None"
    )

  if (
    connector_before_block_id is None
  ) != (
    connector_text is None
  ):
    raise ValueError(
      "connector_before_block_id and connector_text "
      "must be provided together"
    )

  if (
    conclusion_step is not None
    and not isinstance(
      conclusion_step,
      ProofStep,
    )
  ):
    raise TypeError(
      "conclusion_step must be a ProofStep or None"
    )

  if (
    conclusion_step is not None
    and connector_before_block_id is None
  ):
    raise ValueError(
      "conclusion_step requires connector placement"
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
  connector_inserted = False

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
      block_lines = (
        _render_toda_group_proof_narrative_argument_exactness_body_block(
          presentation,
          blocks,
          block_index,
          primary_component,
          excluded_exactness_contribution_keys,
        )
      )
    else:
      if (
        excluded_non_exact_block_ids is not None
        and id(
          block
        ) in excluded_non_exact_block_ids
      ):
        continue

      reordered_block = block

      if (
        conclusion_step is not None
        and connector_before_block_id is not None
        and id(
          block
        ) == connector_before_block_id
        and conclusion_step in block.steps
      ):
        reordered_block = (
          _reorder_toda_group_proof_narrative_block_conclusion_step_last(
            block,
            conclusion_step,
          )
        )

      render_blocks = blocks

      if reordered_block is not block:
        render_blocks = (
          blocks[
            :block_index
          ]
          + (
            reordered_block,
          )
          + blocks[
            block_index + 1:
          ]
        )

      block_lines = tuple(
        _render_generic_narrative_proof_block(
          presentation,
          render_blocks,
          block_index,
          show_dependency_labels=False,
          suppress_provenance_only=True,
        )
      )

    if not block_lines:
      continue

    if (
      not connector_inserted
      and connector_before_block_id is not None
      and id(
        block
      ) == connector_before_block_id
    ):
      if (
        conclusion_step is not None
        and conclusion_step in block.steps
        and block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        block_lines = (
          _insert_toda_group_proof_narrative_connector_before_conclusion_step(
            block_lines,
            conclusion_step,
            connector_text,
          )
        )
      else:
        block_lines = (
          connector_text,
          "",
        ) + block_lines

      connector_inserted = True

    lines.extend(
      block_lines
    )

  return "\n".join(
    lines
  ).rstrip()
