from toda_group_proof_narrative_argument_body_renderer import (
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_header_method_section,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


def _normalize_toda_group_proof_narrative_argument_header_spacing(
  header: str,
) -> str:
  if not isinstance(
    header,
    str,
  ):
    raise TypeError(
      "header must be a string"
    )

  return header.replace(
    ".そのために、",
    ". そのために、",
  )


def render_toda_group_proof_narrative_single_argument_markdown(
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
  argument_index: int,
  discourse_role: TodaGroupProofNarrativeArgumentDiscourseRole,
  primary_component: (
    TodaGroupProofNarrativeExactnessMethodComponent
    | None
  ),
) -> str:
  if not isinstance(
    discourse_role,
    TodaGroupProofNarrativeArgumentDiscourseRole,
  ):
    raise TypeError(
      "discourse_role must be a "
      "TodaGroupProofNarrativeArgumentDiscourseRole"
    )

  local_body_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
  )

  argument = arguments[
    argument_index
  ]

  header = (
    render_toda_group_proof_narrative_argument_header_method_section(
      argument,
      discourse_role,
      primary_component,
    )
  )
  header = (
    _normalize_toda_group_proof_narrative_argument_header_spacing(
      header
    )
  )

  body = (
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      local_body_blocks,
      primary_component,
    )
  )

  parts = tuple(
    part
    for part in (
      header,
      body,
    )
    if part
  )

  return "\n\n".join(
    parts
  )
